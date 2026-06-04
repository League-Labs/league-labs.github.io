#!/usr/bin/env python3
"""Generate the meeting calendar from the project's calendar feeds.

Reads one or more calendar feed URLs from the project .env, pulls every
upcoming event (from the current Monday onward), and renders them onto
month-grid calendars (June/July/August) on the main /calendar/ page. Each
day cell shows its meetings with start time and name; entries link to their
enrollment / event page where one is available.

Feeds (see SOURCES below):
  - PIKE_CALENDAR   Pike13 — only the known meetings are shown, each with its
                    own label/color: Robot Garage, Robots (Online),
                    Web Applications. Entries link to Pike13 enrollment.
  - LL_CALENDAR     League Labs Google Calendar — every event shown, labeled
                    by its own title.
  - MEETUP_CALENDAR Meetup (Code Clinics) — every event shown by title.

The Robots and Web Applications team pages just link to /calendar/.

This script runs from the justfile before every Hugo build, so it is
idempotent: generated blocks live between HTML comment markers and are
rewritten in place on each run.
"""

import base64
import calendar as calmod
import re
import shutil
import sys
import urllib.parse
import urllib.request
from collections import defaultdict
from datetime import date, datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent.parent
ENV = ROOT / ".env"
SUMMER = ROOT / "site" / "content" / "teams" / "2026" / "summer"
MEETINGS_DIR = SUMMER / "meetings"
MAIN_CALENDAR = ROOT / "site" / "content" / "calendar.md"

PACIFIC = ZoneInfo("America/Los_Angeles")
UTC = ZoneInfo("UTC")

# Months rendered as full calendar grids on the calendar page.
CALENDAR_MONTHS = [(2026, 6), (2026, 7), (2026, 8)]
WEEKDAY_HEADERS = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]

# Pike13: only these SUMMARY values are shown, each with its own label + color.
PIKE_GROUPS = {
    "Robot Garage": ("Robot Garage", "rg"),
    "League Labs Robots": ("Robots (Online)", "ro"),
    "League Labs Web Applications": ("Web Applications", "wa"),
}

# Calendar feeds pulled from .env.
#   env:    .env key holding the feed URL.
#   mode:   "pike"  -> keep only PIKE_GROUPS, label/color per group.
#           "named" -> show every event, labeled by its own title; one color
#                      and one legend entry (css/legend) for the whole feed.
#   popup:  True  -> clicking an entry opens a details dialog (time, location,
#                    description) instead of following a link.
SOURCES = [
    {"name": "Pike13", "env": "PIKE_CALENDAR", "mode": "pike"},
    {
        "name": "League Labs",
        "env": "LL_CALENDAR",
        "mode": "named",
        "css": "ll",
        "legend": "League Labs",
        "popup": True,
    },
    {
        "name": "Code Clinics",
        "env": "MEETUP_CALENDAR",
        "mode": "named",
        "css": "cc",
        "legend": "Code Clinics",
    },
]

BEGIN = "<!-- BEGIN GENERATED MEETINGS - edited by scripts/gen_meetings.py -->"
END = "<!-- END GENERATED MEETINGS -->"


def read_env():
    if not ENV.exists():
        sys.exit(f"error: {ENV} not found")
    env = {}
    for line in ENV.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        env[key.strip()] = value.strip()
    return env


def resolve_ics_url(value):
    """Turn an .env calendar value into a fetchable ICS URL."""
    value = value.strip()
    if value.startswith("webcal://"):
        return "https://" + value[len("webcal://") :]
    # A Google Calendar "add by cid" link -> public ICS feed.
    m = re.search(r"[?&]cid=([^&]+)", value)
    if m:
        cid = urllib.parse.unquote(m.group(1))
        cid += "=" * (-len(cid) % 4)  # restore base64 padding
        calid = base64.b64decode(cid).decode()
        return (
            "https://calendar.google.com/calendar/ical/"
            + urllib.parse.quote(calid)
            + "/public/basic.ics"
        )
    return value


def fetch_ics(url):
    req = urllib.request.Request(url, headers={"User-Agent": "league-labs-build"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8", "replace")


def unfold(text):
    # RFC 5545 line folding: a CRLF followed by a space/tab continues the line.
    return text.replace("\r\n", "\n").replace("\n ", "").replace("\n\t", "")


def ical_unescape(value):
    # RFC 5545 TEXT escaping: \n \, \; \\ .
    return (
        value.replace("\\n", "\n")
        .replace("\\N", "\n")
        .replace("\\,", ",")
        .replace("\\;", ";")
        .replace("\\\\", "\\")
    )


def attr_escape(value):
    """Escape a string for use inside an HTML double-quoted attribute."""
    value = (
        value.replace("&", "&amp;")
        .replace('"', "&quot;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )
    return value.replace("\r\n", "\n").replace("\n", "&#10;")


def parse_when(block, key):
    """Return (naive Pacific datetime, all_day) for a DTSTART/DTEND, or
    (None, False). UTC and TZID times are converted to America/Los_Angeles."""
    m = re.search(r"^" + key + r"([^:\n]*):([0-9TZ]+)", block, re.M)
    if not m:
        return None, False
    params, raw = m.group(1), m.group(2)
    if "VALUE=DATE" in params or "T" not in raw:
        return datetime.strptime(raw[:8], "%Y%m%d"), True
    naive = datetime.strptime(raw[:15], "%Y%m%dT%H%M%S")
    if raw.endswith("Z"):
        return naive.replace(tzinfo=UTC).astimezone(PACIFIC).replace(tzinfo=None), False
    tz = re.search(r"TZID=([^;:]+)", params)
    if tz:
        try:
            zone = ZoneInfo(tz.group(1))
            return (
                naive.replace(tzinfo=zone).astimezone(PACIFIC).replace(tzinfo=None),
                False,
            )
        except Exception:
            pass
    return naive, False


def parse_entries(text, source):
    """Parse a feed into calendar entries per the source's mode."""
    entries = []
    for block in re.findall(r"BEGIN:VEVENT(.*?)END:VEVENT", text, re.S):

        def field(key):
            m = re.search(r"^" + key + r"[^:\n]*:(.*)$", block, re.M)
            return ical_unescape(m.group(1).strip()) if m else ""

        summary = field("SUMMARY")
        start, all_day = parse_when(block, "DTSTART")
        if not start:
            continue
        end, _ = parse_when(block, "DTEND")
        if source["mode"] == "pike":
            if summary not in PIKE_GROUPS:
                continue
            label, css = PIKE_GROUPS[summary]
            legend = label
        else:
            label = summary or source["name"]
            css = source["css"]
            legend = source["legend"]
        entries.append(
            {
                "start": start,
                "end": end,
                "all_day": all_day,
                "label": label,
                "css": css,
                "url": field("URL"),
                "legend": legend,
                "popup": bool(source.get("popup")),
                "location": field("LOCATION"),
                "body": field("DESCRIPTION"),
            }
        )
    return entries


def fmt_time(dt):
    return dt.strftime("%I:%M %p").lstrip("0")


def format_when(entry):
    s = entry["start"]
    text = f"{s.strftime('%A, %B')} {s.day}, {s.year}"
    if not entry["all_day"]:
        text += f" · {fmt_time(s)}"
        if entry["end"]:
            text += f" – {fmt_time(entry['end'])}"
    return text


def current_monday():
    today = datetime.now().date()
    return today - timedelta(days=today.weekday())


CALENDAR_CSS = """<style>
.meeting-cal table.cal { width: 100%; border-collapse: collapse; table-layout: fixed; margin: 0.25rem 0 2rem; }
.meeting-cal th, .meeting-cal td { border: 1px solid #ccc; vertical-align: top; padding: 2px 3px; }
.meeting-cal th { background: #f3f3f3; text-align: center; font-size: 0.8rem; }
.meeting-cal td { height: 88px; font-size: 0.72rem; }
.meeting-cal td.empty { background: #fafafa; }
.meeting-cal .dnum { font-weight: bold; font-size: 0.8rem; text-align: right; color: #555; }
.meeting-cal .ev { display: block; border-radius: 3px; padding: 1px 4px; margin-top: 2px; line-height: 1.25; }
.meeting-cal .ev, .meeting-cal a.ev:link, .meeting-cal a.ev:visited, .meeting-cal a.ev:hover, .meeting-cal a.ev:focus { color: #fff; text-decoration: none; }
.meeting-cal a.ev:hover, .meeting-cal button.ev:hover { filter: brightness(1.1); }
.meeting-cal button.ev { width: 100%; border: 0; cursor: pointer; font: inherit; font-size: 0.72rem; text-align: left; }
.meeting-cal .ev .t { font-weight: bold; color: inherit; }
.meeting-cal .ev.wa { background: #2d6cdf; }
.meeting-cal .ev.rg { background: #2f9e44; }
.meeting-cal .ev.ro { background: #7048e8; }
.meeting-cal .ev.ll { background: #0c8599; }
.meeting-cal .ev.cc { background: #495057; }
.meeting-cal .legend { font-size: 0.8rem; margin-bottom: 1rem; }
.meeting-cal .legend span { display: inline-block; padding: 1px 8px; border-radius: 3px; color: #fff; margin-right: 0.5rem; margin-bottom: 0.25rem; }
.meeting-cal .legend .wa { background: #2d6cdf; }
.meeting-cal .legend .rg { background: #2f9e44; }
.meeting-cal .legend .ro { background: #7048e8; }
.meeting-cal .legend .ll { background: #0c8599; }
.meeting-cal .legend .cc { background: #495057; }
.meeting-dialog { max-width: 480px; width: 90%; border: 1px solid #ccc; border-radius: 6px; padding: 1.25rem 1.5rem; font-size: 0.95rem; line-height: 1.45; color: #222; }
.meeting-dialog::backdrop { background: rgba(0, 0, 0, 0.45); }
.meeting-dialog form.md-closeform { margin: 0; float: right; }
.meeting-dialog .md-close { border: 0; background: none; font-size: 1.5rem; line-height: 1; cursor: pointer; color: #888; padding: 0 0.25rem; }
.meeting-dialog .md-title { margin: 0 0 0.5rem; font-size: 1.15rem; }
.meeting-dialog .md-when { margin: 0 0 0.35rem; font-weight: bold; }
.meeting-dialog .md-loc { margin: 0 0 0.85rem; color: #555; }
.meeting-dialog .md-body { white-space: pre-wrap; }
</style>"""

DIALOG_HTML = """<dialog id="meeting-dialog" class="meeting-dialog">
<form method="dialog" class="md-closeform"><button class="md-close" aria-label="Close">&times;</button></form>
<h3 class="md-title"></h3>
<p class="md-when"></p>
<p class="md-loc"><strong>Location:</strong> <span class="md-loc-val"></span></p>
<div class="md-body"></div>
</dialog>"""

DIALOG_SCRIPT = """<script>
(function () {
  var dlg = document.getElementById("meeting-dialog");
  if (!dlg) return;
  document.querySelectorAll(".meeting-cal .ev[data-popup]").forEach(function (el) {
    el.addEventListener("click", function () {
      dlg.querySelector(".md-title").textContent = el.getAttribute("data-title") || "";
      dlg.querySelector(".md-when").textContent = el.getAttribute("data-when") || "";
      var loc = el.getAttribute("data-loc") || "";
      var locRow = dlg.querySelector(".md-loc");
      var locVal = dlg.querySelector(".md-loc-val");
      locRow.style.display = loc ? "" : "none";
      if (/^https?:\\/\\//.test(loc)) {
        locVal.innerHTML = "";
        var a = document.createElement("a");
        a.href = loc; a.textContent = loc; a.target = "_blank"; a.rel = "noopener";
        locVal.appendChild(a);
      } else {
        locVal.textContent = loc;
      }
      var body = el.getAttribute("data-body") || "";
      var bodyEl = dlg.querySelector(".md-body");
      if (/<[a-z][\\s\\S]*>/i.test(body)) { bodyEl.innerHTML = body; }
      else { bodyEl.textContent = body; }
      bodyEl.style.display = body ? "" : "none";
      if (typeof dlg.showModal === "function") { dlg.showModal(); }
      else { dlg.setAttribute("open", ""); }
    });
  });
  dlg.addEventListener("click", function (e) { if (e.target === dlg) dlg.close(); });
})();
</script>"""


def render_calendar(entries):
    """Render month-grid calendars with each day's meetings and times."""
    monday = current_monday()
    months = set(CALENDAR_MONTHS)
    shown = [
        e
        for e in entries
        if (e["start"].year, e["start"].month) in months
        and e["start"].date() >= monday
    ]

    byday = defaultdict(list)
    for e in shown:
        byday[e["start"].date()].append(e)

    # Legend: one entry per (color, label) actually visible, first-seen order.
    legend_items = []
    for e in shown:
        item = (e["css"], e["legend"])
        if item not in legend_items:
            legend_items.append(item)
    legend = "".join(f'<span class="{css}">{lbl}</span>' for css, lbl in legend_items)

    parts = [
        CALENDAR_CSS,
        '<div class="meeting-cal">',
        f'<p class="legend">{legend}</p>',
    ]
    cal = calmod.Calendar(firstweekday=6)  # weeks start on Sunday
    for year, month in CALENDAR_MONTHS:
        parts.append(f"<h2>{calmod.month_name[month]} {year}</h2>")
        parts.append('<table class="cal"><thead><tr>')
        parts.extend(f"<th>{wd}</th>" for wd in WEEKDAY_HEADERS)
        parts.append("</tr></thead><tbody>")
        for week in cal.monthdayscalendar(year, month):
            parts.append("<tr>")
            for day in week:
                if day == 0:
                    parts.append('<td class="empty"></td>')
                    continue
                cell = [f'<td><div class="dnum">{day}</div>']
                # all-day events first, then by start time.
                day_events = sorted(
                    byday.get(date(year, month, day), []),
                    key=lambda e: (not e["all_day"], e["start"]),
                )
                for e in day_events:
                    if e["all_day"]:
                        text = e["label"]
                    else:
                        text = f'<span class="t">{fmt_time(e["start"])}</span> {e["label"]}'
                    if e["popup"]:
                        cell.append(
                            f'<button type="button" class="ev {e["css"]}" data-popup="1"'
                            f' data-title="{attr_escape(e["label"])}"'
                            f' data-when="{attr_escape(format_when(e))}"'
                            f' data-loc="{attr_escape(e["location"])}"'
                            f' data-body="{attr_escape(e["body"])}">{text}</button>'
                        )
                    elif e["url"]:
                        cell.append(
                            f'<a class="ev {e["css"]}" href="{e["url"]}" '
                            f'target="_blank" rel="noopener">{text}</a>'
                        )
                    else:
                        cell.append(f'<span class="ev {e["css"]}">{text}</span>')
                cell.append("</td>")
                parts.append("".join(cell))
            parts.append("</tr>")
        parts.append("</tbody></table>")
    parts.append("</div>")
    if any(e["popup"] for e in shown):
        parts.append(DIALOG_HTML)
        parts.append(DIALOG_SCRIPT)
    return "\n".join(parts)


def replace_block(path: Path, default_front: str, body: str):
    """Insert/replace the generated block between markers, creating the file
    from default_front (a complete file template) if it does not yet exist."""
    block = f"{BEGIN}\n{body}\n{END}"
    if path.exists():
        text = path.read_text()
        if BEGIN in text and END in text:
            # Use a function replacement so backslashes in `block` (e.g. JS
            # regex escapes) are not interpreted as re replacement escapes.
            text = re.sub(
                re.escape(BEGIN) + r".*?" + re.escape(END),
                lambda _m: block,
                text,
                flags=re.S,
            )
        else:
            text = text.rstrip() + "\n\n" + block + "\n"
    else:
        text = default_front.rstrip() + "\n\n" + block + "\n"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def main():
    env = read_env()
    all_entries = []
    print("Reading calendar feeds:")
    for src in SOURCES:
        raw = env.get(src["env"])
        if not raw:
            print(f"  - {src['name']}: {src['env']} not set, skipping")
            continue
        try:
            text = unfold(fetch_ics(resolve_ics_url(raw)))
        except Exception as exc:
            print(f"  - {src['name']}: fetch failed ({exc}), skipping")
            continue
        ents = parse_entries(text, src)
        all_entries.extend(ents)
        print(f"  - {src['name']}: {len(ents)} event(s)")

    # Calendar entries link straight to their source, so the old per-meeting
    # detail pages are unused — remove them if a prior run created them.
    if MEETINGS_DIR.exists():
        shutil.rmtree(MEETINGS_DIR)

    # Team pages just link to the calendar.
    link_block = (
        "## Meetings\n\n"
        "See the **[meeting calendar](/calendar/)** for all upcoming session "
        "dates, times, and how to enroll."
    )
    replace_block(
        SUMMER / "web-applications.md",
        "---\ntitle: AI First Web Applications\n---\n",
        link_block,
    )
    replace_block(SUMMER / "robots.md", "---\ntitle: Robots\n---\n", link_block)

    # Main calendar page: full month grids for June, July, and August.
    replace_block(
        MAIN_CALENDAR,
        "---\ntitle: Calendar\n---\n",
        render_calendar(all_entries),
    )

    print("Done.")


if __name__ == "__main__":
    main()

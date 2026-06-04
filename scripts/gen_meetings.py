#!/usr/bin/env python3
"""Generate meeting pages from the Pike13 calendar feed.

Reads the PIKE_CALENDAR webcal/ICS URL from the project .env, pulls every
upcoming event (from the current Monday onward), and groups them into
"meetings" keyed by (group, start-end time). For each meeting it writes a
detail page that links to the Pike13 enrollment URL for every upcoming
session, and it lists those meetings under a level-one heading on the
Web Applications, Robots, and Calendar pages.

Only two groups are presented: Robot Garage and Web Applications. Anything
else on the calendar is ignored.

This script is run from the justfile before every Hugo build, so it is
idempotent: generated blocks live between HTML comment markers and are
rewritten in place on each run.
"""

import os
import re
import sys
import urllib.request
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ENV = ROOT / ".env"
SUMMER = ROOT / "site" / "content" / "teams" / "2026" / "summer"
MEETINGS_DIR = SUMMER / "meetings"

# SUMMARY value in the iCal -> presentation group.
#   label:     the level-one heading shown on listing pages.
#   slug_base: prefix for generated meeting page slugs.
GROUPS = {
    "Robot Garage": {"label": "Robots", "slug_base": "robot-garage"},
    "League Labs Web Applications": {
        "label": "Web Applications",
        "slug_base": "web-applications",
    },
}

# Order groups are presented in on the combined calendar page.
GROUP_ORDER = ["Web Applications", "Robots"]

BEGIN = "<!-- BEGIN GENERATED MEETINGS - edited by scripts/gen_meetings.py -->"
END = "<!-- END GENERATED MEETINGS -->"


def read_calendar_url():
    if not ENV.exists():
        sys.exit(f"error: {ENV} not found")
    for line in ENV.read_text().splitlines():
        line = line.strip()
        if line.startswith("PIKE_CALENDAR="):
            url = line.split("=", 1)[1].strip()
            return re.sub(r"^webcal://", "https://", url)
    sys.exit("error: PIKE_CALENDAR not set in .env")


def fetch_ics(url):
    req = urllib.request.Request(url, headers={"User-Agent": "league-labs-build"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8", "replace")


def unfold(text):
    # RFC 5545 line folding: a CRLF followed by a space/tab continues the line.
    return text.replace("\r\n", "\n").replace("\n ", "").replace("\n\t", "")


def parse_dt(value):
    # value like "20260601T140000" (already local America/Los_Angeles time).
    return datetime.strptime(value[:15], "%Y%m%dT%H%M%S")


def parse_events(text):
    events = []
    for block in re.findall(r"BEGIN:VEVENT(.*?)END:VEVENT", text, re.S):
        def field(key):
            m = re.search(r"^" + key + r"[^:\n]*:(.*)$", block, re.M)
            return m.group(1).strip() if m else ""

        summary = field("SUMMARY")
        if summary not in GROUPS:
            continue
        ds = re.search(r"DTSTART[^:\n]*:([0-9T]+)", block)
        de = re.search(r"DTEND[^:\n]*:([0-9T]+)", block)
        if not ds:
            continue
        start = parse_dt(ds.group(1))
        end = parse_dt(de.group(1)) if de else None
        url = field("URL")
        events.append({"summary": summary, "start": start, "end": end, "url": url})
    return events


def fmt_time(dt):
    s = dt.strftime("%I:%M %p").lstrip("0")
    return s


def time_range(start, end):
    if not end:
        return fmt_time(start)
    return f"{fmt_time(start)}–{fmt_time(end)}"


def fmt_date(dt):
    # "Saturday, June 6, 2026"
    return f"{dt.strftime('%A')}, {dt.strftime('%B')} {dt.day}, {dt.year}"


def current_monday():
    today = datetime.now().date()
    return today - timedelta(days=today.weekday())


def build_meetings(events):
    """Group events into meetings keyed by (summary, start time, end time)."""
    monday = current_monday()
    buckets = defaultdict(list)
    for ev in events:
        if ev["start"].date() < monday:
            continue
        key = (
            ev["summary"],
            ev["start"].strftime("%H%M"),
            ev["end"].strftime("%H%M") if ev["end"] else "",
        )
        buckets[key].append(ev)

    meetings = []
    for (summary, hstart, _hend), occ in buckets.items():
        occ.sort(key=lambda e: e["start"])
        first = occ[0]
        g = GROUPS[summary]
        meetings.append(
            {
                "summary": summary,
                "label": g["label"],
                "slug": f"{g['slug_base']}-{hstart}",
                "title": f"{summary} — {time_range(first['start'], first['end'])}",
                "range": time_range(first["start"], first["end"]),
                "occurrences": occ,
            }
        )
    # Stable ordering: by group order, then by start time.
    meetings.sort(key=lambda m: (GROUP_ORDER.index(m["label"]), m["slug"]))
    return meetings


def replace_block(path: Path, default_front: str, body: str):
    """Insert/replace the generated block between markers, creating the file
    from default_front (a complete file template) if it does not yet exist."""
    block = f"{BEGIN}\n{body}\n{END}"
    if path.exists():
        text = path.read_text()
        if BEGIN in text and END in text:
            text = re.sub(
                re.escape(BEGIN) + r".*?" + re.escape(END), block, text, flags=re.S
            )
        else:
            text = text.rstrip() + "\n\n" + block + "\n"
    else:
        text = default_front.rstrip() + "\n\n" + block + "\n"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def meeting_page_body(meeting):
    lines = [
        f"Meetings run on the following dates at **{meeting['range']}**. "
        "Click the enrollment link for the session you want to attend — "
        "Pike13 has the meeting link and the full schedule, including when the "
        "meeting ends.",
        "",
        "## Upcoming Sessions",
        "",
    ]
    for ev in meeting["occurrences"]:
        date = fmt_date(ev["start"])
        time = fmt_time(ev["start"])
        if ev["url"]:
            lines.append(
                f"- **{date} — {time}** — "
                f"[To enroll in this meeting, click here]({ev['url']})"
            )
        else:
            lines.append(f"- **{date} — {time}**")
    return "\n".join(lines)


def listing_for_group(meetings, label):
    """Build the level-one heading + dated list block for one group."""
    group = [m for m in meetings if m["label"] == label]
    lines = [f"# {label}", ""]
    if not group:
        lines.append("_No upcoming meetings scheduled._")
        return "\n".join(lines)
    multi = len(group) > 1
    for m in group:
        page = f"/teams/2026/summer/meetings/{m['slug']}/"
        if multi:
            lines.append(f"**{m['summary']} — {m['range']}**")
            lines.append("")
        for ev in m["occurrences"]:
            label_txt = f"{fmt_date(ev['start'])} — {fmt_time(ev['start'])}"
            lines.append(f"- [{label_txt}]({page})")
        lines.append("")
    return "\n".join(lines).rstrip()


def main():
    url = read_calendar_url()
    print(f"Fetching calendar: {url.split('?')[0]}...")
    text = unfold(fetch_ics(url))
    events = parse_events(text)
    meetings = build_meetings(events)
    print(f"Found {len(meetings)} meeting(s) from {len(events)} matching event(s):")
    for m in meetings:
        print(f"  - {m['title']}  ({len(m['occurrences'])} sessions)  /{m['slug']}/")

    # Ensure the meetings section has an _index so Hugo lists it.
    replace_block(
        MEETINGS_DIR / "_index.md",
        "---\ntitle: Meeting Schedule\n---\n",
        "Select a meeting below to see upcoming sessions and how to enroll.",
    )

    # One detail page per meeting.
    for m in meetings:
        front = f"---\ntitle: {m['title']}\n---\n"
        replace_block(MEETINGS_DIR / f"{m['slug']}.md", front, meeting_page_body(m))

    # Listing blocks on the two team pages (one group each).
    replace_block(
        SUMMER / "web-applications.md",
        "---\ntitle: AI First Web Applications\n---\n",
        listing_for_group(meetings, "Web Applications"),
    )
    replace_block(
        SUMMER / "robots.md",
        "---\ntitle: Robots\n---\n",
        listing_for_group(meetings, "Robots"),
    )

    # Combined calendar page with both groups.
    combined = "\n\n".join(listing_for_group(meetings, g) for g in GROUP_ORDER)
    replace_block(
        SUMMER / "calendar.md",
        "---\ntitle: Meeting Calendar\n---\n",
        combined,
    )

    print("Done.")


if __name__ == "__main__":
    main()

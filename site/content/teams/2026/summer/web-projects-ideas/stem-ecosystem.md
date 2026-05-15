---
title: STEM Ecosystem
weight: 70
menu:
  main:
    parent: project-ideas
    weight: 70
---

A revamp of the [San Diego STEM Ecosystem](https://www.sdstemecosystem.org) site, centered on a scraper-fed event aggregator that pulls kid-friendly STEM happenings from across the region into one searchable calendar.

## The problem

San Diego is full of casual, kid-friendly STEM events — beach cleanups, tide-pool walks, astronomy nights, bug-collecting field days, museum free-admission days, "pet the sharks" sessions at aquariums, citizen-science bird counts, robotics open houses. They're run by dozens of different organizations: the Birch Aquarium, the Fleet Science Center, the Natural History Museum, regional parks, Audubon chapters, university outreach groups, and a long tail of small nonprofits and clubs.

The information lives in dozens of separate event calendars, Eventbrite pages, Facebook events, and PDFs. A parent looking for "something STEM-y to do with the kids on Saturday" has no single place to look. The current sdstemecosystem.org site is a partner directory, not a calendar — it lists organizations but not what they're doing this weekend.

## Users

* **Parents and caregivers** looking for weekend or after-school STEM activities for their kids.
* **Teachers and youth-group leaders** scouting field-trip targets or extra-credit opportunities.
* **Partner organizations** that want their events to show up in a regional calendar without having to publish them in two places.
* **Site editors** who curate, tag, and clean up scraped data.

## What the app does

* Scrapes events from a configurable list of partner sites — museums, aquariums, parks, universities, nonprofits — on a schedule.
* Normalizes each scraped event into a common shape: title, description, date and time, location, age range, cost, source URL, organization.
* Tags events with STEM categories (astronomy, marine biology, coding, engineering, ecology, etc.) and audience (toddlers, grade school, middle school, families).
* Presents a searchable, filterable event calendar — by date range, category, age, neighborhood, cost.
* Provides an editor view where humans can review newly scraped events, fix bad data, hide duplicates, or promote an event to "featured."
* Keeps the existing partner directory but ties each partner to the events scraped from its site.

## Core pieces to build

* A scraper framework with a per-source adapter — each partner site needs its own small extractor (HTML, RSS, ICS feed, Eventbrite API, etc.).
* A scheduled job runner to refresh sources without overwhelming them.
* An event model with normalized fields, source provenance, and a dedup key.
* A tagging / categorization step, possibly with an LLM-assisted first pass that an editor reviews.
* A public calendar UI with filters and a map view.
* An admin UI for source management, event review, and overrides.

## Possible stretch features

* Email or SMS subscriptions: "tell me about astronomy events for ages 8–12 within 20 miles."
* A submission form for organizations whose sites aren't scrapeable.
* Auto-detection of recurring events and series.
* iCal / Google Calendar export of any filtered view.
* A "this weekend" digest published as a newsletter.
* Photos and short summaries auto-generated from the source page.
* Attendance check-ins or a passport program — kids earn badges for visiting different STEM sites over the summer.


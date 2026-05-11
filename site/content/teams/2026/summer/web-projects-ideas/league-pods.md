---
title: League Pods
weight: 10
menu:
  main:
    parent: project-ideas
    weight: 10
---

A platform that lets parents organize small after-school or enrichment pods around a class or activity, then book a vendor to actually run it.

## The problem

Lots of good after-school programs exist — science classes, language tutors, robotics, music — but families end up booking them one at a time, alone. The vendor has to travel to a venue or rent a space, the family has to drive their kid across town, and friends rarely end up in the same session. Meanwhile, plenty of parents would happily host four to eight kids at their house, church basement, or community room if someone else handled the coordination.

For the League of Amazing Programmers specifically, this is how we'd recruit small neighborhood cohorts: a parent commits to hosting ten sessions of a programming class, the system finds the other families, and a League instructor shows up.

## Users

* **Host parents** — willing to commit a space (home, church, community room) and a recurring time slot.
* **Member families** — want their kid in a small-group enrichment activity with people they know.
* **Vendors** — providers like the League, science enrichment companies, language tutors, art instructors. They want filled cohorts without having to do their own marketing.

## What the app does

* Lets a host pick an activity from a vendor catalog (or invite a new vendor).
* Lets the host post the pod: where, when, how many seats, what the per-session cost is, and how long the commitment runs (e.g., ten sessions).
* Recruits other families through the system — invites to existing friends, plus a discovery feed for parents looking for pods nearby.
* Handles enrollment, the cost split, and the booking handoff to the vendor once a quorum is reached.
* Tracks the session schedule and sends reminders.

## Core pieces to build

* A vendor catalog with offerings, pricing, group-size requirements.
* A pod object: host, location, schedule, vendor, roster, cost split, status.
* A discovery and invitation flow (search by zip code, age range, activity type; invite by email or share link).
* A simple payments hand-off (this can be a stub for v1 — record amounts owed, don't actually process cards yet).
* A vendor dashboard so the vendor can see committed pods and confirm them.

## Possible stretch features

* Rotating hosts within a pod, with the schedule reflecting whose house is up next.
* A waitlist that auto-promotes when someone drops.
* Vendor self-onboarding (a vendor signs up, lists their offering, gets discovered).
* Integration with a calendar feed so parents can subscribe.


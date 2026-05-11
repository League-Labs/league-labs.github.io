---
title: Summer Camp Jam
weight: 20
menu:
  main:
    parent: project-ideas
    weight: 20
---

A planning app for parents who want their kids to go to summer camps *with their friends*, not just to summer camps in general.

## The problem

Picking summer camps is already painful — dozens of providers, sessions that run a week or two at a time, registration that opens months in advance, prices and ages and locations all different. Now add the real constraint: most parents care less about which camp than about which other kids will be there. Their kid wants to be with their friends. The parents would like to carpool. Trying to coordinate this across four families and twelve weeks of summer over text messages is miserable.

## Users

* **Parents** with kids age roughly 6–14 who plan summer in advance with a friend group.
* **Friend-group organizers** — usually one parent per group who informally does the coordinating.
* Optionally **camp providers**, but the v1 doesn't need their cooperation; the app can pull data without them.

## What the app does

* Scrapes or imports summer camp listings from common sources (city rec departments, local providers, well-known regional camps, individual provider websites).
* Lets a parent build their kid's "wishlist" of camps and weeks.
* Lets parents form a friend group and share their wishlists.
* Computes the overlap — which weeks do multiple kids in the group have at the same camp, where are the gaps, where could a small nudge ("switch from Week 3 to Week 4 of Camp X") get four kids in one room.
* Helps organize carpools for the weeks where the overlap exists.
* Optionally tracks registration status (registered, on waitlist, missed the deadline) so the group can see at a glance who's set.

## Core pieces to build

* A scraper or import pipeline for camp listings, with a normalized schema (name, provider, weeks offered, ages, location, price, URL).
* A wishlist model per kid.
* A friend-group object with shared visibility into wishlists.
* A schedule-overlap view — calendar grid, color coded by kid, with markers for "matched with friends here."
* A carpool roster per matched week.

## Possible stretch features

* A "what if" mode that suggests small wishlist changes to maximize friend-overlap.
* Direct deep-links to registration pages, with a queue for "registration opens at 9am on March 1" reminders.
* Cost summary across the summer per family.
* iCal export.


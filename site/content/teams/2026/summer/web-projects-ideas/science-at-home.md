---
title: Science at Home
weight: 40
menu:
  main:
    parent: project-ideas
    weight: 40
---

A booking marketplace for short, science-themed events — birthday parties, classroom visits, library demos, scout meetings. Same shape as League Pods, but for one-off bookings instead of multi-session pods.

## The problem

Parents planning a kid's birthday will happily pay someone to show up with volcanoes, robots, or a portable planetarium for an hour. Teachers and librarians want the same thing for a classroom or after-school slot. There are providers who do exactly this work — moonlighting science teachers, robotics clubs, the occasional small business — but finding them is mostly word of mouth and Google. Booking is usually email tag.

A focused marketplace just for short, science-flavored events would solve both ends of the problem: providers get a listing and a booking calendar, and parents and teachers get a quick way to find and book someone for a specific date.

## Users

* **Parents** planning birthday parties or backyard events.
* **Teachers, librarians, scout leaders** booking demos for groups.
* **Providers** — science educators, robotics enthusiasts, makers, college students with kits — who'll show up with materials and run a 60–90 minute session.

## What the app does

* Lists providers and their offerings: "volcano chemistry, ages 5–8, 60 minutes, $200, serves up to 12 kids."
* Shows provider availability — a calendar with bookable slots.
* Lets families and teachers request a booking for a specific date and address.
* Handles confirmation, basic logistics (number of kids, ages, space available, power outlets, who brings what), and a follow-up review.
* Optionally collects a deposit or payment.

## Core pieces to build

* Provider profile and offering catalog.
* Booking-request and confirmation flow.
* A calendar / availability model per provider.
* A booking object with logistics fields, location, status.
* A search and filter UI by topic, age range, location, price.

## Possible stretch features

* Geographic search and travel-fee calculation.
* Reviews and ratings.
* Provider self-onboarding with verification.
* Package deals (e.g., a science-themed birthday includes demo + party favors + a printable invite kit).


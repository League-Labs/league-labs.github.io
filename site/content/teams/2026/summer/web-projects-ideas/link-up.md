---
title: Link Up
weight: 60
menu:
  main:
    parent: project-ideas
    weight: 60
---

A group scheduling app for friend groups, clubs, and study squads — merges everyone's calendars, asks an AI for the parts that aren't on a calendar, and proposes the times when the most people can actually pull up.

## The problem

Pinning down a time when six friends are all free is brutal. Calendar merging (Google's "find a time") only works if everyone's in the same org and only sees literal events. Polling tools (Doodle, When2Meet) work across groups but everyone has to click a grid for every meeting, and nobody does. Group chats spiral into "Thursday?" "Can't, practice" "Friday?" "Saturday morning?" forever.

What's missing: most of what makes someone unavailable isn't on their calendar. "I never do mornings on weekends." "I have practice Tuesdays and Thursdays." "Don't text me Sunday nights." Those rules live in people's heads. An app that captures them — without making someone fill out a grid — and merges them across a friend group would land on a working time on the first try.

## Users

* **Friend groups** trying to plan a hangout, a movie night, a game session.
* **Clubs, teams, group projects** that need a recurring weekly time.
* **Whoever ends up organizing things** — they get the bot that proposes times so they don't have to.
* **People who don't actually keep a calendar** but have a predictable life (most teenagers). The voice-AI preferences mode is mostly for them.

## What the app does

* Each person joins a squad. Their availability gets merged with the squad's.
* Optionally connects a real calendar (Google, Apple) read-only — the app sees busy/free, not what the event is.
* Or — and this is the interesting part — builds a "preferences calendar" by talking to an AI. You say: "I'm free Tuesday and Thursday after 5, never weekends before noon, hate mornings, busy with practice 6-8pm weeknights." The AI turns that into a soft weekly availability pattern you can share.
* When someone in the squad asks for a meeting, the app proposes the top five times in the next two weeks when the most people are available. Hard busy (a real event on a calendar) counts more than soft busy (a preference rule).
* The squad votes on the proposed times by reacting.
* Optionally lives in your group chat. Drop "@linkup find us 2 hours next week" in Discord and the bot replies with options the group reacts to.
* Once locked, the meeting gets published to everyone's calendar.

## Core pieces to build

* Google Calendar OAuth for the read-only busy/free feed. (iCal URL import is a faster v1 if OAuth becomes a rabbit hole.)
* A preferences-calendar model: a weighted, recurring availability pattern per user (a grid of weights, not just busy/free).
* The AI preferences capture: a text or voice intake that turns a paragraph like "I hate mornings, busy with practice Tues/Thurs night" into the structured availability pattern. The team can use an LLM API and a careful prompt — it's the smallest amount of ML for the biggest win.
* A squad object with members and shared scheduling state.
* A scoring function that combines hard busy, soft busy, and preference weight across all members and ranks candidate time slots.
* A voting UI on the proposed slots.
* A chat-bot integration. Discord webhook is the simplest target.

## Possible stretch features

* Recurring meetings — once a time is set, the bot watches for someone's calendar changing and proposes a reschedule before it conflicts.
* "Never again" reactions — react to a proposed slot with a no-emoji and the AI updates your preferences so it stops suggesting that window.
* Time-zone-aware grouping if the squad has members in different cities.
* Anonymous mode — the squad sees proposed times but not who's blocking which slot, so nobody feels called out.
* "Slide" mode — instead of voting, the first three people to react to a slot lock it in.

## Why it's a reasonable summer project

The scheduling core (busy-merge + scoring + voting) is well-understood territory — a working v1 ships fast. The interesting work is the preferences model and the AI intake; that's where the team builds something that doesn't exist in Doodle or Google. The Discord bot makes for a demo that immediately works in the team's own group chat. And the students are the target users — they can dogfood it on every meeting and group project they have for the rest of the year.

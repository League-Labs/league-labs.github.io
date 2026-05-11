---
title: The Quartermaster
weight: 50
menu:
  main:
    parent: project-ideas
    weight: 50
---

An inventory and lending system for tabletop gamers — Dungeon Masters and players who own boxes of minis, terrain tiles, dungeon walls, doors, props, dice, and books, and who want to keep track of what they own and lend or trade items with friends.

## The problem

D&D and other tabletop games quietly accumulate stuff. A long-running DM might have hundreds of painted minis, a couple of terrain sets, a tower of pre-painted dungeon tiles, modular walls, doors, treasure chests, the printed adventures, the maps, the dice. Players have their own minis. Nobody knows where anything is. Friends would happily lend out the goblin warband they painted three years ago and haven't used since, but there's no convenient way to know who has what.

Right now this is solved by group chats, a memory of who painted the bugbears, and the occasional sad email asking whether anyone has a frost giant. A real inventory + lending app would let a small gaming community share their collections.

## Users

* **Dungeon Masters and game masters** who own most of the terrain and minis.
* **Players** with their own minis and books they're willing to share.
* **Game groups and clubs** that want a shared visible pool of equipment.

## What the app does

* Lets a user catalog their collection: minis (with creature type, size, paint status, photo), terrain pieces, books, modules, dice, accessories.
* Supports bulk entry — most collectors don't want to add 200 items one form at a time. Photo upload with optional tagging, CSV import, or quick-add by typing.
* Groups items into sets ("Reaper Bones III Kickstarter", "Dwarven Forge Cavern Set", "Goblin warband — painted").
* Lets users mark items as available for loan, trade, or sale.
* Tracks who has what right now — if you lend the dragon to your friend, the app records the loan and reminds both of you.
* Supports a "wishlist" so you can flag items you'd like to borrow if they ever show up in a friend's collection.
* Has a search across a connected group of users — "who has a tarrasque?", "any modular cavern walls within ten miles?"

## Core pieces to build

* An item model with category, attributes, photos, location, owner.
* A collection / set model for grouping.
* A loan transaction with a status machine (requested, agreed, picked up, returned).
* A user-to-user "connection" so collections are shared with friends/groups, not the whole internet.
* Search and filtering by category, size, system, paint status.
* A photo upload and gallery view.

## Possible stretch features

* OCR or barcode scanning for printed books and boxed sets.
* Integration with public mini databases (Reaper, WizKids, etc.) to auto-fill creature type and stats when you add a mini.
* A "campaign-mode" view: tag items as in-use for a current campaign so they show up flagged when you're prepping the next session.
* Wear-and-paint condition tracking with photos over time.
* A printable inventory sheet for con or game-day setup.
* A "session bag" — pack a list of items for tonight's game, check them out, check them back in.

## Why it's a reasonable summer project

The core inventory model is small but the app needs to handle the messy reality of tabletop gear: a hundred kinds of object, photo-heavy entries, social trust between owners and borrowers. It exercises CRUD, file uploads, search, a state machine for loans, and a permission model — all genuinely useful skills, in a domain the students likely care about. Bonus: the team can dogfood it on its own collections during the build.

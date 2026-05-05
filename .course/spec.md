# Curik Course Specification

## Course Concept
League Labs is a public-facing site for the League of Amazing Programmers' introductory internship program for high school students. Interns join project teams, study a programming or computer science topic, build a short class or artifact, and share their work with other students.

The site's core jobs are to explain the program, onboard participants, organize current teams, archive prior cohorts, and publish operational updates such as schedules and kickoff instructions.

Primary audience: current and prospective League Labs interns in high school, plus mentors and instructors who coordinate teams and logistics.

## Pedagogical Model
The pedagogical model is project-based apprenticeship rather than a linear lesson sequence. Students learn inside a team structure, work on a shared robotics-oriented theme or other cohort project, use curated resources, and produce practical outputs such as guides, firmware, datasets, analyses, or mini-lessons for peers.

Instruction is lightweight and distributed across team pages, onboarding posts, calendar coordination, and mentor-led meetings. The Hugo conversion should preserve that model by treating the site as a curriculum-adjacent internship hub with sections for onboarding, teams, archives, and news.

## Research Summary
Evidence from the existing Jekyll site shows three recurring content patterns: program overview and logistics pages, current and archived team pages with project/resource lists, and dated announcement posts. Team pages emphasize hands-on tools such as Python, data analysis, machine vision, robotics, and simulation. Posts focus on onboarding, meetup links, and scheduling workflows.

This indicates that the converted Hugo site should optimize for easy navigation, durable archives, and low-friction publishing of updates, rather than for a conventional lesson-by-lesson curriculum progression.

## Alignment Decision
Alignment decision: model the repo in Curik as a curriculum-supporting internship site rather than a traditional course. Use Curik metadata and Hugo structure to describe the program clearly, while preserving the existing public information architecture: home page, calendar, teams, summer-archive pages, and news posts. Where Curik expects course-style fields, map them to the internship program at a coarse grain instead of inventing a fake lesson sequence.

## Course Structure Outline
Proposed Hugo information architecture:

1. Home page with program description, active teams, archive link, and announcement listing.
2. Calendar page for League Labs and Code Clinic schedules.
3. Teams section for current cohort subteams.
4. Summer 2025 archive subsection for prior team pages and idea/resource lists.
5. News section migrated from Jekyll posts for announcements and onboarding updates.
6. Optional about page retained only if it is still intentionally part of the site.

This preserves existing URLs where practical while moving all publishable content under Hugo's content tree.

## Assessment Plan
Assessment is indirect and programmatic rather than quiz-based. Success indicators are whether interns can find their team, complete onboarding steps, access schedules and communication channels, and use team pages to identify project ideas and resources.

For the conversion itself, acceptance criteria are structural: all current pages and posts render in Hugo, the main navigation and internal links still work, archives remain accessible, and the site builds cleanly with Curik/Hugo tooling.

## Technical Decisions
Technical decisions for the conversion:

1. Use Hugo as the sole site generator and retire Jekyll-only layout assumptions.
2. Migrate the repository from the legacy root Hugo layout into Curik's current site structure if required by the CLI.
3. Move Markdown content into Hugo's content tree, converting Jekyll pages to Hugo pages and _posts entries to Hugo news posts with preserved dates and slugs.
4. Preserve relative URLs and public paths where feasible, using Hugo front matter and section structure instead of custom theme edits.
5. Keep the Curik-managed theme read-only and confine changes to content, configuration, and non-theme templates only when strictly necessary.

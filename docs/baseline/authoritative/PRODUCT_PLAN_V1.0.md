# Product Plan v1.0 — Consolidated reconstruction

Status: PROPOSED replacement baseline; pending Project Owner ratification. Not a verbatim historical document. Read BASELINE_INDEX.md and PO_REVIEW_RESPONSE.md for controlling scope changes.

## Vision and positioning
Build a premium AI personal fitness coach that connects training, nutrition, recovery, progress and eventually community and endurance. Inspiration: Zing Coach premium experience, Cal AI low-friction nutrition, Strava engagement; independent brand and design. The coach is a contextual product experience, not merely a chatbot. Core loop: onboarding → personalized plan → workout → feedback → coaching → confirmed adjustment → progress.

Initial audience hypothesis: adults 18+, beginner/intermediate, busy professionals seeking strength, muscle, general fitness or basic weight loss. Market, geography, willingness to pay and accessibility research remain pending. No medical diagnosis or treatment positioning.

## Product requirements and roadmap
P0 means required for the relevant release, P1 important but deferrable, P2 optional, P3 future. Historical feature IDs below are preserved; individual story mapping requires repository reconciliation. Current MVP overrides are in PO review and technical plan.

| Release | Indicative window | Scope |
|---|---|---|
| Discovery | Weeks 1–2 target | Research, prototype, feasibility, governance |
| Functional alpha | End week 8 target | Plan, workout, feedback, basic coaching; safety gate before external users |
| Closed beta | End week 16 target | Core MVP, offline, contextual AI, basic adaptation, progress |
| Commercial V1 | Months 5–6 hypothesis | Nutrition, annual subscription, billing |
| V1.5 | Months 7–8 hypothesis | Advanced adaptation, recovery, proactive coach, health integrations |
| V2 | Months 9–10 hypothesis | Social, challenges |
| V3 | Months 11–12 hypothesis | Running and endurance |

No date or budget is committed. Later phases require separate discovery and approval.

## Core MVP scope
P0: email/Apple/Google authentication, password recovery where applicable, account deletion and data management; onboarding (profile, age, height, weight, goals, experience, equipment, availability, limitations); approved exercise library (target 50–100, rights and expert review pending); personalized plan, schedule/rest days, substitutions, rescheduling, immutable versions; workout sets/reps/weights/rest timer, history, local persistence, resume and synchronization; AI chat, context, structured memory with user controls, recommendation cards, basic adaptive suggestions, pre/post-workout coaching, feedback including difficulty/soreness; basic progress and weight tracking; reminders/preferences; privacy-safe analytics, minimal administration, security, consent and evaluation.

P1: PRs, basic expert-approved progressive overload, weekly summary, missed-workout reminders, AI feedback, entitlement foundation; Nutrition Lite conditional on evidence and capacity. Nutrition Lite means approved calorie/protein targets, manual calorie/macros logging, daily summary and read-only coaching context; no photo recognition or food database. No automatic plan activation or material adjustment without confirmation.

## Product backlog inventory
IDs are historical feature families, not new technical tasks. Priorities in the controlling MVP scope supersede earlier priorities. Do not silently renumber or infer missing individual mappings.

| IDs | Capabilities | Release |
|---|---|---|
| DIS-001–006 | Market, competitors, personas, journey, PRD, information architecture | Discovery |
| UX-001–005 | Brand, design system, wireframes, high fidelity, usability | Discovery/MVP |
| ARCH-001–006 | Architecture, data, AI POC, security, CI/CD, cost | Discovery |
| AUTH-001–006 | Email, Apple, Google, password, deletion, data | MVP |
| ONB-001–009 | Personal details, measurements, goal, experience, equipment, availability, limitations, assessment, AI plan | MVP |
| AI-001–013 | Chat, streaming, history, memory, context, recommendations, generation, modification, motivation, safety, feedback, usage, rate limits | MVP |
| TRN-001–012 | Muscle, weight loss, general, home, gym, weekly schedule, calendar, replacement, reschedule, versioning, overload, regeneration | MVP |
| EXL-001–004 | Library, demonstrations, search/filter, muscle groups | MVP |
| WKT-001–011 | Start, sets, reps, weights, timer, previous reference, summary, history, PR, offline, resume | MVP |
| PRG-001–005 | Weight, frequency, volume, strength, weekly summary | MVP |
| NTF-001–003 | Reminders, preferences, missed workouts | MVP |
| REC-001 | Post-workout feedback | MVP |
| ADM-001–006 | Admin auth, users, catalog, AI usage, configuration, feedback | MVP minimal subset |
| OPS-001–003 | Errors, cost, audit | MVP |
| NUT-001–016 | Photo capture, recognition, calorie/protein/carbs/fat estimates, portion correction, manual logging, food database, dashboard, targets, history, favorites, barcode, recommendations | Commercial (Lite conditional earlier) |
| PRG-006 | Body composition | Commercial |
| SUB-001–011 | Annual plan, Apple/Google billing, verification, restore, management, entitlement, expiry, fair use, trial, conversion | Commercial |
| REC-002–007 | Daily check-in, energy, soreness, sleep, motivation, recovery | V1.5 |
| AI-014–019 | Performance/fatigue/recovery adaptation, proactive coaching, missed workout, weekly review | V1.5 |
| TRN-013–014 | Advanced overload, deload | V1.5 |
| NTF-004–007 | Check-ins, contextual notifications, replies, quiet hours | V1.5 |
| INT-001–010 | HealthKit, Health Connect, steps, workouts, sleep, heart rate, weight, permissions, dedup, disconnect | V1.5 |
| SOC-001–011 | Profile, search, follow, feed, workout/achievement sharing, likes/comments, privacy, report/block | V2 |
| ADM-007 | Moderation | V2 |
| CHL-001–009 | Weekly/rest-aware streaks, badges, friends leaderboard, individual/group challenges, invites, progress, rewards | V2 |
| RUN-001–010 | GPS, distance/pace/duration, map, history, beginner, 5k/10k, half/full marathon, analytics, adaptive endurance | V3 |
| INT-011–013 | Garmin, WHOOP, other integrations | Future, access unverified |

## Experience
Proposed five tabs: Today, Training, Coach, Nutrition, Progress. Hide unavailable modules in MVP; validate navigation in prototype. Onboarding: welcome/account → profile → goal → experience/equipment → schedule/limitations → plan preview → confirmation → Today. Premium typography, consistent tokens, accessible contrast and touch targets, low-tap workout logging, offline and failure states, streaming and structured cards. Community entry points deferred. Full-product screen count 82–123 was an early rough hypothesis, not a deliverable count.

## Monetization and operations
Annual all-access subscription hypothesis; Apple/Google IAP, restore, server verification, entitlement and expiry, transparent fair use and usage monitoring. Trial/preview and pricing require research. No unlimited AI promise. Admin access restricted; health data private by default. Food-photo estimates must be editable; social reporting/blocking and rest-day-aware streaks required when released.

## Measurement hypotheses
North Star: Weekly Active Coached Users (at least one training/nutrition plan action plus meaningful coaching interaction in a week). Define denominators and event windows before launch. Proposed targets, not observed benchmarks: onboarding completion ≥75%; plan acceptance ≥70%; first workout within 48h ≥50%; adherence ≥60%; WAU/MAU ≥50%; D7 ≥35%; D30 ≥20%; trial conversion ≥10%; helpful AI ≥85%; valid plan ≥99%; crash-free sessions ≥99.5%. D30 requires follow-up beyond beta. Small samples are directional, not automatic release gates.

## Research and risks
Interview 10–15, prototype test 5–8, alpha 10–20, beta 50–100 as proposed sample sizes. Validate personalized plan, contextual memory, feedback adaptation, nutrition demand, annual willingness to pay and non-annoying reminders. Risks: scope, unsafe advice, inaccurate nutrition, content rights, privacy, AI cost, retention, store review, integration access, moderation. PO owns prioritization; fitness/nutrition experts approve rules. Target market, budget, team, content rights, provider contracts and actual benchmarks remain pending.

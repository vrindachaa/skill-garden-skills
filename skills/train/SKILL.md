---
name: train
description: "Use when teaching an agent a skill. Run the course."
version: 0.2.0
author: V + Chiron
license: MIT
platforms: [linux, macos, windows]
metadata:
  published: true
  hermes:
    tags: [training, teaching, curriculum, agents, grading, professor, entrustment]
    related_skills: [course-design, student-drills, gradebook]
---

# Train

The entrypoint. Runs a full course: a subject goes in, a student agent that provably has the skill comes out — or a diagnosis explaining why it doesn't.

Load `course-design` for phase 3, `student-drills` for phase 5, `gradebook` for phase 6.

## Vocabulary

| Term | Meaning |
|---|---|
| **student** | A Hermes profile invoked non-interactively over the CLI. |
| **course** | One subject taught to one student, in `<training-root>/courses/<student>-<subject>/`. |
| **packet** | syllabus + lessons + formative work + demonstrations + exams + rubrics. The thing the course owner signs off. |
| **formative run** | Ungraded, mechanically-checked dry run. **Not** an attempt; no letter. |
| **attempt** | One paid student run against a graded exam. Max 3 per exam. |
| **calibration gap** | \|student's self-grade − your grade\|. Measures whether it knows what it doesn't know. |
| **entrustment** | Supervision level at which the student may do this without you (1–5). |

## Resume existing coursework before planning

When the course owner names a student and unit, search `<training-root>/courses/` and the gradebook first. Read the existing syllabus, matching lesson/exam/rubric and sign-off; resume that scope rather than redesigning the course. Treat approval of one deliverable as authorization for that deliverable only, not the whole syllabus or a retry batch.

For a requested quick baseline, provide one standalone, copy-paste task brief: state the subject, output directory, constraints, evidence and stopping condition directly. Remove unit labels, course explanations, lesson/demo links and instructor-rubric references from student-facing instructions. A fresh student should need no teaching context to attempt the task. Preserve the assessment contract for the later comparison; a baseline is pre-instruction evidence, not a separate control group.

## Phase 0 — Placement (before planning)

Don't design a course for a student you haven't measured. Placement decides *what coverage is required*, and stops you teaching what it already owns.

**Performance-based, never a survey.** "What do you know about X" is self-report and earns nothing.

**Adaptive ladder, not a fixed test.** Start easy, stop at first failure — the stopping point *is* the coverage map. A fixed hard test scores F everywhere and tells you nothing about where to start.

**Two micro-tasks minimum:**
1. A **tooling** task — can it run the tool headlessly at all. This checks the chain, not knowledge.
2. A **judgment** task — does a trivial artifact of the right kind read correctly.

Record separate approval for placement time, access and spend in `PLACEMENT-APPROVAL.md` before invoking the student. Output goes into `00-intake.md` as a coverage map: for each candidate unit, `already-passes / partial / absent`.

**Placement may conclude there is no course.** If the student already passes everything, say so and stop. That is a legitimate, money-saving result — report it, don't invent a course to justify the effort.

## Phase 1 — Intake

Do not start design until you can state all six in one line each:

1. **Student** — which profile. Confirm: `hermes profile list`.
2. **Subject** — the capability, phrased as something the student *does*, not knows.
3. **Competence** — what it can do after that it cannot do now, observable in an artifact.
4. **Coverage** — from placement: which units are actually needed.
5. **Sources** — what the course owner handed you, plus what you may go find.
6. **Budget** — attempt cap, spend ceiling and wall-clock scope. **Get an explicit dollar number from the course owner.** For a quick test, state a short elapsed-time checkpoint and what work is included before launching; a cheap model call can still take too long. Do not silently convert a quick comparison into a full production assessment.

Check the selected profile with `hermes -p STUDENT skills list` (replace STUDENT with the approved profile name). Select a private writable training root outside the profile and record both locations in `00-intake.md`.

## Phase 2 — Study

Ingest, then **derive**. Sources in priority order:

1. **Handed to you by the course owner** — authoritative. If an item is ambiguous, ask which one; never guess from nearby files.
2. **The tool's own truth** — `--help`, source, API reference, the student's existing skills.
3. **Existing skills in the ecosystem** — yours, the student's, `hermes skills search`, the catalog.
4. **Your own research** — web, docs, papers. Last, and cited.

Rules:

- **Context discipline.** Read through scripts and greps that pull out load-bearing parts; never paste whole manuals into context. Summarize each source to a few lines in `01-sources.md`, keep raw material on disk.
- **Separate fact from folklore.** Anything unverified against the tool or an authoritative source is marked `unverified` and never becomes a rubric criterion.
- **Find the failure modes.** The valuable part of a source is what goes wrong.
- **Name the gaps.** What you couldn't learn is part of the output.

## Phase 3 — Design

→ Load `course-design`. Produces the **15-section** packet: syllabus with per-unit objectives, lessons, **formative dry runs**, **a demonstration on a different subject**, exams with undisclosed traps, A/B/C/F rubrics, self-grade requirement, entrustment target. Nothing is taught yet.

## Phase 4 — Sign-off (HARD GATE)

Present the course owner with: the syllabus in one screen, per-unit objectives, the exam list, the grade bar, the attempt cap, the **formative/demonstration/critique plan**, the prior-artsy curriculum menu you chose from and what you rejected, the **entrustment target**, and the estimated cost of the whole course.

Then **stop and wait**. No teaching or graded run is authorized before approval. Any earlier placement/baseline needs its own explicit authorization.

On approval write `SIGNOFF.md` from `course-design/templates/SIGNOFF.md`: date, what the owner approved, amendments, and the **authorized spend ceiling**. That file is the authorization record — no file, no training.

If the course owner amends the packet, update the packet *and* the rubric before proceeding. Never carry an amendment only in your head.

## Phase 5 — Teach, drill, grade

→ Load `student-drills`. Per unit:

```
lesson → formative dry run (ungraded, mechanical) → coaching
      → exam attempt 1 → grade → coach
      → attempt 2 → attempt 3
```

Three attempts maximum per exam. Formative runs don't count against that.

## Phase 6 — Graduate or escalate

**Pass** (course C or better, no must-pass F): install the skill, verify it loads, record the letter **and the entrustment level**.

With approval, copy the complete course skill directory into the verified student profile’s skills directory. Check discovery in that exact profile with `hermes -p STUDENT skills list`, then load the installed skill in a fresh session.

Entrustment scale (ten Cate), recorded per graduated capability:

| Level | Meaning |
|---|---|
| 1 | observe only |
| 2 | execute under direct supervision — supervisor reviewing the work |
| 3 | execute with reactive supervision — available, key decisions checked |
| 4 | execute unsupervised (4a remote monitoring, 4b none) |
| 5 | supervise others |

Record the *earned* level, not the hoped-for one. "Level 2" means the course owner still reviews every artifact — say so plainly.

→ Load `gradebook` to record either way.

**Fail** (3 attempts, or an F on a must-pass criterion that won't clear): write `DIAGNOSIS.md` and bring it to the course owner. Attribute honestly:

- **student** — capability or tooling gap (missing tool, wrong model, no credentials).
- **lesson** — the skill taught the wrong thing or taught it unclearly.
- **rubric** — the bar was wrong, unmeasurable, or tested something the lesson never covered.
- **subject** — not teachable as scoped.

"The student failed" is not a diagnosis.

## Pitfalls

- **Teaching before sign-off.** The gate is the product.
- **Skipping placement.** Designing coverage before measuring it is guessing.
- **Skipping formative work to save money.** The dry run is the cheapest part of the course and the part that makes learning happen. Cutting it means paying more later for graded discovery.
- **Doing the work for the student.** You never produce the artifact under grade.
- **Writing the rubric after reading the answer.** Rubric first, always.
- **Announcing the trap and grading it as a trap.** Pick one.
- **Burning attempts on a broken harness.** A run that errors before the model works is `I`, not a failed attempt.
- **Passing on self-report.** No artifact, no evidence, no grade above F.
- **Grading an image by assertion.** Visual criteria get a real `vision_analyze` call and a verbatim quote.
- **Recording an entrustment level you haven't earned.** Level 4 means the course owner stops checking. Don't say it unless it's true.
- **Dumping whole manuals into context.** Phase 2 derives; it does not hoard.

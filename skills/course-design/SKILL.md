---
name: course-design
description: "Use when designing a course. Author syllabus and exams."
version: 0.3.0
author: V + Chiron
license: MIT
platforms: [linux, macos, windows]
metadata:
  published: true
  hermes:
    tags: [training, curriculum, syllabus, rubric, exam, assessment, formative, critique]
    related_skills: [train, student-drills, gradebook, prior-artsy, brainstorm]
---

# Course design

Phase 3 of `train`. Turns derived knowledge into a **packet** the course owner signs off: syllabus, lessons, formative dry runs, demonstrations, exams, rubrics. No student is touched here.

Course folder: `<training-root>/courses/<student>-<subject>/`

```
00-intake.md        who/what/why, budget, attempt cap
01-sources.md       every source, one summary each, cited, gaps named
02-curricula.md     the prior-artsy menu: how others teach this, cited
SYLLABUS.md         the course on one screen — 15 sections
lessons/01-*.md     the teaching material, one file per unit
formative/01-*.md   ungraded dry runs — mechanically checked, no letter
demo/               worked example on a DIFFERENT subject
exams/01-*.md       the prompt handed to the student, verbatim
rubrics/01-*.md     how each exam is graded — written BEFORE attempt 1
SIGNOFF.md          the course owner's authorization (does not exist = not authorized)
attempts/           raw student runs, graded transcripts
skill/<name>/       the SKILL.md that gets installed on a pass
DIAGNOSIS.md        only on escalation
```

Choose a private writable `<training-root>`; do not place completed packets, sign-offs, usage or attempts in the installed skill. `prior-artsy` and `brainstorm` are optional workflow aids: without them, collect primary syllabi, verify citations, and rank sequences against the constraints below.

Templates live in `templates/` next to this skill. Copy, don't improvise the shape.

## The 15-section syllabus template

Ground the sequence in institutional course specifications and record your sources in `02-curricula.md`.

| # | Section | Requirement |
|---|---|---|
| 1 | **Identity** | student profile, model, tools — each **verified by running something**, never assumed |
| 2 | **Description** | the capability, observable, one sentence |
| 3 | **Prerequisites** | every one checked, with the command used and its result |
| 4 | **Materials** | tools, versions, paths and required access (never credential values) |
| 5 | **Outcomes** | course goal **plus a per-unit objective**, verb-first and observable |
| 6 | **Units** | each = lesson + formative exercise + demonstration + summative exam |
| 7 | **Assessment** | criteria, A/B/C/F bands, weights, grade bar |
| 8 | **Formative work** | ungraded dry runs before each exam, mechanically checked |
| 9 | **Demonstration** | a worked example of a **different** subject |
| 10 | **Critique** | student self-grade before submitting → calibration gap |
| 11 | **Schedule** | token/time budget per unit, not just an attempt count |
| 12 | **Policies** | evidence contract, attempt cap, integrity, harness-error rule |
| 13 | **Feedback** | what coaching may/may not reveal — critique order: keep → fix → next |
| 14 | **Entrustment** | the supervision level this course targets |
| 15 | **Cost** | what passes, what it costs, what is unknown |

### Per-unit objectives (section 5) — the thing most packets skip

"The student can sculpt" is a course goal. A unit needs an objective a grader could disagree with:

> By the end of unit 2, given a creature head brief, the student produces a closed manifold head whose eye sockets, mouth line and neck junction are integrated into one continuous volume — verified by the mechanical checker and by vision on `detail.png`.

Verb-first, observable, testable against an artifact. Use Bloom-style verbs (*identify, construct, integrate, diagnose, justify*); never *understand* or *know* — those cannot be graded.

### Formative work (section 8) — non-negotiable

**Every unit gets a dry run before its exam.**

- **Ungraded.** No letter, not counted as an attempt, not in the attempt GPA.
- **Mechanically checked only.** No vision call — keep it near $0.05.
- **Cheap and narrow.** One sub-skill, not a miniature exam.
- **Feedback lands before the summative attempt**, so the student isn't paying to discover what it should have practised.

Rationale: mastery learning and deliberate-practice research both treat the feedback loop as the learning mechanism, not a nicety. First feedback arriving *after* a graded attempt is assessment, not teaching.

### Demonstration (section 9) — worked example, different subject

Give a worked example that **demonstrates the technique and gives away nothing**:

- **Never the exam subject.** Use unrelated material.
- **Same methods, different content** — the identical deformation pattern applied to a teapot or a boot.
- **Runnable, on disk**, so the student can read it end to end.
- **No target coordinates** from the exam anywhere in it.

Withholding every example starves the learner; change the subject rather than withholding the method.

### Critique (section 10) — and the calibration metric

Before submitting, the student **grades its own work** A/B/C/F, per criterion, with reasons. The professor then grades blind.

**Calibration gap = |self-grade − graded|**, per criterion. Reported, not itself graded.

| Self-grade vs graded | Reads as |
|---|---|
| Match, both high | has the judgment, not just the output |
| Self-grade too high | confidently wrong — the dangerous case |
| Self-grade too low | under-confident; over-cautious, not blind |
| No self-grade | F on that criterion (no evidence produced) |

The cleanest available signal separating *learned* from *lucky*, and it costs one extra file. 

## How to build a syllabus

A syllabus is a **sequence decision**: which capabilities, in what order, with what proof at each step. Don't invent the sequence from intuition — the order *is* the pedagogy, and for most subjects someone has already worked it out.

### Step 1 — Work backwards from the terminal artifact

Start at the end: the single artifact a competent student produces. Write it concretely ("a 2-manifold sculpted bust at ≤50k tris, exported .blend plus 3 turntable renders"), then ask repeatedly: *what must be true before this is possible?* Each answer is a candidate unit. Stop when you reach something the student already has — that's the floor, and unit 1 starts just above it.

### Step 2 — Scan how others teach it → **load `prior-artsy`**

Scope it to *the curriculum*, not the subject — and to **in-person classes**:

> "How do in-person college/art-school classes actually teach and sequence <subject>? Give me 3-6 distinct real courses with syllabi."

**Scan real classrooms, not marketing pages.** Online course outlines (CG Cookie, Schoolism,
CAVE) tell you a topic order; only a real course specification tells you contact hours, the
lab-to-lecture split, whether critique is a scheduled event, and whether the class demands work
outside class time. Those are the parts that transfer into a training design. If a source says
"taught online only", it is not an IRL class — say so and don't count it.

Prioritise: accredited art-school / university course specifications, community-college master
syllabi with assessment tables, atelier programmes, and course catalogs with weekly calendars.

Pull three things into `02-curricula.md`:

1. **The sequence most practitioners use**, and *why* that order — usually a dependency you'd have missed.
2. **The underrated sequence worth stealing** — often better for an *agent* student than the human-standard one, because an agent has no hands to build muscle memory and no patience cost for repetition.
3. **The failure modes teachers report** — those become your exam traps, pre-validated by other people's experience.

Respect prior-artsy's rules: don't pad to six, cite every exemplar, run its citation gate.

### Step 3 — Pick the sequence → **load `brainstorm`** (selection mode)

Score the top 2–3 against real constraints: what the student profile can do, the attempt cap, the cost ceiling, whether each unit yields a gradeable artifact. Record the loser and why. Nothing is lost.

### Step 4 — Write the 15 sections

If it doesn't fit one screen, the course is too big — split it.

### Step 5 — Sanity-check

- **Each unit's exam is gradeable alone.** If unit 2 needs unit 3, they're one unit.
- **Each unit adds a capability, not a topic.** "Brushes" is a topic. "Blocks out primary form at low resolution" is a capability.
- **No gap the student must guess across.**
- **Unit 1 is above the floor** — check `hermes -p <student> skills list` and the gradebook transcript.
- **Every unit has all four**: lesson, formative dry run, demonstration, exam.

## Lessons

Written for an agent, not a human:

- **Procedure in order**, with real commands/API calls, verified against the tool itself.
- **Failure modes first-class** — symptom, cause, fix. This separates a skill from a cheat sheet.
- **The judgment call** — when to choose A over B, and the tell that says which you're in.
- **No lore.** Anything marked `unverified` while studying does not become fact.

The lesson set becomes the installed skill, so write it in SKILL.md shape from the start.

## Exams

The **verbatim prompt** handed to the student. It must:

1. **Produce an artifact you can inspect** — file, diff, stdout, render, JSON. "The student says it did it" is not an artifact.
2. **Test judgment, not recall.**
3. **Contain at least one undisclosed trap** drawn from real failure modes. See below — an announced trap is a hint.
4. **State where to write the artifact**, at an absolute path.
5. **Be self-contained.** The student has no memory of your conversation with the course owner.
6. **Require a self-grade before submission** (section 10).

### Measured targets, not adjectives

A human studio student measures with calipers and steps back to compare. An agent has neither, so
"make it read as a pear" asks for an impression and gets one. Give **numbers where numbers exist**:

- ratio targets (widest point as a fraction of height, height/width, fill ratio)
- tolerance bands, not single values
- and a checker that measures them off the exported artifact

Keep the vision question for what genuinely resists measurement — does it read as the subject.
Report both, and **take the lower band when they disagree**.

### Propose before producing

Studio courses run *research → propose → produce → document*; the proposal exists so a bad plan is
caught before a week is spent building it. Require a short written plan (targets, order of
operations, intended masks/parameters, expected failure) and **grade it as its own criterion**.

This is the only clean way to separate judgment from execution: a correct plan executed badly and a
lucky build with no plan produce the same artifact and deserve different verdicts.

### Traps must be undisclosed

A warning in the exam turns a test of judgment into a hint. Pick one:

- **Keep it secret** → it can discriminate, and the A band may cite trap-handling as evidence of judgment.
- **Announce it** → it is teaching, not assessment; the A band must then rest on something else.

Default: **trap undisclosed**, and the lesson teaches the failure mode so a student that studied can legitimately avoid it.

## Rubrics — the load-bearing part

Written **before** attempt 1, never edited after reading an attempt. (If an attempt proves the rubric wrong that's a *rubric fault*: stop, tell the course owner, revise, restart from attempt 1 with the new rubric recorded.)

### Letter grades

| Grade | Means | Test |
|---|---|---|
| **A** | Exceeds | Correct, handles the unannounced trap, justifies the choice |
| **B** | Correct | Correct; thin justification or minor nuance missed |
| **C** | Minimally acceptable | Usable result reached sloppily, or by luck rather than method |
| **F** | Wrong, or not shown | Incorrect, skipped, or **no evidence produced** |

**No evidence = F.** A criterion you can't check because the student produced nothing is an F, exactly like an unsubmitted assignment. The sole exception is a **harness failure** (the run errored before the model did anything), marked `I`: not a grade, not an attempt, re-run after the harness is fixed.

Rolling up:

- Points **A=4, B=3, C=2, F=0**. Exam = mean of criteria, must-pass ×2; ≥3.5 A, ≥2.5 B, ≥1.5 C, else F.
- **Any F on a must-pass criterion caps the exam at F.**
- Course = mean of exam letters. Default bar: **C or better, no must-pass F.**
- No curve, never round up. A C passes *and* flags a weak lesson — that signal is the point.

### Every criterion needs four fields

| Field | Meaning |
|---|---|
| `id` | `R1`, `R2`, … |
| `criterion` | one observable thing, phrased so two graders agree |
| `evidence` | exactly where you look — path, command, image, grep |
| `grade bands` | what earns A, B, C, F for this criterion |

Rules:

- **Mechanical first.** If a script can decide it, script it. Judge by eye only what a script cannot.
- **Visual criteria are expected.** Use a configured vision evaluator (`vision_analyze` in Hermes). Name the exact image path; write bands as describable features, not taste; ask a question that maps onto the bands; quote the answer.
- **Split delivery from substance.** Missing a *graded artifact* is must-pass F. Missing an auxiliary file (`notes`, log, self-grade) costs that criterion only — clerical slips must not zero a good build.
- **Mark the must-passes.** Say which are fatal.
- **Grade the artifact, not the prose.**

## Cost estimate

Before sign-off, give the course owner a number and label it an estimate.

Estimate provider/model pricing, tokens per run, formative work, maximum graded attempts and any vision calls separately. Use current rates; reconcile with reported usage and distinguish estimated cost from billing.

## Verification

- All 15 sections present; every unit has lesson + formative + demonstration + exam.
- Per-unit objectives are verb-first and observable — no "understand".
- No trap is announced while still being scored as a trap.
- Delivery and substance graded separately (no clerical F).
- Every rubric criterion has an evidence locator and A/B/C/F bands.
- Self-grade + calibration gap specified.
- Entrustment target stated.
- `SIGNOFF.md` does not exist yet — you have not trained anyone.

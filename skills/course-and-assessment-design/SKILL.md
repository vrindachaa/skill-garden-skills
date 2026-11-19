---
name: course-and-assessment-design
description: "Use when designing or reviewing a course, rubric or eval."
version: 0.1.0
author: V + Hermes
license: MIT
platforms: [linux, macos, windows]
metadata:
  published: true
  hermes:
    tags: [assessment, curriculum, rubric, training, evals, grading, syllabus]
    related_skills: [prior-artsy, brainstorm, grounded-citations]
---

# Course and assessment design

Designing something that *teaches and then proves* a capability — a course packet, an exam, a rubric,
an eval set, or a training program for an agent or a person. Also used to review one.

## When to Use

- "Design a course / syllabus / curriculum to teach <capability>."
- "Write the rubric / exam / eval" for something that must be graded on evidence.
- "How do I know it actually learned?" — the evidence question, including placement and retention.
- Reviewing a packet someone else wrote ("what do you think of this syllabus?"): check it against the
  hard rules and pitfalls below, and name the missing sections rather than rewriting by taste.
- Setting up training for a subagent or a separate agent profile.

Not for: scoring a single prompt (use `prompt-optimizer`) or reviewing code (use
`requesting-code-review`).

Use A/B/C/F, not pass/fail. Missing evidence earns F on its criterion; a failure before learner work is `I` (incomplete).

For an executable Hermes workflow, pair this methodology with `train`, `course-design`, `student-drills` and `gradebook`. The methodology itself needs no CLI or account.

## Hard rules

1. **Rubric before the attempt, and never edited after seeing the work.** If an attempt proves the
   rubric wrong, that is a *rubric fault*: declare it, revise, and restart from attempt 1 with the
   new rubric recorded. Hash the rubric set at sign-off so drift is detectable.
2. **Core artifacts and auxiliary files are separate criteria.** A missing log, note or self-grade
   must cost that criterion only — never cap the whole assessment at F. Clerical slips must not zero
   good work.
3. **No evidence = F on that criterion.** You do not grade work that wasn't shown. The only
   exception is a **harness failure** (the run errored before the subject did anything): that is `I`,
   it does not count against the attempt budget, and you fix the harness and re-run.
4. **Mechanical checks first, judgment second.** Script everything a script can decide; only ask a
   vision model or a reader for what genuinely resists measurement.
5. **Never grade the prose.** A confident explanation of something absent from the artifact is an F
   on that criterion.
6. **Traps must be undisclosed to be scored as traps.** If the brief announces the failure mode, it
   is a hint — keep it, but then the top band cannot cite "handled the trap" as evidence of judgment.
7. **The assessor must not be the only examiner.** See the conflict-of-interest section.

## Procedure

### 1. Work backwards from the terminal artifact
Write the one artifact a competent subject produces, concretely. Then ask repeatedly: *what must be
true before this is possible?* Each answer is a candidate unit. Stop when you reach something the
subject already has — that is the floor, and unit 1 starts just above it. Name the assessment for
each unit as you go.

### 2. Source the sequence from real practice
Use `prior-artsy` if available, or collect primary course specifications directly. Scope the scan to *the curriculum* of **in-person classes**, not vendor course
pages — a real course specification carries contact hours, the lab/lecture split, assessment
weights, and whether critique is scheduled. Those are the parts that transfer. Record what you
rejected and why.

### 3. Write per-unit objectives, verb-first
"The subject can do X" is a course goal. A unit needs an objective a grader could disagree with:
*by the end of unit 2, given <brief>, the subject produces <artifact> in which <observable> — verified
by <check>*. Ban *understand* and *know*; they cannot be graded.

### 4. Put formative work before every summative attempt
An ungraded, cheap, mechanically-checked dry run before each graded attempt. Narrow (one sub-skill),
no judgment calls, no vision, roughly the cost of a trivial run. Rationale: mastery learning and
deliberate practice both treat the feedback loop as the learning mechanism — if the first feedback
arrives after a graded attempt, the subject pays to discover what it should have practised.

### 5. Supply a worked example — of a different subject
The most effective instructional device, and the easiest place to leak the answer. Give the same
method on unrelated content: identical technique, zero coordinates from the assessment. Withholding
all examples protects the exam and starves the learner.

### 6. Define measured targets wherever numbers exist
A subject with no instrument gets an impression and returns one. Replace adjectives with ratios and
tolerances (a dimension as a fraction of total, an aspect ratio, a fill ratio) and measure them off
the artifact. Keep judgment questions for *does it read as the intended thing*. **When the mechanical
check and the judgment disagree, take the lower band** and report both.

### 7. Require a proposal before the build, graded separately
*research → propose → produce → document* is how studio courses run, because a bad plan caught early
is cheaper than a bad build. A short written plan (targets, order of operations, parameters, expected
failure) is the only clean way to separate **judgment** from **execution**: a correct plan built
badly and a lucky build with no plan produce the same artifact and deserve different verdicts.

### 8. Require a self-grade, and report the calibration gap
Subject grades itself against the rubric before submitting; examiner grades blind; the difference is
**metacognitive accuracy** — reported, not separately scored (but no self-grade is an F on its own
criterion). A subject that self-grades A and earns C produced a result *without* the judgment. This
is the cleanest available signal separating *learned* from *lucky*, and it costs one file.

### 9. State how to know it generalised
A course cannot prove transfer using subjects it taught. Lock a **held-out eval set outside the
course**, before the course is designed, with parallel forms (A/B/C) so placement, post-test and a
delayed retention test don't share content. Placement is just the first administration of that
instrument — it decides *what coverage is needed* and may legitimately conclude **no course needed**.

### 10. Record an entrustment level, not only a grade
See `references/entrustment-and-competency.md`. A grade describes a past performance; an entrustment
level states what the supervisor stops checking. Name that explicitly, and refuse the level the
evidence doesn't support.

## Grading scheme

| Grade | Test |
|---|---|
| **A** | Correct, handles the undisclosed trap, and justifies the choice |
| **B** | Correct; thin justification or nuance missed |
| **C** | Usable result reached sloppily, or by luck rather than method |
| **F** | Wrong, skipped, or no evidence produced |

Roll up as points A=4 B=3 C=2 F=0; **weight must-pass criteria x2**; >=3.5 A, >=2.5 B, >=1.5 C, else F.
**Any F on a must-pass criterion caps the whole thing at F**, whatever the mean says. No curve, and
never round up — a C passing *and* flagging a weak lesson is the signal, not a problem.

Every criterion needs four fields: `id`, one observable `criterion` two graders would agree on, an
`evidence` locator (path / command / image / grep), and explicit **A/B/C/F bands** written for that
criterion.

## Coaching after a failure

Studio-critique order: **what to keep → what failed → what to do next.** Name failed criteria by id
and quote what was actually produced. Going straight to failures is how a subject fixes one criterion
and regresses another. Never supply the answer: no target coordinates, no completed artifact, no
procedure that removes the judgment.

## Conflict of interest

An assessor who writes the lessons, writes the rubrics, runs the subject and grades the result is
self-grading with no external examiner — the weakest link in the system, not the subject's ability.
Mitigate in this order: **hash-lock the rubric** at sign-off and verify at grade time; **external
examiner** on the graduation assessment only, blind to the lessons (disagreement rate becomes a metric
about the *trainer*); **owner spot-checks one grade**.

## Pitfalls

- **All-summative design.** Every assessment graded, nothing practised. That measures instruction-
  following, not learning, and it is the most common defect in a first draft.
- **Announced traps scored as traps.** Pick one: hidden (discriminating) or announced (teaching).
- **A must-pass criterion that covers every deliverable.** If paperwork is inside the must-pass set,
  one missing note fails excellent work; split core artifacts from auxiliary files.
- **Grading an artifact by looking at a thumbnail.** If a criterion is visual, call the vision tool,
  ask a question that maps onto the published bands, and quote the answer.
- **Trusting a mechanical pass as a quality pass.** Topology checks cannot see form: an artifact can
  be clean, valid, on-budget and still unrecognisable. The visual gate is separate and mandatory.
- **Adjectives as acceptance criteria.** "Looks right" is not a specification.
- **Rubric drift.** Editing bands after seeing an attempt, even to be fair.
- **Letting the course design its own eval.** A test written after the teaching is a test the teaching
  can be tuned to.

## References

- `references/entrustment-and-competency.md` — the five-level supervision scale, and the evidence base
  for formative-before-summative.

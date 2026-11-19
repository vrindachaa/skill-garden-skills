---
name: student-drills
description: "Use when drilling a student agent. Run and grade attempts."
version: 0.1.0
author: V + Chiron
license: MIT
platforms: [linux, macos, windows]
metadata:
  published: true
  hermes:
    tags: [training, grading, cli, attempts, evaluation, agents]
    related_skills: [train, course-design, gradebook]
---

# Student drills

Phase 5 of `train`. Teach the lesson, make the student attempt the exam in its own profile, grade against the rubric already written. Requires `SIGNOFF.md` to exist — check it first, by path, every time.

## The loop

```
for each exam in the syllabus:
    install/refresh the lesson skill in the student profile
    formative → mechanical check → coaching
    attempt 1 → grade → C or better? next exam
    coach (what failed, by rubric id — never the answer) → attempt 2 → grade
    coach → attempt 3 → grade
    still failing → STOP. DIAGNOSIS.md → the course owner.
```

Only a failure before the model worked is `I` and does not consume an attempt. Timeout, empty stdout or a lost terminal response alone does not establish that exemption. Inspect session messages, usage, artifacts and live processes before retrying: a model that already worked produced an attempt to grade, even if the wrapper lost its final response. Never launch a duplicate while the original may still run.

## Giving the student the lesson

The student is a separate profile with no memory of your work. It learns by receiving the skill:

Confirm the target profile and its skills directory. With sign-off, copy the complete lesson bundle there, including references and helpers; do not copy instructor notes, traps or solutions. Confirm discovery with `hermes -p STUDENT skills list` (replace STUDENT with the actual profile).

For an exam taken **without** the lesson, run before installing and label it `attempt-0-baseline`. Use it to measure the pre-instruction floor, not to claim causality: one repeated task before/after cannot separate teaching from practice or sampling. If the baseline already meets the bar, resolve any contradictory evidence and report that fact before spending on teaching; do not manufacture a deficit to justify the course.

## Running an attempt

Requirements: Python 3.10+, a configured student profile, a working Hermes CLI and a private course directory. One-shot mode bypasses interactive approvals: use an isolated workspace, least-privilege tools, approved access and a bounded budget. On Windows the wrapper needs a native `hermes.exe` on PATH, not a `.bat` launcher; use a POSIX installation otherwise. Use `--attempt formative-1` (or `formative-2` for the sanctioned retry) for ungraded practice. The wrapper checks for a sign-off file, not its authenticity, scope or remaining budget. For an explicitly authorized pre-instruction run, use `--attempt 0-baseline` with written authorization in `PLACEMENT-APPROVAL.md` first.

The prompt file is sent in full. Save only the student-facing exam text (without instructor headers, rubric paths or internal comments) as `prompts/01-validation.md` before using this example.

Use the script — it handles the quoting, the timeout, the usage file and the evidence layout:

```bash
python "<skill_dir>/scripts/run_student.py" \
  --student learner \
  --course "training/courses/learner-data-checks" \
  --exam 01-validation \
  --attempt 1 \
  --prompt-file prompts/01-validation.md \
  --timeout 900
```

It saves the prompt, stdout, stderr and metadata under `<course>/attempts/<exam>/attempt-<n>/`; `usage.json` is present when the CLI supplied it. Treat this evidence as private. Exit 4 means inspect the evidence before deciding whether a run counts. Never infer a free retry from a timeout.

The underlying call is `hermes -p <student> -z "<prompt>" --usage-file <path>` — one-shot, prints only the final response, approvals auto-bypassed. Notes that matter:

- **`-z` starts a fresh conversation, not a clean profile.** Make the prompt self-contained, but account for persistent skills, memory and project rules. Explicitly exclude baseline artifacts and prior solutions; do not call the run uncontaminated solely because it uses one-shot mode.
- **Run it from the student's working directory** if the exam writes relative paths — pass `--cwd`.
- **Long jobs:** give a generous `--timeout` and run the wrapper with `terminal(background=True, notify=True)` so a foreground transport timeout does not lose capture. A killed run is `I` only if it failed before model work; otherwise preserve and grade the evidence actually produced.
- **Never pass `--yolo`** unless the course owner authorized it for that course in writing.
- **Don't batch attempts.** One attempt, grade it, then decide. Parallel attempts burn money on a lesson you may be about to rewrite.

## Keep quick tests quick

Before launching, verify the actual model/provider and assess both elapsed-time and dollar limits. Preserve the baseline model for a fair comparison, but disclose a slow-model tradeoff instead of silently allowing a long run or switching models mid-comparison.

Use one approved student run at a time, background capture with completion notification, and a bounded verification stage. Give the course owner the agreed progress checkpoint even without completion: report elapsed time, the last evidenced stage, artifact availability and recorded spend. Distinguish model generation, local build/render and verification; do not describe all elapsed time as learning or claim a stall from quiet stdout alone. When a short task overruns, recommend stopping or explicitly extending it rather than letting a generous process timeout become the user-facing schedule.

Inspect completed core artifacts without waiting for a polished student write-up, but mark the result provisional. Save an in-progress snapshot under a distinct preview/checkpoint path; create the final attempt archive only after completion or confirmed termination. Otherwise late notes and self-grades can be omitted from the archive and falsely graded missing. Preserve core-artifact credit separately from unfinished auxiliary paperwork.

## Standalone baseline handoff

When the course owner asks for instructions to pass to the student, give a self-contained task brief, not an instruction to read the course exam. Strip unit numbers, training/baseline framing, lesson links and instructor rubric access; retain the subject, observable requirements, tool restrictions, absolute output directory and evidence contract. A fresh student must be able to execute it without knowing the curriculum. Keep grading criteria available to the professor before the handoff, but do not leak instructor-only traps through a referenced file. Do not invoke the student when the course owner asked only for copy-paste instructions.

## Showing before and after

When the course owner says “show me both,” lead with the actual before/after images under short labels, not another progress explanation or the student's summary. Use matching views and identify unfinished outputs as provisional. Provide timings, usage and grade qualifications separately when requested or when essential to prevent a false comparison.

Apply requested presentation-only changes, such as a different background color, to both images consistently. Keep original submissions and grading images unchanged; save derivatives under a separate comparison directory. Protect the object using a real silhouette/alpha mask, not gray-color similarity: shaded object pixels can match the background and a flood fill can cut holes through the surface. Verify both edited images before showing them. For the saved-mesh mask procedure, see `references/comparison-images.md`.

## Baseline comparability and recovery

- Recover the exact baseline session's model/provider and usage from its runtime usage file or read-only session database before choosing the trained model. Profile configuration may differ from the model that actually ran. Hold model/provider constant with per-run overrides, not persistent configuration edits; disclose mismatches rather than attribute them to teaching.
- Archive baseline artifacts and hashes before teaching. Exclude baseline code and instructor-only traps from the trained prompt; keep the artifact contract and prewritten bands constant. Report practice/repeated-subject confounds; passing after an already-passing baseline is not evidence of a training gain.
- If the wrapper capture is lost but the student completed, recover the exact session transcript and usage with provenance. Do not invent a process exit status or classify a completed student run as `I`.
- Validate measurement harnesses on artifact axis conventions. Blender OBJ import defaults need not match the export's Z-up/-Y-forward basis. Snapshot vertex coordinates before loading a checkpoint with factory reset, which invalidates earlier RNA objects. Preserve erroneous checker outputs; repair implementation bugs without changing grade bands.

## Grading

1. **Run the mechanical checks first.** Every rubric criterion whose `evidence` is a command — run it, capture real output. Never eyeball what a script can decide.
2. **Then inspect the artifact** for the judgment criteria — the artifact itself, not the student's summary of it.
   - **Visual criteria:** call `vision_analyze` on the exact required image path with the prewritten question and quote its answer. Check the whole response for contradictions before assigning a letter: a high panel count does not erase prose identifying the wrong object. Topology, smooth integration and target ratios do not establish semantic identity.
   - **Identity review:** have the evaluator identify the visible object from shape before comparing it with the target and plausible confusers. Use the same question, rubric and evidence views for baseline and trained artifacts. Do not replace a target-leading prompt with a confuser-leading prompt only for the result being challenged; a changed question is evaluator drift, not an automatic correction. Preserve both answers, label the grade disputed and use one consistent adjudication protocol on both artifacts. Do not keep rephrasing until a preferred verdict appears.
   - **Disagreement:** resolve contact/detail or cross-review contradictions before announcing a confirmed grade. Report the mechanical result and disputed visual criterion separately; withhold graduation when a must-pass judgment remains unresolved. A user challenge calls for checking evidence, not either defending or reversing a letter by reflex.
3. **Grade each criterion A / B / C / F** against its written bands. No evidence produced = **F** for that criterion — you don't grade work the student didn't show.
4. **Roll up as written:** A=4 B=3 C=2 F=0, must-pass weighted ×2, ≥3.5 A / ≥2.5 B / ≥1.5 C / else F — and **any F on a must-pass criterion caps the exam at F**. Don't negotiate with yourself and never round up to spare the student.
5. **Fill the grade report** (`attempts/<exam>/attempt-<n>/GRADE.md`) from the template: one row per rubric id with `grade`, `evidence observed`, `note`, then the exam letter.
6. **Quote the evidence.** Every grade below A cites the actual observed output or the vision tool's words. "Didn't follow the procedure" without a quote is not grading.

A run that errored before the model did anything is `I` (incomplete), not F — fix the harness and re-run; it doesn't consume an attempt.

Self-check before reporting: *would the course owner assign the same letters reading only my evidence column?* If not, you're asserting, not grading.

## Coaching between attempts

Feedback goes in the next attempt's prompt. It must:

- Name the criteria that scored below the bar **by rubric id**, with their letters, and quote what the student actually produced.
- Point at the part of the lesson that covers it.
- **Never contain the answer.** If you hand over the artifact or the exact commands, attempt 2 proves nothing and you have invalidated the course.
- Say what to keep — criteria already at B or A must not regress.

If two attempts score F on the *same* criterion for the *same* reason, stop early. More attempts won't help; the lesson or the rubric is the problem.

## Pitfalls

- **Training without `SIGNOFF.md`.** Hard stop. Check the file exists before the first run.
- **Inferring harness failure from exit status.** Empty stdout or nonzero exit does not prove the model never worked; inspect usage, transcript and artifacts before granting `I`.
- **Doing the exam yourself to "check it's possible."** If you must validate feasibility, do it mechanically or state the risk to the course owner — never produce the graded artifact.
- **Editing the rubric mid-exam.** That's a rubric fault: declare it, revise, restart from attempt 1.
- **Grading the explanation.** The artifact is the evidence.
- **Grading an image by assertion.** If a criterion is visual, actually call `vision_analyze` and quote it. "Looks right" is not a grade.
- **Inflating to a B.** C is a legitimate, useful grade: it passes and it tells the course owner the lesson is weak.
- **Inventing cost or calling estimates invoiced spend.** Report the runtime's recorded token counts and cost field with its exact status: `estimated_cost_usd` is an estimate produced by the runtime, not verified billing. Recover missing usage with provenance; keep unexposed auxiliary costs unknown rather than zero.

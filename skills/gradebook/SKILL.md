---
name: gradebook
description: "Use when recording training results. Keep the gradebook."
version: 0.1.0
author: V + Chiron
license: MIT
platforms: [linux, macos, windows]
metadata:
  published: true
  hermes:
    tags: [training, records, gradebook, provenance, agents]
    related_skills: [train, course-design, student-drills]
---

# Gradebook

The durable record of who was taught what, by whom, and whether it stuck. Lives in a private training workspace, outside any profile, so it survives profile deletion:

```
<training-root>/
  gradebook.json        machine-readable record of record
  GRADEBOOK.md          human view, regenerated from the JSON
  courses/<student>-<subject>/
```

Choose a private training root outside the installed skills. The helper needs Python 3.10+ (stdlib only), write access to that root, and no network or credentials. Its default is `training` under the current directory; use the same `--root` before each subcommand. Serialize writes: atomic replacement is not a multi-writer lock.

Example commands (illustrative records, not a transcript):

```bash
GB="<skill_dir>/scripts/gradebook.py"
python "$GB" --root training init
python "$GB" --root training record --student learner --course data-checks --event enrolled
python "$GB" --root training record --student learner --course data-checks --event signoff --notes "See signed packet"
python "$GB" --root training record --student learner --course data-checks --event attempt --exam 01-validation --attempt 1 --grade B --self-grade A --evidence attempts/01-validation/attempt-1
python "$GB" --root training record --student learner --course data-checks --event graduated --skill data-checks --grade B --entrustment 2
python "$GB" --root training show --student learner
python "$GB" --root training transcript --student learner
python "$GB" --root training render
```

Events: `placement`, `enrolled`, `signoff`, `baseline`, `formative`, `attempt`, `eval`, `retention`, `graduated`, `escalated`, `rubric-fault`, `withdrawn`. Record costs only when available, labelling estimates in notes. The helper records the signed self-minus-assessor gap; its absolute value is the size of the discrepancy.

## Rules

- **Record as it happens**, not at the end. A course abandoned mid-run must still show what was attempted.
- **One event per real thing.** Every attempt gets a row — C and F included — because the weak attempts are the interesting data.
- **Invalidate grades in summaries, not just prose.** Preserve a rejected grade and its evidence, but ensure active roll-ups and certification exclude it. An appended correction note does not necessarily remove the original letter from a script's GPA. If the gradebook lacks supported supersession/invalidation, label its aggregate stale and do not cite it as a valid grade; record the dispute without inventing a replacement letter.
- **Letters are A/B/C/F.** A harness-error run is `--grade I`: recorded, not counted as an attempt, never averaged in.
- **No graduating on an F.** `graduated` requires `--skill` and `--grade` (course letter A/B/C); an F or I is refused — record `escalated` instead.
- **Use recorded estimates.** `--cost` comes from the attempt's `usage.json`. Omit it rather than guess.
- **A skill is only "known" if it graduated.** `transcript` is the answer to "does learner know X?" — and it must never report a capability that didn't pass a signed-off rubric.
- **Escalations are recorded too.** `escalated` with the diagnosis attribution (student / lesson / rubric / subject) is how the trainer gets better at teaching.
- **Point at the evidence.** Notes reference the course folder path; the JSON holds the index, not the transcripts.

## Why this exists

Two reasons beyond bookkeeping. First, before enrolling a student you check the transcript so you don't re-teach what it has. Second, the accumulated `escalated` rows are the only honest signal about whether the *trainer* is any good — repeated `lesson` or `rubric` attributions mean the professor needs work, not the students.

# Formative dry run — Unit <n>: <name>

**Ungraded.** No letter, no attempt number, not in the attempt GPA. Money is the only cost.

- **Runs before:** `exams/0<n>-<name>.md`
- **Checked by:** `<mechanical command only — NO vision call>`
- **Cost target:** the approved per-run estimate (near the one-shot floor; keep it one run)
- **Student deliverable:** `<absolute path>` — one artifact, small

## Why this exists

Deliberate practice and mastery learning both put the feedback loop *before* high-stakes
assessment. Without a dry run the student pays for a graded attempt in order to discover what it
should have practised. This is the cheapest part of the course and the part that makes it teaching.

## The task (verbatim to the student)

```
<prompt>

Deliver to: <absolute path>
Success condition (mechanical, no judgement): <e.g. closed manifold, 2k-40k tris, correct
principal axis within X degrees, build.py exits 0 from factory startup>

If it fails, you will get the checker output and one coaching note. This run is not graded
and does not use an attempt.
```

## What coaching after it may say

- The checker's output, verbatim.
- Which part of the lesson covers the failure.
- **Not** the answer, and not the exam's subject or coordinates.

## Failure handling

- Dry run fails → coach → optionally allow **one** more dry run (still ungraded, still the approved per-run estimate).
- Two dry runs fail the same mechanical check → the lesson or the harness is broken, not the
  student. Stop and diagnose before spending on the exam.
- Dry run passes trivially on the first try → the difficulty is too low; say so in `DIAGNOSIS.md`
  rather than letting it inflate confidence.

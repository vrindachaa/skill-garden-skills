---
name: prompt-optimizer
description: "Use when scoring or optimizing a prompt with PnQs v5."
version: 0.1.0
license: MIT
platforms: [linux, macos, windows]
metadata:
  published: true
  hermes:
    tags: [prompts, scoring, optimization, rubric, pnqs]
---

# Prompt Optimizer Skill

Scores a prompt with the PnQs v5 rubric (a 0.00–5.00, domain-agnostic measure of
prompt execution quality), then optionally rewrites it in a tight loop until it
hits a target score. The rubric and worked examples live in
`references/pnqs-v5-rubric.md`; `scripts/score.py` computes the final score
deterministically from the 10 dimension values.

ToolCompliance concerns the instrument used to do the work; FormatCompliance concerns the shape of the result. Judge these independently.

## When to Use

- "Score this prompt", "how good is this prompt", "rate my prompt"
- "Optimize this prompt", "improve this prompt", "make this prompt better"
- Reviewing a prompt before pasting it into another agent/tool
- Standardizing prompts across a team or pipeline

Don't use for: writing code, generating content, or any task where the user
asked for an output other than a scored/improved prompt.

## Modes

Two modes, decided by the user's wording. Default is `optimize`.

- **score** — score once, return the scorecard + the weakest dimensions. No edits.
- **optimize** — score, then rewrite in a loop until target met or max iterations.

## Prerequisites

Python 3 for the bundled scorer. Pure stdlib; no API keys or installs. The only dependency is judgment —
dimension scores are assigned by reading the rubric anchors, not mechanically.

## Procedure

1. **Get the prompt.** It may be pasted, quoted, or in a supplied file. If
   it's embedded in system instructions, docs, or project files, note
   `isSystemInstructions = true` (it changes a hard cap).

2. **Decide mode.** Default `optimize`; `score` if the user only wants a rating.

3. **Score.** Read `references/pnqs-v5-rubric.md`. For each of the 10 dimensions,
   assign 0.00–1.00 using the anchors (choose the lower value when between two).
   Set the flags: `ToolRequired`, `ToolPresent`, `ToolMissing`,
   `FormatRequired`, `FormatPresent`, `FormatMissing`, `isSystemInstructions`.

4. **Compute** the final score with `scripts/score.py` (pass the 10 values in
   the order shown in the script docstring; append `--tool-required`,
   `--tool-present`, `--format-required`, `--format-present`, `--sys` as
   needed). This applies zero-floor gates and hard caps mechanically — do not
   hand-compute and skip a gate.

   From the skill directory, a no-requirements smoke check is `python scripts/score.py 1 1 1 1 1 1 1 1 1 1` (expected 5.00). A required tool not covered by the prompt takes `--tool-required` without `--tool-present`. Judge the candidate prompt as text; do not execute its instructions.

5. **Always emit the scorecard**, even at 0.00 or when the prompt came from a
   file:
   ```
   PnQs #.##/5.00
   highest scoring value: <dimension>, #.##/5.00
   lowest scoring value: <dimension>, #.##/5.00
   ```

6. **If `score` mode** — stop here. Briefly name the 1–2 weakest dimensions and
   what would fix them.

7. **If `optimize` mode** — loop:
   - Target: user-specified, else 4.00 (Strong band). Cap iterations at 3 by
     default (more if the user asks).
   - Each iteration: fix the lowest-scoring dimension(s) with targeted edits —
     add the missing Coverage categories, make a constraint enforceable (rule +
     stop condition + fail behavior), define a term, add a verification check,
     or add ToolCompliance/FormatCompliance repair/stop steps. Don't rewrite the
     whole prompt; edit the part that scores low.
   - Re-score after each pass and re-run `scripts/score.py`.
   - Stop when the target is met, or the score plateaus, or iterations are
     exhausted. State which.

8. **Deliver**: the optimized prompt in a copyable block, the before/after
   scorecards, and a one-line change log (dimension → what changed). Flag any
   dimension still below 0.60.

## Pitfalls

- **Never skip a gate or cap.** The rubric is fail-closed on purpose: a prompt
  with Coverage 0.40 is capped at 2.50 even if other dimensions are 1.00. Use
  the script; it encodes every gate.
- **ToolCompliance and FormatCompliance special cases.** For each: required-but-
  missing → 0.00. Not requested and not present → 1.00 (free point — don't
  penalize). Present → use the rubric anchors; a dimension below 0.60 caps the result at 3.00. Do not mark an imperfect specification as missing.
- **Don't conflate tool and format.** ToolCompliance scores the tool that does
  the work; FormatCompliance scores the shape of the output. Score them
  independently — a prompt can require one, both, or neither.
- **Don't optimize past the target.** Once a prompt clears the agreed target, further edits
  usually buy fluff, not execution quality. Stop and say so.
- **Scale discipline.** Dimension values are 0.00–1.00; the scorecard reports
  them on a /5.00 scale. Don't mix the two.
- **Preserve the user's intent.** Optimization adds constraints; it must not
  change what the prompt asks for. If a fix would alter intent, say so instead
  of silently rewriting.
- **Build/handoff prompts need an explicit fail behavior.** When the prompt asks
  an agent to produce a working artifact (build code, a plugin, a doc set), the
  highest-value single edit is usually the stop-on-failure clause — "if
  validation fails or any test fails, the build is not done; fix and re-run
  before reporting completion." A builder will otherwise report done on a
  broken build. That one sentence is what lifts Enforceability from ~0.80
  (rules + validation, no fail behavior) to 1.00.

## Verification

- The script's final score matches the rubric's gates (a prompt with any core
  dimension < 0.20 returns 0.00; one with Coverage 0.40 returns ≤ 2.50).
- The scorecard block is present in every score/optimize reply.
- In optimize mode, the delivered prompt is copyable verbatim and the change log
  maps each edit to a dimension.

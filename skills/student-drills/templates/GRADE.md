# Grade — <student> / Unit <n>: <name> / attempt <k>

- **Evidence folder:** `attempts/<exam>/attempt-<k>/`
- **Rubric:** `rubrics/<n>-<name>.md` (unchanged since before attempt 1)
- **Run:** exit <rc>, <duration>s, estimated cost $<from usage.json `estimated_cost_usd`>

## Scorecard

| id | must-pass | grade | evidence observed | note |
|---|---|---|---|---|
| R1 | yes | B | `<quoted output / file fact>` | correct, justification thin |
| R2 | yes | F | `<quoted output>` | expected <x>, got <y> |
| R3 | no | C | vision_analyze: "<verbatim quote>" | reads from the front only |

**Weighted mean:** <x.xx>  (A=4 B=3 C=2 F=0, must-pass x2)
**Exam grade: <LETTER>** — <"capped at F by must-pass R2" / "mean maps to B"> · bar was <C or better>
**Result: PASS / FAIL**

## Calibration (reported, not scored)

After grading blind, record self-grade, assessor grade and gap per criterion.

## Coaching for the next attempt (no answers)

- **R2 (F)** — you produced `<quote>`. The lesson covers this in <section>; re-read it and say what
  you changed and why. Keep R1 and R3 as they are — don't let them regress.

## For the course owner

- <only if something needs the owner: a capped exam, a suspected rubric fault, a cost overrun, or a
  visual call you think is genuinely arguable>

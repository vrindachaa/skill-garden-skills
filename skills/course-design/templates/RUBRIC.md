# Rubric — Unit <n>: <name>

Written **before** attempt 1. Not editable after reading an attempt; if it turns out to be wrong,
that is a **rubric fault** — declare it to the course owner, revise, and restart this exam from attempt 1.

**Grade bar:** <C or better> · must-pass: <R1, R2>

Scale: **A** exceeds (correct + handles the undisclosed trap + justifies) · **B** correct ·
**C** minimally acceptable · **F** wrong, skipped, or no evidence produced.
Roll-up: A=4 B=3 C=2 F=0, must-pass x2, >=3.5 A / >=2.5 B / >=1.5 C / else F.
**Any F on a must-pass criterion caps the exam at F.**
A run that errored before the model worked is `I` (incomplete) — not a grade, not an attempt.

## Criteria

### R1 — Core graded artifacts delivered and inspectable · **must-pass**
- **Evidence:** `<absolute paths of the shared artifacts only — e.g. sculpt.blend, sculpt.obj, contact.png>`
- **A:** all present, parse, and are internally consistent
- **B:** all present and parse; one minor inconsistency in supporting output
- **C:** all present and usable, but with a caveat the grader had to work around
- **F:** any **core** artifact absent, empty, corrupt, or unparseable

*Core = the artifacts the grade actually rests on. Auxiliary files (`notes.md`, build log,
self-grade) are graded at R<n>, never here — a clerical slip must not zero a good build.*

### R2 — <mechanical criterion> · must-pass
- **Evidence:** run `<command>`; expect exit 0 and `<value>` within <tolerance>
- **A:** exit 0, value within <tight tolerance>
- **B:** exit 0, value within <loose tolerance>
- **C:** exit 0 but <marginal>
- **F:** non-zero exit, outside tolerance, or nothing to run against

### R3 — <visual criterion> · quality
- **Evidence:** `vision_analyze` on `<exact image path>`, asked:
  "<question whose answer maps onto the bands below>"
- **A:** <describable feature set — e.g. silhouette reads as the subject from all 3 angles,
  limb proportion within a head-length, no visible pinching at the joints>
- **B:** <reads correctly from 2 of 3 angles; minor proportion drift>
- **C:** <reads from the front only>
- **F:** <unrecognizable, or no render at the required path>
- Quote the vision answer verbatim in the grade report. Never grade an image by assertion.

### R4 — Decision log and self-grade · quality
- **Evidence:** `<submission>/notes.md` and `<submission>/self-grade.md`
- **A:** explains key choices and tradeoffs using artifact evidence; self-grades every criterion with reasons
- **B:** documents the decisions and self-grades each criterion; one reason is thin
- **C:** supplies both files but several reasons are generic or incomplete
- **F:** required self-grade absent, or log claims actions not evident in the artifact

After the independent grade, report the calibration gap separately. Do not penalize disagreement itself.

## Mechanical check script (run first, even on visual units)

```bash
# every criterion a script can decide, decided by the script
```

## Grader's self-check

- [ ] Every criterion has an evidence locator, not a vibe.
- [ ] Every criterion has all four bands, A through F.
- [ ] Core artifacts and auxiliary files are on separate criteria.
- [ ] Visual criteria name an exact image path and a vision question.
- [ ] Self-grade + calibration gap recorded.
- [ ] Must-pass set marked; exam grade bar stated.
- [ ] Would the course owner assign the same letters from my evidence column alone?

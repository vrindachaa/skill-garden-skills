# PnQs v5 — Prompt Net Quality Score (agnostic)

A 0.00–5.00 rubric for judging whether a prompt makes successful execution likely. This is a structured review, not an empirical performance measurement.

**Tool vs format.** ToolCompliance scores how the prompt specifies the *tool
that does the work* (CLI, API, DSL, code interpreter, MCP server).
FormatCompliance scores how the prompt specifies the *shape of the output*
(JSON schema, CSV columns, field types, markdown structure). A prompt can
require a tool, a format, both, or neither.

## The 10 dimensions

Assign each input 0.00–1.00 using the anchors. If uncertain between two
levels, choose the lower.

| Dimension | Wt | 1.00 | 0.80 | 0.60 | 0.00–0.20 |
|---|---|---|---|---|---|
| TokenEfficiency | 0.18 | Minimal fluff. No repeated sections. Constraints concise. | Mostly dense. Some repetition but instruction-forward. | Noticeable filler or restating. | Mostly fluff. Instructions hard to locate. |
| Coverage | 0.14 | All 5 categories explicit: inputs, outputs, constraints, edge cases, success criteria. | 4 categories clear. | 2–3 categories, or implied. | 0–1 category. |
| Enforceability | 0.14 | Clear rules + stop condition + fail behavior + validation. | Rules + either stop or fail, not both. | Some rules, weak gating. | Mostly suggestions. |
| MisinterpretationSafety | 0.14 | Defines terms, restricts degrees of freedom, has fallback logic. | Mostly constrained, few open terms. | Multiple ambiguous terms. | Highly ambiguous. |
| Modularity | 0.12 | Sections editable independently. | Mostly separable, few cross-deps. | Interwoven; changes cascade. | Monolithic. |
| Clarity | 0.10 | Clean hierarchy. No backtracking. | Clear overall, minor jumps. | Requires re-reading. | Hard to follow. |
| NoContradictions | 0.06 | None. | Minor tension, resolvable. | One clear contradiction. | Multiple contradictions. |
| VerificationRigor | 0.04 | Explicit checks + structured output format. | Verification but loose format. | Mentions verification, not actionable. | No verification. |
| ToolCompliance | 0.04 | Required tool/API/DSL usage constrained + validated + repair/stop behavior. | Present + constrained, incomplete validation. | Loosely handled, missing repair. | Required but missing, or unusable. |
| FormatCompliance | 0.04 | Required output format/schema constrained + validated + repair/stop behavior. | Present + constrained, incomplete validation. | Loosely handled, missing repair. | Required but missing, or unusable. |

## Base equation

```
PnQs_v5 = 5.00 × (
    TokenEfficiency         × 0.18
  + Coverage                × 0.14
  + Enforceability          × 0.14
  + MisinterpretationSafety × 0.14
  + Modularity              × 0.12
  + Clarity                 × 0.10
  + NoContradictions        × 0.06
  + VerificationRigor       × 0.04
  + ToolCompliance          × 0.04
  + FormatCompliance        × 0.04
)
```

## Hard caps (fail-closed)

Start `cap = 5.00`. Apply each; `cap = min(cap, value)`.

| Condition | cap |
|---|---|
| NoContradictions < 0.70 | 2.00 |
| Coverage < 0.60 | 2.50 |
| Enforceability < 0.60 | 3.00 |
| MisinterpretationSafety < 0.60 | 2.50 |
| ToolCompliance < 0.60 | min(cap, 3.00) |
| FormatCompliance < 0.60 | min(cap, 3.00) |
| isSystemInstructions && VerificationRigor < 0.40 | min(cap, 3.00) |

`PnQs_v5_final = min(PnQs_v5, cap)`

## Zero-floor gates (score forced to 0.00)

Any of these → final = 0.00:

- TokenEfficiency < 0.20
- Coverage < 0.20
- Enforceability < 0.20
- MisinterpretationSafety < 0.20
- NoContradictions < 0.20
- ToolRequired && ToolMissing
- FormatRequired && FormatMissing

ToolCompliance and FormatCompliance special cases (each applies independently):

- Required but missing → 0.00.
- Not requested and not present → 1.00 (free point).
- Present but imperfect → score against the anchors; the hard cap of 3.00 applies when that dimension is below 0.60. Reserve full credit for validation and repair/stop behavior.

## Execution protocol (in order)

1. Set booleans: `isSystemInstructions`, `ToolRequired`, `ToolPresent`,
   `ToolMissing`, `FormatRequired`, `FormatPresent`, `FormatMissing`.
2. Assign the 10 dimension scores (0.00–1.00).
3. Apply zero-floor gates.
4. Compute the base equation.
5. Apply hard caps → `PnQs_v5_final`.
6. Always output the scorecard.

## Scorecard (required output)

```
PnQs #.##/5.00
highest scoring value: <dimension>, #.##/5.00
lowest scoring value: <dimension>, #.##/5.00
```

## Interpretation bands

- 4.70–5.00 — Elite
- 4.00–4.69 — Strong
- 3.00–3.99 — Adequate
- 1.50–2.99 — Weak
- 0.01–1.49 — Near-fail (barely meets minimum gates)
- 0.00 — Failing (hit a zero-floor gate or hard-cap collapse)

## Worked examples (agnostic)

### Example 1 — Failing (0.00)

> "Write me a report on our data. Make it look good."

**PnQs v5: 0.00.** No inputs named, no outputs specified, no constraints, no
verification, no success criteria — Coverage and Enforceability are ~0.0,
tripping zero-floor gates.

### Example 2 — Score a cap, not just the average

> Summarize the attached event list for the coordinator. Include decisions and risks.

Suppose the evaluator assigns Coverage 0.40 (inputs and output are named, but no success test or failure behavior). Even with all other dimensions at 1.00 for illustration, the score cannot exceed 2.50. A useful edit specifies how to handle an undated event and how to check completeness.

### Example 3 — Separate tool from format

> Read the supplied event list. Return a JSON array with event ID and date; validate both keys per row. If a date is unknown, use null. Check that every source ID appears exactly once; repair mismatches before returning the array.

The output format is present. If the surrounding task also requires a specific transformation tool and the candidate never specifies it, the tool-missing gate still forces 0.00. Without such a requirement, do not invent one. Reassess all ten dimensions rather than assuming the edit earns a perfect score.

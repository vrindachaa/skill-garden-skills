---
name: cost-gated-fanout
description: "Design multi-agent fan-outs: cost table, caps, models."
version: 0.1.0
license: MIT
metadata:
  published: true
  hermes:
    tags: [fan-out, cost, multi-agent, budget, orchestration]
    related_skills: [batch-harness-design]
---

# Cost-Gated Fan-out

Use before launching multiple paid workers or reviewing a plan that delegates work. The output is a priced, bounded plan and a launch decision, not permission to spend. Use a frozen manifest and independent acceptance checks (see `batch-harness-design`). For mechanical work, use a deterministic script instead of an agent.

## Price the real route

1. Separate extraction and mechanical validation from drafting and judgment. Assign an explicit provider, model and effort to each paid stage. Verify IDs and prices against the selected route's current catalog; record currency, pricing unit and retrieval date. Do not silently substitute another model. If workers inherit the parent route, pin it per worker or reprice at the inherited rate. Do not change shared settings for a single job.
2. Sample real input sizes in bytes or tokens, not file counts. Include instructions, tool output and resent context over **all turns**. Separate input and output rates; include other billable components if relevant. Derive an output length limit from an accepted exemplar. Treat caching discounts as conditional.
3. Price retries and likely escalation as rows, not free exceptions. For rates per million tokens, row cost is `max_runs × (cumulative_input_per_run × input_rate + output_per_run × output_rate) / 1_000_000`, plus non-token charges. Do not double count retry rows inside base rows.

| Stage | Provider / resolved model | Effort | Max runs incl. retries or escalation | Input / run | Output / run | Rates and units | Est. cost |
|---|---|---|---:|---:|---:|---|---:|

Show total estimated cost, what is actually enforceable, approval state and ship-partial deadline. If no budget was supplied, propose a numeric pilot ceiling and a conditional scale-up bound; ask for confirmation without starting. Cost estimates are not cash kill-switches. If a hard money limit is required but cannot be guaranteed by enforceable quotas or a conservative upper bound including in-flight work, decline launch under that constraint.

## Admission gate

- Require approved manifest and budget, resolved route, retry-inclusive launch count, turn and token allowances, per-unit timeout and overall deadline. Enforce per-run output limits in the request; enforce input size and cumulative usage in the launcher. If metering lags, reserve worst-case allowances before dispatch and reconcile actual use afterwards. Reject configurations whose required limits the runtime cannot enforce.
- Dry-run the exact launcher first: log units, model, token allowance, concurrency, max starts and deadline **without spawning**. Test rejection of an extra unit, unknown route and exhausted allowance. Cap concurrency locally; reserve a slot and budget atomically so two workers cannot claim the last allowance.
- After approval, pilot one cheap, representative unit on the pinned route; record resolved model, actual usage, elapsed time, tool calls and accepted output. A catalog listing does not prove routing or credential access. If the unit fails, park it or use a pre-priced retry; do not fan out on the strength of an unreviewed pilot.
- Compare measured cumulative usage with the table. Reprice before scaling; seek fresh approval for an increased ceiling, changed scope or unplanned escalation. Cancel outstanding work when required and report partial completion rather than extending the deadline silently.

## Accept outputs independently

Close each brief over a named manifest key, allowed inputs and writes, numeric output bounds and acceptance checks. Reject out-of-scope output in code. Verify changes against a baseline including untracked files. Check schema, counts and cited locations mechanically; spot-check that cited values belong to the right entities. Run each checker on both a known-good and known-bad artifact, then rerun it independently on worker output. A worker's “done” is not an acceptance record.

**Release check:** The estimate covers the route that actually ran, remaining count and token reservations cannot go negative, and every charged attempt maps to an accepted, failed or cancelled unit. Report estimated versus observed usage and any billing uncertainty.

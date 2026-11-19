---
name: batch-harness-design
description: "Build long-running batch and fan-out jobs with checkpoints."
version: 0.1.0
license: MIT
metadata:
  published: true
  hermes:
    tags: [batch, fan-out, orchestration, reliability, checkpoints]
    related_skills: [cost-gated-fanout]
---

# Batch Harness Design

Use when partial failure is normal and completed work must survive a restart. Before launch, design four pieces: a frozen manifest, a one-unit producer, an outer supervisor, and a reconciler. These can be files and processes, queue workers and a database, or local functions. No particular scheduler is required.

## Define the unit and evidence

- Choose the smallest output worth delivering independently. Freeze one manifest row per unit: `key, input_revision, parameters, acceptance_check`. Reject duplicate keys after normalization. Use the same key and revision rules on write, read and resume. For shared interfaces, record the signature, lifecycle and teardown before dividing implementation work.
- Make acceptance decidable: “all required columns present and row count matches the source” is a check; “finished export” is a label. If a human must inspect the result, name the observation and distinguish awaiting review from accepted.
- A producer takes exactly one manifest row, emits a heartbeat, and returns an artifact or a typed error. No internal retries or invented substitute output. Capture stdout and stderr separately; keep per-attempt diagnostics in access-controlled storage and remove secrets from distributed reports.
- Validate the artifact before marking it accepted. Commit artifact and checkpoint together where possible; otherwise publish the durable artifact first, then its checkpoint, and verify the pair on restart. Use an atomic rename or transaction and an idempotent output key. Avoid concurrent appends to an unprotected shared file.

## Supervise recovery

| Failure or limit | Supervisor action |
|---|---|
| Invalid input, no eligible data, explicit refusal | Record reason and revision; do not retry unchanged. |
| Timeout, temporary service or quota failure | Bounded retries with backoff and jitter; honor retry-after. |
| Unknown error | Retain diagnostics; at most one exploratory retry, then park for inspection. |
| Stale heartbeat | Check worker or lease before replacement; prevent two active writers accepting the same key. |
| Same residue on consecutive passes | Pause automatic relaunch; investigate a common cause. Repetition alone does not prove permanence. |
| Deadline or retry budget reached | Stop admitting units, settle or cancel in-flight attempts, ship a reconciled partial report. |

Set count, per-attempt timeout, retry limit, polling cadence and overall deadline before launch. Use a small pilot to estimate duration; when enough samples exist, a multiple of observed p95 is a starting timeout, not a guarantee. Put limits in the supervisor, not in worker instructions.

## Reconcile from delivered outputs

```text
expected = keys(frozen_manifest)
accepted = keys(durable_outputs passing revision and acceptance checks)
unexpected = accepted - expected
missing = expected - accepted
pending = missing - permanently_skipped_at_this_revision
```

Reject unexpected, duplicate, stale and corrupt results rather than counting them. Resume only eligible pending keys. Report every missing key in exactly one category with a reason, evidence and an owner action; distinguish retry exhaustion from invalid input. Never call an exit code or heartbeat proof of coverage.

**Offline rehearsal:** For manifest `A,B,C`, accept `A`, fail `B` transiently and permanently skip `C`. Restart: only `B` should run. After `B` succeeds, report `A,B` accepted and `C` missing with its skip reason. Inject a duplicate `A` and a partial `B` write separately; neither should inflate the accepted count. For paid workers, pair this design with a preflight budget and admission gate (see `cost-gated-fanout`).

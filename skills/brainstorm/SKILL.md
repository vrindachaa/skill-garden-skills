---
name: brainstorm
description: "Question the framing and premise to find the real problem."
version: 0.1.0
license: MIT
metadata:
  published: true
  hermes:
    tags: [brainstorm, ideas, framing, premise, problem-solving, planning]
    related_skills: [prior-artsy]
---

# Brainstorm

Use before committing effort to an idea, or when choosing among competing approaches. The output is a decision about a problem, not a long list of features. No tools are required. If the problem and approach are already settled and the user wants execution, skip this procedure.

1. **Capture the seed.** Quote the idea in one line. Separately state who has the problem, what they do today, what goes wrong and what observable change would count as solved. Distinguish the triggering example from the class of problems it represents.
2. **Check the frame.** State the premise that must be true for this idea to help. Offer a materially different diagnosis. What evidence would distinguish them? If a missing fact would reverse the recommendation, ask for it; label assumptions rather than attributing them to the user.
3. **Compare approaches.** Include the current practice, a smaller intervention and the proposed change. For each, walk through one real use: who initiates it, what happens, and what changes for that person. A new interface and a new capability are not necessarily the same thing.
4. **Stress-test each serious contender.** Cover both success and a plausible failure: no adoption, missing input, a wrong assumption, excess maintenance or a slow path. Say whether the failure is tolerable, reversible, testable or disqualifying. Separate a fixable defect from a failure of the premise.
5. **Rank against the decision maker's criteria.** Name must-haves before trade-offs. Eliminate options that miss a must-have; compare survivors by benefit, effort and downside. State why the runner-up lost and what would change the ordering. If novelty matters, distinguish new to the field from new to the host; verify against exemplars and the existing implementation, or mark it unknown. Use `prior-artsy` if available for a cited comparison.
6. **Converge.** Recommend one next action that tests the most consequential uncertainty. Give an observable pass/fail signal. Recommend, but do not treat a recommendation as approval to build or spend. Reopen the decision if new evidence invalidates the winning premise.

## Example

Seed: “Let's add reminders for unreviewed drafts.” If reviewers already know a draft exists but cannot tell who owns it, more reminders add noise. Try assigning a named reviewer to the next small set of drafts instead. Compare time to first review with the previous comparable set; if ownership was already clear and timing does not improve, revisit the diagnosis.

## Deliverable and check

Return **seed → real problem → alternative frame → options and failure modes → decision → next test**. Keep rejected options with a short reason so they can be revisited. Save only to an agreed destination; otherwise return the decision in the conversation. Check that the problem statement still makes sense without naming the proposed solution and that the next test could actually change the decision.

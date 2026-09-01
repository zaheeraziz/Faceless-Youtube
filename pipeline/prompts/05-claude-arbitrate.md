# Step 5 — Claude arbitrates disagreements

- **Role:** Claude Code (`claude -p --allowedTools "Bash,Read,Edit"`)
- **Input:** `Projects/<slug>/Claude/decision.json` entries where `codex_response: disagree`
- **Output:** `claude_arbitration` filled in per entry in `Projects/<slug>/Claude/decision.json`, plus a human notification if flagged

## Instructions

Read `Projects/<slug>/Claude/decision.json`, `Projects/<slug>/Claude/feedback.json` (for each contested point's original issue/suggested_fix), and `Projects/<slug>/Codex/draft-v02.md` (to see how Codex actually left the line).

For each disagreement, weigh Codex's stated reason against the original feedback point.

- **Concur (5a):** if Codex's reason is sound, the line stands as Codex wrote it. Record `claude_arbitration.verdict: concur`, `status: resolved_concur`. The episode finalizes.
- **Still disagree (5b):** if Codex's reason doesn't hold up, record `claude_arbitration.verdict: still_disagree`, `status: flagged`. Only this one point is flagged — not the whole script. Write the contested line and both sides' reasoning clearly into `decision.json` so whatever's driving this run (a live Claude session, or `run-pipeline.sh`'s own notification step afterward) can surface it to the owner — don't attempt to send a push notification yourself here. If you're running inside a live, supervised Claude Code session (not headless), you may additionally use the `PushNotification` tool directly; a headless `claude -p` call can't reliably do this, so don't claim to have notified anyone unless you actually have that tool available and used it.

You are not splitting a tie between two equally-weighted opinions. You are checking whether Codex gave a real reason. A weak reason loses; a real one wins, even if you'd have written the line differently yourself.

This is also the step that runs the GitHub checkpoint for the episode (commit + push) and, on a flag, opens the PR-as-flag pull request — see `COVERAGE-DESK-SPEC.md` section 5.

## Task

Episode slug: `<slug>`

Arbitrate every `disagree` entry in `Projects/<slug>/Claude/decision.json` now, write the results back into that file, then do the checkpoint (commit, push to `origin {{push_branch}}`, PR-as-flag on any 5b).

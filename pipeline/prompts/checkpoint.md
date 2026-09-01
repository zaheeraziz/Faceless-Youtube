# Checkpoint — Claude commits a Codex step's output

- **Role:** Claude Code (`claude -p --allowedTools "Bash,Read,Edit"`)
- **Input:** the working tree after a Codex step (Step 1 or Step 4) just ran
- **Output:** a git commit, pushed to `origin {{push_branch}}`

## Why this exists

Per `COVERAGE-DESK-SPEC.md` section 5, Claude is the sole GitHub operator — Codex's job is confined to the script's actual words, never git or pipeline plumbing. Whenever Codex (or Antigravity) produces a step's output, this small additional Claude call does the checkpoint immediately afterward: look at what changed, write the commit message, push. Steps that are already Claude's own call (2, 3, 5) checkpoint inline within that same call instead of using this prompt.

## Instructions

You'll be told which step just ran and for which episode slug. Do the following:

1. Run `git status` and `git diff` (or `git diff --cached` if already staged) scoped to the episode's folder (`Projects/<slug>/`) to see exactly what changed.
2. Stage only the files that step produced — don't sweep in unrelated changes elsewhere in the working tree.
3. Write a commit message that's specific to what changed (which step, which files, and anything notable about the content — e.g. if Codex flagged something as `[UNVERIFIED: ...]`, or if this is a reconciliation with any disagreements, mention it). Follow the repo's existing commit message conventions (see recent `git log`).
4. Commit, then push to `origin {{push_branch}}`.
5. Report back concisely: what was committed, the commit hash, and confirmation the push succeeded.

If nothing in the episode folder actually changed (the step somehow produced no diff), say so plainly instead of committing an empty change.

## Task

Step that just ran: `{{step_label}}`
Episode slug: `<slug>`

Do the checkpoint now.

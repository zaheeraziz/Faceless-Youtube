# Coverage Desk — Script-Stage Pipeline Spec

Design spec for the first automated stage of video production: script writing. Draft → review → ground → feedback → reconcile → arbitrate → finalize or flag. Git-backed twin of the working Artifact; update both together.

Status: **Phase 0 scaffolding committed. Phase 1 hand-run in progress, blocked on `claude -p` auth.** See "Owner decision" below for why this exists despite the business-before-tools gate in `PROJECT-CONTEXT.md` still being open. See section 9 for the Phase 1 findings log.

## 1. Owner decision — proceeding ahead of the business gate

`PROJECT-CONTEXT.md`'s business-before-tools gate blocks automation until niche validation, competitor analysis, packaging demand, and revenue economics are done — and as of 2026-08-29 the niche is still undecided. Logged here rather than edited into that document: the owner decided to proceed with Coverage Desk scaffolding anyway, treating this as pipeline tooling prep rather than full production automation. The gate itself is unchanged and still governs channel launch, subscriptions, and full video production.

## 2. The steps

| Step | Role | What happens | In → out |
|---|---|---|---|
| 1 | Codex | Drafts the script from topic + notes | topic, notes → draft v1 |
| 2 | Claude | Reviews for accuracy + language | draft v1 → review notes |
| 2.5 | Antigravity | Grounds each accuracy claim against live search | candidate claims → verdict + source |
| 3 | Claude | Writes itemized feedback | review notes + grounding → feedback.json |
| 4 | Codex | Reconciles feedback point by point (4a agree/revise, 4b disagree + reason) | feedback.json → draft v2 + decision.json |
| — | auto | If every point was 4a, finalize — no second review pass | — |
| 5 | Claude | Arbitrates any 4b disagreement (5a concur, 5b still disagrees) | decision.json → concur or flag |
| — | owner | Breaks the tie on a 5b flag; that decision resumes the loop | — |

Full prompt text for each step lives in `pipeline/prompts/`. JSON contracts: `pipeline/schemas/feedback.schema.json`, `pipeline/schemas/decision.schema.json`.

## 3. Why grounding is Step 2.5, not part of Step 5

Codex and Claude agreeing on a claim is not the same as the claim being true — both can be confidently wrong about the same fact. Step 2.5 checks accuracy claims against live search before they ever become official feedback, so "both models agree" stops being the only bar a fact has to clear. Runs on Antigravity CLI (`agy`), verified headless with no API key; Gemini via Vertex AI is the fallback if rate limits or reliability become an issue, billed against the existing $1,000 Vertex budget.

## 4. Tools — verified headless, no API keys

All three CLIs run on subscription/OAuth login, not metered API keys — status as of the Phase 1 hand-run (see section 9 for the live findings):

- **Codex CLI** (`codex exec`) — requires `--skip-git-repo-check` outside a trusted/git-repo directory; not needed once run from inside this repo. Also defaults to a **read-only sandbox**; writing the draft file needs `-s workspace-write`. Confirmed working headless.
- **Claude Code** (`claude -p`) — headless mode is permission-gated by default; checkpoint calls need `--allowedTools "Bash,Read,Edit"`, not the bare `claude -p` form, **and the prompt must be piped via stdin, not passed positionally after `--allowedTools`** (see section 9). **Not currently authenticated for headless use** — `claude -p` returns "Not logged in" even from a plain terminal, contradicting this section's original claim. Needs `claude setup-token` (or interactive `/login`) before Step 2/3/5 can run.
- **Antigravity CLI** (`agy -p`) — successor to Gemini CLI, which sunset for free/consumer use. Installer left the binary off PATH; add `~/.local/bin` to the shell profile if `agy: command not found` shows up again. Not yet exercised in the Phase 1 hand-run — Step 2.5 hasn't been reached.

## 5. Ownership — Claude is the sole GitHub operator, and owns all software work

One writer, always — not Codex, not a separate script wrapper. Wherever Claude is already running a step (review, feedback, arbitration), staging/committing/pushing rides along in that same call. Wherever Codex or Antigravity produced a step's output, one small additional Claude call does the checkpoint afterward: look at what changed, write the commit message, push.

This extends past GitHub: anything that counts as code, automation, or pipeline plumbing — the orchestrator script, prompt templates, wrapper code — goes through Claude specifically, never Codex. Codex's job is confined to the script's actual words (drafting in Step 1, reconciling in Step 4).

Checking whether a PR has been merged is a mechanical status check (`gh pr view <n> --json state`), not a judgment call — the orchestrator does that directly rather than spending a Claude call on it.

**PR-as-flag (idea for later, not built yet):** a Step 5b flag could become an actual pull request — the contested line as the diff, both agents' reasoning as PR comments, the owner's merge as the decision that resumes the loop.

## 6. Storage — GitHub for text, Google Drive for media

Already the repo's own rule (`PRODUCTION-STRUCTURE.md`), not a new one: GitHub stores plans, scripts, prompts, code, and small thumbnails; Google Drive stores heavy media (MP4/WAV drafts, frame exports, final renders, large source assets). Coverage Desk's script-stage files — drafts, feedback, decisions — are text, so they stay git-only.

```
Faceless-Youtube/
├── COVERAGE-DESK-SPEC.md      ← this file
├── pipeline/                  ← shared machinery, one copy for every episode
│   ├── prompts/
│   │   ├── 01-codex-draft.md
│   │   ├── 02-claude-review.md
│   │   ├── 02.5-antigravity-ground.md
│   │   ├── 04-codex-reconcile.md
│   │   └── 05-claude-arbitrate.md
│   ├── pipeline.yaml
│   ├── run-pipeline.sh
│   └── schemas/
│       ├── feedback.schema.json
│       └── decision.schema.json
└── Projects/
    └── <video-slug>/
        ├── Codex/              ← draft-v01.md, draft-v02.md, disagreement reasons
        ├── Claude/             ← review notes, feedback.json, decision.json
        ├── Shared/             ← the locked, finalized script
        └── Production/         ← downstream of the script, unaffected by this spec
```

Auth lives outside the repo entirely (`~/.codex`, `~/.claude`, `~/.gemini`); `.gitignore` is a backstop, not the control. `gh auth login` covers both `git push` and future `gh pr` commands. Losing the Mac means reinstalling and logging back in everywhere — never restoring a secret from a backup.

## 7. Known doc conflict — not yet resolved

`END-TO-END-WORKFLOW.md` has Claude drafting the script end-to-end with Gemini/OpenAI as the independent auditor — Codex isn't in that document at all. This spec's Codex-drafts/Claude-reviews split is confirmed as the actual design (it also matches how the `AI-Agent-Map` pilot was run in practice), but `END-TO-END-WORKFLOW.md` itself hasn't been edited yet to remove the contradiction. Do that before Phase 2.

## 8. Project plan

| Phase | Owner | What |
|---|---|---|
| 0 | Claude | Scaffold `pipeline/` and this file into the repo. One commit, nothing runs. |
| 1 | Owner | Hand-run the flow once on a real topic, calling each CLI directly, to prove the prompt wording and JSON shape before anything runs unattended. |
| 2 | Claude | Build `pipeline/run-pipeline.sh` for real: sequence the CLI calls, parse JSON between steps, branch on 4a/4b and 5a/5b, checkpoint to git. |
| 3 | Owner | First unattended run end to end — confirm it either auto-finalizes or flags, and that the push notification actually arrives. |
| 4 | Claude | Harden: retries/timeouts around headless CLI calls, clearer errors, a switch to Vertex if Antigravity's free tier gets rate-limited. |
| later | — | Extend the same shape (draft → review → ground → feedback → reconcile → arbitrate) to voiceover, editing, and thumbnails. Not scheduled. |

## 9. Phase 1 findings log

Live notes from the first hand-run, topic: *"The Life of a Packet — What Actually Happens on the Network When Your AI Agent Does a Task"* (episode folder: `Projects/Life-of-a-Packet/`). Grounded in the owner's own Cisco Live 2026 (Las Vegas) session on this topic. Updated as each step is actually run — this is the evidence Phase 2's orchestrator gets built from, not a prediction of it.

**Step 1 (Codex draft) — done.** `codex exec --skip-git-repo-check -s workspace-write "<prompt>"` produced `Projects/Life-of-a-Packet/Codex/draft-v01.md` (13 scenes, ~2,500 words) on the second attempt. First attempt failed silently on the write — Codex's sandbox defaults to read-only, so `-s workspace-write` is required, not optional. Codex also self-corrected a claim from the owner's own notes ("every agent is its own IP endpoint" isn't quite right — agents typically share a host IP; NAT/PAT tracks per-flow state, not per-agent identity) rather than repeating it uncritically, which is the behavior the spec's uncertainty rule is meant to produce.

**Step 2 (Claude review) — blocked.** Two issues surfaced, in order:

1. `claude -p --allowedTools "Bash,Read,Edit" "<prompt>"` fails: `--allowedTools` greedily consumes the next argv as more comma-separated tool rules instead of treating it as the prompt, so the prompt text gets shredded into garbage permission rules and `claude -p` then errors with no prompt provided. **Fix:** pipe the prompt via stdin instead of passing it positionally — `cat prompt.md | claude -p --allowedTools "Bash,Read,Edit"`.
2. With that fixed, `claude -p` returns `Not logged in · Please run /login` — reproduced both from inside a Claude Code session's Bash tool and from a plain Terminal window (`echo hi | claude -p`), so this isn't a nested-session artifact. This section's earlier claim that `claude -p` was "confirmed working headless on this Mac" was stale/wrong. **Fix, not yet applied:** run `claude setup-token` (headless-appropriate, unlike interactive browser `/login`) and retry.

Steps 2.5 through 5 haven't been attempted yet — blocked behind the Step 2 auth fix.

---

*Coverage Desk · script-stage automation spec · git-backed twin of the published Artifact*

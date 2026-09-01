# Step 4 — Codex reconciles feedback

- **Role:** Codex CLI (`codex exec --skip-git-repo-check -s workspace-write`)
- **Input:** `Projects/<slug>/Claude/feedback.json` + `Projects/<slug>/Codex/draft-v01.md`
- **Output:** `Projects/<slug>/Codex/draft-v02.md` + `Projects/<slug>/Claude/decision.json`

## Instructions

Read `Projects/<slug>/Claude/feedback.json`, `Projects/<slug>/Codex/draft-v01.md`, and `pipeline/schemas/decision.schema.json`.

Go through every point in `feedback.json`, one at a time.

- **Agree (4a):** revise the script to fix it. Record `codex_response: agree`, `status: resolved_agree`.
- **Disagree (4b):** leave the line as written, but you must give a specific reason — not "I think it's fine," but why the feedback is wrong, unnecessary, or would hurt the video. Record `codex_response: disagree`, `codex_reason: "..."`.

Every `id` in `feedback.json` needs a matching entry in `decision.json` — do not silently drop a point.

For accuracy points that already have a `grounded` object: a `supported` verdict with a `note` suggesting a precision edit is your judgment call whether it rises to "agree" (make the edit) or "disagree" (explain why the current phrasing is already fine). For accuracy points with no `grounded` object (ungrounded, per `feedback.json`'s own `issue` text): treat "this hasn't been verified yet" as a real constraint on your reasoning — either soften confident-sounding language as a cautious agree, or give a specific reason the claim is safe to leave as-is pending grounding. Don't treat an ungrounded claim as already cleared.

## Output format

Write the full revised script as `Projects/<slug>/Codex/draft-v02.md`, in the same format as `draft-v01.md` (scene headings, narration, on-screen text, visual direction, pronunciation notes).

Write `Projects/<slug>/Claude/decision.json` matching the schema exactly: `episode_slug` matching the episode slug, `draft_version: "v02"`, and a `decisions` array with one entry per feedback point.

If every point resolves `agree`, say so explicitly at the end of your response (the episode auto-finalizes and Step 5 is skipped). If any point is `disagree`, list which ones need Step 5 arbitration.

## Task

Do the reconciliation now and write both files.

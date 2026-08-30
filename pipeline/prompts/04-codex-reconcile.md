# Step 4 — Codex reconciles feedback

- **Role:** Codex CLI (`codex exec`)
- **Input:** `Projects/<slug>/Claude/feedback.json`
- **Output:** `Projects/<slug>/Codex/draft-v02.md` + a `decision.json` entry per feedback point

## Instructions

Go through every point in `feedback.json`, one at a time.

- **Agree (4a):** revise the script to fix it. Record `codex_response: agree`, `status: resolved_agree`.
- **Disagree (4b):** leave the line as written, but you must give a specific reason — not "I think it's fine," but why the feedback is wrong, unnecessary, or would hurt the video. Record `codex_response: disagree`, `codex_reason: "..."`.

Every `id` in `feedback.json` needs a matching entry in `decision.json` — do not silently drop a point. If every point resolves `agree`, the episode auto-finalizes and Step 5 is skipped.

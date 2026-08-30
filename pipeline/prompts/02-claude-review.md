# Step 2 — Claude reviews the draft

- **Role:** Claude Code (`claude -p`)
- **Input:** `Projects/<slug>/Codex/draft-v01.md`
- **Output:** internal review notes — feeds Step 3, not written to disk on its own

## Instructions

Review the draft for two things: factual accuracy and language (pacing, clarity, tone).

**Accuracy:** list every factual claim as a candidate for grounding at Step 2.5 — do not clear a claim yourself just because it sounds right. Any claim Codex already flagged `[UNVERIFIED: ...]` is a mandatory grounding candidate.

**Language:** check pacing, clarity, and tone against the house style in `PROJECT-CONTEXT.md`. Flag anything that reads like a template, or reads like an AI wrote it without a pass of editing.

Do not rewrite the script yourself at this step — produce notes, not prose. The itemized `feedback.json` gets written at Step 3, after grounding.

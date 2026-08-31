# Step 3 — Claude writes itemized feedback

- **Role:** Claude Code (`claude -p`)
- **Input:** review notes (Step 2) + grounding verdicts (Step 2.5) + any owner decisions made along the way
- **Output:** `Projects/<slug>/Claude/feedback.json`

## Instructions

Read `pipeline/schemas/feedback.schema.json` — your output must validate against it exactly (required fields, enums, structure).

Read `Projects/<slug>/Codex/draft-v01.md` for scene/line references.

Turn the Step 2 review notes and Step 2.5 grounding verdicts into itemized `points`, each with a stable `id` (`fb-01`, `fb-02`, ...), a `category` (`accuracy` or `language`), a `location` (scene reference), an `issue`, and a `suggested_fix`.

- Every accuracy candidate that went through Step 2.5 grounding must include the `grounded` object (`checked_by`, `verdict`, `source`, and `note` when the verdict isn't a clean `supported`).
- Not every accuracy candidate has to be grounded before Step 3 — grounding a large candidate list one claim at a time is expensive, and a hand-run or a time-boxed pass may only sample it. Ungrounded accuracy points are still valid `feedback.json` entries: say so plainly in `issue` (this claim has not been grounded yet) rather than treating an ungrounded claim as already cleared.
- Any point that resolves an explicit owner decision (a house-style call, a policy question, anything that isn't a fact to verify) should say so in `issue` and skip the `grounded` object entirely — grounding answers "is this true," not "should we say this."
- Pronunciation-completeness findings from Step 2 (see `02-claude-review.md`) are `category: language` points, one per abbreviation missing a note, or grouped into a single point if there are many.

## Output format

Write the complete `feedback.json` to `Projects/<slug>/Claude/feedback.json`. Valid JSON only, matching the schema. Set `episode_slug` to the episode's slug, `draft_version` to the draft version being reviewed (e.g. `v01`), and `generated_by` to `claude`.

After writing the file, print a short confirmation: how many points, and the accuracy/language breakdown.

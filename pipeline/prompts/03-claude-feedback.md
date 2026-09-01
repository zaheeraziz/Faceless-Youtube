# Step 3 — Claude writes itemized feedback

- **Role:** Claude Code (`claude -p --allowedTools "Bash,Read,Write,Edit"`)
- **Input:** Step 2's review notes (piped in) + `Projects/<slug>/Codex/draft-v01.md` + any owner decisions made along the way
- **Output:** `Projects/<slug>/Claude/feedback.json`, committed and pushed

## Instructions

Read `pipeline/schemas/feedback.schema.json` — your output must validate against it exactly (required fields, enums, structure).

Read `Projects/<slug>/Codex/draft-v01.md` for scene/line references.

### Ground the accuracy candidates yourself

Step 2's review notes (below) list candidate factual claims. Step 2.5 — grounding those claims against live search — is your job to run, not something handed to you pre-computed: read `pipeline/prompts/02.5-antigravity-ground.md` for the grounding prompt format, then invoke `agy -p "<prompt>"` yourself via Bash, once per claim you decide is worth checking.

Not every accuracy candidate has to be grounded — grounding a large candidate list one claim at a time is expensive, and a time-boxed pass may only sample it. Use judgment: prioritize claims that are load-bearing (the video's argument depends on them), claims stated as flat assertions rather than hedges, and anything Step 2 flagged as `[UNVERIFIED: ...]` (always ground those). An ungrounded accuracy point is still a valid `feedback.json` entry — say so plainly in `issue` (this claim has not been grounded yet) rather than treating an ungrounded claim as already cleared.

### Write the itemized points

Turn Step 2's review notes and your own grounding results into itemized `points`, each with a stable `id` (`fb-01`, `fb-02`, ...), a `category` (`accuracy` or `language`), a `location` (scene reference), an `issue`, and a `suggested_fix`.

- Every accuracy candidate you grounded must include the `grounded` object (`checked_by: "antigravity"`, `verdict`, `source`, and `note` when the verdict isn't a clean `supported`).
- Any point that resolves an explicit owner decision (a house-style call, a policy question, anything that isn't a fact to verify) should say so in `issue` and skip the `grounded` object entirely — grounding answers "is this true," not "should we say this."
- Pronunciation-completeness and pronunciation-correctness findings from Step 2 (see `02-claude-review.md`) are `category: language` points, one per abbreviation, or grouped into a single point if there are many.

## Output format

Write the complete `feedback.json` to `Projects/<slug>/Claude/feedback.json`. Valid JSON only, matching the schema. Set `episode_slug` to the episode's slug, `draft_version` to the draft version being reviewed (e.g. `v01`), and `generated_by` to `claude`.

## Checkpoint

Once `feedback.json` is written, commit and push it yourself — you're already the Claude call for this step, so the checkpoint rides along in the same turn (see `COVERAGE-DESK-SPEC.md` section 5). Stage only `Projects/<slug>/Claude/feedback.json`, write a commit message specific to what's in it (point count, how many were grounded, anything notable), commit, and push to `origin {{push_branch}}`.

After pushing, print a short confirmation: how many points, the accuracy/language breakdown, how many accuracy points were actually grounded (and how many were left ungrounded and why), and the commit hash.

## Step 2's review notes

Everything below this line is Step 2's raw review output for this draft, appended as-is.

---


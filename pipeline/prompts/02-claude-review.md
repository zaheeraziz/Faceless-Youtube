# Step 2 — Claude reviews the draft

- **Role:** Claude Code (`claude -p`)
- **Input:** `Projects/<slug>/Codex/draft-v01.md`
- **Output:** internal review notes — feeds Step 3, not written to disk on its own

## Instructions

Review the draft for two things: factual accuracy and language (pacing, clarity, tone).

**Accuracy:** list every factual claim as a candidate for grounding at Step 2.5 — do not clear a claim yourself just because it sounds right. Any claim Codex already flagged `[UNVERIFIED: ...]` is a mandatory grounding candidate.

**Language:** check pacing, clarity, and tone against the house style in `PROJECT-CONTEXT.md`. Flag anything that reads like a template, or reads like an AI wrote it without a pass of editing.

**Pronunciation completeness and correctness:** list every abbreviation/acronym used in the narration or on-screen text (e.g. via a scan for all-caps tokens) and cross-check it against the scene's existing `Pronunciation notes` — this isn't optional polish, it's a real TTS/narrator failure mode. Two separate things to check, not one:

- **Missing:** an abbreviation with no note at all. Don't skip one just because it seems common — flag it and let Step 4 decide whether a note is actually needed.
- **Wrong:** an abbreviation that *has* a note, but the note gets the letter-vs-word call backwards. Every abbreviation is read one of two ways — as a word (e.g. `RAG` → "rag," `LISP` → "lisp," `QUIC` → "quick," `NAT` → "nat," `PAT` → "pat") or letter-by-letter (e.g. `SLA`, `DNS`, `DHCP`) — and this is a real, checkable industry convention per term, not a style preference. Don't assume a grouped note is uniformly correct just because most of the group is right: `"DHCP, NAT, PAT: say each letter"` was wrong for two of its three entries (NAT and PAT are both word-pronounced), and grouping them together is exactly what let the error hide. Check each abbreviation's convention individually, even inside an existing group.

If you're not confident which way a specific abbreviation goes, send it to Step 2.5 as a grounding candidate rather than guessing — this is a checkable fact, not a judgment call.

**Acronym expansion:** separate from pronunciation (which is *how* to say it) — check that every acronym/abbreviation used in narration is actually expanded in words the first time it appears (e.g. "NAT — Network Address Translation"). A pronunciation note doesn't tell the viewer what the term means. Flag any acronym that's spoken correctly but never defined.

**Length:** count narration words only (not on-screen text or visual direction). The hard budget is ~650-700 words (~5 minutes at a deliberate educational pace) — see `PROJECT-CONTEXT.md`. If the draft runs meaningfully over, this is not a minor style note — flag it as a priority language point naming the actual word count and the overage, since it drives a real structural cut at Step 4, not a line edit.

**Title/theme bookend:** check that the episode's own title or theme phrase (not just a loosely similar idea) is explicitly spoken in both the opening hook and the closing line. If it only appears in the file header/title and never in narration, flag it.

Do not rewrite the script yourself at this step — produce notes, not prose. The itemized `feedback.json` gets written at Step 3, after grounding.

## Task

Read `Projects/<slug>/Codex/draft-v01.md` and review it now. Print your review notes directly as your response — plain text/markdown, organized by accuracy candidates then language notes (including pronunciation). This is an internal handoff to Step 3, not a repo deliverable — don't write any files.

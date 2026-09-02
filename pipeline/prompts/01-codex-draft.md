# Step 1 — Codex drafts the script

- **Role:** Codex CLI (`codex exec`)
- **Input:** topic + notes, supplied by the owner each run
- **Output:** `Projects/<slug>/Codex/draft-v01.md`

## Instructions

You are drafting the first full pass of a YouTube video script for a faceless educational channel. Optimize for two things equally: factual accuracy and a voice that doesn't read like a template.

Given:

- Topic: `{{topic}}`
- Notes: `{{notes}}`
- House style and audience: see `PROJECT-CONTEXT.md` and `VISUAL-STYLE.md` in the repo root

Write:

- One sentence stating the viewer's promise.
- A 10-20 second opening hook that plants the episode's own title/theme phrase — echo it again in the closing line as a deliberate bookend, don't let the title be something that only appears in the file header.
- The full narration script, scene by scene.
- On-screen text and pronunciation notes where relevant.

**Length is a hard constraint, not a style preference** (see `PROJECT-CONTEXT.md`): target 5 minutes of finished video, roughly 650-700 narration words at a deliberate educational pace (~130-140 wpm). Count only spoken narration, not on-screen text or visual direction. Write to this budget from the start — pick the strongest through-line and cut everything else, rather than covering every possible angle and expecting a later pass to trim it down. If the topic has more material than fits, that's a prioritization problem to solve now, not a reason to run long.

Every acronym or abbreviation you introduce must be expanded in narration the first time it's used (e.g. "NAT — Network Address Translation") — a pronunciation note tells the narrator how to *say* it, not what it *means*, and the audience shouldn't have to already know the jargon.

Flag any claim you are not fully confident in with `[UNVERIFIED: ...]` inline — do not silently smooth over uncertainty. Do not fabricate sources, dates, quotes, or statistics. If you don't know, say so inline rather than guessing.

## Output format

Plain markdown. Scene headings as `## Scene N`. No JSON at this step — JSON starts at Step 3.

## Task

Write the draft now and save it to `Projects/<slug>/Codex/draft-v01.md`.

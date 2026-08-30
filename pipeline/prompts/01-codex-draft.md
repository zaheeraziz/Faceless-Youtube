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
- A 10-20 second opening hook.
- The full narration script, scene by scene.
- On-screen text and pronunciation notes where relevant.

Flag any claim you are not fully confident in with `[UNVERIFIED: ...]` inline — do not silently smooth over uncertainty. Do not fabricate sources, dates, quotes, or statistics. If you don't know, say so inline rather than guessing.

## Output format

Plain markdown. Scene headings as `## Scene N`. No JSON at this step — JSON starts at Step 3.

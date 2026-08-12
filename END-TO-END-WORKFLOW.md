# End-to-End Faceless YouTube Workflow

## Provisional stack—not a fixed tool limit

Tool consolidation is a goal, not a rule. The stack below is the smallest plausible starting system. Add or replace tools when a pilot exposes a real capability, quality, licensing, reliability, or cost gap.

### Provisional paid services to test

1. **Claude / Claude Code** — control center for research, scripts, storyboards, editing, thumbnails, QA, and project management.
2. **ElevenLabs** — consistent AI narration plus speech timing for captions and scene synchronization.
3. **Higgsfield** — generated images and video shots that cannot be created efficiently with geometric animation.
4. **Gemini or OpenAI** — independent audit of Claude's work; it must not share authorship of the first draft.

These three are hypotheses, not commitments. Higgsfield in particular must earn its place through output quality and cost. A licensed music library, archival-media provider, specialist image generator, or different editing service may be required after testing.

### Production engine—not additional services the owner operates

- **Remotion** — code-based video timeline, 2D animation, captions, audio, and rendering.
- **React Three Fiber / Three.js** — selected 3D architectural scenes inside Remotion.
- **FFmpeg** — rendering and media processing behind the workflow.
- **GitHub** — versioned scripts, code, prompts, style rules, and project history.
- **YouTube Studio** — manual publishing and analytics.

## Workflow

### 1. Select the episode

**Claude produces:**

- One historical question connecting a city, food, and architecture.
- Five possible titles and three thumbnail directions.
- Demand, competition, visual potential, source availability, cost, and copyright-risk scores.

**Approval gate:** Do not research the full episode until the owner approves the question and packaging direction.

### 2. Build the research dossier

**Claude produces:**

- Source list favoring museums, universities, archives, books, government cultural institutions, and strong historical publications.
- Claim ledger: each factual claim, supporting source, confidence, and disputed interpretations.
- Timeline, key people, food origins, architectural facts, geometry, pronunciations, and visual-rights notes.

**Approval gate:** Weakly sourced claims are removed or clearly qualified.

### 3. Write the story package

**Claude produces:**

- One-sentence viewer promise.
- 10–20 second opening hook.
- Full narration script.
- Scene-by-scene storyboard.
- Visual asset list and music/sound plan.
- On-screen text and pronunciation guide.

**Editorial rule:** Food and architecture must answer the central historical question. They cannot feel like unrelated list segments.

### 4. Create narration

**ElevenLabs produces:**

- Narration using one consistent, commercially licensed voice.
- Timing data used for captions and scene synchronization.

**Claude checks:** pronunciation, pauses, emphasis, pacing, and factual deviations before visuals are finalized.

### 5. Create visual assets

**Claude Code + Remotion create:**

- Maps, timelines, labels, captions, diagrams, geometric construction, transitions, and 2D architectural reveals.
- Selected 2D-to-3D transformations using Three.js/React Three Fiber.

**Higgsfield creates:**

- Atmospheric city, food, historical, and establishing shots where generated footage adds real value.

**Licensed/public-domain sources provide:** authentic artwork, maps, manuscripts, photographs, and architecture where accuracy matters.

### 6. Assemble and edit

**Claude Code:**

1. Imports narration, assets, music, and effects.
2. Builds the Remotion timeline from narration timings.
3. Adds captions and purposeful visual changes.
4. Mixes narration, music, and sound effects.
5. Renders a low-resolution review draft.
6. Applies owner feedback expressed in plain language.
7. Renders the final master only after approval.

### 7. Independent second-model audit

After Claude completes the draft, send the audit package to **Gemini or OpenAI**. Use a different provider from the authoring model to reduce correlated errors.

The package contains:

- Final script and claim ledger.
- Full source list and exact source-to-claim mappings.
- Storyboard and low-resolution rendered video.
- Asset inventory with origin, license, required attribution, and generated-media status.
- Music, sound-effect, narration, footage, image, and font licenses.
- Proposed title, description, disclosure, and thumbnails.

The second model returns a structured report:

- **Factual audit:** unsupported, contradicted, overstated, ambiguous, or outdated claims.
- **Source audit:** weak sources, citation mismatch, missing context, and claims that require primary evidence.
- **Copyright audit:** unclear ownership, license incompatibility, missing attribution, excessive third-party use, trademark/trade-dress concerns, and reused-content risk.
- **Quality audit:** hook, clarity, pacing, visual continuity, narration, captions, mobile readability, and thumbnail/title alignment.
- **Policy audit:** synthetic-media disclosure, advertiser-suitability concerns, and likely YouTube policy issues.
- **Verdict:** pass, pass with required fixes, or block publication.

Claude must answer every finding with **fixed, rejected with evidence, or accepted risk requiring owner approval**. The auditing model then reviews the corrections. A model opinion is not evidence; factual clearance still requires authoritative sources, and legal uncertainty may require licensed material or professional advice.

### 8. Technical quality assurance

Claude runs checklists for:

- Facts and source traceability.
- Names and pronunciation.
- Narration/caption/visual synchronization.
- Copyright and commercial-use documentation.
- Synthetic-media disclosure requirements.
- Audio levels, blank frames, broken assets, and rendering errors.
- Pacing, mobile readability, and repetitive visuals.

**Owner approval remains mandatory.** Full automation cannot judge historical nuance or whether the story is genuinely engaging.

### 9. Create thumbnails

**Claude owns the complete task:**

- Develops three concepts tied to the title and opening promise.
- Generates necessary assets through Higgsfield or constructs them with shapes/code.
- Composes and exports three 1280×720 variants.
- Checks contrast, focal point, minimal text, factual accuracy, and mobile-size legibility.

Claude is the director and compositor; an image engine is still needed when the thumbnail requires generated photographic imagery.

The independent model audits all three variants for misleading implications, copied visual identity, factual errors, and mobile clarity.

### 10. Publish manually

Claude prepares the title, description, chapters, sources, disclosure wording, and thumbnail files. The owner approves and publishes through YouTube Studio.

Do not automate publishing until the production checklist has passed reliably across multiple videos.

### 11. Learn from performance

After 48 hours, 7 days, and 28 days, record:

- Impressions and click-through rate.
- First-30-second retention.
- Average percentage viewed and watch time.
- Returning viewers and subscriber conversion.
- Comments indicating confusion, trust, or topic demand.
- Actual tool cost and human review time.

Claude converts the results into specific changes for the next episode. Do not change the entire format based on one video.

## Tool-sprawl decisions

| Removed tool | Reason |
|---|---|
| NotebookLM | Claude maintains the sourced research dossier and claim ledger in the repository |
| Descript | Claude Code performs final text-directed editing in Remotion |
| Canva | Claude composes and renders thumbnail variants |
| AssemblyAI | No raw human narration; ElevenLabs supplies speech timing |
| Base44 | App builder, not part of video production |
| Separate caption tool | Captions derive from the approved script and ElevenLabs timing |
| YouTube API automation | Premature and increases publishing risk |

The Gemini/OpenAI audit is intentionally **not removed as tool sprawl**. Independence is the capability; Claude cannot independently audit its own work.

## Tool admission rule

Add a tool only when the pilot demonstrates a specific gap and the candidate materially improves at least one of these:

- Historical accuracy or source traceability.
- Commercial licensing safety.
- Visual or audio quality.
- Production reliability.
- Production time.
- Cost per finished minute.

Do not reject a necessary tool merely to preserve a numerical limit. Do not keep a tool because a creator promoted it.

## Minimum viable pilot

- Length: 5–7 minutes.
- One city, one central question, one dish, and one landmark.
- One signature geometric construction sequence.
- One short 3D reveal—not an entire 3D film.
- Maximum three Higgsfield-generated shots.
- Three Claude-produced thumbnail variants.
- Manual review before publishing.

This pilot tests the channel idea and the production system without disguising technical complexity as progress.

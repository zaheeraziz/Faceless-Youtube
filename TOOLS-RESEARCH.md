# Faceless YouTube Tool Research

Extracted from the saved video transcripts. Tool claims remain unverified until tested.

## Owner capability requirement

The owner is not a scriptwriter, narrator, video editor, or animator. The stack must therefore assist with the complete workflow and present reviewable drafts rather than require manual production expertise.

The number of paid tools is not capped. Consolidation must not sacrifice accuracy, licensing, quality, or reliability. The pilot determines which tools remain.

An independent Gemini or OpenAI review is required. This is not redundant tool sprawl because Claude cannot provide an independent audit of its own script, edit, sources, and asset decisions.

## Recommended practical stack

| Need | Recommended starting tool | Purpose |
|---|---|---|
| Source-grounded research | NotebookLM plus primary sources | Organize sources and reduce unsupported historical claims |
| Story and script | Claude | Turn approved research into the hook, narrative, scene plan, and narration script |
| Narration | ElevenLabs | Generate a consistent licensed channel voice |
| Signature geometry | Claude Code + Remotion | Generate reusable 2D shape construction, maps, captions, and transitions |
| 3D signature scenes | React Three Fiber / Three.js inside Remotion | Create selected 2D-to-3D architectural reveals |
| Generated visual clips | Higgsfield | Produce shots that are impractical to build from shapes or licensed media |
| Final assembly and correction | Claude Code + Remotion project | Edit scenes, timing, captions, audio, transitions, and effects through instructions and code |
| Thumbnails | Claude plus the project's image/rendering tools | Create concepts, generate assets, compose the design, and export finished variants |
| Storage and version control | GitHub plus cloud storage | Preserve code/templates separately from large rendered assets |
| Publishing and analytics | YouTube Studio | Upload, schedule, package, and measure performance |

## What each AI must deliver

- **Claude:** research brief, sourced fact table, script, pronunciation guide, storyboard, and asset list.
- **ElevenLabs:** final narration only after the script is approved.
- **Claude Code/Remotion:** rendered geometric sequences from approved storyboard instructions.
- **Higgsfield:** only the missing visual shots—not the entire editorial product by default.
- **Claude Code:** assembled draft and revision passes; the owner reviews rendered previews and requests changes in plain language.
- **Claude:** three finished thumbnail variants using reusable brand rules, with text kept minimal and checked at mobile size.

## Setup reality

The geometric 2D-to-3D signature is not a dependable one-click effect. Use the referenced Claude/Remotion repository, but expect a one-time technical setup and template-building phase. If Claude Code cannot make it repeatable, hire a Remotion developer once to build the reusable scene system; do not hire an editor for every episode.

## Optional production tools

| Tool | Transcript use | Decision |
|---|---|---|
| ElevenLabs | AI voice generation and narration | Current leading option; compare against at least one alternative before committing |
| AssemblyAI | Transcription used to find silence, filler words, and bad takes | Useful when editing recorded narration or presenter footage |
| Higgsfield AI / Higgsfield MCP | Scene generation, visuals, voice, music, editing, and Claude integration | Pilot alternative to a custom Remotion workflow; compare quality and cost |
| Nano Banana | AI image generation | Optional visual source; licensing and consistency must be checked |
| AI image generator | Creates illustrated assets for stories and animated explainers | Provider is not clearly identified in the transcript |
| YouTube Data API | Automated upload and scheduling | Add only after manual quality control is reliable |
| Base44 | AI app builder demonstrated in one video | Not needed for the channel; only its planning method is relevant |
| Visual editor | Cosmetic changes without regenerating logic/content | General technique; no specific video editor is identified |

## Production system described

1. Define the video promise and audience.
2. Research and write an original script.
3. Plan the hook, scenes, timing, and layers before generation.
4. Generate or source visual assets.
5. Animate layers in Remotion or generate scenes with Higgsfield.
6. Generate narration with a consistent, commercially licensed AI voice.
7. Align captions, music, and effects to narration timestamps.
8. Run human and automated quality checks.
9. Create three title-and-thumbnail combinations.
10. Upload manually first; automate only after the workflow is stable.

## Cost and risk checks

- Measure total cost per finished minute, including failed generations, revisions, rendering, storage, subscriptions, and human review.
- Verify commercial-use rights for every generated or sourced asset.
- Keep scripts, narration, editing, and visual composition original.
- Do not rely on automatic uploads until factual, audio, timing, and policy checks are dependable.
- Build a reusable asset library and style guide only after the first format performs.

## Pilot recommendation

For the first pilot, use **Claude/Claude Code + ElevenLabs + Higgsfield**, with Remotion and Three.js as the underlying production engine. Claude will maintain the sourced research dossier, perform the final edit, and produce thumbnail variants. Include only one short geometric-to-3D sequence. Expand complex 3D work only if it is reliable and materially improves the video.

## Tools not recommended as the core workflow

- **Base44:** app builder; its planning ideas are useful, but it does not solve video production.
- **Fully automatic faceless-video generators:** fast, but likely to produce generic scripts, repetitive visuals, and weak differentiation.
- **Automated YouTube API uploads:** unnecessary until the channel has a stable human-review checklist.

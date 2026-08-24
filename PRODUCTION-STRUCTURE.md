# Production Structure

Purpose: keep each video organized across Codex, Claude, GitHub, and Google Drive.

## Rule

GitHub stores lightweight working knowledge:

- plans
- scripts
- prompts
- code
- small thumbnails
- render scripts

Google Drive stores heavy media:

- MP4 drafts
- WAV/AIFF/M4A audio drafts
- frame exports
- final renders
- large source assets

## Folder Pattern

Each video gets one project folder:

```text
Projects/
  AI-Agent-Map/
    Codex/
    Claude/
    Shared/
    Production/
      brief/
      script/
      storyboard/
      assets/
      thumbnails/
      audio/
      video-drafts/
      final/
      archive/
```

Mirror the same folder in Google Drive:

```text
AI-Projects/
  Youtube Videos/
    Faceless-Youtube/
      Projects/
        AI-Agent-Map/
          Production/
            audio/
            video-drafts/
            thumbnails/
            final/
            source-assets/
```

## Version Naming

Use this pattern:

```text
video-slug_asset-type_v01_short-note.ext
```

Examples:

```text
ai-agent-graph_script_v01_master.md
ai-agent-graph_audio_v01_temp-voice.m4a
ai-agent-graph_thumb_v01_ai-needs-map.png
ai-agent-graph_scene01_v04_mobile-test.mp4
ai-agent-graph_full-video_v01_rough-cut.mp4
```

## Version Rules

- `v01`, `v02`, `v03` are real saved versions.
- Do not overwrite a version after sharing it.
- Use `draft` only for disposable local work.
- Use `final` only after QA is complete.
- Keep raw frames out of GitHub.
- Keep generated previews if they explain a decision.
- Archive rejected versions only if they contain useful learning.

## Decision Log

Each production folder should include a short decision log:

```text
brief/decision-log.md
```

Track:

- locked title
- thumbnail direction
- script version
- voice version
- final tool used
- QA result
- publish decision

## Current Video

Video folder:

```text
Projects/AI-Agent-Map/Production/
```

Locked title:

The Graph Behind Smart AI Agents

Thumbnail direction:

AI NEEDS A MAP

Lead planning source:

```text
Projects/AI-Agent-Map/Shared/AI-AGENT-MAP-MASTER-SCRIPT.md
```

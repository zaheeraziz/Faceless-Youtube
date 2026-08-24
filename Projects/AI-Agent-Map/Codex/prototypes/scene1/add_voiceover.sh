#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
VIDEO_IN="$SCRIPT_DIR/scene1_lost_agent_probe.mp4"
AUDIO_OUT="$SCRIPT_DIR/scene1_temp_voice.aiff"
VIDEO_OUT="$SCRIPT_DIR/scene1_lost_agent_probe_with_voice.mp4"

say -v Samantha -r 158 \
  "An AI agent can sound smart. But without a map, it can still get lost. It can loop, skip checks, or rush to the wrong answer." \
  -o "$AUDIO_OUT"

ffmpeg -y \
  -i "$VIDEO_IN" \
  -i "$AUDIO_OUT" \
  -c:v copy \
  -c:a aac \
  "$VIDEO_OUT"

echo "$VIDEO_OUT"

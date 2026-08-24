#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
OUT_AIFF="$SCRIPT_DIR/the_graph_behind_smart_ai_agents_draft.aiff"
OUT_M4A="$SCRIPT_DIR/the_graph_behind_smart_ai_agents_draft.m4a"

TEXT='It looks smart, until it skips verification.

Without control flow, an agent can miss the step that matters.

A prompt can describe what you want.

But a graph defines what runs next.

In an agent graph, nodes do the work.

Edges control the route.

And state carries the context from step to step.

The important part is not just connecting boxes.

The important part is deciding what happens after each step.

After Check, the graph can ask: did this pass?

If yes, publish.

If no, revise.

That decision is not magic. The Check node still needs an evaluator: a rule, a tool, a model call, or a human review.

State is what keeps the process connected.

It can carry research notes, the draft, feedback, and errors.

Without state, every step starts half-blind.

When something fails, the graph can loop.

It can revise, re-check, and continue without losing the whole process.

And if unchanged work already ran with the same input, caching can reuse that result instead of paying for the same step again.

So smart agents do not just need bigger prompts.

They need a map: nodes for work, edges for control, and state for context.

That is the graph behind smart AI agents.'

say -v Samantha -r 158 "$TEXT" -o "$OUT_AIFF"

ffmpeg -y -i "$OUT_AIFF" -c:a aac -b:a 128k "$OUT_M4A"

echo "$OUT_M4A"

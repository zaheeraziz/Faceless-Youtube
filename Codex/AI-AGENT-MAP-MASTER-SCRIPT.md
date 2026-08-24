# Master Script - The Graph Behind Smart AI Agents

## Locked Package

Title:

The Graph Behind Smart AI Agents

Thumbnail direction:

AI NEEDS A MAP

Lead thumbnail:

Codex/thumbnails/ai-agent-map/03-ai-needs-map.png

Audience:

Technical AI learners who know prompting but are new to graph-based agent workflows.

Target length:

60-75 seconds.

Core promise:

Explain how graph-based workflows help AI agents know what to do next.

## Accuracy Frame

This video is about graph-based AI agent workflows, not a claim that every agent must use a graph framework.

Use these definitions:

- Node: a step, function, model call, or tool call.
- Edge: the route/control flow between steps.
- State: structured context/data passed through the workflow.
- Cache: reuse of a prior node result when the same input can safely use the same output.

Do not say:

- Prompts are useless.
- Graphs guarantee correctness.
- Graph engineering is the only way to build agents.
- Caching improves reasoning quality.
- The graph magically knows truth.

## Full Voiceover

"It looks smart, until it skips verification."

"Without control flow, an agent can miss the step that matters."

"A prompt can describe what you want."

"But a graph defines what runs next."

"In an agent graph, nodes do the work."

"Edges control the route."

"And state carries the context from step to step."

"The important part is not just connecting boxes."

"The important part is deciding what happens after each step."

"After Check, the graph can ask: did this pass?"

"If yes, publish."

"If no, revise."

"That decision is not magic. The Check node still needs an evaluator: a rule, a tool, a model call, or a human review."

"State is what keeps the process connected."

"It can carry research notes, the draft, feedback, and errors."

"Without state, every step starts half-blind."

"When something fails, the graph can loop."

"It can revise, re-check, and continue without losing the whole process."

"A graph can reduce avoidable errors by making verification a required step."

"Caching can cut cost by reusing unchanged work instead of paying for the same call again."

"So smart agents do not just need bigger prompts."

"They need a map: nodes for work, edges for control, and state for context."

"That is the graph behind smart AI agents."

"Optional CTA: I put three small assignments in the GitHub repo. Pick one, build it, and comment what you changed."

## Scene Breakdown

### Scene 1 - Skipped Check

Purpose:

Show the failure.

Visual:

The probe follows the wrong path:

Research -> Draft -> Publish

The correct graph route is visible:

Research -> Draft -> Check -> Publish

On-screen text:

- Smart agents still fail
- Graph Route
- Skipped Check
- No usable map

Voiceover:

"It looks smart, until it skips verification."

"Without control flow, an agent can miss the step that matters."

### Scene 2 - Prompt To Graph

Purpose:

Explain that a prompt can describe desired behavior, but a graph defines execution.

Visual:

A prompt block transforms into nodes and edges. A state packet appears beside the probe.

On-screen text:

- Prompt describes
- Graph executes
- Node
- Edge
- State

Voiceover:

"A prompt can describe what you want."

"But a graph defines what runs next."

"In an agent graph, nodes do the work. Edges control the route. And state carries the context from step to step."

### Scene 3 - Decision Point

Purpose:

Show conditional routing after evaluation.

Visual:

The probe reaches Check. Check expands into a diamond:

Pass?

Yes -> Publish

No -> Revise

On-screen text:

- Decision point
- Pass?
- Yes -> Publish
- No -> Revise

Voiceover:

"The important part is not just connecting boxes."

"The important part is deciding what happens after each step."

"After Check, the graph can ask: did this pass?"

"If yes, publish. If no, revise."

"That decision is not magic. The Check node still needs an evaluator: a rule, a tool, a model call, or a human review."

### Scene 4 - State Carries Context

Purpose:

Explain state clearly.

Visual:

A glowing state packet opens and shows layers:

- notes
- draft
- feedback
- errors

The packet travels with the probe and updates at each node.

On-screen text:

- State
- notes
- draft
- feedback
- errors

Voiceover:

"State is what keeps the process connected."

"It can carry research notes, the draft, feedback, and errors."

"Without state, every step starts half-blind."

### Scene 5 - Loop And Cache

Purpose:

Show controlled recovery, plus caching as a small optimization.

Visual:

Check fails once. The route loops to Revise, then back to Check. Research flashes:

Cache hit

Research reused

On-screen text:

- Controlled loop
- Revise
- Re-check
- Cache hit
- Research reused

Voiceover:

"When something fails, the graph can loop."

"It can revise, re-check, and continue without losing the whole process."

"A graph can reduce avoidable errors by making verification a required step."

"Caching can cut cost by reusing unchanged work instead of paying for the same call again."

### Scene 6 - The Map

Purpose:

Land the thesis and optionally invite the build-along.

Visual:

The full graph assembles:

Research -> Draft -> Check -> Revise -> Check -> Publish

Then pull back to the title.

On-screen text:

- Nodes = work
- Edges = control
- State = context
- Smart agents follow a map

Optional CTA card:

Build this graph:

Research -> Draft -> Check -> Revise/Publish

Voiceover:

"So smart agents do not just need bigger prompts."

"They need a map: nodes for work, edges for control, and state for context."

"That is the graph behind smart AI agents."

"Optional CTA: I put three small assignments in the GitHub repo. Pick one, build it, and comment what you changed."

## GitHub Hook Status

Keep the GitHub hook as a draft, not locked.

Possible opening hook:

"I put three small assignments in the GitHub repo. Watch the concept, pick one assignment, and comment what you built."

Risk:

This may distract from the concept if placed too early.

Safer placement:

Use it as an end CTA unless the GitHub project is complete before publishing.

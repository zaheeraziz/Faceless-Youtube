# Scene 2 - A Prompt Is Not a Graph

Video title: The Graph Behind Smart AI Agents

Audience: technical AI learners

Target length: 10-12 seconds

Purpose: Explain why the Scene 1 failure happened. A large prompt can describe desired behavior, but it does not automatically create explicit control flow, state transitions, or verification routing.

## Concept Accuracy

This scene should distinguish prompting from graph-based workflow design.

Credibility-safe claim:

> A prompt can describe the task. A graph defines the execution path.

More technical version:

> In graph-based agent workflows, nodes represent steps, edges route execution, and state carries information between steps.

Avoid saying:

- Prompts are useless.
- A prompt cannot contain instructions for steps.
- Every reliable agent must use LangGraph.
- A graph guarantees correctness.

## Voiceover Draft

Line 1:
"A prompt can describe what you want."

Line 2:
"But a graph defines what runs next."

Line 3:
"Nodes do the work. Edges control the route. State carries the context."

## On-Screen Text

Use short technical labels:

- Prompt describes
- Graph executes
- Node
- Edge
- State

## Visual Beats

Beat 1:
The heavy prompt block from Scene 1 returns in the center. It contains vague instruction lines like:

- research
- write
- check
- publish

Beat 2:
The prompt block compresses into structured pieces. Lines detach and become separate nodes.

Beat 3:
Four nodes arrange into a graph:

Research -> Draft -> Check -> Publish

Beat 4:
Edges light up between nodes. A small "state packet" moves with the probe from node to node.

Beat 5:
Labels appear briefly:

- Node = step
- Edge = route
- State = memory/context

End frame:
Text appears: "Graph executes."

## Motion Direction

Feel like the viewer is watching a system assemble itself:

- Prompt block should not just disappear; it should transform.
- Nodes should snap into place with satisfying motion.
- Edges should draw themselves.
- State packet should travel visibly beside or behind the probe.
- Keep all key action inside the mobile-safe center area.

## Shape Language

- Prompt: large rectangle made of text-like bars.
- Nodes: bright circles or rounded squares.
- Edges: dotted or glowing lines.
- State: small cube or capsule carrying tiny data lines.
- Probe: same navigation probe from Scene 1.

## Accuracy Notes

For this video, "graph" means a workflow graph for an AI agent system.

Working definitions:

- Node: a function, model call, tool call, or step in the workflow.
- Edge: the routing rule that decides which node runs next.
- State: the shared data structure passed through the workflow.

This can be single-agent or multi-agent. Do not introduce multi-agent yet unless needed later.

## Transition To Scene 3

The graph route reaches the Check node and pauses.

Next scene idea:

"The important part is not the line. It is the decision."

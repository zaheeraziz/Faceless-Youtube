# Agent Graph Learning Brief Builder

Build a tiny graph-based workflow that turns a learning topic into a short video brief.

This is the companion project for:

The Graph Behind Smart AI Agents

## What It Teaches

- Node: one step in the workflow.
- Edge: where the workflow goes next.
- State: shared data passed between steps.
- Loop: controlled recovery after a failed check.
- Cache: reuse unchanged work instead of recomputing it.

## Base Graph

```text
Research -> Draft -> Check -> Revise/Export
```

## Run The Pure Python Version

```bash
python3 examples/python_functions.py
```

It does not call an LLM yet. That is intentional. First learn the graph shape.

## Sample Topics

- Astronomy navigation
- Graph-based AI agents
- City history and architecture

## Assignments

1. Add a `HumanReview` node after `Check`.
2. Add a `Cache Hit` path for unchanged `Research`.
3. Add a second `Check` node for factual/copyright risk.

## Not Production Ready

This is an educational project. It is designed to explain the graph pattern before adding real LLM calls, tests, or deployment.


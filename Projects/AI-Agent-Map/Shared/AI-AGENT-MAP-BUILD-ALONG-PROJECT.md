# Build-Along Project - The Graph Behind Smart AI Agents

Purpose: Pair the video with a small GitHub artifact that improves creator visibility and gives viewers something concrete to build.

## Project Idea

Build a tiny graph-based AI agent workflow:

Research -> Draft -> Check -> Revise/Publish

The project should teach the concept, not pretend to be a production agent framework.

## Learning Goals

- Understand node, edge, state, loop, and cache.
- See why a graph gives an agent controlled next steps.
- Practice turning an AI workflow idea into runnable structure.

## Suggested Repo Shape

```text
agent-graph-map/
  README.md
  examples/
    pseudocode.md
    python_functions.py
    langgraph_version.py
  diagrams/
    workflow.png
  prompts/
    research_prompt.md
    check_prompt.md
```

## Viewer Challenge

Build the base graph, then change one thing:

- Add a Human Review node.
- Add a Cache Hit for unchanged research.
- Add a second Check node for copyright/factual risk.
- Replace Publish with Export Video Brief.

## Video CTA

"I put a tiny version of this graph in GitHub. Build it, change one node, and share your version."

## Opening GitHub Hook Options - Draft

Status: keep these ideas in the script, but do not treat the hook as final yet.

Use one early hook when the video has a build-along project:

1. "I built a tiny version of this graph on GitHub. Watch the video, then build your own version and comment what you changed."

2. "This is not just a concept. There is a small GitHub project you can fork, modify, and share back in the comments."

3. "By the end, you should be able to build this graph yourself. The starter project is on GitHub."

4. "If you want to learn this properly, do not just watch. Fork the GitHub project, change one node, and post your version."

5. "I put three small assignments in the GitHub repo. Watch the concept, pick one assignment, and comment what you built."

Current leading draft, not locked:

"I put three small assignments in the GitHub repo. Watch the concept, pick one assignment, and comment what you built."

Why it works:

- Creates a clear action without overbuilding examples.
- Gives viewers a reason to open the GitHub project.
- Ties the video to a concrete GitHub artifact.
- Invites comments without begging for engagement.

## Three Assignments

1. Add a Human Review node after Check.

2. Add a Cache Hit path for unchanged Research.

3. Add a second Check node for factual/copyright risk.

## Guardrails

- Label as educational.
- Keep it small enough to finish in one sitting.
- Do not require paid tools for the basic version.
- Include a clear README before asking viewers to star or share.

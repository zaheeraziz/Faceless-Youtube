# Pseudocode

```text
state = {
  topic,
  audience,
  notes,
  draft,
  feedback,
  attempts,
  approved
}

research(state) -> state
draft(state) -> state
check(state) -> state

if approved:
  export(state)
else:
  revise(state)
  check(state)
```

Key idea:

The graph controls what runs next. The prompt only describes what a node should do.


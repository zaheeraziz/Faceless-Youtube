from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class State:
    topic: str
    audience: str
    notes: List[str] = field(default_factory=list)
    draft: str = ""
    feedback: List[str] = field(default_factory=list)
    attempts: int = 0
    approved: bool = False
    cache: Dict[str, List[str]] = field(default_factory=dict)


def research(state: State) -> State:
    cache_key = f"research:{state.topic}:{state.audience}"
    if cache_key in state.cache:
        state.notes = state.cache[cache_key]
        state.feedback.append("Cache hit: reused research notes.")
        return state

    state.notes = [
        f"Define the core idea of {state.topic}.",
        f"Explain why {state.topic} matters to {state.audience}.",
        "Use one simple example and one accuracy check.",
    ]
    state.cache[cache_key] = state.notes
    return state


def draft(state: State) -> State:
    state.draft = (
        f"Topic: {state.topic}\n"
        f"Audience: {state.audience}\n"
        "Hook: Show the problem in one sentence.\n"
        "Explain: Turn the concept into three simple steps.\n"
        "Visual: Use a graph route with nodes, edges, and state.\n"
        "Close: Give the viewer one small thing to build."
    )
    return state


def check(state: State) -> State:
    state.attempts += 1
    state.feedback.clear()

    if "accuracy check" not in " ".join(state.notes).lower():
        state.feedback.append("Missing accuracy check in notes.")

    if "Visual:" not in state.draft:
        state.feedback.append("Missing visual direction.")

    if state.attempts == 1:
        state.feedback.append("First pass: add stronger verification language.")

    state.approved = len(state.feedback) == 0
    return state


def revise(state: State) -> State:
    state.draft += "\nRevision: Make verification a required step before export."
    state.feedback.clear()
    return state


def export(state: State) -> State:
    print("FINAL LEARNING BRIEF")
    print("-" * 22)
    print(state.draft)
    print("\nNotes:")
    for note in state.notes:
        print(f"- {note}")
    return state


def run_graph(topic: str, audience: str) -> State:
    state = State(topic=topic, audience=audience)

    state = research(state)
    state = draft(state)
    state = check(state)

    while not state.approved and state.attempts < 3:
        state = revise(state)
        state = research(state)
        state = check(state)

    if state.approved:
        return export(state)

    raise RuntimeError(f"Brief failed check: {state.feedback}")


if __name__ == "__main__":
    run_graph(
        topic="Astronomy navigation",
        audience="curious beginners",
    )


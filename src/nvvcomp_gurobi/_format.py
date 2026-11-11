"""Competition witness representation shared by replay and executable output."""


def witness_text(witness: dict[str, list[float]]) -> str:
    assignments = [
        f"({prefix}_{i} {value:.17g})"
        for prefix, key in [("X", "inputs"), ("Y", "outputs")]
        for i, value in enumerate(witness[key])
    ]
    return "(" + "\n ".join(assignments) + ")\n"

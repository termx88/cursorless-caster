from contextlib import suppress
from typing import Any

from dragonfly import Compound, Repetition


BASE_TARGET: dict[str, Any] = {"type": "primitive"}
IMPLICIT_TARGET = {"type": "primitive", "isImplicit": True}


def get_modifier_repetition() -> Repetition:
    from .modifiers.modifiers import get_modifier_compound

    return Repetition(
        name="modifier_repetition",
        child=Compound(
            spec="<modifier>",
            name="modifier_repetition",
            extras=[
                get_modifier_compound(),
            ],
        ),
        min=1,
        # longest modifier list, that i've found is "its value tail"
        # so setting to 3 repetitions (max=4 means 4 won't be recognized)
        max=4,
    )


def get_primitive_target_compound() -> Compound:
    from .marks.mark import get_mark_compound
    from .modifiers.position import get_position_compound

    return Compound(
        spec="[<position>] (<modifier_repetition> [<mark>] | <mark>)",
        name="primitive_target",
        extras=[
            get_position_compound(),
            get_mark_compound(),
            get_modifier_repetition(),
        ],
        value_func=lambda node, extras: cursorless_primitive_target(extras),
    )


def cursorless_primitive_target(m) -> dict[str, Any]:
    """Supported extents for cursorless navigation"""
    result = BASE_TARGET.copy()

    position_list = []
    with suppress(KeyError):
        position_list.append(m["position"])

    modifier_list = []
    with suppress(KeyError):
        modifier_repetition = m["modifier_repetition"]
        for modifier in modifier_repetition:
            modifier_list.append(modifier)

    modifiers = [
        *position_list,
        *modifier_list,
    ]

    if modifiers:
        result["modifiers"] = modifiers

    with suppress(KeyError):
        result["mark"] = m["mark"]

    return result

from contextlib import suppress

from dragonfly import Compound

from ..cursorless_lists import get_list_ref

head_tail_modifiers = {
    "head": "extendThroughStartOf",
    "tail": "extendThroughEndOf",
}


def get_head_tail_modifier_compound() -> Compound:
    from .interior import get_interior_modifier_compound
    from .modifiers import get_head_tail_swallowed_modifier_compound

    return Compound(
        spec=(
            "<head_tail_modifier> "
            "[<interior_modifier>] "
            "[<head_tail_swallowed_modifier>]"
        ),
        name="head_tail_modifier",
        extras=[
            get_list_ref("head_tail_modifier"),
            get_interior_modifier_compound(),
            get_head_tail_swallowed_modifier_compound(),
        ],
        value_func=lambda node, extras: cursorless_head_tail_modifier(extras),
    )


def cursorless_head_tail_modifier(m) -> dict[str, str]:
    """Cursorless head and tail modifier"""
    modifiers = []

    with suppress(KeyError):
        modifiers.append(m["interior_modifier"])

    with suppress(KeyError):
        modifiers.append(m["head_tail_swallowed_modifier"])

    result = {
        "type": m["head_tail_modifier"],
    }

    if modifiers:
        result["modifiers"] = modifiers

    return result

from typing import Any

from dragonfly import Compound

from .cursorless_lists import get_list_ref
from .modifiers.position import construct_positional_modifier


def get_positional_target_compound() -> Compound:
    from .compound_targets import get_target_compound
    from .modifiers.position import get_position_compound

    return Compound(
        spec="(<position> | <source_destination_connective>) <target>",
        name="positional_target",
        extras=[
            get_position_compound(),
            get_list_ref("source_destination_connective"),
            get_target_compound(),
        ],
        value_func=lambda node, extras: cursorless_positional_target(extras),
    )


def cursorless_positional_target(m) -> dict[str, Any]:
    target: dict[str, Any] = m["target"]
    try:
        # talon uses "position" from list
        # but here this position is gotten from get_position_compound
        # so is already wrapped
        # modifier = construct_positional_modifier(m["position"])
        modifier = m["position"]
        return update_first_primitive_target(target, modifier)
    except KeyError:
        return target


def update_first_primitive_target(target: dict[str, Any], modifier: dict[str, Any]):
    if target["type"] == "primitive":
        if "modifiers" not in target:
            target["modifiers"] = []
        target["modifiers"].insert(0, modifier)
        return target
    elif target["type"] == "range":
        return {
            **target,
            "anchor": update_first_primitive_target(target["anchor"], modifier),
        }
    else:
        elements = target["elements"]
        return {
            **target,
            "elements": [
                update_first_primitive_target(elements[0], modifier),
                *elements[1:],
            ],
        }

from contextlib import suppress
from typing import Any

from dragonfly import Compound, Repetition

from .connective import default_range_connective
from .ruleref import get_ruleref
from .cursorless_lists import get_list_ref
from .primitive_target import BASE_TARGET


def get_range_connective_with_type_compound() -> Compound:
    from .modifiers.range_type import get_range_type_compound

    return Compound(
        spec="[<range_type>] <range_connective> | <range_type>",
        name="range_connective_with_type",
        extras=[
            get_range_type_compound(),
            get_list_ref("range_connective"),
        ],
        value_func=lambda node, extras: cursorless_range_connective_with_type(extras),
    )


def cursorless_range_connective_with_type(m) -> dict[str, Any]:
    connective = default_range_connective
    with suppress(KeyError):
        connective = m["range_connective"]

    range_type = None
    with suppress(KeyError):
        range_type = m["range_type"]

    return {
        "connective": connective,
        "type": range_type,
    }


def get_range_compound() -> Compound:
    from .primitive_target import get_primitive_target_compound

    return Compound(
        spec=(
            "<primitive_target1> | "
            "<range_connective_with_type> <primitive_target1> | "
            "<primitive_target1> <range_connective_with_type> <primitive_target2>"
        ),
        name="range",
        extras=[
            get_ruleref(get_primitive_target_compound(), "primitive_target1"),
            get_range_connective_with_type_compound(),
            get_ruleref(get_primitive_target_compound(), "primitive_target2"),
        ],
        value_func=lambda node, extras: cursorless_range(extras),
    )


def cursorless_range(m) -> dict[str, Any]:
    primitive_targets = [m["primitive_target1"]]
    with suppress(KeyError):
        primitive_targets.append(m["primitive_target2"])

    range_connective_with_type = {}
    try:
        range_connective_with_type = m["range_connective_with_type"]
    except KeyError:
        return primitive_targets[0]

    if len(primitive_targets) == 1:
        anchor = BASE_TARGET.copy()
    else:
        anchor = primitive_targets[0]

    range_connective = range_connective_with_type["connective"]
    range_type = range_connective_with_type["type"]

    range = {
        "type": "range",
        "anchor": anchor,
        "active": primitive_targets[-1],
        "excludeAnchor": not is_anchor_included(range_connective),
        "excludeActive": not is_active_included(range_connective),
    }

    if range_type:
        range["rangeType"] = range_type

    return range


def is_anchor_included(range_connective: str):
    return range_connective not in ["rangeExclusive", "rangeExcludingStart"]


def is_active_included(range_connective: str):
    return range_connective not in ["rangeExclusive", "rangeExcludingEnd"]


def get_range_repetition() -> Repetition:
    return Repetition(
        name="range_repetition",
        child=Compound(
            spec="<list_connective> <range>",
            name="range_repetition",
            extras=[
                get_list_ref("list_connective"),
                get_range_compound(),
            ],
        ),
        min=0,
        max=2,
    )


def get_target_compound() -> Compound:
    return Compound(
        spec="<range> [<range_repetition>]",
        name="target",
        extras=[
            get_range_compound(),
            get_range_repetition(),
        ],
        value_func=lambda node, extras: cursorless_target(extras),
    )


def cursorless_target(m) -> dict:
    ranges = [m["range"]]
    range_repetition = m["range_repetition"]
    for connective_range in range_repetition:
        range_dict = connective_range[1]
        ranges.append(range_dict)

    if len(ranges) == 1:
        return ranges[0]
    return {
        "type": "list",
        "elements": ranges,
    }

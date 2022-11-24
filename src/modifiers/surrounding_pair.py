from contextlib import suppress
from typing import Any

from dragonfly import Choice, Compound

from ..cursorless_lists import get_list_ref
from ..paired_delimiter import paired_delimiters_map


def get_surrounding_pair_scope_type_compound() -> Compound:
    from ..paired_delimiter import get_selectable_paired_delimiter_compound
    
    return Compound(
        spec="<selectable_paired_delimiter> | <surrounding_pair_scope_type>",
        name="surrounding_pair_scope_type",
        extras=[
            get_selectable_paired_delimiter_compound(),
            get_list_ref("surrounding_pair_scope_type"),
        ],
        value_func=lambda node, extras: cursorless_surrounding_pair_scope_type(extras),
    )


def cursorless_surrounding_pair_scope_type(m) -> str:
    """Surrounding pair scope type"""
    try:
        return m["surrounding_pair_scope_type"]
    except KeyError:
        return paired_delimiters_map[
            m["selectable_paired_delimiter"]
        ].cursorlessIdentifier


def get_surrounding_pair_compound() -> Compound:
    delimiter_force_directions = ["left", "right"]

    return Compound(
        spec="[<delimiter_force_direction>] <surrounding_pair_scope_type>",
        name="surrounding_pair",
        extras=[
            Choice("delimiter_force_direction", delimiter_force_directions),
            get_surrounding_pair_scope_type_compound(),
        ],
        value_func=lambda node, extras: cursorless_surrounding_pair(extras),
    )


def cursorless_surrounding_pair(m) -> dict[str, Any]:
    """Expand to containing surrounding pair"""
    surrounding_pair_scope_type = "any"
    with suppress(KeyError):
        surrounding_pair_scope_type = m["surrounding_pair_scope_type"]

    scope_type = {
        "type": "surroundingPair",
        "delimiter": surrounding_pair_scope_type,
    }

    with suppress(KeyError):
        scope_type["forceDirection"] = m["delimiter_force_direction"]

    return {
        "type": "containingScope",
        "scopeType": scope_type,
    }

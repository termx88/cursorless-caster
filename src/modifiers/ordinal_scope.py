from contextlib import suppress
from typing import Any

from dragonfly import Compound, ShortIntegerRef

from ..compound_targets import is_active_included, is_anchor_included
from ..ruleref import get_ruleref
from ..cursorless_lists import get_list_ref

first_modifiers = {"first": "first"}
last_modifiers = {"last": "last"}


def get_ordinal_or_last_compound() -> Compound:
    return Compound(
        spec="<ordinals_small> | [<ordinals_small>] <last_modifier>",
        name="ordinal_or_last",
        extras=[
            ShortIntegerRef("ordinals_small", 0, 10),
            get_list_ref("last_modifier"),
        ],
        value_func=lambda node, extras: ordinal_or_last(extras),
    )


def ordinal_or_last(m) -> int:
    """An ordinal or the word 'last'"""
    if m["_node"].words()[-1] == "last":
        number = 1
        with suppress(KeyError):
            number = m["ordinals_small"]
        return -number
    return m["ordinals_small"] - 1


def get_ordinal_range_compound() -> Compound:
    from .scopes import get_scope_type_compound

    return Compound(
        spec=(
            "<ordinal_or_last1>"
            "[<range_connective> <ordinal_or_last2>]"
            "<scope_type>"
        ),
        name="ordinal_range",
        extras=[
            get_ruleref(get_ordinal_or_last_compound(), "ordinal_or_last1"),
            get_list_ref("range_connective"),
            get_ruleref(get_ordinal_or_last_compound(), "ordinal_or_last2"),
            get_scope_type_compound(),
        ],
        value_func=lambda node, extras: cursorless_ordinal_range(extras),
    )


def cursorless_ordinal_range(m) -> dict[str, Any]:
    """Ordinal range"""
    ordinal_or_last_list = [m["ordinal_or_last1"]]
    with suppress(KeyError):
        ordinal_or_last_list.append(m["ordinal_or_last2"])
        
    anchor = create_ordinal_scope_modifier(
        m["scope_type"], ordinal_or_last_list[0]
    )
    if len(ordinal_or_last_list) > 1:
        active = create_ordinal_scope_modifier(
            m["scope_type"], ordinal_or_last_list[1]
        )
        include_anchor = is_anchor_included(m.cursorless_range_connective)
        include_active = is_active_included(m.cursorless_range_connective)
        return {
            "type": "range",
            "anchor": anchor,
            "active": active,
            "excludeAnchor": not include_anchor,
            "excludeActive": not include_active,
        }
    return anchor


def get_first_last_compound() -> Compound:
    from .scopes import get_scope_type_plural_compound

    return Compound(
        spec="(<first_modifier> | <last_modifier>) <number_small> <scope_type_plural>",
        name="first_last",
        extras=[
            get_list_ref("first_modifier"),
            get_list_ref("last_modifier"),
            ShortIntegerRef("number_small", 0, 10),
            get_scope_type_plural_compound(),
        ],
        value_func=lambda node, extras: cursorless_first_last(extras),
    )


def cursorless_first_last(m) -> dict[str, Any]:
    """First/last `n` scopes; eg "first three funk"""
    if m["_node"].words()[0] == "first":
        return create_ordinal_scope_modifier(
            m["scope_type_plural"], 0, m["number_small"]
        )
    return create_ordinal_scope_modifier(
        m["scope_type_plural"], -m["number_small"], m["number_small"]
    )


def get_ordinal_scope_compound() -> Compound:
    return Compound(
        spec="<ordinal_range> | <first_last>",
        name="ordinal_scope",
        extras=[
            get_ordinal_range_compound(),
            get_first_last_compound(),
        ],
        # returns exact
        # value_func=lambda node, extras: _func(extras),
    )


# def cursorless_ordinal_scope(m) -> dict[str, Any]:
#     """Ordinal ranges such as subwords or characters"""
#     return m[0]


def create_ordinal_scope_modifier(scope_type: dict, start: int, length: int = 1):
    return {
        "type": "ordinalScope",
        "scopeType": scope_type,
        "start": start,
        "length": length,
    }

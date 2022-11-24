from contextlib import suppress
from typing import Any

from dragonfly import Compound, ShortIntegerRef

from ..cursorless_lists import get_list_ref

previous_next_modifiers = {"previous": "previous", "next": "next"}
forward_backward_modifiers = {
    "forward": "forward",
    "backward": "backward",
}


def get_relative_direction_compound() -> Compound:
    return Compound(
        spec="<previous_next_modifier>",
        name="relative_direction",
        extras=[
            get_list_ref("previous_next_modifier"),
        ],
        value_func=lambda node, extras: cursorless_relative_direction(extras),
    )


def cursorless_relative_direction(m) -> str:
    """Previous/next"""
    return "backward" if m["_node"].words()[0] == "previous" else "forward"


def get_relative_scope_singular_compound() -> Compound:
    from .scopes import get_scope_type_compound

    return Compound(
        spec="[<ordinals_small>] <relative_direction> <scope_type>",
        name="relative_scope_singular",
        extras=[
            ShortIntegerRef("ordinals_small", 0, 10),
            get_relative_direction_compound(),
            get_scope_type_compound(),
        ],
        value_func=lambda node, extras: cursorless_relative_scope_singular(extras),
    )


def cursorless_relative_scope_singular(m) -> dict[str, Any]:
    """Relative previous/next singular scope, eg `"next funk"` or `"third next funk"`."""
    ordinals_small = 1
    with suppress(KeyError):
        ordinals_small = m["ordinals_small"]
    return create_relative_scope_modifier(
        m["scope_type"],
        ordinals_small,
        1,
        m["relative_direction"],
    )


def get_relative_scope_plural_compound() -> Compound:
    from .scopes import get_scope_type_plural_compound

    return Compound(
        spec="<relative_direction> <number_small> <scope_type_plural>",
        name="relative_scope_plural",
        extras=[
            get_relative_direction_compound(),
            ShortIntegerRef("number_small", 0, 10),
            get_scope_type_plural_compound(),
        ],
        value_func=lambda node, extras: cursorless_relative_scope_plural(extras),
    )


def cursorless_relative_scope_plural(m) -> dict[str, Any]:
    """Relative previous/next plural scope. `next three funks`"""
    return create_relative_scope_modifier(
        m["scope_type_plural"],
        1,
        m["number_small"],
        m["relative_direction"],
    )


def get_relative_scope_count_compound() -> Compound:
    from .scopes import get_scope_type_plural_compound

    return Compound(
        spec="<number_small> <scope_type_plural> [<forward_backward_modifier>]",
        name="relative_scope_count",
        extras=[
            ShortIntegerRef("number_small", 0, 10),
            get_scope_type_plural_compound(),
            get_list_ref("forward_backward_modifier"),
        ],
        value_func=lambda node, extras: cursorless_relative_scope_count(extras),
    )


def cursorless_relative_scope_count(m) -> dict[str, Any]:
    """Relative count scope. `three funks`"""
    forward_backward_modifier = "forward"
    with suppress(KeyError):
        forward_backward_modifier = m["forward_backward_modifier"]
    return create_relative_scope_modifier(
        m["scope_type_plural"],
        0,
        m["number_small"],
        forward_backward_modifier,
    )


def get_relative_scope_one_backward_compound() -> Compound:
    from .scopes import get_scope_type_compound

    return Compound(
        spec="<scope_type> <forward_backward_modifier>",
        name="relative_scope_one_backward",
        extras=[
            get_scope_type_compound(),
            get_list_ref("forward_backward_modifier"),
        ],
        value_func=lambda node, extras: cursorless_relative_scope_one_backward(extras),
    )


def cursorless_relative_scope_one_backward(m) -> dict[str, Any]:
    """Take scope backward, eg `funk backward`"""
    return create_relative_scope_modifier(
        m["scope_type"],
        0,
        1,
        m["forward_backward_modifier"],
    )


def get_relative_scope_compound() -> Compound:
    return Compound(
        spec=(
            "<relative_scope_singular> | "
            "<relative_scope_plural> | "
            "<relative_scope_count> | "
            "<relative_scope_one_backward>"
        ),
        name="relative_scope",
        extras=[
            get_relative_scope_singular_compound(),
            get_relative_scope_plural_compound(),
            get_relative_scope_count_compound(),
            get_relative_scope_one_backward_compound(),
        ],
        # return exact
        # value_func=lambda node, extras: cursorless_relative_scope(extras),
    )


# def cursorless_relative_scope(m) -> dict[str, Any]:
#     """Previous/next scope"""
#     return m["_node"].words()[0]


def create_relative_scope_modifier(
    scope_type: dict, offset: int, length: int, direction: str
) -> dict[str, Any]:
    return {
        "type": "relativeScope",
        "scopeType": scope_type,
        "offset": offset,
        "length": length,
        "direction": direction,
    }

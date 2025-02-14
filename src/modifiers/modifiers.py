from dragonfly import Compound

from ..csv_overrides import init_csv_and_watch_changes
from ..cursorless_lists import get_list_ref
from .head_tail import head_tail_modifiers
from .interior import interior_modifiers
from .ordinal_scope import first_modifiers, last_modifiers
from .range_type import range_types
from .relative_scope import forward_backward_modifiers, previous_next_modifiers
from .simple_scope_modifier import simple_scope_modifiers


# NOTE: Please do not change these dicts.  Use the CSVs for customization.
# See https://www.cursorless.org/docs/user/customization/
simple_modifiers = {
    "bounds": "excludeInterior",
    "just": "toRawSelection",
    "leading": "leading",
    "trailing": "trailing",
    "content": "keepContentFilter",
    "empty": "keepEmptyFilter",
    "its": "inferPreviousMark",
}


def get_simple_modifier_compound() -> Compound:
    return Compound(
        spec="<simple_modifier>",
        name="simple_modifier",
        extras=[
            get_list_ref("simple_modifier"),
        ],
        value_func=lambda node, extras: cursorless_simple_modifier(extras),
    )


def cursorless_simple_modifier(m) -> dict[str, str]:
    """Simple cursorless modifiers that only need to specify their type"""
    return {
        "type": m["simple_modifier"],
    }


# These are the modifiers that will be "swallowed" by the head/tail modifier.
# For example, saying "head funk" will result in a "head" modifier that will
# select past the start of the function.
# Note that we don't include "inside" here, because that requires slightly
# special treatment to ensure that "head inside round" swallows "inside round"
# rather than just "inside".
head_tail_swallowed_modifiers = [
    "<simple_modifier>",  # bounds, just, leading, trailing
    "<simple_scope_modifier>",  # funk, state, class, every funk
    "<ordinal_scope>",  # first past second word
    "<relative_scope>",  # next funk, 3 funks
    "<surrounding_pair>",  # matching/pair [curly, round]
]

modifiers = [
    "<interior_modifier>",  # inside
    "<head_tail_modifier>",  # head, tail
    *head_tail_swallowed_modifiers,
]


def get_modifier_compound() -> Compound:
    from .head_tail import get_head_tail_modifier_compound
    from .interior import get_interior_modifier_compound

    return Compound(
        spec=(
            "<interior_modifier> |"
            "<head_tail_modifier> |"
            "<head_tail_swallowed_modifier>"
        ),
        name="modifier",
        extras=[
            get_interior_modifier_compound(),
            get_head_tail_modifier_compound(),
            get_head_tail_swallowed_modifier_compound(),
	],
        # returns exact
        # value_func=lambda node, extras: cursorless_modifier(extras),
    )


# def cursorless_modifier(m) -> str:
#     """Cursorless modifier"""
#     return m[0]


def get_head_tail_swallowed_modifier_compound() -> Compound:
    from .ordinal_scope import get_ordinal_scope_compound
    from .relative_scope import get_relative_scope_compound
    from .simple_scope_modifier import get_simple_scope_modifier_compound
    from .surrounding_pair import get_surrounding_pair_compound

    return Compound(
        spec="|".join(head_tail_swallowed_modifiers),
        name="head_tail_swallowed_modifier",
        extras=[
            get_simple_modifier_compound(),
            get_simple_scope_modifier_compound(),
            get_ordinal_scope_compound(),
            get_relative_scope_compound(),
            get_surrounding_pair_compound(),
        ],
        # returns exact
        # value_func=lambda node, extras: cursorless_head_tail_swallowed_modifier(extras),
    )


# def cursorless_head_tail_swallowed_modifier(m) -> str:
#     """Cursorless modifier that is swallowed by the head/tail modifier, excluding interior, which requires special treatment"""
#     return m[0]


def on_ready():
    init_csv_and_watch_changes(
        "modifiers",
        {
            "simple_modifier": simple_modifiers,
            "interior_modifier": interior_modifiers,
            "head_tail_modifier": head_tail_modifiers,
            "range_type": range_types,
            "simple_scope_modifier": simple_scope_modifiers,
            "first_modifier": first_modifiers,
            "last_modifier": last_modifiers,
            "previous_next_modifier": previous_next_modifiers,
            "forward_backward_modifier": forward_backward_modifiers,
        },
    )

on_ready()

from dragonfly import Compound

from ..cursorless_lists import get_list_ref

# NOTE: Please do not change these dicts.  Use the CSVs for customization.
# See https://www.cursorless.org/docs/user/customization/
interior_modifiers = {
    "inside": "interiorOnly",
}


def get_interior_modifier_compound() -> Compound:
    return Compound(
        spec="<interior_modifier>",
        name="interior_modifier",
        extras=[
            get_list_ref("interior_modifier"),
        ],
        value_func=lambda node, extras: cursorless_interior_modifier(extras),
    )


def cursorless_interior_modifier(m) -> dict[str, str]:
    """Cursorless interior modifier"""
    return {
        "type": m["interior_modifier"],
    }

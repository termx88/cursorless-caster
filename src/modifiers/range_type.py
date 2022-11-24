from dataclasses import dataclass

from dragonfly import Compound

from ..cursorless_lists import get_list_ref


@dataclass
class RangeType:
    defaultSpokenForm: str
    cursorlessIdentifier: str
    type: str


# NOTE: Please do not change these dicts.  Use the CSVs for customization.
# See https://www.cursorless.org/docs/user/customization/
range_type_list = [
    RangeType("slice", "verticalRange", "vertical"),
]

range_type_map = {t.cursorlessIdentifier: t.type for t in range_type_list}
range_types = {t.defaultSpokenForm: t.cursorlessIdentifier for t in range_type_list}


def get_range_type_compound() -> Compound:
    return Compound(
        spec="<range_type>",
        name="range_type",
        extras=[
            get_list_ref("range_type"),
        ],
        value_func=lambda node, extras: cursorless_range_type(extras),
    )


def cursorless_range_type(m) -> str:
    """Range type modifier"""
    return range_type_map[m["range_type"]]

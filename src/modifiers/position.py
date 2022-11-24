from typing import Any

from dragonfly import Compound

from ..csv_overrides import init_csv_and_watch_changes
from ..cursorless_lists import get_list_ref

# NOTE: Please do not change these dicts.  Use the CSVs for customization.
# See https://www.cursorless.org/docs/user/customization/
positions = {
    "start of": "start",
    "end of": "end",
    "before": "before",
    "after": "after",
}


def construct_positional_modifier(position: str) -> dict[str, Any]:
    return {"type": "position", "position": position}


def get_position_compound() -> Compound:
    return Compound(
        spec="<position>",
        name="position",
        extras=[
            get_list_ref("position"),
        ],
        value_func=lambda node, extras: cursorless_position(extras),
    )


# Note that we allow positional connectives such as "before" and "after" to appear
# as modifiers. We may disallow this in the future.
def cursorless_position(m) -> dict[str, Any]:
    return construct_positional_modifier(m["position"])


def on_ready():
    init_csv_and_watch_changes(
        "positions",
        {"position": positions},
    )


on_ready()

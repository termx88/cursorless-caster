from contextlib import suppress

from dragonfly import Compound

from ..ruleref import get_ruleref
from ..cursorless_lists import get_list_ref
from ..primitive_target import BASE_TARGET


def get_swap_targets_compound() -> Compound:
    from ..compound_targets import get_target_compound

    return Compound(
        spec="[<target1>] <swap_connective> <target2>",
        name="swap_targets",
        extras=[
            get_ruleref(get_target_compound(), "target1"),
            get_list_ref("swap_connective"),
            get_ruleref(get_target_compound(), "target2"),
        ],
        value_func=lambda node, extras: cursorless_swap_targets(extras),
    )


def cursorless_swap_targets(m) -> list[dict]:
    target_list = [m["target2"]]
    with suppress(KeyError):
        target_list.append(m["target1"])

    if len(target_list) == 1:
        target_list = [BASE_TARGET] + target_list

    return target_list

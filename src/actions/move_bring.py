from dragonfly import Compound

from ..primitive_target import IMPLICIT_TARGET


def get_move_bring_targets_compound() -> Compound:
    from ..compound_targets import get_target_compound
    from ..positional_target import get_positional_target_compound

    return Compound(
        spec="<target> [<positional_target>]",
        name="move_bring_targets",
        extras=[
            get_target_compound(),
            get_positional_target_compound(),
        ],
        value_func=lambda node, extras: cursorless_move_bring_targets(extras),
    )


def cursorless_move_bring_targets(m) -> list[dict]:
    target_list = [m["target"]]

    try:
        target_list += [m["positional_target"]]
    except KeyError:
        target_list += [IMPLICIT_TARGET.copy()]

    return target_list

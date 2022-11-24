from dataclasses import dataclass
from typing import Literal

from dragonfly import Compound

from ..command import Actions as command_actions
from ..cursorless_lists import get_list_ref
from ..paired_delimiter import paired_delimiters_map


@dataclass
class Wrapper:
    type: Literal["pairedDelimiter", "snippet"]
    extra_args: list[str]


def get_wrapper_compound() -> Compound:
    from ..paired_delimiter import get_wrapper_paired_delimiter_compound

    return Compound(
        spec="<wrapper_paired_delimiter> | <wrapper_snippet>",
        name="wrapper",
        extras=[
            get_wrapper_paired_delimiter_compound(),
            get_list_ref("wrapper_snippet"),
        ],
        value_func=lambda node, extras: cursorless_wrapper(extras),
    )


def cursorless_wrapper(m) -> Wrapper:
    try:
        paired_delimiter_info = paired_delimiters_map[
            m["wrapper_paired_delimiter"]
        ]
        return Wrapper(
            type="pairedDelimiter",
            extra_args=[paired_delimiter_info.left, paired_delimiter_info.right],
        )
    except KeyError:
        return Wrapper(type="snippet", extra_args=[m["wrapper_snippet"]])


# Maps from (action_type, wrapper_type) to action name
action_map: dict[tuple[str, Literal["pairedDelimiter", "snippet"]], str] = {
    ("wrapWithPairedDelimiter", "pairedDelimiter"): "wrapWithPairedDelimiter",
    # This is awkward because we used an action name which was to verbose previously
    ("wrapWithPairedDelimiter", "snippet"): "wrapWithSnippet",
    ("rewrap", "pairedDelimiter"): "rewrapWithPairedDelimiter",
    # Not yet supported
    ("rewrap", "snippet"): "rewrapWithSnippet",
}


class Actions:
    def cursorless_wrap(action_type: str, targets: dict, cursorless_wrapper: Wrapper):
        """Perform cursorless wrap action"""
        wrapper_type = cursorless_wrapper.type
        action = action_map[(action_type, wrapper_type)]

        command_actions.cursorless_single_target_command_with_arg_list(
            action, targets, cursorless_wrapper.extra_args
        )

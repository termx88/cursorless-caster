from typing import Any

from .command_client.command_client import Actions as client_actions
from .cursorless_command_server import (
    run_rpc_command_and_wait,
    run_rpc_command_get,
    run_rpc_command_no_wait,
)
from .primitive_target import IMPLICIT_TARGET

CURSORLESS_COMMAND_ID = "cursorless.command"


class NotSet:
    def __repr__(self):
        return "<argument not set>"


class Actions:
    def cursorless_single_target_command(
        action: str,
        target: dict,
        arg1: Any = NotSet,
        arg2: Any = NotSet,
        arg3: Any = NotSet,
    ):
        """Execute single-target cursorless command"""
        Actions.cursorless_multiple_target_command(
            action, [target], arg1, arg2, arg3
        )

    def cursorless_single_target_command_no_wait(
        action: str,
        target: dict,
        arg1: Any = NotSet,
        arg2: Any = NotSet,
        arg3: Any = NotSet,
    ):
        """Execute single-target cursorless command"""
        Actions.cursorless_multiple_target_command_no_wait(
            action, [target], arg1, arg2, arg3
        )

    def cursorless_single_target_command_with_arg_list(
        action: str, target: dict, args: list[Any]
    ):
        """Execute single-target cursorless command with argument list"""
        Actions.cursorless_single_target_command(
            action,
            target,
            *args,
        )

    def cursorless_single_target_command_get(
        action: str,
        target: dict,
        arg1: Any = NotSet,
        arg2: Any = NotSet,
        arg3: Any = NotSet,
    ):
        """Execute single-target cursorless command and return result"""
        return run_rpc_command_get(
            CURSORLESS_COMMAND_ID,
            construct_cursorless_command_argument(
                action=action,
                targets=[target],
                args=[x for x in [arg1, arg2, arg3] if x is not NotSet],
            ),
        )

    def cursorless_implicit_target_command(
        action: str,
        arg1: Any = NotSet,
        arg2: Any = NotSet,
        arg3: Any = NotSet,
    ):
        """Execute cursorless command with implicit target"""
        Actions.cursorless_single_target_command(
            action, IMPLICIT_TARGET, arg1, arg2, arg3
        )

    def cursorless_multiple_target_command(
        action: str,
        targets: list[dict],
        arg1: Any = NotSet,
        arg2: Any = NotSet,
        arg3: Any = NotSet,
    ):
        """Execute multi-target cursorless command"""
        run_rpc_command_and_wait(
            CURSORLESS_COMMAND_ID,
            construct_cursorless_command_argument(
                action=action,
                targets=targets,
                args=[x for x in [arg1, arg2, arg3] if x is not NotSet],
            ),
        )

    def cursorless_multiple_target_command_no_wait(
        action: str,
        targets: list[dict],
        arg1: Any = NotSet,
        arg2: Any = NotSet,
        arg3: Any = NotSet,
    ):
        """Execute multi-target cursorless command"""
        run_rpc_command_no_wait(
            CURSORLESS_COMMAND_ID,
            construct_cursorless_command_argument(
                action=action,
                targets=targets,
                args=[x for x in [arg1, arg2, arg3] if x is not NotSet],
            ),
        )


def construct_cursorless_command_argument(
    action: str, targets: list[dict], args: list[Any]
):
    try:
        use_pre_phrase_snapshot = client_actions.did_emit_pre_phrase_signal()
    except KeyError:
        use_pre_phrase_snapshot = False

    return {
        "version": 3,
        "spokenForm": get_spoken_form(),
        "action": {
            "name": action,
            "args": args,
        },
        "targets": targets,
        "usePrePhraseSnapshot": use_pre_phrase_snapshot,
    }


def get_spoken_form():
    # too minor to do properly
    return "spoken form"
    # return " ".join(last_phrase["phrase"])

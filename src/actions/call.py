from ..command import Actions as command_actions
from ..primitive_target import IMPLICIT_TARGET


def run_call_action(target: dict):
    targets = [target, IMPLICIT_TARGET.copy()]
    command_actions.cursorless_multiple_target_command("callAsFunction", targets)

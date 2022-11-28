from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.state.short import R
from dragonfly import Function, MappingRule

from .actions.actions import (
    Actions as action_actions,
    get_action_or_ide_command_compound,
)

from .compound_targets import get_target_compound

class Cursorless(MappingRule):
    mapping = {
        "<action_or_ide_command> <target>":
            R(Function(
                lambda action_or_ide_command, target:
                    action_actions.cursorless_action_or_ide_command(
                        action_or_ide_command, target
                    )
            )),
    }
    extras = [
        get_action_or_ide_command_compound(),
        get_target_compound(),
    ]

def get_rule():
    details = RuleDetails(
        name="cursor less",
        executable=["code", "VSCodium"],
        title=["Visual Studio Code", "VSCodium"],
    )
    return Cursorless, details

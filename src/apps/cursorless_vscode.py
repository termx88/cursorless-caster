from dragonfly import Pause, Text

from ..actions.get_text import get_text
from ..cursorless_command_server import run_rpc_command_no_wait


class Actions:
    def cursorless_private_run_find_action(targets: dict):
        """Find text of targets in editor"""
        texts = get_text(targets, ensure_single_target=True)
        search_text = texts[0]
        if len(search_text) > 200:
            search_text = search_text[:200]
            print("Search text is longer than 200 characters; truncating")
        run_rpc_command_no_wait("actions.find")
        Pause("5").execute()
        Text(search_text).execute()

    def cursorless_show_settings_in_ide():
        """Show Cursorless-specific settings in ide"""
        run_rpc_command_no_wait("workbench.action.openGlobalSettings")
        Pause("25").execute()
        Text("cursorless").execute()

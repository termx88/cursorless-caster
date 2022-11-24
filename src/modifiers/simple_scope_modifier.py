from typing import Any

from dragonfly import Compound

from ..cursorless_lists import get_list_ref

simple_scope_modifiers = {"every": "every"}


def get_simple_scope_modifier_compound() -> Compound:
    from .scopes import get_scope_type_compound

    return Compound(
        spec="[every] <scope_type>",
        name="simple_scope_modifier",
        extras=[
            get_list_ref("simple_scope_modifier"),
            get_scope_type_compound(),
        ],
        value_func=lambda node, extras: cursorless_simple_scope_modifier(extras),
    )


def cursorless_simple_scope_modifier(m) -> dict[str, Any]:
    """Containing scope, every scope, etc"""
    return {
        "type": "everyScope" if m["_node"].words()[0] == "every" else "containingScope",
        "scopeType": m["scope_type"],
    }

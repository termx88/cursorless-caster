import re
from castervoice.lib.textformat import TextFormat 

from ..cheatsheet.get_list import de_camel
from .get_text import get_text
from .replace import Actions as replace_actions 

class Actions:
    def cursorless_reformat(targets: dict, capitalization: int, spacing: int):
        """Reformat targets with formatter"""
        texts = get_text(targets, show_decorations=False)
        capitalization, spacing = TextFormat.normalize_text_format(capitalization, spacing)
        updated_texts = list(
            map(lambda text: reformat_text(text, capitalization, spacing), texts)
        )
        replace_actions.cursorless_replace(targets, updated_texts)

def reformat_text(text: str, capitalization: int, spacing: int) -> str:
    text = unformat_text(text)
    return TextFormat.formatted_text(capitalization, spacing, text)

def unformat_text(text: str) -> str:
    unformatted = re.sub(r"[\W_]+", " ", text)
    unformatted = de_camel(unformatted)
    return unformatted

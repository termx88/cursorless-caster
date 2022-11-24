from dragonfly import Choice, Compound, ShortIntegerRef

try:  # Try first loading from caster user directory
    from caster_user_content.rules.alphabet_rules import alphabet_support
except ImportError:
    from castervoice.rules.core.alphabet_rules import alphabet_support
try:  # Try first loading from caster user directory
    from caster_user_content.rules.punctuation_rules.punctuation_support import (
        text_punc_dict,
    )
except ImportError:
    from castervoice.rules.core.punctuation_rules.punctuation_support import (
        text_punc_dict,
    )


def get_any_alphanumeric_key_compound() -> Compound:
    # used to make number output as string, rather than int
    number_key_compound = Compound(
        spec="<number_key>",
        name="number_key",
        extras=[
            ShortIntegerRef("number_key", 0, 10),
        ],
        value_func=lambda node, extras: str(extras["number_key"]),
    )

    symbol_keys = text_punc_dict()

    return Compound(
        spec="<letter> | <number_key> | <symbol_key>",
        name="any_alphanumeric_key",
        extras=[
            alphabet_support.get_alphabet_choice("letter"),
            number_key_compound,
            Choice("symbol_key", symbol_keys),
        ],
        # returns exact and no corresponding function in cursorless
    )

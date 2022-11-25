from dragonfly import Compound

from .command import Actions as command_actions
from .csv_overrides import init_csv_and_watch_changes
from .cursorless_lists import get_list_ref


def get_insertion_snippet_compound() -> Compound:
    return Compound(
        spec="<insertion_snippet_no_phrase> | <insertion_snippet_single_phrase>",
        name="insertion_snippet",
        extras=[
            get_list_ref("insertion_snippet_no_phrase"),
            get_list_ref("insertion_snippet_single_phrase"),
        ],
        value_func=lambda node, extras: cursorless_insertion_snippet(extras),
    )

def cursorless_insertion_snippet(m) -> str:
    try:
        return m["insertion_snippet_no_phrase"]
    except KeyError:
        pass

    return m["cursorless_insertion_snippet_single_phrase"].split(".")[0]


# NOTE: Please do not change these dicts.  Use the CSVs for customization.
# See https://www.cursorless.org/docs/user/customization/
wrapper_snippets = {
    "else": "ifElseStatement.alternative",
    "funk": "functionDeclaration.body",
    "if else": "ifElseStatement.consequence",
    "if": "ifStatement.consequence",
    "try": "tryCatchStatement.body",
    "link": "link.text",
}

# NOTE: Please do not change these dicts.  Use the CSVs for customization.
# See https://www.cursorless.org/docs/user/customization/
insertion_snippets_no_phrase = {
    "if": "ifStatement",
    "if else": "ifElseStatement",
    "try": "tryCatchStatement",
}

# NOTE: Please do not change these dicts.  Use the CSVs for customization.
# See https://www.cursorless.org/docs/user/customization/
insertion_snippets_single_phrase = {
    "funk": "functionDeclaration.name",
    "link": "link.text",
}

phrase_terminators = {"over": "phraseTerminator"}


class Actions:
    def cursorless_insert_snippet_with_phrase(
        action: str, snippet_description: str, text: str
    ):
        """Perform cursorless wrap action"""
        snippet_name, snippet_variable = snippet_description.split(".")
        command_actions.cursorless_implicit_target_command(
            action, snippet_name, {snippet_variable: text.format()}
        )


def on_ready():
    init_csv_and_watch_changes(
        "experimental/wrapper_snippets",
        {
            "wrapper_snippet": wrapper_snippets,
        },
        allow_unknown_values=True,
        default_list_name="wrapper_snippet",
    )
    init_csv_and_watch_changes(
        "experimental/insertion_snippets",
        {
            "insertion_snippet_no_phrase": insertion_snippets_no_phrase,
        },
        allow_unknown_values=True,
        default_list_name="insertion_snippet_no_phrase",
    )
    init_csv_and_watch_changes(
        "experimental/insertion_snippets_single_phrase",
        {
            "insertion_snippet_single_phrase": insertion_snippets_single_phrase,
        },
        allow_unknown_values=True,
        default_list_name="insertion_snippet_single_phrase",
    )
    init_csv_and_watch_changes(
        "experimental/miscellaneous",
        {
            "phrase_terminator": phrase_terminators,
        },
    )


on_ready()

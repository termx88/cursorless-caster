from dragonfly import Compound

from ..csv_overrides import SPOKEN_FORM_HEADER, init_csv_and_watch_changes
from ..cursorless_lists import get_list_ref

# NOTE: Please do not change these dicts.  Use the CSVs for customization.
# See https://www.cursorless.org/docs/user/customization/
scope_types = {
    "arg": "argumentOrParameter",
    "attribute": "attribute",
    "call": "functionCall",
    "callee": "functionCallee",
    "class name": "className",
    "class": "class",
    "comment": "comment",
    "funk name": "functionName",
    "funk": "namedFunction",
    "if state": "ifStatement",
    "item": "collectionItem",
    "key": "collectionKey",
    "lambda": "anonymousFunction",
    "list": "list",
    "map": "map",
    "name": "name",
    "regex": "regularExpression",
    "section": "section",
    "-one section": "sectionLevelOne",
    "-two section": "sectionLevelTwo",
    "-three section": "sectionLevelThree",
    "-four section": "sectionLevelFour",
    "-five section": "sectionLevelFive",
    "-six section": "sectionLevelSix",
    "selector": "selector",
    "state": "statement",
    "string": "string",
    "type": "type",
    "value": "value",
    "condition": "condition",
    "unit": "unit",
    #  XML, JSX
    "element": "xmlElement",
    "tags": "xmlBothTags",
    "start tag": "xmlStartTag",
    "end tag": "xmlEndTag",
    # Text-based scope types
    "char": "character",
    "word": "word",
    "identifier": "identifier",
    "block": "paragraph",
    "cell": "notebookCell",
    "file": "document",
    "line": "line",
    "paint": "nonWhitespaceSequence",
    "short paint": "boundedNonWhitespaceSequence",
    "link": "url",
    "token": "token",
    # LaTeX
    "part": "part",
    "chapter": "chapter",
    "subsection": "subSection",
    "subsubsection": "subSubSection",
    "paragraph": "namedParagraph",
    "subparagraph": "subParagraph",
    "environment": "environment",
}


def get_scope_type_compound() -> Compound:
    return Compound(
        spec="<scope_type> | <custom_regex_scope_type>",
        name="scope_type",
        extras=[
                get_list_ref("scope_type"),
                get_list_ref("custom_regex_scope_type")
            ],
        value_func=lambda node, extras: cursorless_scope_type(extras),
    )


def cursorless_scope_type(m) -> dict[str, str]:
    """Cursorless scope type singular"""
    try:
        return {"type": m["scope_type"]}
    except KeyError:
        return {"type": "customRegex", "regex": m["custom_regex_scope_type"]}


def get_scope_type_plural_compound() -> Compound:
    return Compound(
        spec="<scope_type_plural> | <custom_regex_scope_type_plural>",
        name="scope_type_plural",
        extras=[
            get_list_ref("scope_type_plural"),
            get_list_ref("custom_regex_scope_type_plural"),
        ],
        value_func=lambda node, extras: cursorless_scope_type_plural(extras),
    )


def cursorless_scope_type_plural(m) -> dict[str, str]:
    """Cursorless scope type plural"""
    try:
        return {"type": m["scope_type_plural"]}
    except KeyError:
        return {
            "type": "customRegex",
            "regex": m["custom_regex_scope_type_plural"],
        }


# NOTE: Please do not change these dicts.  Use the CSVs for customization.
# See https://www.cursorless.org/docs/user/customization/
# NB: This is a hack until we support having inside and outside on arbitrary
# scope types
surrounding_pair_scope_types = {
    "string": "string",
}


def on_ready():
    init_csv_and_watch_changes(
        "modifier_scope_types",
        {
            "scope_type": scope_types,
            "surrounding_pair_scope_type": surrounding_pair_scope_types,
        },
        pluralize_lists=["scope_type"],
    )
    init_csv_and_watch_changes(
        "experimental/regex_scope_types",
        {},
        headers=[SPOKEN_FORM_HEADER, "Regex"],
        allow_unknown_values=True,
        default_list_name="custom_regex_scope_type",
        pluralize_lists=["custom_regex_scope_type"],
    )

on_ready()

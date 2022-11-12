<<<<<<< HEAD:src/modifiers/scopes.py
=======
from typing import Any

>>>>>>> 9162137b7b93ff1450ed8be4b41bc47737eb3283:src/modifiers/containing_scope.py
from ..csv_overrides import SPOKEN_FORM_HEADER, init_csv_and_watch_changes

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


def cursorless_scope_type(m) -> dict[str, str]:
    """Cursorless scope type singular"""
    try:
        return {"type": m["scope_type"]}
    except KeyError:
        return {"type": "customRegex", "regex": m["custom_regex_scope_type"]}


<<<<<<< HEAD:src/modifiers/scopes.py
def cursorless_scope_type_plural(m) -> dict[str, str]:
    """Cursorless scope type plural"""
    try:
        return {"type": m["scope_type_plural"]}
    except AttributeError:
        return {
            "type": "customRegex",
            "regex": m.["custom_regex_scope_type_plural"],
        }
=======
def cursorless_containing_scope(m) -> dict[str, Any]:
    """Expand to containing scope"""
    return {
        "type": "everyScope" if "every" in m["_node"].words() else "containingScope",
        "scopeType": m["scope_type"],
    }
>>>>>>> 9162137b7b93ff1450ed8be4b41bc47737eb3283:src/modifiers/containing_scope.py


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

<<<<<<< HEAD:src/modifiers/scopes.py
on_ready()
=======
on_ready()
>>>>>>> 9162137b7b93ff1450ed8be4b41bc47737eb3283:src/modifiers/containing_scope.py

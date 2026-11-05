"""Minimal, string-aware JSONC preprocessing.

Strips ``//`` and ``/* */`` comments and trailing commas so that JSONC (and the
subset of JSON5 that only uses those features) can be parsed by the standard
library :mod:`json`. Full JSON5 (single-quoted strings, unquoted keys, hex
numbers, etc.) is *not* handled here and requires the optional ``json5``
dependency.
"""

from __future__ import annotations

_WHITESPACE = " \t\r\n"


def _copy_string(text: str, i: int, out: list[str]) -> int:
    """Copy a double-quoted string verbatim, returning the index after it."""
    length = len(text)
    out.append(text[i])  # opening quote
    i += 1
    while i < length:
        char = text[i]
        out.append(char)
        if char == "\\" and i + 1 < length:
            # Copy the escaped character so an escaped quote does not
            # prematurely close the string.
            out.append(text[i + 1])
            i += 2
        elif char == '"':
            i += 1
            break
        else:
            i += 1
    return i


def _skip_line_comment(text: str, i: int) -> int:
    """Skip a ``// ...`` comment, returning the index of the line ending."""
    i += 2
    length = len(text)
    while i < length and text[i] not in "\r\n":
        i += 1
    return i


def _skip_block_comment(text: str, i: int) -> int:
    """Skip a ``/* ... */`` comment, returning the index after it."""
    i += 2
    length = len(text)
    while i + 1 < length and not (text[i] == "*" and text[i + 1] == "/"):
        i += 1
    return i + 2  # Past the end is harmless; the caller re-checks bounds.


def _drop_trailing_comma(out: list[str]) -> None:
    """Remove a trailing comma before a closing bracket, ignoring whitespace."""
    last = len(out) - 1
    while last >= 0 and out[last] in _WHITESPACE:
        last -= 1
    if last >= 0 and out[last] == ",":
        del out[last]


def strip_jsonc(text: str) -> str:
    """Remove comments and trailing commas from JSONC ``text``.

    The scan is string-aware: characters inside double-quoted strings (and their
    backslash escapes) are copied verbatim, so comment markers or commas that
    appear inside string values are left untouched. The function is total and
    never raises; validating the result is left to the caller's ``json.loads``.
    """
    out: list[str] = []
    i = 0
    length = len(text)

    while i < length:
        char = text[i]
        if char == '"':
            i = _copy_string(text, i, out)
        elif char == "/" and text.startswith("//", i):
            i = _skip_line_comment(text, i)
        elif char == "/" and text.startswith("/*", i):
            i = _skip_block_comment(text, i)
        elif char in "}]":
            _drop_trailing_comma(out)
            out.append(char)
            i += 1
        else:
            out.append(char)
            i += 1

    return "".join(out)

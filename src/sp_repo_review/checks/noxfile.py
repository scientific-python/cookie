# NOX: Noxfile checks
## NOXxxx: noxfile checks

from __future__ import annotations

import ast
import dataclasses
import re
from typing import Any

from .._compat import tomllib
from .._compat.importlib.resources.abc import Traversable
from . import mk_url

REGEX = re.compile(
    r"(?m)^# /// (?P<type>[a-zA-Z0-9-]+)$\s(?P<content>(^#(| .*)$\s)+)^# ///$"
)


@dataclasses.dataclass(frozen=True, kw_only=True, slots=True, eq=False)
class NoxfileInfo:
    module: ast.Module
    shebang: str
    script: dict[str, Any]

    __hash__ = None  # type: ignore[assignment]

    @classmethod
    def from_str(cls, content: str) -> NoxfileInfo:
        module = ast.parse(content, filename="noxfile.py")
        shebang_match = re.match(r"^#!.*\n", content)
        shebang = shebang_match.group(0).strip() if shebang_match else ""
        script = _load_script_block(content)
        return cls(module=module, shebang=shebang, script=script)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, NoxfileInfo):
            return NotImplemented

        ast_equal = ast.dump(self.module, include_attributes=True) == ast.dump(
            other.module, include_attributes=True
        )
        return (
            self.shebang == other.shebang and self.script == other.script and ast_equal
        )


def _load_script_block(content: str, /) -> dict[str, Any]:
    name = "script"
    matches = list(filter(lambda m: m.group("type") == name, REGEX.finditer(content)))

    if not matches:
        return {}

    if len(matches) > 1:
        msg = f"Multiple {name} blocks found"
        raise ValueError(msg)

    content = "".join(
        line[2:] if line.startswith("# ") else line[1:]
        for line in matches[0].group("content").splitlines(keepends=True)
    )
    return tomllib.loads(content)


def noxfile(root: Traversable) -> NoxfileInfo | None:
    """
    Returns the shabang line (or empty string if missing), the noxfile script block, and the AST of the noxfile.py.
    Returns None if noxfile.py is not present.
    """

    noxfile_path = root.joinpath("noxfile.py")
    if not noxfile_path.is_file():
        return None

    with noxfile_path.open("r", encoding="utf-8") as f:
        return NoxfileInfo.from_str(f.read())


class Noxfile:
    family = "noxfile"
    requires = {"PY007"}
    url = mk_url("tasks")


class NOX101(Noxfile):
    "Sets minimum nox version"

    @staticmethod
    def check(noxfile: NoxfileInfo | None) -> bool | None:
        """Set a minimum nox version:

        ```python
        nox.needs_version = "2025.10.14"
        ```
        """

        if noxfile is None:
            return None

        for statement in noxfile.module.body:
            if isinstance(statement, ast.Assign):
                for target in statement.targets:
                    match target:
                        case ast.Attribute(
                            value=ast.Name(id="nox"), attr="needs_version"
                        ):
                            return True

        return False


class NOX102(Noxfile):
    "Sets venv backend"

    @staticmethod
    def check(noxfile: NoxfileInfo | None | None) -> bool | None:
        """
        The default venv backend should be set, ideally to `uv|virtualenv`:

        ```python
        nox.options.default_venv_backend = "uv|virtualenv"
        ```
        """
        if noxfile is None:
            return None

        for statement in noxfile.module.body:
            if isinstance(statement, ast.Assign):
                for target in statement.targets:
                    match target:
                        case ast.Attribute(
                            value=ast.Attribute(
                                value=ast.Name(id="nox"), attr="options"
                            ),
                            attr="default_venv_backend",
                        ):
                            return True

        return False


class NOX103(Noxfile):
    "Set default per session instead of session list"

    @staticmethod
    def check(noxfile: NoxfileInfo | None) -> bool | None:
        """
        You should use `default=` in each session instead of setting a global list.
        """
        if noxfile is None:
            return None

        for statement in noxfile.module.body:
            if isinstance(statement, ast.Assign):
                for target in statement.targets:
                    match target:
                        case ast.Attribute(
                            value=ast.Attribute(
                                value=ast.Name(id="nox"), attr="options"
                            ),
                            attr="sessions",
                        ):
                            return False

        return True


class NOX201(Noxfile):
    "Set a script block with dependencies in your noxfile"

    @staticmethod
    def check(noxfile: NoxfileInfo | None) -> bool | None:
        """
        You should have a script block with nox in it, for example:

        ```toml
        # /// script
        dependencies = ["nox"]
        # ///
        ```
        """
        if noxfile is None:
            return None
        match noxfile.script:
            case {"dependencies": list()}:
                return True
        return False


class NOX202(Noxfile):
    "Has a shebang line"

    @staticmethod
    def check(noxfile: NoxfileInfo | None) -> bool | None:
        """
        You should have a shabang line at the top of your noxfile.py, for example:

        ```python
        #!/usr/bin/env -S uv run --script
        ```
        """
        if noxfile is None:
            return None
        return bool(noxfile.shebang)


class NOX203(Noxfile):
    "Provide a main block to run nox"

    @staticmethod
    def check(noxfile: NoxfileInfo | None) -> bool | None:
        """
        You should have a main block at the bottom of your noxfile.py, for example:

        ```python
        if __name__ == "__main__":
            nox.main()
        ```
        """
        if noxfile is None:
            return None

        for statement in noxfile.module.body:
            if isinstance(statement, ast.If):
                match statement.test:
                    case ast.Compare(
                        left=ast.Name(id="__name__"),
                        ops=[ast.Eq()],
                        comparators=[ast.Constant(value="__main__")],
                    ):
                        return True

        return False


def repo_review_checks(
    list_all: bool = True, noxfile: tuple[str, dict[str, Any], ast.Module] | None = None
) -> dict[str, Noxfile]:
    if not list_all and noxfile is None:
        return {}
    return {p.__name__: p() for p in Noxfile.__subclasses__()}

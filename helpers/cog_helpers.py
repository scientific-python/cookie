from __future__ import annotations

import ast
import contextlib
import tempfile
import typing
from collections.abc import Generator
from pathlib import Path
from types import SimpleNamespace

if typing.TYPE_CHECKING:
    from typing import Self

from cookiecutter.main import cookiecutter

DIR = Path(__file__).parent.resolve()


@contextlib.contextmanager
def render_cookie(**context: str) -> Generator[Path, None, None]:
    with tempfile.TemporaryDirectory() as tmpdir:
        cookiecutter(
            str(DIR.parent),
            no_input=True,
            default_config=True,
            output_dir=tmpdir,
            extra_context=context,
        )
        yield Path(tmpdir).joinpath("package").resolve()


class Matcher:
    def __init__(self, txt: str):
        self.ast = ast.parse(txt)
        self.lines = txt.splitlines()

    @classmethod
    def from_file(cls, filename: Path) -> Self:
        with filename.open(encoding="utf-8") as f:
            return cls(f.read())

    def get_source(self, name: str) -> str:
        o = SimpleNamespace(name=name)
        for item in self.ast.body:
            match item:
                case ast.FunctionDef(
                    name=o.name, decorator_list=ds, lineno=start, end_lineno=end
                ):
                    for decorator in ds[:1]:
                        start = decorator.lineno
                    return "\n".join(self.lines[start - 1 : end])
        msg = f"{name} not found"
        raise RuntimeError(msg)


@contextlib.contextmanager
def code_fence(lang: str, /, *, width: int = 3) -> Generator[None, None, None]:
    tics = "`" * width
    print("<!-- prettier-ignore-start -->")  # noqa: T201
    print(f"{tics}{lang}")  # noqa: T201
    yield
    print(tics)  # noqa: T201
    print("<!-- prettier-ignore-end -->")  # noqa: T201

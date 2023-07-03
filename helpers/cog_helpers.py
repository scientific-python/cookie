from __future__ import annotations

import contextlib
import tempfile
from collections.abc import Generator
from pathlib import Path

from cookiecutter.main import cookiecutter

DIR = Path(__file__).parent.resolve()
PKG = DIR.parent


@contextlib.contextmanager
def render_cookie(**context: str) -> Generator[Path, None, None]:
    with tempfile.TemporaryDirectory() as tmpdir:
        cookiecutter(
            str(PKG),
            no_input=True,
            default_config=True,
            output_dir=tmpdir,
            extra_context=context,
        )
        yield Path(tmpdir).joinpath("package").resolve()

import argparse
import importlib.resources
import json
import sys
from collections.abc import Iterator
from pathlib import Path

from rich import print
from rich.columns import Columns
from rich.panel import Panel

from .._compat import tomllib
from ..checks.ruff import get_rule_selection, ruff

libs = {"AIR", "ASYNC", "DJ", "FAST", "INT", "NPY", "PD"}
specialty = {
    "CPY",  # preview only
    "A",  # Naming related
    "N",  # Naming related
    "ANN",  # Not all rules good
    "TID",  # Not all rules good
    "C90",  # Complexity
    "COM",  # Trailing commas inform the formatter
    "D",  # Requires everything documented
    "DOC",  # Style-specific
    "ERA",  # Check for commented code
    "FBT",  # Can't be applied to old code very well
    "FIX",  # TODO's are okay
    "TD",  # Picky on todo rules
    "INP",  # Namespace packages are correct sometimes
    "S",  # Security (can be picky)
    "SLF",  # Very picky
}


def process_dir(path: Path) -> None:
    try:
        with path.joinpath("pyproject.toml").open("rb") as f:
            pyproject = tomllib.load(f)
    except FileNotFoundError:
        pyproject = {}

    ruff_config = ruff(pyproject=pyproject, root=path)
    if ruff_config is None:
        print(
            "[red]Could not find a ruff config [dim](.ruff.toml, ruff.toml, or pyproject.toml)",
            file=sys.stderr,
        )
        raise SystemExit(1)
    selected = get_rule_selection(ruff_config)
    if not selected:
        print(
            "[red]No rules selected",
            file=sys.stderr,
        )
        raise SystemExit(2)

    # Create using ruff linter --output-format=json > src/sp_repo_review/ruff/linter.json
    with (
        importlib.resources.files("sp_repo_review.ruff_checks")
        .joinpath("linter.json")
        .open(encoding="utf-8") as ff
    ):
        linter = json.load(ff)

    lint_info = {r["prefix"]: r["name"] for r in linter if r["prefix"] not in {"", "F"}}
    lint_info = dict(sorted(lint_info.items()))

    if "ALL" in selected:
        selected = frozenset(lint_info.keys())

    selected_items = {k: v for k, v in lint_info.items() if k in selected}
    all_uns_items = {k: v for k, v in lint_info.items() if k not in selected}
    unselected_items = {
        k: v for k, v in all_uns_items.items() if k not in libs | specialty
    }
    libs_items = {k: v for k, v in all_uns_items.items() if k in libs}
    spec_items = {k: v for k, v in all_uns_items.items() if k in specialty}

    def print_each(items: dict[str, str]) -> Iterator[str]:
        for k, v in items.items():
            kk = f'[green]"{k}"[/green],'
            yield f"  {kk:23} [dim]# {v}[/dim]"

    panel_sel = Panel(
        "\n".join(print_each(selected_items)), title="Selected", border_style="green"
    )
    panel_lib = Panel(
        "\n".join(print_each(libs_items)),
        title="Library specific",
        border_style="yellow",
    )
    panel_spec = Panel(
        "\n".join(print_each(spec_items)), title="Specialized", border_style="yellow"
    )
    uns = "\n".join(print_each(unselected_items))

    print(Columns([panel_sel, panel_lib, panel_spec]))
    if uns:
        print("[red]Unselected [dim](copy and paste ready)")
        print(uns)


def main() -> None:
    parser = argparse.ArgumentParser(description="Look up Ruff rules in a directory")
    parser.add_argument(
        "path",
        nargs="?",
        type=Path,
        default=Path.cwd(),
        help="Directory to process (default: current working directory)",
    )
    args = parser.parse_args()

    process_dir(args.path)


if __name__ == "__main__":
    main()

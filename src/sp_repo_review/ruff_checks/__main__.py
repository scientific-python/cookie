import argparse
import importlib.resources
import json
import sys
from collections.abc import Iterator, Mapping
from pathlib import Path

from rich import print
from rich.columns import Columns
from rich.panel import Panel

from .._compat import tomllib
from ..checks.ruff import get_rule_selection, ruff

# Create using ruff linter --output-format=json > src/sp_repo_review/ruff/linter.json
RESOURCE_DIR = importlib.resources.files("sp_repo_review.ruff_checks")
with RESOURCE_DIR.joinpath("linter.json").open(encoding="utf-8") as f:
    linter = json.load(f)

LINT_INFO = {r["prefix"]: r["name"] for r in linter if r["prefix"] not in {"", "F"}}
LINT_INFO = dict(sorted(LINT_INFO.items()))

with RESOURCE_DIR.joinpath("select.json").open(encoding="utf-8") as f:
    select_info = json.load(f)
LIBS = frozenset(select_info["libs"])
SPECIALTY = frozenset(r["name"] for r in select_info["specialty"])

with RESOURCE_DIR.joinpath("ignore.json").open(encoding="utf-8") as f:
    IGNORE_INFO = json.load(f)


def print_each(items: Mapping[str, str]) -> Iterator[str]:
    size = max(len(k) for k in items) if items else 0
    for k, v in items.items():
        kk = f'[green]"{k}"[/green],'
        yield f"  {kk:{size + 18}} [dim]# {v}[/dim]"


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

    if "ALL" in selected:
        ignored = get_rule_selection(ruff_config, "ignore")
        missed = [
            r
            for r in IGNORE_INFO
            if not any(
                x.startswith((r.get("rule", "."), r.get("family", ".")))
                for x in ignored
            )
        ]

        print('[green]"ALL"[/green] selected.')
        ignores = {v.get("rule", v.get("family", "")): v["reason"] for v in missed}
        if ignores:
            print("Some things that sometimes need ignoring:")
            for item in print_each(ignores):
                print(item)
        return

    selected_items = {k: v for k, v in LINT_INFO.items() if k in selected}
    all_uns_items = {k: v for k, v in LINT_INFO.items() if k not in selected}
    unselected_items = {
        k: v for k, v in all_uns_items.items() if k not in LIBS | SPECIALTY
    }
    libs_items = {k: v for k, v in all_uns_items.items() if k in LIBS}
    spec_items = {k: v for k, v in all_uns_items.items() if k in SPECIALTY}

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

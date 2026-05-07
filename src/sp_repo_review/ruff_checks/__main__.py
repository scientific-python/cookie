__lazy_modules__ = [
    "argparse",
    "collections",
    "collections.abc",
    "os",
    "pathlib",
    "sp_repo_review._compat",
    "sp_repo_review.checks",
    "sp_repo_review.checks.ruff",
    "sys",
    "typing",
]

import argparse
import importlib
import importlib.resources
import json
import os
import sys
from collections.abc import Iterator, Mapping
from importlib.util import find_spec
from pathlib import Path

from sp_repo_review._compat import tomllib
from sp_repo_review.checks.ruff import get_rule_selection, ruff

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

# Tool-specific agent variables
# Based on https://github.com/agentsmd/agents.md/issues/136
_AGENT_VARS = [
    "AGENT",  # Pi, Goose, Amp
    "CLAUDECODE",
    "CURSOR_AGENT",
    "CLINE_ACTIVE",
    "GEMINI_CLI",
    "CODEX_SANDBOX",
    "AUGMENT_AGENT",
    "TRAE_AI_SHELL_ID",
    "OPENCODE_CLIENT",
]


def _is_agent_environment() -> bool:
    """Check if running from an AI coding agent using env vars."""
    return any(os.environ.get(var) for var in _AGENT_VARS)


def _resolve_format(format_arg: str) -> str:
    """Resolve 'auto' format to either 'rich' or 'plain'."""
    if format_arg != "auto":
        return format_arg

    if _is_agent_environment():
        return "plain"

    return "rich" if _has_rich() else "plain"


def _has_rich() -> bool:
    return find_spec("rich") is not None


def _print_each_plain(items: Mapping[str, str], indent: int = 2) -> Iterator[str]:
    """Generate plain text formatted rule lines."""
    size = max(len(k) for k in items) if items else 0
    for k, v in items.items():
        yield f'{" " * indent}"{k}",{" " * (size - len(k))} # {v}'


def _print_each_rich(items: Mapping[str, str]) -> Iterator[str]:
    """Generate rich formatted rule lines."""
    size = max(len(k) for k in items) if items else 0
    for k, v in items.items():
        kk = f'[green]"{k}"[/green],'
        yield f"  {kk:{size + 18}} [dim]# {v}[/dim]"


def _output_error(fmt: str, message: str) -> None:
    """Output error message in appropriate format."""
    if fmt == "rich":
        import rich

        rich.print(message, file=sys.stderr)
    else:
        print(message, file=sys.stderr)


def _print_output_rich(
    selected_items: dict[str, str],
    libs_items: dict[str, str],
    spec_items: dict[str, str],
    unselected_items: dict[str, str],
) -> None:
    """Print rich formatted output."""
    import rich.columns
    import rich.panel

    panel_sel = rich.panel.Panel(
        "\n".join(_print_each_rich(selected_items)),
        title="Selected",
        border_style="green",
    )
    panel_lib = rich.panel.Panel(
        "\n".join(_print_each_rich(libs_items)),
        title="Library specific",
        border_style="yellow",
    )
    panel_spec = rich.panel.Panel(
        "\n".join(_print_each_rich(spec_items)),
        title="Specialized",
        border_style="yellow",
    )
    uns = "\n".join(_print_each_rich(unselected_items))

    rich.print(rich.columns.Columns([panel_sel, panel_lib, panel_spec]))
    if uns:
        rich.print("[red]Unselected [dim](copy and paste ready)")
        rich.print(uns)


def _print_output_plain(
    selected_items: dict[str, str],
    libs_items: dict[str, str],
    spec_items: dict[str, str],
    unselected_items: dict[str, str],
) -> None:
    """Print plain formatted output."""
    print("Selected:")
    for item in _print_each_plain(selected_items):
        print(item)

    if libs_items:
        print("\nLibrary specific:")
        for item in _print_each_plain(libs_items):
            print(item)

    if spec_items:
        print("\nSpecialized:")
        for item in _print_each_plain(spec_items):
            print(item)

    if unselected_items:
        print("\nUnselected (copy and paste ready):")
        for item in _print_each_plain(unselected_items):
            print(item)


def _handle_all_selected(fmt: str, ruff_config: dict[str, object]) -> None:
    """Handle the case when ALL rules are selected."""
    ignored = get_rule_selection(ruff_config, "ignore")
    missed = [
        r
        for r in IGNORE_INFO
        if not any(
            x.startswith((r.get("rule", "."), r.get("family", ".")))
            for x in (ignored or [])
        )
    ]

    msg = '[green]"ALL"[/green] selected.' if fmt == "rich" else '"ALL" selected.'
    if fmt == "rich":
        import rich

        rich.print(msg)
    else:
        print(msg)

    ignores = {v.get("rule", v.get("family", "")): v["reason"] for v in missed}
    if ignores:
        msg_header = "Some things that sometimes need ignoring:"
        if fmt == "rich":
            import rich

            rich.print(msg_header)
            for item in _print_each_rich(ignores):
                rich.print(item)
        else:
            print(msg_header)
            for item in _print_each_plain(ignores):
                print(item)


def process_dir(path: Path, format: str = "auto") -> None:
    """Process a directory and display ruff rules configuration.

    Args:
        path: Directory to process
        format: Output format - 'auto', 'rich', or 'plain'
    """
    fmt = _resolve_format(format)

    try:
        with path.joinpath("pyproject.toml").open("rb") as f:
            pyproject = tomllib.load(f)
    except FileNotFoundError:
        pyproject = {}

    ruff_config = ruff(pyproject=pyproject, root=path)
    if fmt == "rich" and not _has_rich():
        _output_error(
            "plain", "Error: --format rich requested, but rich is not installed"
        )
        raise SystemExit(3)

    if ruff_config is None:
        msg = (
            "[red]Could not find a ruff config [dim](.ruff.toml, ruff.toml, or pyproject.toml)"
            if fmt == "rich"
            else "Error: Could not find a ruff config (.ruff.toml, ruff.toml, or pyproject.toml)"
        )
        _output_error(fmt, msg)
        raise SystemExit(1)

    selected = get_rule_selection(ruff_config)
    if not selected:
        msg = "[red]No rules selected" if fmt == "rich" else "Error: No rules selected"
        _output_error(fmt, msg)
        raise SystemExit(2)

    if "ALL" in selected:
        _handle_all_selected(fmt, ruff_config)
        return

    selected_items = {k: v for k, v in LINT_INFO.items() if k in selected}
    all_uns_items = {k: v for k, v in LINT_INFO.items() if k not in selected}
    unselected_items = {
        k: v for k, v in all_uns_items.items() if k not in LIBS | SPECIALTY
    }
    libs_items = {k: v for k, v in all_uns_items.items() if k in LIBS}
    spec_items = {k: v for k, v in all_uns_items.items() if k in SPECIALTY}

    if fmt == "rich":
        _print_output_rich(selected_items, libs_items, spec_items, unselected_items)
    else:
        _print_output_plain(selected_items, libs_items, spec_items, unselected_items)


def main() -> None:
    parser = argparse.ArgumentParser(description="Look up Ruff rules in a directory")
    parser.add_argument(
        "path",
        nargs="?",
        type=Path,
        default=Path.cwd(),
        help="Directory to process (default: current working directory)",
    )
    parser.add_argument(
        "--format",
        choices=["auto", "rich", "plain"],
        default="auto",
        help="Output format (default: auto)",
    )
    args = parser.parse_args()

    process_dir(args.path, format=args.format)


if __name__ == "__main__":
    main()

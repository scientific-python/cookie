import sys
from importlib.util import find_spec as _find_spec

from sp_repo_review.ruff_checks import __main__ as ruff_checks


def test_auto_and_plain_do_not_require_rich(monkeypatch, tmp_path, capsys):
    def no_rich_find_spec(name, package=None):
        if name == "rich" or name.startswith("rich."):
            return None
        return _find_spec(name, package=package)

    monkeypatch.setattr(ruff_checks, "ruff", lambda *_a, **_k: {"tool": "ruff"})
    monkeypatch.setattr(ruff_checks, "get_rule_selection", lambda *_a, **_k: {"A"})
    monkeypatch.setattr(ruff_checks, "LINT_INFO", {"A": "Rule A"})
    monkeypatch.setattr(ruff_checks, "LIBS", frozenset())
    monkeypatch.setattr(ruff_checks, "SPECIALTY", frozenset())
    monkeypatch.setattr(ruff_checks, "_is_agent_environment", lambda: False)
    monkeypatch.setattr(ruff_checks, "find_spec", no_rich_find_spec)

    for mod in list(sys.modules):
        if mod == "rich" or mod.startswith("rich."):
            monkeypatch.delitem(sys.modules, mod, raising=False)

    for fmt in ("plain", "auto"):
        ruff_checks.process_dir(tmp_path, format=fmt)
        captured = capsys.readouterr()
        assert "Selected:" in captured.out
        assert captured.err == ""


def test_plain_format_has_quotes_and_comma(monkeypatch, tmp_path, capsys):
    """Regression test: plain format should quote rules for copy-paste."""
    monkeypatch.setattr(ruff_checks, "ruff", lambda *_a, **_k: {"tool": "ruff"})
    monkeypatch.setattr(ruff_checks, "get_rule_selection", lambda *_a, **_k: {"A"})
    monkeypatch.setattr(ruff_checks, "LINT_INFO", {"A": "Rule A"})
    monkeypatch.setattr(ruff_checks, "LIBS", frozenset())
    monkeypatch.setattr(ruff_checks, "SPECIALTY", frozenset())

    ruff_checks.process_dir(tmp_path, format="plain")
    captured = capsys.readouterr()
    assert '"A",' in captured.out

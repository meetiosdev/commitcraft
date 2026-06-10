from pathlib import Path

import pytest

from commitcraft import cli
from commitcraft.models import GitChangeSet
from commitcraft.terminal import progress


class FakeClient:
    def __init__(self, output: str, running: bool = True) -> None:
        self.output = output
        self.running = running

    def is_running(self) -> bool:
        return self.running

    def generate(self, model: str, prompt: str) -> str:
        return self.output


def _changes(tmp_path: Path) -> GitChangeSet:
    return GitChangeSet(
        repo_root=tmp_path,
        repo_name="repo",
        status="?? file.py",
        staged_files=[],
        unstaged_files=[],
        untracked_files=["file.py"],
        staged_diff="",
        unstaged_diff="",
    )


def test_resolve_repo_path_prompts_for_path(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("builtins.input", lambda prompt: "/tmp/repo")

    assert cli.resolve_repo_path(None) == "/tmp/repo"


def test_resolve_repo_path_blank_uses_cwd_if_git(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("builtins.input", lambda prompt: "")
    monkeypatch.setattr(cli, "validate_repo_path", lambda path: Path(path))

    assert cli.resolve_repo_path(None) == str(Path.cwd())


def test_progress_function_output(capsys: pytest.CaptureFixture[str]) -> None:
    progress(40)

    assert "Processing [********------------] 40%" in capsys.readouterr().out


def test_clean_output_hides_files_by_default(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setattr(cli, "read_git_changes", lambda repo_path: _changes(tmp_path))
    monkeypatch.setattr(cli, "build_context", lambda changes, max_context: "context")
    monkeypatch.setattr(cli, "OllamaClient", lambda url: FakeClient(VALID_OUTPUT))

    cli.main([str(tmp_path)])

    output = capsys.readouterr().out
    assert "FILES" not in output
    assert "FULL DETAILED:" in output


def test_show_files_still_works(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setattr(cli, "read_git_changes", lambda repo_path: _changes(tmp_path))
    monkeypatch.setattr(cli, "build_context", lambda changes, max_context: "context")
    monkeypatch.setattr(cli, "OllamaClient", lambda url: FakeClient(VALID_OUTPUT))

    cli.main([str(tmp_path), "--show-files"])

    output = capsys.readouterr().out
    assert "FILES" in output
    assert "file.py" in output


def test_pyproject_has_command_aliases() -> None:
    pyproject = Path("pyproject.toml").read_text()

    assert 'commitcraft = "commitcraft.cli:main"' in pyproject
    assert 'make_commit = "commitcraft.cli:main"' in pyproject
    assert 'make_commit_message = "commitcraft.cli:main"' in pyproject


VALID_OUTPUT = """FULL DETAILED:
feat(core): add file

* add file
* update repo
* prepare commit

MEDIUM:
feat(core): add file

ONE LINER:
feat(core): add file"""

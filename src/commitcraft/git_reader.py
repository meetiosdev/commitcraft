from __future__ import annotations

import subprocess
from pathlib import Path

from commitcraft.constants import ALLOWED_GIT_COMMANDS
from commitcraft.exceptions import InvalidRepoPathError, NotGitRepoError, UnsafeGitCommandError
from commitcraft.file_context import should_ignore_change_path
from commitcraft.models import GitChangeSet


def validate_repo_path(repo_path: str) -> Path:
    path = Path(repo_path).expanduser().resolve()
    if not path.exists():
        raise InvalidRepoPathError(f"Path does not exist: {path}")
    if not path.is_dir():
        raise InvalidRepoPathError(f"Path is not a directory: {path}")
    if _run_git(["git", "rev-parse", "--is-inside-work-tree"], path) != "true":
        raise NotGitRepoError(f"Path is not inside a Git repository: {path}")
    root = _run_git(["git", "rev-parse", "--show-toplevel"], path)
    if not root:
        raise NotGitRepoError("Could not detect Git repository root.")
    return Path(root)


def read_git_changes(repo_path: str) -> GitChangeSet:
    root = validate_repo_path(repo_path)
    return GitChangeSet(
        repo_root=root,
        repo_name=root.name,
        status=_run_git(["git", "status", "--short"], root),
        staged_files=_filter_files(_lines(_run_git(["git", "diff", "--cached", "--name-only"], root))),
        unstaged_files=_filter_files(_lines(_run_git(["git", "diff", "--name-only"], root))),
        untracked_files=_filter_files(_lines(_run_git(["git", "ls-files", "--others", "--exclude-standard"], root))),
        staged_diff=_run_git(["git", "diff", "--cached"], root),
        unstaged_diff=_run_git(["git", "diff"], root),
    )


def _run_git(command: list[str], cwd: Path) -> str:
    if tuple(command) not in ALLOWED_GIT_COMMANDS:
        raise UnsafeGitCommandError(f"Refusing unsafe git command: {' '.join(command)}")
    result = subprocess.run(command, cwd=cwd, text=True, capture_output=True, shell=False)
    if result.returncode != 0:
        return ""
    return result.stdout.strip()


def _lines(text: str) -> list[str]:
    return [line.strip() for line in text.splitlines() if line.strip()]


def _filter_files(files: list[str]) -> list[str]:
    return [file for file in files if not should_ignore_change_path(file)]

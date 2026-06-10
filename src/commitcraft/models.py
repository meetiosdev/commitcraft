from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class GitChangeSet:
    repo_root: Path
    repo_name: str
    status: str
    staged_files: list[str]
    unstaged_files: list[str]
    untracked_files: list[str]
    staged_diff: str
    unstaged_diff: str

    @property
    def all_files(self) -> list[str]:
        return sorted(set(self.staged_files + self.unstaged_files + self.untracked_files))


@dataclass(frozen=True)
class CommitMessageOptions:
    full_detailed: str
    medium: str
    one_liner: str


@dataclass(frozen=True)
class FileContextResult:
    path: str
    content: str
    skipped_reason: str = ""

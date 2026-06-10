from __future__ import annotations

from pathlib import Path
import re

from commitcraft.constants import (
    BINARY_SUFFIXES,
    MAX_UNTRACKED_FILE_CHARS,
    SENSITIVE_NAMES,
    SENSITIVE_SUFFIXES,
    SKIP_FOLDERS,
    TEXT_SUFFIXES,
)


def should_skip_path(path: str) -> str:
    p = Path(path)
    lowered_name = p.name.lower()
    parts = set(p.parts)
    if parts & SKIP_FOLDERS:
        return "skipped folder"
    if lowered_name in SENSITIVE_NAMES or p.suffix.lower() in SENSITIVE_SUFFIXES:
        return "sensitive file"
    if p.suffix.lower() in BINARY_SUFFIXES:
        return "binary file"
    return ""


def read_untracked_context(repo_root: Path, files: list[str]) -> str:
    chunks: list[str] = []
    for file in files:
        reason = should_skip_path(file)
        chunks.append(f"\nNEW FILE:\n{file}")
        if reason:
            chunks.append(f"[Skipped content: {reason}]")
            continue

        path = repo_root / file
        if path.suffix.lower() not in TEXT_SUFFIXES:
            chunks.append("[Skipped content: unsupported file type]")
            continue
        try:
            content = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            chunks.append("[Skipped content: unreadable file]")
            continue
        if len(content) > MAX_UNTRACKED_FILE_CHARS:
            content = content[:MAX_UNTRACKED_FILE_CHARS] + "\n[Truncated file content]"
        chunks.append("CONTENT:\n" + content)
    return "\n".join(chunks).strip()


def truncate_context(context: str, max_chars: int) -> str:
    if len(context) <= max_chars:
        return context
    return context[:max_chars] + "\n[Context truncated]"


def filter_safe_diff(diff: str) -> str:
    blocks = re.split(r"(?=^diff --git )", diff, flags=re.MULTILINE)
    safe: list[str] = []
    for block in blocks:
        if not block.strip():
            continue
        first = block.splitlines()[0] if block.splitlines() else ""
        paths = [
            token.removeprefix("a/").removeprefix("b/")
            for token in first.split()
            if token.startswith(("a/", "b/"))
        ]
        reason = next((should_skip_path(path) for path in paths if should_skip_path(path)), "")
        if reason:
            safe.append(f"{first}\n[Skipped content: {reason}]\n")
            continue
        if "Binary files " in block:
            safe.append(f"{first}\n[Skipped content: binary file]\n")
            continue
        safe.append(block)
    return "".join(safe).strip()

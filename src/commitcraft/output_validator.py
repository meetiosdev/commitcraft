from __future__ import annotations

import re

ASSISTANT_PHRASES = (
    "It appears",
    "Here's",
    "If you need",
    "feel free",
    "brief overview",
    "The files",
)

CONVENTIONAL_RE = re.compile(
    r"\b(feat|fix|chore|docs|refactor|style|test|perf|build|ci)(\([a-z0-9._-]+\))?:",
    re.IGNORECASE,
)
SUBJECT_RE = re.compile(
    r"^(?P<type>feat|fix|chore|docs|refactor|style|test|perf|build|ci)(?P<scope>\([a-z0-9._-]+\))?: .+",
    re.IGNORECASE,
)

HALLUCINATION_TERMS = (
    "auth",
    "login",
    "jwt",
    "endpoint",
    "axios",
    "lodash",
    "uuid",
    "mobile",
    "layout",
)


def is_valid_commit_output(output: str) -> bool:
    if "FULL DETAILED:" not in output:
        return False
    if "MEDIUM:" not in output:
        return False
    if "ONE LINER:" not in output:
        return False
    lowered = output.lower()
    if any(phrase.lower() in lowered for phrase in ASSISTANT_PHRASES):
        return False
    if not CONVENTIONAL_RE.search(output):
        return False
    return _has_consistent_subjects(output)


def is_relevant_commit_output(output: str, files: list[str]) -> bool:
    joined_files = " ".join(files).lower()
    lowered_output = output.lower()
    if _is_docs_only(files):
        first_subject = _subjects(output)[0] if _subjects(output) else ""
        if not first_subject.lower().startswith(("docs:", "docs(", "chore:", "chore(")):
            return False
    for term in HALLUCINATION_TERMS:
        if term in lowered_output and term not in joined_files:
            return False
    return True


def is_weak_jobs_output(output: str) -> bool:
    lowered = output.lower()
    if "feat(jobs):" not in lowered:
        return True
    weak_terms = (
        "refactor(doc",
        "refactor(docs",
        "update cover letter and resume templates",
        "latex",
    )
    if any(term in lowered for term in weak_terms):
        return True
    return "jobs_data" not in lowered and "scraped job" not in lowered and "job application" not in lowered


def _subjects(output: str) -> list[str]:
    lines = [line.strip() for line in output.splitlines()]
    subjects: list[str] = []
    for index, line in enumerate(lines):
        if line in {"FULL DETAILED:", "MEDIUM:", "ONE LINER:"}:
            for candidate in lines[index + 1 :]:
                if candidate:
                    subjects.append(candidate)
                    break
    return subjects


def _has_consistent_subjects(output: str) -> bool:
    subjects = _subjects(output)
    if len(subjects) != 3:
        return False
    matches = [SUBJECT_RE.match(subject) for subject in subjects]
    if not all(matches):
        return False
    first = matches[0]
    assert first is not None
    first_key = (first.group("type").lower(), (first.group("scope") or "").lower())
    for match in matches[1:]:
        assert match is not None
        key = (match.group("type").lower(), (match.group("scope") or "").lower())
        if key != first_key:
            return False
    return True


def _is_docs_only(files: list[str]) -> bool:
    if not files:
        return False
    docs_markers = ("readme", "docs/", ".md", ".rst", ".txt")
    return all(any(marker in file.lower() for marker in docs_markers) for file in files)

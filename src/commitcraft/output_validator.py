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
    return bool(CONVENTIONAL_RE.search(output))


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

from __future__ import annotations

from commitcraft.file_context import filter_safe_diff, read_untracked_context, truncate_context
from commitcraft.models import GitChangeSet
from commitcraft.project_detector import detect_project_type


def build_context(changes: GitChangeSet, max_context: int) -> str:
    project_type = detect_project_type(changes.repo_root, changes.all_files)
    parts = [
        f"REPO NAME:\n{changes.repo_name}",
        f"PROJECT TYPE:\n{project_type}",
        "PATH SUMMARY:\n" + build_path_summary(changes.all_files),
        "CHANGED FILES:\n" + "\n".join(f"- {file}" for file in changes.all_files),
    ]
    if changes.staged_diff:
        parts.append("STAGED DIFF:\n" + filter_safe_diff(changes.staged_diff))
    if changes.unstaged_diff:
        parts.append("UNSTAGED DIFF:\n" + filter_safe_diff(changes.unstaged_diff))
    if changes.untracked_files:
        parts.append("UNTRACKED FILES:\n" + read_untracked_context(changes.repo_root, changes.untracked_files))
    return truncate_context("\n\n".join(parts), max_context)


def build_prompt(context: str) -> str:
    return f"""
You are not a chat assistant.
You are a Git commit message generator.
Do not explain the files.
Do not summarize like a report.
Do not say "It appears".
Do not give advice.
Do not mention LaTeX unless it is part of the commit message.
Return only 3 commit message options.
Prioritize file paths, folders, and job metadata over raw document text.
If paths include AppliedJobs, jobs_data, resume, coverletter, job_details, job_content, or full_page, prefer feat(jobs) and summarize generated job application assets.

Generate 3 Git commit message options from the provided Git changes.
Use Conventional Commits.
Do not invent changes.
Use present tense.
Do not mention AI.
Do not mention Ollama.
Do not use markdown code fences.
Return exactly this format and nothing else:

FULL DETAILED:
type(scope): summary

* bullet
* bullet
* bullet

MEDIUM:
type(scope): summary

ONE LINER:
type(scope): summary

Allowed types:
feat, fix, refactor, chore, docs, style, test, perf, build, ci

For full detailed:
- First line under 72 characters.
- Add 2 to 5 bullets.
- Bullets should summarize real changes.

For medium:
- One line only.
- Under 100 characters.

For one liner:
- One line only.
- Under 72 characters.

GIT CHANGES:
{context}
""".strip()


def build_repair_prompt(bad_output: str) -> str:
    return f"""
You are not a chat assistant.
You are a Git commit message generator.
Rewrite this into the required 3 commit message format only.
Do not explain.
Do not add advice.
Do not mention AI.
Do not use markdown code fences.

Return exactly this format and nothing else:

FULL DETAILED:
type(scope): summary

* bullet
* bullet
* bullet

MEDIUM:
type(scope): summary

ONE LINER:
type(scope): summary

BAD OUTPUT:
{bad_output}
""".strip()


def build_path_summary(files: list[str]) -> str:
    lowered = " ".join(file.lower() for file in files)
    if any(
        key in lowered
        for key in ("appliedjobs", "jobs_data", "resume", "coverletter", "job_details", "job_content", "full_page")
    ):
        return (
            "Job application asset changes detected: AppliedJobs and jobs_data paths include "
            "generated resumes, cover letters, scraped job pages, job content, and job metadata. "
            "Prefer feat(jobs) over document-only or LaTeX-focused messages."
        )
    return "General repository changes."

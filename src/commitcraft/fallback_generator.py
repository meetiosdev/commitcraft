from __future__ import annotations

JOBS_FALLBACK = """FULL DETAILED:
feat(jobs): add generated job application assets

* add resumes and cover letters for multiple company applications
* store scraped job pages, job content, and metadata
* organize applications by company, week, and job id

MEDIUM:
feat(jobs): add generated job files and scraped job data

ONE LINER:
feat(jobs): add job application assets"""


def generate_fallback_messages(files: list[str]) -> str:
    joined = " ".join(file.lower() for file in files)
    if _is_job_application_repo_change(joined):
        return JOBS_FALLBACK

    scope = _scope(files)
    scoped = f"({scope})" if scope else ""

    if any(key in joined for key in ["readme", ".md", "docs"]):
        base = "docs: update documentation"
    elif any(key in joined for key in ["test", "spec"]):
        base = f"test{scoped}: update tests"
    elif any(key in joined for key in ["package.json", "requirements.txt", "pyproject.toml", "gradle"]):
        base = f"build{scoped}: update dependencies"
    elif any(key in joined for key in ["fix", "bug", "error"]):
        base = f"fix{scoped}: update implementation"
    elif any(key in joined for key in ["job", "resume", "cover", "application"]):
        base = f"feat{scoped or '(jobs)'}: add job application assets"
    else:
        base = f"chore{scoped}: update project files"

    return f"""FULL DETAILED:
{base}

* update changed and untracked project files
* organize current repository changes
* prepare changes for review and commit

MEDIUM:
{base}

ONE LINER:
{base}"""


def _scope(files: list[str]) -> str:
    joined = " ".join(file.lower() for file in files)
    scopes = {
        "jobs": ["job", "resume", "cover", "application"],
        "auth": ["auth", "login", "session"],
        "api": ["api", "service", "client", "request"],
        "ui": ["ui", "view", "screen", "component"],
        "config": ["config", ".env", "yaml", "toml", "json"],
        "docs": ["readme", "docs", ".md"],
    }
    for scope, keys in scopes.items():
        if any(key in joined for key in keys):
            return scope
    return ""


def _is_job_application_repo_change(joined: str) -> bool:
    keys = (
        "appliedjobs",
        "jobs_data",
        "resume",
        "coverletter",
        "job_details",
        "job_content",
    )
    return any(key in joined for key in keys)


def is_job_application_change(files: list[str]) -> bool:
    return _is_job_application_repo_change(" ".join(file.lower() for file in files))

from commitcraft.cli import generate_output_with_retry
from commitcraft.config import Config


class FakeClient:
    def __init__(self, responses: list[str]) -> None:
        self.responses = responses
        self.calls = 0

    def is_running(self) -> bool:
        return True

    def generate(self, model: str, prompt: str) -> str:
        self.calls += 1
        return self.responses.pop(0)


def test_retry_trigger_repairs_invalid_output() -> None:
    client = FakeClient(
        [
            "It appears that the files are job application assets.",
            """FULL DETAILED:
feat(jobs): add generated job assets

* add resumes for companies
* store job metadata
* organize application files

MEDIUM:
feat(jobs): add generated job files

ONE LINER:
feat(jobs): add job assets""",
        ]
    )

    output = generate_output_with_retry(
        client,  # type: ignore[arg-type]
        Config(),
        "context",
        ["jobs_data/acme/job_details.json"],
    )

    assert client.calls == 2
    assert "FULL DETAILED:" in output
    assert "It appears" not in output


def test_jobs_fallback_replaces_weak_refactor_output() -> None:
    client = FakeClient(
        [
            """FULL DETAILED:
refactor(docs): update cover letter and resume templates

* update LaTeX formatting
* revise document layout
* adjust templates

MEDIUM:
refactor(docs): update LaTeX templates

ONE LINER:
refactor: update LaTeX files""",
            """FULL DETAILED:
refactor(docs): update cover letter and resume templates

* update LaTeX formatting
* revise document layout
* adjust templates

MEDIUM:
refactor(docs): update LaTeX templates

ONE LINER:
refactor: update LaTeX files""",
        ]
    )

    output = generate_output_with_retry(
        client,  # type: ignore[arg-type]
        Config(),
        "context",
        ["AppliedJobs/ACME/resume.pdf", "jobs_data/acme/job_details.json"],
    )

    assert "feat(jobs): add generated job application assets" in output
    assert "refactor(docs)" not in output

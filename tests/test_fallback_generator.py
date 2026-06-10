from commitcraft.fallback_generator import generate_fallback_messages


def test_fallback_jobs_scope() -> None:
    output = generate_fallback_messages(["jobs_data/company/job_details.json"])

    assert "FULL DETAILED:" in output
    assert "feat(jobs): add generated job application assets" in output


def test_fallback_docs() -> None:
    output = generate_fallback_messages(["README.md"])

    assert "docs(docs): update documentation" in output


def test_fallback_applied_jobs_exact_output() -> None:
    output = generate_fallback_messages(
        [
            "AppliedJobs/June2026/week_2/ACME/123/resume.pdf",
            "jobs_data/acme/job_123/job_content.txt",
        ]
    )

    assert "feat(jobs): add generated job application assets" in output
    assert "* add resumes and cover letters for multiple company applications" in output
    assert "feat(jobs): add generated job files and scraped job data" in output
    assert "feat(jobs): add job application assets" in output

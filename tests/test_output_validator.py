from commitcraft.output_validator import is_relevant_commit_output, is_valid_commit_output


VALID_OUTPUT = """FULL DETAILED:
feat(jobs): add generated job assets

* add resumes for companies
* store job metadata
* organize application files

MEDIUM:
feat(jobs): add generated job files

ONE LINER:
feat(jobs): add job assets"""


def test_valid_three_message_output() -> None:
    assert is_valid_commit_output(VALID_OUTPUT)


def test_invalid_assistant_style_output() -> None:
    output = "It appears that you've provided a detailed list of new files."

    assert not is_valid_commit_output(output)


def test_invalid_inconsistent_three_message_output() -> None:
    output = """FULL DETAILED:
refactor(api): update endpoint for user authentication

* update auth endpoint
* add token handling
* update docs

MEDIUM:
chore(deps): bump dependencies

ONE LINER:
fix(ui): resolve mobile layout"""

    assert not is_valid_commit_output(output)


def test_docs_only_rejects_hallucinated_auth_output() -> None:
    output = """FULL DETAILED:
refactor(api): update endpoint for user authentication

* update login endpoint
* add JWT validation
* revise request handling

MEDIUM:
refactor(api): update authentication endpoint

ONE LINER:
refactor(api): update auth endpoint"""

    assert not is_relevant_commit_output(output, ["README.md"])

from commitcraft.output_validator import is_valid_commit_output


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

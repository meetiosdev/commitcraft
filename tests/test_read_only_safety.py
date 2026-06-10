from commitcraft.constants import ALLOWED_GIT_COMMANDS


def test_allowed_git_commands_are_read_only() -> None:
    forbidden = {"add", "commit", "reset", "checkout", "clean"}

    for command in ALLOWED_GIT_COMMANDS:
        assert not forbidden.intersection(command)

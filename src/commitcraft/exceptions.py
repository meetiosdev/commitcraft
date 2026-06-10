class CommitCraftError(Exception):
    """Base CommitCraft error."""


class InvalidRepoPathError(CommitCraftError, ValueError):
    """Repo path does not exist or is not a directory."""


class NotGitRepoError(CommitCraftError, ValueError):
    """Path is not inside a Git repository."""


class OllamaError(CommitCraftError):
    """Local Ollama request failed."""


class UnsafeGitCommandError(CommitCraftError):
    """Blocked unsafe Git command."""

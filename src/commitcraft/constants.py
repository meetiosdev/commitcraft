from __future__ import annotations

APP_NAME = "commitcraft"
VERSION = "0.1.0"
DEFAULT_MODEL = "qwen2.5-coder:7b"
DEFAULT_OLLAMA_URL = "http://localhost:11434"
DEFAULT_MAX_CONTEXT = 14000
MAX_UNTRACKED_FILE_CHARS = 3000

ALLOWED_GIT_COMMANDS = {
    ("git", "rev-parse", "--is-inside-work-tree"),
    ("git", "rev-parse", "--show-toplevel"),
    ("git", "status", "--short"),
    ("git", "diff"),
    ("git", "diff", "--cached"),
    ("git", "diff", "--name-only"),
    ("git", "diff", "--cached", "--name-only"),
    ("git", "ls-files", "--others", "--exclude-standard"),
}

SENSITIVE_NAMES = {
    ".env",
    ".env.local",
    ".env.production",
    "google-services.json",
    "googleservice-info.plist",
    "id_rsa",
    "id_ed25519",
}
SENSITIVE_SUFFIXES = {".pem", ".key", ".p12", ".mobileprovision", ".keystore", ".jks"}
SKIP_FOLDERS = {
    ".git",
    "node_modules",
    "build",
    "dist",
    ".next",
    ".venv",
    "venv",
    "Pods",
    ".dart_tool",
    "__pycache__",
    ".pytest_cache",
    ".ruff_cache",
}
BINARY_SUFFIXES = {
    ".pdf",
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".webp",
    ".mp4",
    ".mov",
    ".zip",
    ".tar",
    ".gz",
    ".dmg",
}
TEXT_SUFFIXES = {
    ".py",
    ".js",
    ".ts",
    ".tsx",
    ".jsx",
    ".dart",
    ".swift",
    ".kt",
    ".java",
    ".php",
    ".html",
    ".css",
    ".scss",
    ".md",
    ".json",
    ".yaml",
    ".yml",
    ".txt",
    ".sh",
    ".tex",
    ".xml",
    ".toml",
    ".ini",
}

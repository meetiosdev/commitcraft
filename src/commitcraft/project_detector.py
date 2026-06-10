from __future__ import annotations

from pathlib import Path


def detect_project_type(repo_root: Path, files: list[str]) -> str:
    lower_files = [file.lower() for file in files]
    joined = " ".join(lower_files)
    if (repo_root / "pubspec.yaml").exists() or any(file.endswith(".dart") for file in lower_files):
        return "Flutter"
    if (
        (repo_root / "build.gradle").exists()
        or (repo_root / "settings.gradle").exists()
        or any(file.endswith((".kt", ".java")) for file in lower_files)
    ):
        return "Android"
    if any(file.endswith(".swift") for file in lower_files) or ".xcodeproj" in joined or ".xcworkspace" in joined or "podfile" in joined:
        return "iOS"
    if (repo_root / "package.json").exists() or any(file.endswith((".tsx", ".jsx", ".ts", ".js")) for file in lower_files):
        return "React/Node"
    if "wp-content" in joined or any(file.endswith(".php") for file in lower_files) or (repo_root / "wp-config.php").exists():
        return "WordPress/PHP"
    if (repo_root / "requirements.txt").exists() or (repo_root / "pyproject.toml").exists() or any(file.endswith(".py") for file in lower_files):
        return "Python"
    return "General"

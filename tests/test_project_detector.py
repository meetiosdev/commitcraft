from pathlib import Path

from commitcraft.project_detector import detect_project_type


def test_detect_python_from_py_file(tmp_path: Path) -> None:
    assert detect_project_type(tmp_path, ["app/main.py"]) == "Python"


def test_detect_react_from_package_json(tmp_path: Path) -> None:
    (tmp_path / "package.json").write_text("{}")

    assert detect_project_type(tmp_path, []) == "React/Node"


def test_detect_flutter_from_pubspec(tmp_path: Path) -> None:
    (tmp_path / "pubspec.yaml").write_text("name: app")

    assert detect_project_type(tmp_path, []) == "Flutter"

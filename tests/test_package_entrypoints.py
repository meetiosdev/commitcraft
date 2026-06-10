import subprocess
import sys
from pathlib import Path
import os

import commitcraft


def test_package_imports_from_src_layout() -> None:
    assert commitcraft.__version__ == "0.1.0"


def test_version_output_uses_commitcraft(capsys) -> None:  # type: ignore[no-untyped-def]
    from commitcraft.cli import main

    try:
        main(["--version"])
    except SystemExit:
        pass

    assert "commitcraft 0.1.0" in capsys.readouterr().out


def test_python_module_entrypoint_works() -> None:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(Path.cwd() / "src")
    result = subprocess.run(
        [sys.executable, "-m", "commitcraft", "--version"],
        text=True,
        capture_output=True,
        cwd=Path.cwd(),
        env=env,
        shell=False,
    )

    assert result.returncode == 0
    assert "commitcraft 0.1.0" in result.stdout

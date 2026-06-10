from __future__ import annotations

import platform
import subprocess
from shutil import which


def copy_text(text: str) -> bool:
    system = platform.system().lower()
    if system == "darwin":
        return _pipe(["pbcopy"], text)
    if system == "linux":
        if which("wl-copy"):
            return _pipe(["wl-copy"], text)
        if which("xclip"):
            return _pipe(["xclip", "-selection", "clipboard"], text)
    if system == "windows":
        return _pipe(["clip"], text)
    return False


def _pipe(command: list[str], text: str) -> bool:
    try:
        process = subprocess.Popen(command, stdin=subprocess.PIPE, text=True)
        process.communicate(text)
        return process.returncode == 0
    except OSError:
        return False

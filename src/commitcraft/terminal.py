from __future__ import annotations


def error(message: str) -> None:
    print(f"Error: {message}")


def section(title: str) -> None:
    print(f"\n{title}")
    print("=" * len(title))


def progress(percent: int) -> None:
    width = 20
    filled = max(0, min(width, round(width * percent / 100)))
    bar = "*" * filled + "-" * (width - filled)
    end = "\n" if percent >= 100 else ""
    print(f"\rProcessing [{bar}] {percent}%", end=end, flush=True)

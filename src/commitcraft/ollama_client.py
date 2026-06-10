from __future__ import annotations

from typing import Any

try:
    import requests
except ModuleNotFoundError:  # pragma: no cover
    requests = None  # type: ignore[assignment]

from commitcraft.exceptions import OllamaError


class OllamaClient:
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url.rstrip("/")

    def is_running(self) -> bool:
        if requests is None:
            return False
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except requests.RequestException:
            return False

    def generate(self, model: str, prompt: str) -> str:
        if requests is None:
            raise OllamaError("requests package is not installed")
        payload: dict[str, Any] = {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0.2},
        }
        try:
            response = requests.post(f"{self.base_url}/api/generate", json=payload, timeout=90)
            response.raise_for_status()
            return str(response.json().get("response", "")).strip()
        except requests.RequestException as exc:
            raise OllamaError(str(exc)) from exc

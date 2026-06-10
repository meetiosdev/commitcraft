from pathlib import Path

from commitcraft.file_context import filter_safe_diff, read_untracked_context, should_skip_path


def test_sensitive_file_skipped() -> None:
    assert should_skip_path(".env") == "sensitive file"
    assert should_skip_path("certs/app.key") == "sensitive file"


def test_binary_file_skipped() -> None:
    assert should_skip_path("resume.pdf") == "binary file"


def test_read_untracked_text_content(tmp_path: Path) -> None:
    file_path = tmp_path / "new.py"
    file_path.write_text("print('hello')\n")

    context = read_untracked_context(tmp_path, ["new.py"])

    assert "NEW FILE:" in context
    assert "print('hello')" in context


def test_filter_safe_diff_skips_env_content() -> None:
    diff = """diff --git a/.env b/.env
index 111..222 100644
--- a/.env
+++ b/.env
@@ -1 +1 @@
-SECRET=old
+SECRET=new
"""

    safe = filter_safe_diff(diff)

    assert "SECRET" not in safe
    assert "sensitive file" in safe

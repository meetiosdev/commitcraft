from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

from commitcraft import __version__
from commitcraft.clipboard import copy_text
from commitcraft.config import DEFAULT_MAX_CONTEXT, DEFAULT_MODEL, DEFAULT_OLLAMA_URL, Config
from commitcraft.fallback_generator import generate_fallback_messages, is_job_application_change
from commitcraft.git_reader import read_git_changes, validate_repo_path
from commitcraft.ollama_client import OllamaClient
from commitcraft.output_validator import is_valid_commit_output, is_weak_jobs_output
from commitcraft.prompt_builder import build_context, build_prompt, build_repair_prompt
from commitcraft.terminal import error, progress, section


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Suggest commit messages for a Git repo.")
    parser.add_argument("repo_path", nargs="?", help="Path to Git repository.")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="Ollama model.")
    parser.add_argument("--show-files", action="store_true", help="Print changed/untracked files.")
    parser.add_argument("--show-context", action="store_true", help="Print context sent to Ollama.")
    parser.add_argument("--max-context", type=int, default=DEFAULT_MAX_CONTEXT, help="Max context chars.")
    parser.add_argument("--copy", action="store_true", help="Copy all 3 messages to clipboard.")
    parser.add_argument("--debug", action="store_true", help="Show debug logs.")
    parser.add_argument("--version", action="version", version=f"commitcraft {__version__}")
    return parser


def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)
    logging.basicConfig(level=logging.DEBUG if args.debug else logging.WARNING)
    config = Config(model=args.model, max_context=args.max_context, debug=args.debug)

    try:
        repo_path = resolve_repo_path(args.repo_path)
        progress(20)
        changes = read_git_changes(repo_path)
        if not changes.all_files:
            print("No changes found.")
            return

        if args.show_files:
            section("FILES")
            for file in changes.all_files:
                print(file)

        progress(40)
        context = build_context(changes, config.max_context)
        if args.show_context:
            section("CONTEXT SENT TO OLLAMA")
            print(context)

        progress(60)
        client = OllamaClient(DEFAULT_OLLAMA_URL)
        progress(80)
        output = generate_output_with_retry(client, config, context, changes.all_files)
        progress(100)

        print(output.strip())

        if args.copy:
            print("\nCopied to clipboard." if copy_text(output) else "\nCould not copy to clipboard.")
    except Exception as exc:
        if args.debug:
            logging.exception("Command failed")
        if isinstance(exc, ValueError):
            error("Invalid repo path." if "Path" in str(exc) or "repository" in str(exc) else str(exc))
        else:
            error(str(exc))
        sys.exit(1)


def resolve_repo_path(repo_path: str | None) -> str:
    if repo_path:
        return repo_path

    entered = input("Enter repo path: ").strip()
    if entered:
        return entered

    cwd = str(Path.cwd())
    try:
        validate_repo_path(cwd)
    except ValueError as exc:
        raise ValueError("Repo path is required.") from exc
    return cwd


def generate_output_with_retry(
    client: OllamaClient,
    config: Config,
    context: str,
    files: list[str],
) -> str:
    if not client.is_running():
        error("Ollama is not running. Start it with: open -a Ollama")
        return generate_fallback_messages(files)

    try:
        output = client.generate(config.model, build_prompt(context))
    except Exception as exc:
        logging.debug("Ollama generation failed: %s", exc)
        error(f"Ollama generation failed: {exc}")
        return generate_fallback_messages(files)

    if is_valid_commit_output(output) and not _should_use_jobs_fallback(output, files):
        return output

    try:
        repaired = client.generate(config.model, build_repair_prompt(output))
    except Exception as exc:
        logging.debug("Ollama repair failed: %s", exc)
        return generate_fallback_messages(files)

    if is_valid_commit_output(repaired) and not _should_use_jobs_fallback(repaired, files):
        return repaired
    return generate_fallback_messages(files)


def _should_use_jobs_fallback(output: str, files: list[str]) -> bool:
    return is_job_application_change(files) and is_weak_jobs_output(output)

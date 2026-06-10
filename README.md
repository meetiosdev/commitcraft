# CommitCraft

Local read-only AI commit message suggestions powered by Ollama.

`commitcraft` is a local, read-only AI CLI that suggests clean Git commit messages for any repository.

It looks at staged changes, unstaged changes, and new untracked files, builds a safe summary, asks local Ollama for 3 Conventional Commit options, then prints only the final commit messages.

It never stages files. It never commits files. It never changes your repository.

## What You Get

```text
FULL DETAILED:
feat(api): add retry handling for failed requests

* add retry logic for temporary network failures
* surface clearer errors when requests keep failing
* update tests for successful and failed retry flows

MEDIUM:
feat(api): add retry handling and clearer request errors

ONE LINER:
feat(api): add request retry handling
```

## Key Features

- One short command: `commitcraft`
- Backward compatible aliases: `make_commit`, `make_commit_message`
- Interactive repo path prompt
- Works with staged, unstaged, and untracked files
- Reads untracked file content without running `git add`
- Uses local Ollama only
- Never sends code to cloud APIs
- Skips secrets, binary files, media, virtual environments, and build folders
- Shows clean progress by default
- Supports `--show-files`, `--show-context`, `--copy`, and custom models
- Falls back to safe local messages when Ollama is unavailable
- Uses path-aware heuristics to avoid weak or misleading commit messages

## Safety Promise

This tool is read-only.

It only runs safe Git read commands:

```bash
git rev-parse --is-inside-work-tree
git rev-parse --show-toplevel
git status --short
git diff
git diff --cached
git diff --name-only
git diff --cached --name-only
git ls-files --others --exclude-standard
```

It never runs:

```bash
git add
git commit
git reset
git checkout
```

It also never uses `shell=True`.

## Requirements

- macOS, Linux, or Windows
- Python 3.9+
- Git
- Ollama
- Local Ollama model, recommended: `qwen2.5-coder:7b`

## First-Time Setup

### 1. Open Project Folder

```bash
cd /path/to/commitcraft
```

### 2. Create Virtual Environment

```bash
python3 -m venv .venv
```

### 3. Activate Virtual Environment

macOS or Linux:

```bash
source .venv/bin/activate
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 4. Install Tool

```bash
pip install -e .
```

### 5. Verify Install

```bash
commitcraft --version
```

Expected:

```text
commitcraft 0.1.0
```

## Ollama Setup

### Install Ollama

macOS with Homebrew:

```bash
brew install ollama
```

Or install from:

```text
https://ollama.com
```

### Start Ollama

Option A, open Ollama app:

```bash
open -a Ollama
```

Option B, start from terminal:

```bash
ollama serve
```

### Download Recommended Model

```bash
ollama pull qwen2.5-coder:7b
```

Optional model:

```bash
ollama pull llama3.1:8b
```

## Daily Usage

### Best Simple Flow

```bash
cd /path/to/commitcraft
source .venv/bin/activate
commitcraft
```

Then enter target repo path:

```text
Enter repo path: /path/to/your/repo
```

The tool shows progress:

```text
Processing [****----------------] 20%
Processing [********------------] 40%
Processing [************--------] 60%
Processing [****************----] 80%
Processing [********************] 100%
```

Then it prints 3 commit messages.

### One-Line Command

```bash
commitcraft /path/to/your/repo
```

### Use Current Directory

If you are already inside a Git repo:

```bash
cd /path/to/your/repo
commitcraft
```

When asked for repo path, press Enter.

## Common Examples

### Show Files Too

```bash
commitcraft /path/to/your/repo --show-files
```

### Show Context Sent To Ollama

Use this only when debugging:

```bash
commitcraft /path/to/your/repo --show-context
```

### Copy Output To Clipboard

```bash
commitcraft /path/to/your/repo --copy
```

### Use Another Model

```bash
commitcraft /path/to/your/repo --model llama3.1:8b
```

### Increase Context Size

Default context size is `14000` characters.

```bash
commitcraft /path/to/your/repo --max-context 24000
```

### Debug Mode

```bash
commitcraft /path/to/your/repo --debug
```

## CLI Reference

```bash
commitcraft [repo_path] [options]
```

Old commands still work:

```bash
make_commit [repo_path] [options]
make_commit_message [repo_path] [options]
```

| Option | Description |
| --- | --- |
| `repo_path` | Optional Git repo path. If missing, tool asks interactively. |
| `--model MODEL` | Ollama model. Default: `qwen2.5-coder:7b`. |
| `--show-files` | Show changed, staged, unstaged, and untracked files. |
| `--show-context` | Show limited context sent to Ollama. |
| `--max-context N` | Max context characters. Default: `14000`. |
| `--copy` | Copy all 3 messages to clipboard. |
| `--debug` | Show debug logs. |
| `--version` | Show installed version. |

## How It Works

1. Validates repo path.
2. Finds repo root.
3. Reads Git status.
4. Reads staged diff.
5. Reads unstaged diff.
6. Reads untracked text files directly from disk.
7. Skips sensitive, binary, media, and generated folders.
8. Detects project type.
9. Builds safe context.
10. Sends context to local Ollama.
11. Validates Ollama output.
12. Retries once with a repair prompt if output is weak.
13. Falls back to local generator if needed.
14. Prints exactly 3 commit message options.

## Output Rules

The final output is always shaped like this:

```text
FULL DETAILED:
type(scope): summary

* bullet
* bullet
* bullet

MEDIUM:
type(scope): summary

ONE LINER:
type(scope): summary
```

## Sensitive File Handling

Content is never included for:

```text
.env
.env.local
.env.production
.pem
.key
.p12
.mobileprovision
google-services.json
GoogleService-Info.plist
.keystore
.jks
id_rsa
id_ed25519
```

Folders skipped:

```text
.git
node_modules
build
dist
.next
.venv
venv
Pods
.dart_tool
```

Binary and media content skipped:

```text
.pdf
.png
.jpg
.jpeg
.gif
.webp
.mp4
.mov
.zip
.tar
.gz
.dmg
```

## Supported Text Files

The tool can read limited content from:

```text
.py .js .ts .tsx .jsx .dart .swift .kt .java .php
.html .css .scss .md .json .yaml .yml .txt .sh
.tex .xml .toml .ini
```

Each untracked file is capped at `3000` characters. Total context is capped by `--max-context`.

## Project Type Detection

The tool detects:

- Flutter
- Android
- iOS
- React/Node
- WordPress/PHP
- Python
- General fallback

## Path-Aware Output

CommitCraft uses file paths, folders, and diffs together. If model output is too generic or focuses on the wrong files, CommitCraft retries once and can fall back to a safer local message.

Generic example:

```text
FULL DETAILED:
feat(api): add retry handling for failed requests

* add retry logic for temporary network failures
* surface clearer errors when requests keep failing
* update tests for successful and failed retry flows

MEDIUM:
feat(api): add retry handling and clearer request errors

ONE LINER:
feat(api): add request retry handling
```

This helps prevent weak messages like `chore: update files` when the real change is more specific.

## Troubleshooting

### `make_commit: command not found`

Activate the virtual environment:

```bash
cd /path/to/commitcraft
source .venv/bin/activate
```

Then reinstall:

```bash
pip install -e .
```

### `Ollama is not running`

Start Ollama:

```bash
open -a Ollama
```

Or:

```bash
ollama serve
```

### Model Missing

```bash
ollama pull qwen2.5-coder:7b
```

### Invalid Repo Path

Check path exists:

```bash
ls /path/to/your/repo
```

Check repo is Git repo:

```bash
cd /path/to/your/repo
git status
```

### No Changes Found

Make sure repo has changes:

```bash
git status --short
```

## Development

### Install For Development

```bash
cd /path/to/commitcraft
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
pip install -r requirements.txt
```

### Run Tests

```bash
python -m pytest
```

### Run Lint

```bash
ruff check .
```

### Run Compile Check

```bash
python3 -m compileall src tests
```

### Full Check

```bash
python3 -m compileall src tests
python -m pytest
ruff check .
```

## Project Structure

```text
commitcraft/
├── README.md
├── CHANGELOG.md
├── LICENSE
├── pyproject.toml
├── requirements.txt
├── requirements-dev.txt
├── .env.example
├── .gitignore
├── scripts/
│   └── install.sh
├── src/
│   └── commitcraft/
│       ├── __init__.py
│       ├── __main__.py
│       ├── cli.py
│       ├── clipboard.py
│       ├── config.py
│       ├── constants.py
│       ├── exceptions.py
│       ├── fallback_generator.py
│       ├── file_context.py
│       ├── git_reader.py
│       ├── models.py
│       ├── ollama_client.py
│       ├── output_validator.py
│       ├── project_detector.py
│       ├── prompt_builder.py
│       └── terminal.py
└── tests/
    ├── test_cli_retry.py
    ├── test_cli_ux.py
    ├── test_fallback_generator.py
    ├── test_file_context.py
    ├── test_output_validator.py
    └── test_project_detector.py
```

## Module Guide

| File | Purpose |
| --- | --- |
| `cli.py` | Parses commands, prompts for repo path, runs main flow. |
| `git_reader.py` | Reads Git status, diffs, and untracked files safely. |
| `file_context.py` | Filters sensitive files and builds safe file context. |
| `prompt_builder.py` | Builds Ollama prompt and repair prompt. |
| `ollama_client.py` | Talks to local Ollama API. |
| `output_validator.py` | Rejects assistant-style or weak output. |
| `fallback_generator.py` | Creates local fallback messages. |
| `project_detector.py` | Detects project type from files. |
| `clipboard.py` | Copies output on macOS, Linux, or Windows. |
| `terminal.py` | Handles clean progress and terminal output. |
| `constants.py` | Holds shared defaults and safety lists. |
| `models.py` | Holds small dataclasses for core data. |
| `exceptions.py` | Holds friendly custom exceptions. |

## Recommended Workflow

First time:

```bash
cd /path/to/commitcraft
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
open -a Ollama
ollama pull qwen2.5-coder:7b
```

Every day:

```bash
cd /path/to/commitcraft
source .venv/bin/activate
commitcraft /path/to/your/repo
```

Copy one of the generated messages, then commit manually in your repo:

```bash
cd /path/to/your/repo
git add .
git commit -m "feat(api): add request retry handling"
```

This final commit step is manual by design.

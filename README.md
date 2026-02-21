# Software Design Patterns & Algorithms — Tutorial Series

A Manim-based tutorial series explaining software design patterns and algorithms with animations and code.

## Prerequisites

- **Python 3.10+** (3.11 or 3.12 recommended; Manim does not support 3.13 yet)

## Setup (isolated env for you and your team)

All dependencies live in a **single virtual environment** so everyone can run the same setup:

```bash
# From the project root
cd /path/to/software-design-algorithms

# Create and activate virtual env
python3 -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate

# Install dependencies (Manim + its deps)
pip install -r requirements.txt

# Optional: upgrade pip first
pip install --upgrade pip && pip install -r requirements.txt
```

After that, `manim` is available only inside this env. Share the repo (and `requirements.txt`); teammates run the same three steps to get an identical environment.

## Structure

Each tutorial lives in its own folder: `NN-topic/` (e.g. `01-lexorank/`). Inside:

- **script.md** — Teleprompter / scene-by-scene narration
- **code/** — Code snippets referenced in the script
- **scenes/** — Manim scene files (`.py`)

See [PLAN.md](PLAN.md) for the full folder layout and workflow.

## Running animations

**Activate the venv first** (`source .venv/bin/activate`), then from the project root:

```bash
# Render a scene (low quality, preview)
manim -pql 01-lexorank/scenes/01_problem.py ProblemIntro

# Higher quality
manim -pqh 01-lexorank/scenes/01_problem.py ProblemIntro

# List all scenes in a file
manim -ql 01-lexorank/scenes/03_lexorank_algorithm.py
```

Or from inside a tutorial folder:

```bash
cd 01-lexorank
manim -pql scenes/01_problem.py ProblemIntro
```

Output (videos) goes to `media/` at the project root by default; this folder is gitignored.

## Tutorials

| #   | Topic     | Description                                      |
|-----|-----------|--------------------------------------------------|
| 01  | Lexorank  | Ordered list inserts without renumbering (Jira-style ranking) |

More to come.

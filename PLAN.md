# Tutorial Series: Software Design Patterns & Algorithms

Plan for a Manim-based tutorial series. Each tutorial is self-contained in its own folder with script, code snippets, and animations.

---

## Folder Structure

```
software-design-algorithms/
├── PLAN.md                    # This file — overall plan and conventions
├── README.md                  # Series intro, how to run, prerequisites
├── requirements.txt           # Python deps (e.g. manim, manim-slides if used)
│
├── 01-lexorank/               # Example: Lexorank algorithm
│   ├── script.md              # Teleprompter / scene-by-scene narration
│   ├── outline.md             # Optional: high-level outline / learning goals
│   ├── code/                  # Runnable or copy-paste code snippets
│   │   ├── naive_integers.py
│   │   ├── distance_integers.py
│   │   └── lexorank.py
│   └── scenes/                # Manim scene files (one file per “act” or topic)
│       ├── 01_problem.py      # Problem intro (drag-n-drop, integer limits)
│       ├── 02_distance_integers.py
│       └── 03_lexorank_algorithm.py
│
├── 02-ot-crdt/                # OT & CRDT (collaboration)
│   ├── script.md              # Teleprompter / storyboard
│   ├── outline.md             # Learning goals, scene list
│   ├── code/                  # Optional: ot_transform.py, crdt_sequence.py
│   └── scenes/                # 01_state_divergence.py … 05_summary_comparison.py
│
└── _templates/                # Optional: template script + scene stub
    ├── script-template.md
    └── scene-template.py
```

### Conventions

- **Tutorial folder names**: `NN-slug` (e.g. `01-lexorank`, `02-factory-pattern`).
- **script.md**: One section per “scene” or “act”; each section maps to one or more Manim scenes. Include:
  - Scene title / ID (matches scene class or file name).
  - Narration (teleprompter text).
  - Brief note on what appears on screen (for animator reference).
- **code/**: Small, focused snippets that the script refers to. Can be runnable or illustrative.
- **scenes/**: One Python file per logical “act”; each file can define multiple `Scene` subclasses. Naming: `NN_short_name.py` so render order is clear.

---

## Workflow

1. **Outline** (optional): Add `outline.md` with learning goals and scene list.
2. **Script**: Write `script.md` with scene IDs and full narration.
3. **Scenes**: Implement Manim scenes in `scenes/` to match script sections.
4. **Code**: Add snippets in `code/` and reference them in the script.
5. **Render**: From repo root or per-tutorial folder, e.g.  
   `manim -pql --disable_caching scenes/01_problem.py ProblemIntro`  
   (Use `--disable_caching` during development so font/layout/color changes show up; see README.)

---

## Lexorank Example: Scene Breakdown (for script.md + scenes)

| # | Scene ID / File      | Purpose |
|---|----------------------|--------|
| 1 | Problem intro        | Drag-n-drop list; positions as integers 1,2,3,…; “insert between 1 and 2” forces renumbering of all following items (costly). |
| 2a | Sparse integers — insert | Positions as 1000, 2000, 3000,…; insert between 1000 and 2000 → use 1500; no need to update others. |
| 2b | Sparse integers — rebalance | Gap runs out (1500, 1501, 1502); rebalance segment to respace. Rebalance *often* with sparse ints. |
| 3 | Lexorank algorithm   | String-based ranks and midpoint; rebalance *rare* (huge space 36^n). |

Each of these becomes one (or more) Manim scene classes and one section in `script.md`.

---

## Next Steps

- [ ] Add `README.md` and `requirements.txt`.
- [ ] Implement Lexorank `script.md` and all three scene files under `01-lexorank/`.
- [ ] Add `_templates/` if you want to clone structure for new tutorials.

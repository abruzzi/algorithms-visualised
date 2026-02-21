# Lexorank — Outline

## Learning goals

- Understand why plain integer positions are costly for drag-and-drop ordering.
- See how sparse (distance) integers reduce updates to a single write.
- Learn the idea of Lexorank: string ranks and lexicographic midpoint when the gap runs out.

## Scenes

1. **Problem** — List with positions 1..5; drag item to between 1 and 2; show cascade of DB updates.
2. **Sparse integers — insert** — Positions 1000, 2000, …; insert between → 1500; no renumbering.
3. **Sparse integers — rebalance** — Gap runs out (1500, 1501, 1502); rebalance segment to restore gaps. Rebalance happens *often*.
4. **Lexorank** — Switch to string ranks "a", "m", "z"; midpoint "a"–"m" → "g". Rebalance *rare*.
5. **Summary** (optional) — Four bullets: integers → sparse (rebalance often) → Lexorank (rebalance rare).

## Code snippets

- `code/naive_integers.py` — Integer positions and renumber loop.
- `code/distance_integers.py` — Sparse positions, `position_between`, and `rebalance_segment` (when gap runs out).
- `code/lexorank.py` — String rank, `mid_string`; `rebalance_ranks` (used rarely).

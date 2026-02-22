# Zoom-out layout options (ProblemIntro)

Ways to illustrate “5 elements vs many” when we zoom out. Current: **200 elements, 5 rows × 40 columns**, first column = our 5 (1–5), rest = 6–200.

---

## Option A — Current: first column = our 5, then 39 columns (200 total)

- **Grid:** 5 rows × 40 columns.
- **Column 0:** positions 1–5 (A, E, B, C, D) — the scene we just animated.
- **Columns 1–39:** positions 6–200 (small boxes).
- **Message:** “This column was your list; imagine 39 more like it.”

---

## Option B — Same idea, fewer elements (100 total)

- **Grid:** 5 rows × 20 columns.
- **Column 0:** 1–5 (our 5).
- **Columns 1–19:** 6–100.
- **Message:** Same story, less visual density.

---

## Option C — “199 columns next to it” (1000 total)

- **Grid:** 5 rows × 200 columns.
- **Column 0:** 1–5 (our 5).
- **Columns 1–199:** 6–1000.
- **Message:** “One column is what we looked at; 199 more columns of the same.”
- **Trade-off:** More elements, heavier to render; may need smaller scale/buff.

---

## Option D — One long row (200 total)

- **Layout:** One row: [1][2][3][4][5] then 6, 7, …, 200.
- **Message:** “We zoomed in on the first 5; the list continues to the right.”
- **Implementation:** `arrange(RIGHT)` one row; first 5 can stay slightly larger or same size as rest.

---

## Option E — Vertical list again (200 total)

- **Layout:** One column: 1, 2, 3, 4, 5, 6, …, 200 (all small).
- **Message:** “We were looking at the top 5; the list goes way down.”
- **Implementation:** Same as earlier vertical zoom-out, but only 200 items.

---

To switch: in `01_problem.py`, change `n_cols` and the ranges for `grid_cells` and `all_labels` to match the option you want.

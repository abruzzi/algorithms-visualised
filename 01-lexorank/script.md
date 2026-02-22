# Lexorank — Teleprompter Script

Scene-by-scene narration and on-screen notes for the Manim animations. Each scene has a rendered video example you can reference.

**Video examples (from project root):**

| Scene | 1080p60 | 4K (2160p60) |
|-------|---------|--------------|
| 1 Problem | `media/videos/01_problem/1080p60/ProblemIntro.mp4` | `media/videos/01_problem/2160p60/ProblemIntro.mp4` |
| 2a Sparse insert | `media/videos/02_distance_integers/1080p60/DistanceIntegers.mp4` | `media/videos/02_distance_integers/2160p60/DistanceIntegers.mp4` |
| 2b Sparse rebalance | `media/videos/03_sparse_rebalance/1080p60/SparseRebalance.mp4` | `media/videos/03_sparse_rebalance/2160p60/SparseRebalance.mp4` |
| 4 Lexorank insert | `media/videos/04_lexorank_insert/1080p60/LexorankInsert.mp4` | `media/videos/04_lexorank_insert/2160p60/LexorankInsert.mp4` |
| 5 Lexorank rebalance | `media/videos/05_lexorank_rebalance/1080p60/LexorankRebalance.mp4` | `media/videos/05_lexorank_rebalance/2160p60/LexorankRebalance.mp4` |

---

## Scene 1: The Problem (ProblemIntro)

**Video:** `media/videos/01_problem/2160p60/ProblemIntro.mp4` (or 1080p60 in same folder)

**On screen:** A simple drag-and-drop list (e.g. "Todo" or "Playlist"). Items labeled by position: 1, 2, 3, 4, 5. Cursor drags item 5 to between 1 and 2.

**Narration:**

> Imagine a drag-and-drop list — a playlist, a todo list, or a kanban board. Every item has a position. The naive approach is to store positions as integers: 1, 2, 3, 4, 5.
>
> Now you drag the last item to the top, between item 1 and item 2. Its new position should be 2. That means we have to renumber: the old 2 becomes 3, 3 becomes 4, 4 becomes 5. We might have to update every single item after the insertion point in the database. For a long list, that's a lot of writes — and it doesn't scale.

**Visual notes:** Show list, then drag, then a "cascade" or list of DB updates (e.g. UPDATE item SET position=3 WHERE id=…), to convey "many updates."

---

## Scene 2a: Sparse Integers — Insert (DistanceIntegers)

**Video:** `media/videos/02_distance_integers/2160p60/DistanceIntegers.mp4`

**On screen:** Same list, but positions are 1000, 2000, 3000, 4000, 5000. Insert a new item between 1000 and 2000; assign 1500. No other positions change.

**Narration:**

> A better idea: leave room between positions. Store 1000, 2000, 3000, 4000, 5000 instead of 1, 2, 3, 4, 5. Each pair is a thousand apart.
>
> When we insert between 1000 and 2000, we don't renumber anything. We just pick a number in between — say 1500. One write. No cascade. That's sparse integers — sometimes called gap-based or fractional-style indexing with integers.

**Visual notes:** Highlight the gap between 1000 and 2000; drop in 1500; other numbers stay fixed.

---

## Scene 2b: Sparse Integers — Gap Runs Out & Rebalance (SparseRebalance)

**Video:** `media/videos/03_sparse_rebalance/2160p60/SparseRebalance.mp4`

**On screen:** Keep inserting in the same gap: 1000, 1500, 1501, 1502, 2000. Highlight "no integer between 1501 and 1502". Then rebalance: respace the crowded segment (e.g. 1000, 1500, 1501, 1502, 2000 → 1000, 2000, 3000, 4000, 5000). Note: rebalance happens *often* with sparse integers.

**Narration:**

> If we keep inserting in the same spot, the gap fills up: 1500, then 1501, then 1502. Soon there's no integer between 1501 and 1502 — we have to rebalance. That means take that segment of items and respace them with the same initial gap again, so we have room for more inserts.
>
> With sparse integers, rebalance happens fairly often. Every time we exhaust the gap between two adjacent positions, we need to rebalance that segment again. So we get cheap inserts until the gap runs out, then a batch of updates to restore the gaps.

**Visual notes:** Show 1000, 1500, 1501, 1502, 2000; "Gap exhausted!"; then rebalance to 1000, 2000, 3000, 4000, 5000. Text: "Rebalance: often (each time gap runs out)."

---

## Scene 3: Lexorank — When the Gap Runs Out (LexorankAlgorithm)

*No rendered video in current set; optional slide deck. Concept covered in Scenes 4 and 5.*

**On screen:** Two ranks get too close (e.g. 1500 and 1501). Show that we can't fit another integer in between. Introduce string-based ranks in a small alphabet (e.g. "a", "m", "z") and show taking the "midpoint" between two strings to get a new rank. Note that rebalance is *rare*: we have 36^n possible ranks; only when we truly can't get a midpoint do we rebalance (or extend string length).

**Narration:**

> What happens when the gap runs out? After many inserts we might get 1500, 1501, 1502 — no integer between 1500 and 1501. We'd have to rebalance again.
>
> Lexorank solves this by using strings instead of integers. We choose a small alphabet — for example the 36 characters 0–9 and a–z. A rank is a string: "a", "m", "z". Order is lexicographic. When we need to insert between "a" and "m", we take the lexicographic midpoint — we get a new string in between, like "g". We have 36 to the power of n possible ranks for length n, so we run out of space much less often. If we ever do get too close, we can extend the string with more characters, or rebalance that range — but with Lexorank, rebalance is rare compared to sparse integers.

**Visual notes:** Show integer overflow problem; then switch to string ranks; one midpoint computation (e.g. "a" + "m" → "g"). Text: "Rebalance: rare (huge space; extend string or rebalance only when needed)."

---

## Scene 4: Lexorank — String Ranks & Midpoint Insert (LexorankInsert)

**Video:** `media/videos/04_lexorank_insert/2160p60/LexorankInsert.mp4`

**On screen:** List with string ranks "a", "b", "c", "d", "e". Insert new item between "a" and "b"; assign midpoint rank "am". Other ranks unchanged. One write, no cascade.

**Narration:**

> With Lexorank we use string ranks instead of numbers — for example "a", "b", "c", "d", "e". Order is lexicographic. When we insert between "a" and "b", we take the midpoint and get a new rank in between — here "am". One write. No renumbering. Same idea as sparse integers, but with a huge space of possible strings so we run out of room much less often.

**Visual notes:** Show ranks a–e; insert F between A and B with rank "am"; highlight that only the new item gets a new label.

---

## Scene 5: Lexorank — Gap Fills Up & Rebalance (LexorankRebalance)

**Video:** `media/videos/05_lexorank_rebalance/2160p60/LexorankRebalance.mp4`

**On screen:** Start with A–F (ranks a, am, b, c, d, e). Insert between "a" and "am" → "ag"; between "a" and "ag" → "ad". Gap fills up; rebalance to sparse ranks a–h. Updated ranks in yellow; rebalance is *rare* compared to sparse integers.

**Narration:**

> If we keep inserting in the same spot, the gap between two ranks eventually gets too small — we can't fit another midpoint. Then we rebalance: assign new sparse ranks over that segment, like a, b, c, d, e, f, g, h. With Lexorank this happens rarely, because the space of possible strings is huge. So we get the same one-write insert as sparse integers, but rebalance much less often.

**Visual notes:** Insert G ("ag"), H ("ad"); "Gap filling up" → rebalance to a–h; yellow = updated. Text: "Rebalance: rare (Lexorank)."

---

## Scene (optional): Summary (LexorankSummary)

*No rendered video in current set.*

**On screen:** Four bullets: (1) Integers → cascade updates. (2) Sparse integers → one write, gap runs out → rebalance *often*. (3) Lexorank → string ranks, midpoint, rebalance *rare*. (4) Trade-off: sparse = simple but frequent rebalance; Lexorank = more logic, rebalance rare.

**Narration:**

> So: integer positions cause expensive cascading updates. Sparse integers give us one write per insert until the gap runs out — then we rebalance that segment, and that happens fairly often. Lexorank uses string ranks and lexicographic midpoints so we have a huge space; rebalance is rare. In practice: sparse integers are simpler but need rebalance more often; Lexorank is a bit more involved but scales better with rare rebalances.

---

## Code References

- **Scene 1:** `code/naive_integers.py` — example of position as int and renumber loop.
- **Scene 2a / 2b:** `code/distance_integers.py` — sparse positions, `position_between`, and `rebalance_segment` (when gap runs out).
- **Scene 4 / 5:** `code/lexorank.py` — string rank, `mid_string`; rebalance rare, `rebalance_ranks` when needed.

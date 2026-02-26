# OT & CRDT — Teleprompter Script

One video (~10–12 min): **evolution and trade-offs** from conflict → LWW → OT → CRDT, including three-user examples. Scene-by-scene narration and on-screen notes.

**Video examples (from project root, after rendering with `-qk` for 4K):**

| Scene | File | Class | 1080p60 | 4K (2160p60) |
|-------|------|-------|---------|--------------|
| 1 Conflict | `01_conflict.py` | Conflict | `media/videos/01_conflict/1080p60/Conflict.mp4` | `media/videos/01_conflict/2160p60/Conflict.mp4` |
| 2 Naive / LWW | `02_lww.py` | NaiveLWW | `media/videos/02_lww/1080p60/NaiveLWW.mp4` | `media/videos/02_lww/2160p60/NaiveLWW.mp4` |
| 3 OT transform | `02_ot_transform.py` | OT | `media/videos/02_ot_transform/1080p60/OT.mp4` | `media/videos/02_ot_transform/2160p60/OT.mp4` |
| 4 CRDT commute | `04_crdt_commute.py` | CRDT | `media/videos/04_crdt_commute/1080p60/CRDT.mp4` | `media/videos/04_crdt_commute/2160p60/CRDT.mp4` |
| 5 Three-user OT | `05_ot_three_user_example.py` | ThreeUserOT | `media/videos/05_ot_three_user_example/1080p60/ThreeUserOT.mp4` | `media/videos/05_ot_three_user_example/2160p60/ThreeUserOT.mp4` |
| 6 Three-user CRDT | `06_crdt_three_user_example.py` | ThreeUserCRDT | `media/videos/06_crdt_three_user_example/1080p60/ThreeUserCRDT.mp4` | `media/videos/06_crdt_three_user_example/2160p60/ThreeUserCRDT.mp4` |

---

## Scene 1: The Conflict (Conflict)

**On screen:** Document "Hello" with positions 0–4. Label: "Both insert at position 0". User A inserts "X" → "XHello"; User B inserts "Y" → "YHello".

**Action:**
1. Show document "Hello" with position indices.
2. "Both insert at position 0" — then A inserts "X", B inserts "Y".
3. **Conflict:** Two possible outcomes; highlight "Conflict: both at position 0 — who wins?"

**Narration:**

> Two people edit the same document at once. We have "Hello". Both users insert at position 0: A inserts "X", B inserts "Y". Now we have a conflict: if we just apply one after the other, who wins? Index-based edits don't commute — we need a smarter way to merge.

**Visual notes:** Document label; character cells with positions; A (blue) and B (orange) inserts; final conflict callout in red.

---

## Scene 2: Naive / Last-Writer-Wins (NaiveLWW)

**On screen:** User A has "XHello" (X in blue); User B has "YHello" (Y in orange). Arrow down; merged result "YHello" with "A's edit lost" in red.

**Action:**
1. Show A's state and B's state stacked.
2. Merge (arrow down) → single result "YHello" (B wins).
3. Mark A's edit as lost (✗, "A's edit lost").

**Narration:**

> The naive approach is last-writer-wins: we take one version and drop the other. Here B's "YHello" overwrites A's "XHello". A's edit is lost — simple but bad for collaboration.

**Visual notes:** Two rows (A, B); arrow; single result; red "A's edit lost".

---

## Scene 3: OT — Transform to Preserve Intent (OT)

**On screen:** Document "Hello" in center. A's edit arrives first → "XHello". B: "insert Y at 0" → transform "0 → 1" → apply → "XYHello". "✓ both kept".

**Action:**
1. Start with "Hello"; A's edit first → "XHello".
2. B wants to insert "Y" at index 0. Show "Transform against A: 0 → 1", then apply B at index 1.
3. Result "XYHello" with both X (blue) and Y (orange). "✓ both kept".

**Narration:**

> Operational Transformation fixes this. A's edit is applied first, so we have "XHello". When B's "insert Y at 0" arrives, the server doesn't just apply it blindly — it **transforms** it. In the context of A's insert, index 0 is already taken; so B's op becomes "insert at 1". After transformation, we apply and get "XYHello". Both edits are kept. OT is the smart interceptor that preserves intent.

**Visual notes:** Doc in center; "Transform against A: 0 → 1"; final "XYHello" with both colors; green "✓ both kept".

---

## Scene 4: CRDT — Merge by ID (CRDT)

**On screen:** Linked list: each node (char, ID). "Hello" as (H,id0)→(e,id1)→(l,id2)→(l,id3)→(o,id4). A inserts a new node (X,A) after the start; B inserts (Y,B) after the start. Merge text: "Merge: both after start → order by ID (A < B) → X then Y". Result row: X(A), Y(B), then the original nodes, i.e. `XYHello`, with "✓ both kept".

**Action:**
1. Show linked list with IDs; label "each node = (char, ID)".
2. A inserts (X,A), B inserts (Y,B) right after the start node (before the original `H` node).
3. Merge step: highlight that both new nodes sit in the same logical spot ("after start"), so we break the tie by their IDs: `A < B`, so X comes before Y.
4. Show merged list `XYHello` with X (blue) and Y (orange) highlighted; "Result: XYHello (both kept)", "✓ both kept".

**Narration:**

> CRDTs take a different approach. We drop the central server. Each character has a **unique ID** — here the original characters use opaque IDs like `id0`, `id1`, and the new nodes from A and B use IDs `A` and `B`. When A inserts "X" with ID `A` and B inserts "Y" with ID `B`, both operations say "insert after the start node". When replicas sync, they don't have to transform indices; they just merge by structure: both nodes attach after the same parent, so we order them by their IDs — here `A < B` — and get X then Y. No matter which order those two operations arrive in, the merged list is `XYHello`. The edits **commute**, which is exactly what we want for P2P and offline-first systems.

**Visual notes:** Linked list with arrows; nodes with char + id below; merge label with ID highlight; final "XYHello", green check.

---

## Scene 5: Three-User OT (ThreeUserOT)

**On screen:** Document "Hello world". Order: C → B → A. Apply C → "Hi world"; transform B (6→3), apply → "Hi darkness"; transform A (6→3), apply → "Hi beautiful darkness". "✓ Hi beautiful darkness".

**Action:**
1. Initial "Hello world". Label "Order: C → B → A".
2. Apply C: "Hello" → "Hi" (teal).
3. Transform B's op (index 6→3), apply: "world" → "darkness" (orange).
4. Transform A's op (index 6→3), apply: insert "beautiful" (blue) at correct position.
5. Final "Hi beautiful darkness" with all three colors; green check.

**Narration:**

> With three users, OT still works: we impose a total order — here C, then B, then A. Each later operation is transformed against the ones already applied. C changes "Hello" to "Hi"; B's "replace at 6" is transformed to the right index and we get "darkness"; A's insert is transformed and we get "beautiful" in the right place. Everyone converges to "Hi beautiful darkness".

**Visual notes:** Single doc in center; step labels (Apply C →, Transform B (6→3), Transform A (6→3)); word cells with colors; final green line.

---

## Scene 6: Three-User CRDT (ThreeUserCRDT)

**On screen:** Same goal as OT: "Hello world" → "Hi beautiful darkness". Step labels below the doc: "Apply C (Hello→Hi) →", then "Apply B (world→darkness) →", then "Apply A (insert 'beautiful') →". The document row transforms in place, ending at `Hi beautiful darkness` with a green "✓ Hi beautiful darkness" line below.

**Action:**
1. Start from "Hello world", exactly as in the OT scene.
2. Step label: "Apply C (Hello→Hi) →" (teal). Replace "Hello" with "Hi" (teal) while keeping "world". Same spacing and layout as in the OT scene.
3. Step label: "Apply B (world→darkness) →" (orange). Replace "world" with "darkness" (orange); result `Hi darkness`.
4. Step label: "Apply A (insert 'beautiful') →" (blue). Insert "beautiful" between `Hi` and `darkness`, using the same spacing and colors as the OT version. Final row: `Hi beautiful darkness`.
5. Show "✓ Hi beautiful darkness" underneath.

**Narration:**

> With a CRDT, we can tell the exact same story from a different angle. Each user’s edit is a separate operation attached to the structure: C rewrites the node for "Hello" into "Hi", B rewrites the node for "world" into "darkness", and A inserts a new node for "beautiful" between them. Because those operations are keyed by stable IDs on the nodes, we can apply them in any order and still converge to the same document — here "Hi beautiful darkness". In the animation we show one ordering, but a real CRDT guarantees they still commute even if C, B, and A arrive in a different order or on different replicas.

**Visual notes:** Same layout and timing as the OT three-user scene: a single doc row in the center, one changing label below, color-coded words (`Hi` teal, `beautiful` blue, `darkness` orange), and a final green confirmation line.

---

## Code references

- **Scenes:** `02-ot-crdt/scenes/` — `01_conflict.py` (Conflict), `02_lww.py` (NaiveLWW), `02_ot_transform.py` (OT), `04_crdt_commute.py` (CRDT), `05_ot_three_user_example.py` (ThreeUserOT), `06_crdt_three_user_example.py` (ThreeUserCRDT).
- **Style:** Shared `common.py` matches 01-lexorank (Fira Code, dark background, rounded cells, timing constants).
- **Lexorank (01-lexorank):** Sequence CRDTs often use ordering schemes like Lexorank for conflict-free ordering; CRDT scene uses (char, id) nodes in a linked list.

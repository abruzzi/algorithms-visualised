# OT & CRDT — Outline

## Learning goals

- Understand the **state divergence** problem: concurrent edits with indices lead to wrong results (e.g. delete wrong character).
- See **Operational Transformation (OT)** as a central-server approach: transform operations so they apply correctly in different orders.
- Recognize **OT’s downsides**: central server, complex N-way concurrency, sync conflicts when offline or under latency.
- See **CRDT** as a decentralized alternative: operations commute (order doesn’t matter), so P2P / offline-first is natural.
- Compare **architecture and trade-offs**: when to choose OT vs CRDT (centralized vs decentralized, complexity vs memory).

## Scenes

1. **State divergence (pain point)** — String `"ABC"`. User A inserts `'X'` at 0 → `XABC`. User B deletes at index 2 (intending `'C'`). If B’s op is applied blindly on A’s state, it deletes `'B'`. Show why naive “last writer wins” or index-based ops break.
2. **OT: the correction logic** — Central server; A and B send ops; server runs **transformation**; e.g. B’s `Delete(2)` becomes `Delete(3)` before reaching A. Both converge to `XAB`.
3. **OT hell** — Multiple users, overlapping edits, server as bottleneck; sync conflict or offline → users locked / out of sync. OT is heavy, centralized, and hard for N-way.
4. **CRDT: commutative logic** — No central server; P2P. Use **unique IDs** per character (e.g. Lexorank-style or LWW). A adds `X_id0`, B deletes `C_id3`. Sync in any order → same final state. Show commutativity.
5. **Summary comparison** — Table: Architecture (centralized vs decentralized), Complexity, Examples (Google Docs vs Figma/Automerge), Best for (heavy text vs real-time/P2P/offline-first).

## Code / references

- **OT:** Conceptual transform function (e.g. `transform(Delete(2), Insert(0,'X'))` → adjusted indices). Optional snippet in `code/ot_transform.py`.
- **CRDT:** Sequence CRDT with unique IDs (can reference Lexorank for ordering). Optional snippet in `code/crdt_sequence.py`.
- **Link to Lexorank:** Sequence CRDTs often use ordering schemes like Lexorank for conflict-free ordering.

## Manim scene files (to implement)

| # | File | Scene class | Purpose |
|---|------|-------------|---------|
| 1 | `01_state_divergence.py` | StateDivergence | Pain point: ABC, A inserts X at 0, B deletes index 2 → wrong char deleted |
| 2 | `02_ot_transform.py` | OTTransform | Server; ops transformed; Delete(2)→Delete(3); converge to XAB |
| 3 | `03_ot_hell.py` | OTHell | Many users, bottleneck, sync conflict / offline |
| 4 | `04_crdt_commute.py` | CRDTCommute | P2P, IDs, A add X_id0 / B delete C_id3, any order → same state |
| 5 | `05_summary_comparison.py` | SummaryComparison | Table: OT vs CRDT (architecture, complexity, examples, best for) |

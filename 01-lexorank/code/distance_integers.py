# Sparse integers (gap-based / fractional-style with ints): leave room between positions.
# e.g. 1000, 2000, 3000 -> insert between 1000 and 2000 -> 1500 (one write).
# When gap runs out (prev + 1 == next), we must rebalance — and that happens often.

INITIAL_GAP = 1000


def position_between(prev: int, next: int) -> int | None:
    """Pick an integer between prev and next. Returns None if no room (gap exhausted)."""
    if next - prev <= 1:
        return None  # need rebalance
    return (prev + next) // 2


def rebalance_segment(
    items: list[dict], start_index: int, end_index: int, gap: int = INITIAL_GAP
) -> None:
    """
    Respace a contiguous segment so positions are gap apart again.
    Use when the gap between adjacent positions has run out (rebalance happens often).
    """
    n = end_index - start_index + 1
    base = items[start_index - 1]["position"] + gap if start_index > 0 else gap
    for i in range(n):
        items[start_index + i]["position"] = base + i * gap


# Example: positions 1000, 2000, 3000, 4000, 5000
items = [
    {"id": "a", "position": 1000},
    {"id": "b", "position": 2000},
    {"id": "c", "position": 3000},
    {"id": "d", "position": 4000},
    {"id": "e", "position": 5000},
]
# Insert between 1000 and 2000 -> 1500. Other positions unchanged.
new_pos = position_between(1000, 2000)  # 1500

# After many inserts: 1000, 1500, 1501, 1502, 2000 — no integer between 1501 and 1502
crowded = [
    {"id": "a", "position": 1000},
    {"id": "x", "position": 1500},
    {"id": "y", "position": 1501},
    {"id": "z", "position": 1502},
    {"id": "b", "position": 2000},
]
# Rebalance segment [x,y,z] (indices 1..3) to 2000, 3000, 4000
rebalance_segment(crowded, 1, 3)
# -> 1000, 2000, 3000, 4000, 2000 (then we'd fix 'b' to 5000 in a full impl)

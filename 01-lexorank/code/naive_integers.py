# Naive approach: positions as integers 1, 2, 3, ...
# Inserting between 1 and 2 forces renumbering all following items.

def insert_at(items: list[dict], new_item: dict, after_index: int) -> None:
    """Insert new_item after position after_index. Renumbers all following items."""
    new_pos = after_index + 1
    for i in range(after_index + 1, len(items)):
        items[i]["position"] = items[i]["position"] + 1  # cascade update
    items.insert(after_index + 1, {**new_item, "position": new_pos})


# Example: list with positions 1..5; insert between 1 and 2
items = [
    {"id": "a", "position": 1},
    {"id": "b", "position": 2},
    {"id": "c", "position": 3},
    {"id": "d", "position": 4},
    {"id": "e", "position": 5},
]
# After moving "e" between "a" and "b": we must set b=3, c=4, d=5, then insert e at 2.
# That's 4 updates instead of 1.

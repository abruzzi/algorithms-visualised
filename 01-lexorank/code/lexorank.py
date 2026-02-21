# Lexorank: string-based ranks in a small alphabet.
# Order is lexicographic. Insert between "a" and "m" by taking midpoint -> "g".
# Rebalance is rare: we have 36^n possible ranks; only when we can't get a midpoint.

import string

# Typical alphabet: 0-9 and a-z (36 chars). Jira uses similar.
ALPHABET = string.digits + string.ascii_lowercase


def mid_string(prev: str, next: str) -> str:
    """
    Lexicographic midpoint between prev and next.
    With 36^n possible ranks, we run out of room rarely; only then rebalance.
    """
    n = max(len(prev), len(next))
    prev = prev.ljust(n, "0")
    next = next.ljust(n, ALPHABET[-1])
    result = []
    for i in range(n):
        p = ALPHABET.index(prev[i]) if i < len(prev) else 0
        q = ALPHABET.index(next[i]) if i < len(next) else len(ALPHABET) - 1
        mid = (p + q) // 2
        result.append(ALPHABET[mid])
    return "".join(result).rstrip("0") or ALPHABET[0]


def rebalance_ranks(ranks: list[str], alphabet: str = ALPHABET) -> list[str]:
    """
    Respace a list of ranks evenly in the alphabet. Used rarely when
    we've exhausted midpoints in a region (much rarer than with sparse integers).
    """
    k = len(ranks)
    if k <= 1:
        return ranks
    # Simple rebalance: assign ranks spread across the alphabet (e.g. "a", "m", "z" for 3)
    step = len(alphabet) // (k + 1)
    return [alphabet[1 + i * step] for i in range(k)]


# Example: ranks "a", "m", "z". Insert between "a" and "m" -> "g"
print(mid_string("a", "m"))  # -> "g"
# Rebalance needed only when mid_string returns None — rare in practice.

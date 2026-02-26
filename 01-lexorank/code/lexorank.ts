/**
 * Lexorank — string-based ordering for lists (e.g. drag-and-drop).
 * Ranks are strings in a small alphabet; order is lexicographic.
 * Insert between two ranks by taking the lexicographic midpoint (e.g. "a"–"m" → "g").
 * Rebalance is rare: we have alphabetSize^n possible ranks.
 *
 * See: 01-lexorank tutorial (sparse integers → Lexorank when gap runs out).
 */

// Typical alphabet: 0–9 and a–z (36 chars). Jira and others use similar.
const ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyz";

/**
 * Lexicographic midpoint between prev and next rank.
 * Pads shorter string so we can compute position between them.
 * Returns a new rank strictly between prev and next (when they differ).
 */
function midString(prev: string, next: string, alphabet: string = ALPHABET): string {
  const n = Math.max(prev.length, next.length);
  const prevPadded = prev.padEnd(n, alphabet[0]);
  const lastChar = alphabet[alphabet.length - 1];
  const nextPadded = next.padEnd(n, lastChar);

  const result: string[] = [];
  for (let i = 0; i < n; i++) {
    const p = alphabet.indexOf(prevPadded[i]);
    const q = alphabet.indexOf(nextPadded[i]);
    const mid = Math.floor((p + q) / 2);
    result.push(alphabet[mid]);
  }
  const raw = result.join("").replace(new RegExp(`${alphabet[0]}+$`), "");
  return raw || alphabet[0];
}

/**
 * Respace a list of ranks evenly in the alphabet.
 * Use rarely when midString can't find a new rank (e.g. prev and next adjacent).
 */
function rebalanceRanks(ranks: string[], alphabet: string = ALPHABET): string[] {
  const k = ranks.length;
  if (k <= 1) return [...ranks];
  const step = Math.floor(alphabet.length / (k + 1));
  return Array.from({ length: k }, (_, i) => alphabet[1 + i * step]);
}

// ---------------------------------------------------------------------------
// Demo: core logic
// ---------------------------------------------------------------------------
function demo() {
  console.log("Lexorank — core logic\n");

  // Insert between "a" and "m" → "g"
  const betweenAM = midString("a", "m");
  console.log('midString("a", "m") =>', JSON.stringify(betweenAM));

  // Initial list: "a", "m", "z". Insert at start: between "" and "a"
  const atStart = midString("", "a");
  console.log('midString("", "a") =>', JSON.stringify(atStart));

  // Insert after last: between "z" and "zz" (use a high sentinel in practice)
  const afterZ = midString("z", "zz");
  console.log('midString("z", "zz") =>', JSON.stringify(afterZ));

  // Rebalance when we have too many ranks in a tight range
  const crowded = ["a", "b", "c", "d"];
  const respaced = rebalanceRanks(crowded);
  console.log("\nrebalanceRanks([\"a\", \"b\", \"c\", \"d\"]) =>", respaced);
}

demo();

export { ALPHABET, midString, rebalanceRanks };

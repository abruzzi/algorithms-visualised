# Yjs API basics

Short reference for the Yjs APIs used in this project. Enough to read the code and try small changes.

---

## How this app uses Yjs

- **Server:** One `Y.Doc` per room; `doc.getText("content")` starts as `"Hello world"`. On WebSocket connect, the server sends `Y.encodeStateAsUpdate(doc)`. When it receives an update from a client, it does `Y.applyUpdate(doc, update, "remote")` and broadcasts the same update to other clients.
- **Client:** Creates a `Y.Doc` and `doc.getText("content")`. Connects via WebSocket; on message, applies with `Y.applyUpdate(doc, data, "remote")`. Sends local changes with `doc.on("update", (update, origin) => { if (origin !== "remote") ws.send(update) })`.
- **Binding to the textarea:** `text.observe(event => { ... })` runs when the shared text changes. If `event.origin === "remote"`, we update the textarea and **transform the cursor** using `event.delta` (insert/delete/retain) so the selection doesn’t jump. On user input we diff the new value against the old, then call `text.insert()` / `text.delete()` so the local doc stays in sync.

---

## 1. Core ideas

- **Y.Doc** — One shared document. Each client has its own `Y.Doc`; you sync by sending *updates* (binary) and applying them on the other side.
- **Shared types** — The doc holds **shared types**: `Y.Text`, `Y.Map`, `Y.Array`. Each is a CRDT; merging updates from another doc gives the same result regardless of order.
- **Names** — `doc.getText("content")` / `doc.getMap("shared")`: the string is a **name** (key) for that shared type. Same name in synced docs = same logical structure.

## 2. Create doc and get shared types

```js
import * as Y from "yjs";

const doc = new Y.Doc();
const text  = doc.getText("content");   // shared string
const map   = doc.getMap("shared");     // key-value map
const array = doc.getArray("items");    // shared array
```

First call with a name creates that type; later calls return the same instance.

## 3. Y.Text

| Method | Description |
|--------|-------------|
| `text.insert(index, string)` | Insert at position (0-based). |
| `text.delete(index, length)` | Delete `length` chars from `index`. |
| `text.toString()` | Current string. |

## 4. Y.Map

| Method | Description |
|--------|-------------|
| `map.set(key, value)` | Set key to value. |
| `map.get(key)` | Get value or `undefined`. |
| `map.has(key)` | Whether key exists. |
| `map.delete(key)` | Remove key. |

## 5. Y.Array

| Method | Description |
|--------|-------------|
| `array.push(...items)` | Append. |
| `array.insert(index, items)` | Insert at index. |
| `array.delete(index, length)` | Remove elements. |
| `array.toArray()` | Copy as plain JS array. |

## 6. Syncing: encode and apply

| API | Description |
|-----|-------------|
| `Y.encodeStateAsUpdate(doc)` | Serialize full doc state to `Uint8Array`. |
| `Y.applyUpdate(doc, update)` | Merge an update into the doc. |

Typical flow: one “root” doc with initial state; clients apply that to start. Then they exchange updates (e.g. over WebSocket); each applies received updates with an **origin** so they don’t re-send them:

```js
doc.on("update", (update, origin) => {
  if (origin === "remote") return;
  sendToServer(update);
});
onMessage((update) => Y.applyUpdate(doc, update, "remote"));
```

## 7. Delta and cursor transformation

When you observe `Y.Text` changes, the event can include a **delta** (e.g. `event.delta` or `event.changes.delta`): an array of `{ insert: string }`, `{ delete: number }`, or `{ retain: number }` describing what changed. This app uses that delta to **transform the cursor**: if someone inserted 5 characters before your cursor, your cursor index increases by 5; if they deleted 3 characters before your cursor, it decreases (or clamps to the delete position if your cursor was inside the deleted range). That way, when we set `textarea.value = text.toString()` after a remote update, we also set `textarea.setSelectionRange(newStart, newEnd)` with the transformed indices so the cursor doesn’t jump to the end or conflict with the other user’s edit.

## 8. Quick reference

| Goal | Use |
|------|-----|
| New document | `new Y.Doc()` |
| Shared text | `doc.getText("content")` |
| Insert/delete text | `text.insert(i, s)`, `text.delete(i, len)` |
| Read text | `text.toString()` |
| Serialize for sync | `Y.encodeStateAsUpdate(doc)` |
| Apply received sync | `Y.applyUpdate(doc, update, "remote")` |
| React to changes | `text.observe(callback)` or `doc.on("update", ...)` |

## 9. Three-users “Hello world” (same as OT/CRDT doc)

- Initial: `"Hello world"`.
- A: insert `"beautiful "` at index 6.
- B: replace `"world"` with `"darkness"` (delete 6,5 then insert `"darkness"`).
- C: replace `"Hello"` with `"Hi"` (delete 0,5 then insert `"Hi"`).

After merging all three docs: `"Hi beautiful darkness"`. Yjs (CRDT) merges by structure/IDs; no transform step—just exchange updates.

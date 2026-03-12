# 04 — CRDT in action

Live collaborative text demo using **Yjs** (a CRDT library) over WebSocket. One shared document; open the page in multiple tabs or devices to see edits sync in real time.

---

## What this demo shows

**CRDT** (Conflict-free Replicated Data Type) lets multiple users edit the same document at the same time without a central server deciding “who wins.” Each client applies the same merge rules, so everyone ends up with the same text no matter what order updates arrive in.

This app is a minimal example: one shared text field (initial value `"Hello world"`), synced over WebSocket. When you type in one tab, the others update immediately. No Operational Transform (OT) or central conflict resolution—just Yjs merging updates by structure.

---

## Quick start

```bash
cd 04-crdt-in-action
npm install
npm start
```

Open **http://localhost:3456** in two or more tabs (or windows). Edit the text in any tab; changes appear in the others. You can also open the same URL on another device on your network (use your machine’s IP and port 3456).

---

## How it works

### Server

- **Express** serves the static page (HTML, CSS, JS).
- A **WebSocket** server runs on the same port. It keeps one **Y.Doc** per room (default room: `"default"`). That doc holds the shared `Y.Text("content")` with initial value `"Hello world"`.
- **When a client connects:** the server sends the full document state (`Y.encodeStateAsUpdate(doc)`) so the new client gets the current text.
- **When the server receives an update from a client:** it applies the update to the server’s doc and **broadcasts** the same update to every other connected client. It does not send the update back to the sender.

So the server is a simple relay: one source of truth (the server’s doc), and everyone gets the same updates.

### Client

- Each tab has its own **Y.Doc** and a **WebSocket** connection to the server.
- **Shared text** is `doc.getText("content")`, bound to the page’s `<textarea>`.
- **When the user types:** the client diffs the new text against the previous value (common prefix/suffix), then applies the corresponding `text.insert()` and `text.delete()` to the local Y.Doc. Yjs emits an update; the client sends that update to the server (only for local edits, not for updates that came from the network).
- **When the client receives an update from the server:** it applies the update with `Y.applyUpdate(doc, update, "remote")`. The `"remote"` origin ensures the client does not send this same update back. The Y.Text changes, so the **observe** callback runs: the textarea is updated to the new string, and the **cursor/selection is transformed** using the change delta so your cursor doesn’t jump to the end when someone else types (e.g. if they insert text before your cursor, your cursor position is shifted forward).

### Why “origin” matters

If the client sent every doc change (including changes caused by applying remote updates) back to the server, the server would broadcast them again and you’d get duplicate or looping updates. So we mark updates that came from the network with origin `"remote"` and only send updates that are not from the network. That’s the same pattern as in the “simulated network” example (example 5) in the Yjs draft.

---

## Simulating multiple users

- **Same machine:** open **http://localhost:3456** in several tabs or windows. Each tab is one “user”; edits in one appear in the others.
- **Same network:** run `npm start`, find your machine’s IP (e.g. `192.168.1.x`), and on another device open **http://&lt;your-IP&gt;:3456**.
- **Try the “three users” scenario:** open three tabs, all starting with `"Hello world"`. In tab A, insert `"beautiful "` between “Hello” and “world”. In tab B, replace “world” with “darkness”. In tab C, replace “Hello” with “Hi”. After sync, all tabs should show **"Hi beautiful darkness"** (same outcome as in the OT/CRDT doc and your Yjs example 4).

---

## Cursor and selection

When another client’s edit is applied, the textarea content is replaced. If we kept the same numeric cursor index, the cursor would end up in the wrong place (or at the end). So on **remote** updates we use the **delta** from the Y.Text observe event (insert/delete/retain operations) to **transform** the current selection: if text was inserted before your cursor, the cursor moves forward; if text was deleted before your cursor, it moves back. That way your cursor and selection stay logically in the same place instead of conflicting with the other user’s edit.

---

## Stack

| Part | Role |
|------|------|
| **Server** | Express (static) + WebSocket (`ws`). One `Y.Doc` per room; initial text `"Hello world"`. On connect: send full state; on message: apply update and broadcast to other clients. |
| **Client** | Vanilla JS + Yjs (ESM from esm.sh). `Y.Doc` + `Y.Text("content")` bound to `<textarea>`. Observe → update textarea and transform cursor; input → diff and apply insert/delete. Updates sent only when origin is not `"remote"`. |

---

## Structure

| Path | Purpose |
|------|---------|
| `server.js` | Express + WebSocket server; Y.Doc per room; initial "Hello world" |
| `public/index.html` | Single page: shared textarea, connection status |
| `public/js/app.js` | Y.Doc, WebSocket, Y.Text ↔ textarea binding, cursor transform |
| `public/css/style.css` | Minimal layout |
| `docs/yjs-api-basics.md` | Short Yjs API reference and how this app uses it |

---

## Room

Default room is `"default"`. To use another room, open:

`http://localhost:3456?room=myroom`

and ensure the WebSocket connects with `?room=myroom`. The server keeps one Y.Doc per room name.

---

## Relation to the draft

- The **three-users “Hello world”** scenario (A: insert "beautiful ", B: replace "world" → "darkness", C: replace "Hello" → "Hi" → merged "Hi beautiful darkness") is the same semantics; here it’s live over the network instead of in-process.
- **Sync pattern:** Server holds the canonical doc; clients send updates, server applies and broadcasts. We use origin `"remote"` when applying received updates so clients don’t re-send them—same idea as your example 5 (simulated network).

---

## More on Yjs

See **`docs/yjs-api-basics.md`** for a short API reference (Y.Doc, Y.Text, Y.Map, Y.Array, encode/apply, observe/delta) and how it’s used in this app.

/**
 * CRDT in action — client: Y.Doc + WebSocket, bind Y.Text to textarea.
 * Uses origin "remote" when applying server updates so we don't re-send them.
 */
import * as Y from "https://esm.sh/yjs@13.6.20";

const REMOTE = "remote";
const wsScheme = location.protocol === "https:" ? "wss:" : "ws:";
const wsUrl = location.host ? `${wsScheme}//${location.host}` : "ws://localhost:3456";

const statusEl = document.getElementById("status");
const textarea = document.getElementById("content");

const doc = new Y.Doc();
const text = doc.getText("content");

let ws;
let ignoreNextInput = false;

function setStatus(msg, className = "") {
  statusEl.textContent = msg;
  statusEl.className = "status " + className;
}

function connect() {
  ws = new WebSocket(wsUrl);

  ws.binaryType = "arraybuffer";
  ws.onopen = () => setStatus("Connected", "connected");
  ws.onclose = () => setStatus("Disconnected", "error");
  ws.onerror = () => setStatus("Connection error", "error");

  ws.onmessage = (event) => {
    const data = new Uint8Array(event.data);
    Y.applyUpdate(doc, data, REMOTE);
  };
}

// Transform cursor (start, end) by a Y.Text delta so it stays in the right place after remote edits
function transformCursorByDelta(start, end, delta) {
  if (!delta || !Array.isArray(delta)) return { start, end };
  let pos = 0;
  let s = start;
  let e = end;
  for (const op of delta) {
    if (op.retain != null) {
      pos += op.retain;
    } else if (op.insert != null) {
      const len = typeof op.insert === "string" ? op.insert.length : 1;
      if (pos <= s) s += len;
      if (pos <= e) e += len;
      pos += len;
    } else if (op.delete != null) {
      const n = op.delete;
      s = s <= pos ? s : s < pos + n ? pos : s - n;
      e = e <= pos ? e : e < pos + n ? pos : e - n;
      pos += n;
    }
  }
  return { start: s, end: e };
}

// Sync Y.Text → textarea (only on remote updates; transform cursor so it doesn't jump)
text.observe((event) => {
  const origin = event.origin ?? event.transaction?.origin;
  const value = text.toString();
  const delta = event.delta ?? event.changes?.delta;

  if (origin === REMOTE) {
    const start = textarea.selectionStart;
    const end = textarea.selectionEnd;
    const { start: newStart, end: newEnd } = transformCursorByDelta(start, end, delta);
    ignoreNextInput = true;
    textarea.value = value;
    const len = value.length;
    textarea.setSelectionRange(Math.max(0, Math.min(newStart, len)), Math.max(0, Math.min(newEnd, len)));
  } else if (textarea.value !== value) {
    textarea.value = value;
  }
});

// Sync textarea → Y.Text (simple diff: common prefix/suffix)
textarea.addEventListener("input", () => {
  if (ignoreNextInput) {
    ignoreNextInput = false;
    return;
  }
  const oldVal = text.toString();
  const newVal = textarea.value;
  let i = 0;
  while (i < oldVal.length && i < newVal.length && oldVal[i] === newVal[i]) i++;
  let j = 0;
  while (
    j < oldVal.length - i &&
    j < newVal.length - i &&
    oldVal[oldVal.length - 1 - j] === newVal[newVal.length - 1 - j]
  )
    j++;
  const deleteFrom = i;
  const deleteLen = oldVal.length - i - j;
  const insertStr = newVal.slice(i, newVal.length - j);
  if (deleteLen > 0) text.delete(deleteFrom, deleteLen);
  if (insertStr.length > 0) text.insert(deleteFrom, insertStr);
});

// Send local updates to server (don't send remote)
doc.on("update", (update, origin) => {
  if (origin === REMOTE) return;
  if (ws && ws.readyState === WebSocket.OPEN) {
    ws.send(update);
  }
});

connect();

// Initial render from doc (in case we had state before first sync)
if (text.length > 0) {
  textarea.value = text.toString();
}

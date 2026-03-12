/**
 * CRDT in action: Express + WebSocket server.
 * One Y.Doc per room (default: "default"); initial text "Hello world".
 * On connect: send full state. On message: apply update to server doc, broadcast to other clients.
 */
import express from "express";
import { WebSocketServer } from "ws";
import { createServer } from "http";
import * as Y from "yjs";
import { fileURLToPath } from "url";
import { dirname, join } from "path";

const __dirname = dirname(fileURLToPath(import.meta.url));
const PORT = process.env.PORT || 3456;

const app = express();
app.use(express.static(join(__dirname, "public")));

const httpServer = createServer(app);
const wss = new WebSocketServer({ server: httpServer });

const docs = new Map();

function getOrCreateDoc(roomName) {
  if (!docs.has(roomName)) {
    const doc = new Y.Doc();
    doc.getText("content").insert(0, "Hello world");
    docs.set(roomName, doc);
  }
  return docs.get(roomName);
}

wss.on("connection", (ws, req) => {
  const url = new URL(req.url || "", `http://${req.headers.host}`);
  const roomName = url.searchParams.get("room") || "default";
  const doc = getOrCreateDoc(roomName);

  const state = Y.encodeStateAsUpdate(doc);
  ws.send(state, { binary: true });

  ws.on("message", (data, isBinary) => {
    if (!isBinary || !(data instanceof Buffer)) return;
    Y.applyUpdate(doc, new Uint8Array(data), "remote");
    wss.clients.forEach((client) => {
      if (client !== ws && client.readyState === 1) {
        client.send(data, { binary: true });
      }
    });
  });
});

httpServer.listen(PORT, () => {
  console.log(`CRDT in action: http://localhost:${PORT}`);
  console.log(`WebSocket: ws://localhost:${PORT} (room=default)`);
});

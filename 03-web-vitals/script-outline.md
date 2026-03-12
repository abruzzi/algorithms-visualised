# Video script outline: Core Web Vitals (LCP, CLS, INP) — ~7 min

Content aligned with code demos (before/after HTML/JS) and Manim scenes. Use this structure for another pass to refine language.

---

## 0. Intro (0:00–0:35)

- **What:** Core Web Vitals = three metrics Google uses for page experience (and SEO).
- **The three:** LCP (loading), CLS (visual stability), INP (responsiveness).
- **Why:** Good scores = better UX and search; we’ll show what each measures and how to fix common issues.
- **What we’ll use:** Short Manim clips to explain each metric; then before/after code demos you can run locally.

---

## 1. LCP — Largest Contentful Paint (0:35–2:35)

**Definition (short)**  
- LCP = when the largest visible content element (image or text block) finishes rendering.
- Good: ≤ 2.5 s. We care about “when does the main content appear?”

**Manim (01_lcp_calculated.py)**  
- Show viewport; title “How LCP is calculated.”
- Three elements appear one by one (small → larger → largest).
- Browser marks the current largest as “LCP candidate” (highlight in green).
- When a larger one appears, the candidate changes; the last one is the LCP element.
- Takeaway: LCP time = when that final largest element has painted.

**Code demo (lcp-before vs lcp-after)**  
- **Before:** Blocking script in `<head>` (e.g. `bundle.js`). Parsing stops until script runs; hero image is requested only after that → LCP delayed.
- **After:** Preload the hero image (`<link rel="preload" as="image">`), script with `defer`, `fetchpriority="high"` on the hero `<img>`. Image request starts early; body can render sooner → better LCP.
- Optional: quick DevTools/Lighthouse LCP comparison.

**Takeaway**  
- Don’t block parsing for above-the-fold content. Preload LCP asset; defer non-critical JS; prioritize the LCP element.

---

## 2. CLS — Cumulative Layout Shift (2:35–4:35)

**Definition (short)**  
- CLS = sum of layout shift scores (how much visible content moved and how much of the viewport it affected).
- Good: ≤ 0.1. We care about “does the page jump while I’m reading?”

**Manim (02_cls_layout_shift.py)**  
- Show viewport; title “How CLS works”; 4×4 grid with six blocks (2×3).
- Step 1: One block grows from 1×1 to 2×2 (e.g. image without dimensions); others reflow. Label: “Square grows to 2×2 → others reflow.”
- Step 2: One block becomes 2×1 rectangle; neighbor reflows. Label: “Square → rectangle (2×1) → neighbor reflows.”
- Step 3: Rectangle shrinks back to 1×1; neighbor reflows back. Label: “Rectangle → square → neighbor reflows back.”
- Caption: same grid, same gap; resize one → others flow. Amber highlight on the element that changed and those that moved.

**Code demo (cls-before vs cls-after)**  
- **Before:** Images with no `width`/`height`; `src` set later (e.g. `data-src` + script at 1.5s, 2.5s, 3.5s). First paint has no image box; when each image loads, layout jumps → CLS.
- **After:** Same layout and images; each `<img>` has `width` and `height`. Browser reserves aspect-ratio space before load → no jump, zero CLS.
- Optional: DevTools Layout shifts panel or Lighthouse CLS.

**Takeaway**  
- Always set `width` and `height` (or aspect-ratio) on images and other content that can shift layout so the browser reserves space.

---

## 3. INP — Interaction to Next Paint (4:35–6:35)

**Definition (short)**  
- INP = time from user input (click, tap, key) to the next paint that could show a response.
- Good: ≤ 200 ms. We care about “does the page feel responsive?”

**Manim (03_inp_responsiveness.py — or 03_inp_blocking + 04_inp_chunked)**  
- **Option A (single scene):** Viewport + “Process” button. Part 1: click → red “main thread busy” bar grows; no UI update until “Done!” (bad INP). Part 2: click → “Processing…” appears immediately; work in chunks; then “Done!” (good INP). Caption: yield so the browser can paint quickly.
- **Option B (two scenes):** Blocking: red bar grows; other buttons A/B are “clicked” but get no result. Chunked: red bar grows in chunks with pauses; during pauses A and B get “OK” (responsiveness).

**Code demo (inp-before vs inp-after)**  
- **Before:** One button “Process Data.” Click runs a long synchronous loop (e.g. 10k items × heavy math). “Processing…” never paints; button jumps straight to “Done!” Second button “Try me while processing”: clicks during the loop do nothing until the loop finishes.
- **After:** Same workload; handler sets “Processing…” and yields with `setTimeout(..., 0)`, processes in chunks. “Processing…” appears immediately; “Try me” responds during processing.
- Optional: DevTools Performance / INP or long-task view.

**Takeaway**  
- Keep the main thread short. For heavy work: do a little, yield (e.g. `setTimeout(0)` or chunked loop), let the browser paint, then continue.

---

## 4. Outro (6:35–7:00)

- Recap: LCP (don’t block, preload, defer), CLS (reserve space with width/height), INP (yield so paint can happen).
- Where to measure: Lighthouse, DevTools Performance, CrUX (field data).
- Point to repo/demos: run `npm start` in 03-web-vitals, open before/after pages, try throttling and DevTools.

---

## Timing summary

| Section   | Start | End  | Duration |
|----------|-------|------|----------|
| Intro    | 0:00  | 0:35 | 35 s     |
| LCP      | 0:35  | 2:35 | 2 min    |
| CLS      | 2:35  | 4:35 | 2 min    |
| INP      | 4:35  | 6:35 | 2 min    |
| Outro    | 6:35  | 7:00 | 25 s     |
| **Total**|       |      | **~7 min** |

---

## Clip / asset checklist

- **Manim:** LCPCalculated.mp4 (2160p60), CLSLayoutShift.mp4 (2160p60), INPResponsiveness (or INPBlocking + INPChunked) as needed.
- **Browser:** lcp-before, lcp-after; cls-before, cls-after; inp-before, inp-after (with “Process Data” and “Try me while processing”).
- **Optional:** DevTools panels (Lighthouse LCP/CLS, Performance INP or long tasks).

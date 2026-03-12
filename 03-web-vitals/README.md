# 03 — Core Web Vitals

Demos for **LCP**, **CLS**, and **INP**: how different code and loading choices affect Core Web Vitals. Use before/after pages to compare in the browser and in DevTools.

## Quick start

```bash
cd 03-web-vitals
npm install
npm start
```

Open **http://localhost:8080**. Use Chrome DevTools (Lighthouse, Performance, Network throttling) to measure.

## Structure

| Path | Purpose |
|------|--------|
| `index.html` | Entry: links to each metric’s before/after demos |
| `lcp-before.html` / `lcp-after.html` | LCP: blocking script vs preload + `defer` + `fetchpriority="high"` |
| `cls-before.html` / `cls-after.html` | CLS: image without dimensions vs intrinsic `width`/`height` |
| `inp-before.html` / `inp-after.html` | INP: blocking click handler vs chunked work + `setTimeout(0)` yield |
| `src/bundle.js` | Simulated heavy script for LCP demos |
| `src/inp-before.js` | Sync loop on button click (blocks main thread) |
| `src/inp-after.js` | Chunked processing with yield for INP |
| `css/main.css` | Shared layout and demo styles |
| `assets/` | Hero and article images (SVG placeholders) |
| `scenes/01_lcp_calculated.py` | Manim scene: how LCP is calculated (viewport, elements, largest = light green) |
| `scenes/02_cls_layout_shift.py` | Manim scene: how CLS works (viewport, blocks grow → others pushed down, amber highlight) |
| `scenes/03_inp_responsiveness.py` | Manim scene: how INP works (blocking → no paint; yield + chunks → quick paint) |
| `scenes/03_inp_blocking.py` | Manim: INP blocking — red bar grows; other interactions (A, B) get no result |
| `scenes/04_inp_chunked.py` | Manim: INP chunked — red bar grows in chunks; between chunks A and B get a result |

## What each demo shows

1. **LCP (Largest Contentful Paint)**  
   - **Before:** `<script src="bundle.js">` in `<head>` blocks parsing; hero image is requested only after the script runs.  
   - **After:** `<link rel="preload" ... as="image">` and `<script defer>`, plus `fetchpriority="high"` on the hero image so the LCP asset loads in parallel and body can render sooner.

2. **CLS (Cumulative Layout Shift)**  
   - **Before:** Image with only `width: 100%; height: auto` — no intrinsic size, so layout jumps when the image loads.  
   - **After:** Same CSS plus `width` and `height` attributes so the browser reserves the correct aspect-ratio space and avoids shift.

3. **INP (Interaction to Next Paint)**  
   - **Before:** Click handler runs a long synchronous loop; the button text doesn’t change to “Processing...” until the loop finishes.  
   - **After:** Set “Processing...” immediately, then run the heavy work in chunks with `setTimeout(processNextChunk, 0)` so the main thread can paint in between.

## Tips for video / live demo

- **LCP:** `bundle.js` does ~1–2s of synchronous work so the "before" page blocks parsing and delays the hero request; compare Lighthouse LCP on before vs after. For a starker difference, run Lighthouse with "Slow 4G" so the blocking script download also hurts the before version.
- **CLS:** Throttle network so the image loads after first paint; compare CLS in Lighthouse or the Experience section.
- **INP:** Click “Process Data” and watch when the button label updates; use Performance to see long tasks on the before version.

## LCP video (Manim)

From the **project root** (with venv active and `manim` installed):

```bash
manim -pql --disable_caching 03-web-vitals/scenes/01_lcp_calculated.py LCPCalculated
```

**High quality (2160p60):** use `-qk` (same as other chapters). Output: `media/videos/01_lcp_calculated/2160p60/LCPCalculated.mp4`, `media/videos/02_cls_layout_shift/2160p60/CLSLayoutShift.mp4`. Preview: `-pql` (low) or `-qh` (1080p). The scene shows a viewport; three elements appear in order (small → larger → largest). The current largest is highlighted in light green as the “LCP candidate”; the final one is the LCP element.

**CLS video:** same style (viewport, shared common). Run `manim -qk --disable_caching 03-web-vitals/scenes/02_cls_layout_shift.py CLSLayoutShift` for 2160p60. Output: `media/videos/02_cls_layout_shift/2160p60/CLSLayoutShift.mp4`. Three blocks in the viewport; one grows (e.g. image loads without dimensions) and pushes content down; another grows and pushes again. Amber highlight marks the element that caused the shift and the content that was pushed.

**INP video:** Run `manim -pql --disable_caching 03-web-vitals/scenes/03_inp_responsiveness.py INPResponsiveness`. Viewport with a “Process Data” button. First: click → main thread busy bar (no paint) → “Done!” (high INP). Second: click → immediate “Processing…” paint → chunked work blocks → “Done!” (good INP).

**INP blocking (two-scene set):** `03_inp_blocking.py` — one rectangle clicked, red bar grows; during growth other interactions (buttons A, B) happen but get no result. `04_inp_chunked.py` — same layout; red bar grows in chunks with pauses; during pauses A and B get a result (OK). Same style as other web-vitals scenes.

---

The LCP demos use `assets/hero-banner.webp` (1200×800, ~570KB), resized from the original PNG for hero use. The original `hero-banner.png` (3750×2501) remains in `assets/` for reference. For CLS, replace `assets/system-diagram.svg` with a real image when you want more realistic numbers.

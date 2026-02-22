# Lexorank Scenes — Style & Conventions

Rules for this tutorial so fonts, colors, timing, and layout stay consistent. **All shared constants and helpers live in `scenes/common.py`.**

---

## Font & font size

- **Single font:** `Fira Code`. No fallback list; one source of truth so every scene uses the same font.
- **Registration:** `common.py` registers Fira Code from disk (`~/Library/Fonts`, `/Library/Fonts`, Linux paths) so Pango always has it. Do not remove this.
- **Usage:** All `Text()` must use `font=FONT_DEFAULT` (or `FONT_POSITION_LABEL`, which is the same). Use `_text_font_kwargs()` for letter/position labels. Never hardcode another font name.
- **Sizes (in common.py):**
  - Titles: `TITLE_FONT_SIZE` (36)
  - Letters in boxes: `LETTER_FONT_SIZE` (32)
  - Position/rank labels: `POSITION_FONT_SIZE` (28)
  - Conclusions: `CONCLUSION_FONT_SIZE` / `CONCLUSION_FONT_SIZE_SMALL`
  - Captions: `LABEL_SMALL_FONT_SIZE`, `LABEL_TINY_FONT_SIZE`
- **Debug:** Call `debug_font_info("SceneName")` at the start of each scene’s `construct()` to log font to console (no on-screen label).

---

## Color & highlight

- **Background / UI:** `COLOR_BG`, `COLOR_NODE`, `COLOR_NODE_BORDER`, `TEXT_LIGHT` (all in common).
- **Position/rank labels:**
  - **Unchanged:** `LABEL_DEFAULT` (white `#ffffff`).
  - **Changed or new:** `LABEL_UPDATED` (yellow `#F1C40F`) so the difference is visible.
- Use yellow for any label that was just updated or newly inserted (e.g. after a move or rebalance). Keep the first/unchanged item white.

---

## Animation timing, speed, transition

- **All timing in common.py.** Do not invent new magic numbers in scene files.
  - Titles: `TITLE_WRITE_RUN_TIME`, `TITLE_WAIT_AFTER`
  - Item entry: `ITEMS_FADEIN_*`, `ITEMS_WAIT_AFTER`
  - Moves: `MOVE_RUN_TIME`, `MOVE_WAIT_AFTER`, `INSERT_MOVE_RUN_TIME`, etc.
  - Label updates: `LABEL_UPDATE_RUN_TIME`, `LABEL_UPDATE_WAIT_AFTER`
  - Conclusions: `CONCLUSION_WRITE_RUN_TIME`, `CONCLUSION_WAIT`, `CONCLUSION_BUFF*`
- **Entry animation:** Same pattern across scenes: `LaggedStart(*(FadeIn(item, shift=...) for item in items), lag_ratio=...)` with common constants.
- **Replacement labels (position/rank):** Never use `.move_to(old_label.get_center())` — that misaligns horizontally when digit width changes. Always use `position_replacement_label(new_label, item_mob)` from common so the new label is placed with `next_to(rect, RIGHT, buff=...)` and baseline-aligned to the letter (same as `make_item` / `make_item_rank`).

---

## Layout & alignment

- **Letter in box:** Centered with `_place_letter_in_rect(letter_text, rect)`.
- **Position/rank label:** Placed with `next_to(rect, RIGHT, buff=POSITION_LABEL_BUFF)` then baseline-aligned to the letter (same bottom y) so letters and numbers line up across rows.
- **Replacement labels:** Use `position_replacement_label(label_text, item_mob)` so both horizontal position and baseline match the original layout.

---

## Manim cache

- Manim caches partial movie files. **During development the cache is annoying:** changes to font, colors, or layout often don’t show up until you bypass or clear cache.
- **Rule: always use `--disable_caching` while developing.** Example:
  ```bash
  manim -pql --disable_caching 01-lexorank/scenes/01_problem.py ProblemIntro
  manim -qh --disable_caching 01-lexorank/scenes/01_problem.py ProblemIntro
  ```
- Optional: `--flush_cache` removes existing cached partials; use if you forgot to disable cache and see stale output.

---

## Checklist for new or edited scenes

- [ ] All text uses `FONT_DEFAULT` / constants from common.
- [ ] Labels: unchanged = `LABEL_DEFAULT`, changed/new = `LABEL_UPDATED`.
- [ ] No `.move_to(old_pos_text.get_center())` for replacement labels; use `position_replacement_label(new_text, mob)`.
- [ ] Timing constants from common; no new magic numbers.
- [ ] `debug_font_info("SceneName")` at start of `construct()`.
- [ ] Render with `--disable_caching` during development (cache hides font/layout/color changes).

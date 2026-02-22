"""
Scene 1: The Problem — drag-and-drop list with integer positions.
Shows cascade update (pain point): drag E between A and B → B,C,D renumber.
Zoom out to 200 boxes (labels hidden) + random Indicate to stress “too many nodes = disaster”.
Refinements: 4K-friendly (font, grid opacity); Indicate lag_ratio raised for 60fps.
Scene 2 (LexoRank solution) can reuse this style and show string midpoint e.g. "aaa"–"aab" → "aaaV".
"""

from manim import *

from common import (
    COLOR_BG,
    LABEL_DEFAULT,
    LABEL_UPDATED,
    TEXT_LIGHT,
    create_plane,
    make_box_only,
    make_item,
    make_position_label_like,
)
from common import (
    BOX_ONLY_HEIGHT,
    BOX_ONLY_WIDTH,
    FONT_DEFAULT,
    ITEM_ARRANGE_BUFF,
    ITEMS_FADEIN_LAG_RATIO,
    ITEMS_FADEIN_RUN_TIME,
    ITEMS_FADEIN_SHIFT,
    ITEMS_WAIT_AFTER,
    LABEL_UPDATE_RUN_TIME,
    LABEL_UPDATE_WAIT_AFTER,
    MOVE_RUN_TIME,
    MOVE_WAIT_AFTER,
    SLOT_OFFSET,
    TITLE_FONT_SIZE,
    TITLE_WAIT_AFTER,
    TITLE_WRITE_RUN_TIME,
)


class ProblemIntro(Scene):
    def construct(self):
        self.camera.background_color = COLOR_BG

        try:
            Text.set_default(font=FONT_DEFAULT)
        except Exception:
            pass

        bg_plane = create_plane()
        if bg_plane is not None:
            self.add(bg_plane)

        title = Text("Ordered list: positions as integers", font_size=TITLE_FONT_SIZE, color=TEXT_LIGHT)
        title.to_edge(UP)
        self.play(Write(title), run_time=TITLE_WRITE_RUN_TIME)
        self.wait(TITLE_WAIT_AFTER)

        # Initial list: A(1), B(2), C(3), D(4), E(5) — centered in the scene
        letters = ["A", "B", "C", "D", "E"]
        positions = [1, 2, 3, 4, 5]
        items = VGroup(*[make_item(ltr, pos) for ltr, pos in zip(letters, positions)])
        items.arrange(DOWN, buff=ITEM_ARRANGE_BUFF, aligned_edge=LEFT)
        items.move_to(ORIGIN)

        # 195 other boxes: drawn from the start but hidden (so they exist in place for the zoom)
        first_five_rects = [items[i][0] for i in range(5)]
        gap = 0.06
        block_195 = VGroup(*[make_box_only(BOX_ONLY_WIDTH, BOX_ONLY_HEIGHT) for _ in range(195)])
        block_195.arrange_in_grid(rows=5, cols=39, buff=gap, flow_order="dr", cell_alignment=ORIGIN)
        block_195.next_to(VGroup(*first_five_rects), RIGHT, buff=gap)
        block_195.set_opacity(0)
        self.add(block_195)
        self.bring_to_back(block_195)
        if bg_plane is not None:
            self.bring_to_back(bg_plane)

        self.play(
            LaggedStart(
                *(FadeIn(item, shift=UP * ITEMS_FADEIN_SHIFT) for item in items),
                lag_ratio=ITEMS_FADEIN_LAG_RATIO,
            ),
            run_time=ITEMS_FADEIN_RUN_TIME,
        )
        self.wait(ITEMS_WAIT_AFTER)

        # Drag E to between A and B; then reflow B, C, D down
        item_a, item_b, item_c, item_d, item_e = items
        slot_height = item_a.height + SLOT_OFFSET
        target_e = item_a.get_center() + DOWN * slot_height
        item_e.generate_target()
        item_e.target.move_to(target_e)

        self.play(MoveToTarget(item_e), run_time=MOVE_RUN_TIME, rate_func=smooth)
        self.wait(MOVE_WAIT_AFTER)

        item_b.generate_target()
        item_b.target.move_to(target_e + DOWN * slot_height)
        item_c.generate_target()
        item_c.target.move_to(target_e + 2 * DOWN * slot_height)
        item_d.generate_target()
        item_d.target.move_to(target_e + 3 * DOWN * slot_height)

        self.play(
            MoveToTarget(item_b),
            MoveToTarget(item_c),
            MoveToTarget(item_d),
            run_time=MOVE_RUN_TIME,
            rate_func=smooth,
        )
        self.wait(MOVE_WAIT_AFTER)

        # Animate position labels: A=1, E=2, B=3, C=4, D=5 (updated → yellow)
        # If stutter on 4K: use FadeTransform(old_pos_text, new_pos_text) instead of Transform
        new_positions = [1, 2, 3, 4, 5]
        order_after = [item_a, item_e, item_b, item_c, item_d]
        for mob, new_pos in zip(order_after, new_positions):
            old_pos_text = mob[2]
            label_color = LABEL_UPDATED if new_pos != 1 else LABEL_DEFAULT
            new_pos_text = make_position_label_like(new_pos, label_color, old_pos_text).move_to(
                old_pos_text.get_center()
            )
            self.play(Transform(old_pos_text, new_pos_text), run_time=LABEL_UPDATE_RUN_TIME)
        self.wait(LABEL_UPDATE_WAIT_AFTER)

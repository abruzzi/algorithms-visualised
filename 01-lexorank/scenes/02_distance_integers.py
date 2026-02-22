"""
Scene 2a: Sparse (distance) integers — positions 1000, 2000, 3000, ...
Same move as problem: drag E between A and B. Only E's label changes (5000 → 1500);
B, C, D stay 2000, 3000, 4000. One write, no cascade. Fair comparison.
Same visual style as 01_problem.py.
"""

from manim import *

from common import (
    COLOR_BG,
    debug_font_info,
    LABEL_UPDATED,
    TEXT_LIGHT,
    create_plane,
    make_item,
    make_position_label_like,
    position_replacement_label,
)
from common import (
    CONCLUSION_BUFF,
    CONCLUSION_FONT_SIZE,
    CONCLUSION_WAIT,
    CONCLUSION_WRITE_RUN_TIME,
    FONT_DEFAULT,
    GAP_LABEL_FADEIN_RUN_TIME,
    GAP_LABEL_FADEOUT_RUN_TIME,
    GAP_LABEL_WAIT,
    ITEM_ARRANGE_BUFF,
    ITEMS_FADEIN_LAG_RATIO,
    ITEMS_FADEIN_RUN_TIME,
    ITEMS_FADEIN_SHIFT,
    ITEMS_WAIT_AFTER,
    LABEL_TINY_FONT_SIZE,
    LABEL_UPDATE_RUN_TIME_SLOW,
    MOVE_RUN_TIME,
    MOVE_WAIT_AFTER,
    SLOT_OFFSET,
    TITLE_FONT_SIZE,
    TITLE_WAIT_AFTER,
    TITLE_WRITE_RUN_TIME,
)


class DistanceIntegers(Scene):
    """Sparse integers: same move as problem; only E updates to 1500; no cascade."""
    def construct(self):
        self.camera.background_color = COLOR_BG

        debug_font_info("02_distance_integers.DistanceIntegers")

        try:
            Text.set_default(font=FONT_DEFAULT)
        except Exception:
            pass

        bg_plane = create_plane()
        if bg_plane is not None:
            self.add(bg_plane)

        title = Text(
            "Sparse integers: leave room between positions",
            font=FONT_DEFAULT,
            font_size=TITLE_FONT_SIZE,
            color=TEXT_LIGHT,
        )
        title.to_edge(UP)
        self.play(Write(title), run_time=TITLE_WRITE_RUN_TIME)
        self.wait(TITLE_WAIT_AFTER)

        # Initial list: A(1000), B(2000), C(3000), D(4000), E(5000)
        letters = ["A", "B", "C", "D", "E"]
        positions = [1000, 2000, 3000, 4000, 5000]
        items = VGroup(*[make_item(ltr, pos) for ltr, pos in zip(letters, positions)])
        items.arrange(DOWN, buff=ITEM_ARRANGE_BUFF, aligned_edge=LEFT)
        items.move_to(ORIGIN)

        self.play(
            LaggedStart(
                *(FadeIn(item, shift=UP * ITEMS_FADEIN_SHIFT) for item in items),
                lag_ratio=ITEMS_FADEIN_LAG_RATIO,
            ),
            run_time=ITEMS_FADEIN_RUN_TIME,
        )
        self.wait(ITEMS_WAIT_AFTER)

        gap_label = Text(
            "gap",
            font=FONT_DEFAULT,
            font_size=LABEL_TINY_FONT_SIZE,
            color=LABEL_UPDATED,
        )
        gap_label.next_to(items[0], RIGHT, buff=1.2)
        self.play(FadeIn(gap_label), run_time=GAP_LABEL_FADEIN_RUN_TIME)
        self.wait(GAP_LABEL_WAIT)
        self.play(FadeOut(gap_label), run_time=GAP_LABEL_FADEOUT_RUN_TIME)

        # Same move as problem: drag E between A and B; reflow B, C, D down
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

        old_pos_text = item_e[2]
        new_pos_text = make_position_label_like(1500, LABEL_UPDATED, old_pos_text)
        position_replacement_label(new_pos_text, item_e)
        self.play(Transform(old_pos_text, new_pos_text), run_time=LABEL_UPDATE_RUN_TIME_SLOW)
        self.wait(0.8)

        # conclusion = Text(
        #     "One write. No cascade.",
        #     font=FONT_DEFAULT,
        #     font_size=CONCLUSION_FONT_SIZE,
        #     color=LABEL_UPDATED,
        # )
        # conclusion.next_to(item_d, DOWN, buff=CONCLUSION_BUFF)
        # self.play(Write(conclusion), run_time=CONCLUSION_WRITE_RUN_TIME)
        # self.wait(CONCLUSION_WAIT)

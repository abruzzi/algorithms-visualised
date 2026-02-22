"""
Scene 2b: Sparse integers — when the gap fills up.
Insert F(1500), then G(1250), then H(1125) in the same gap to show density;
then rebalance to restore sparse positions (1000, 2000, …, 8000).
Same visual style as 01_problem and 02_distance_integers.
"""

from manim import *

from common import (
    COLOR_BG,
    debug_font_info,
    LABEL_DEFAULT,
    LABEL_UPDATED,
    TEXT_LIGHT,
    create_plane,
    make_item,
    make_position_label_like,
    position_replacement_label,
)
from common import (
    CONCLUSION_BUFF_SMALL,
    CONCLUSION_FONT_SIZE_SMALL,
    CONCLUSION_WAIT,
    CONCLUSION_WRITE_RUN_TIME,
    DENSITY_LABEL_WAIT,
    DENSITY_LABEL_WRITE_RUN_TIME,
    FONT_DEFAULT,
    GAP_LABEL_FADEOUT_RUN_TIME,
    INSERT_MOVE_FADEIN_SHIFT,
    INSERT_MOVE_RUN_TIME,
    INSERT_WAIT_AFTER,
    ITEM_ARRANGE_BUFF,
    ITEMS_FADEIN_LAG_RATIO,
    ITEMS_FADEIN_RUN_TIME,
    ITEMS_FADEIN_SHIFT,
    ITEMS_WAIT_AFTER,
    LABEL_SMALL_FONT_SIZE,
    LABEL_UPDATE_RUN_TIME,
    REBALANCE_WAIT_AFTER,
    SLOT_OFFSET,
    TITLE_FONT_SIZE,
    TITLE_WAIT_AFTER,
    TITLE_WRITE_RUN_TIME,
)


class SparseRebalance(Scene):
    """Insert F, G, H in same gap → density; then rebalance to restore sparse gaps."""
    def construct(self):
        self.camera.background_color = COLOR_BG

        debug_font_info("03_sparse_rebalance.SparseRebalance")

        try:
            Text.set_default(font=FONT_DEFAULT)
        except Exception:
            pass

        bg_plane = create_plane()
        if bg_plane is not None:
            self.add(bg_plane)

        title = Text(
            "Sparse integers: when the gap fills up",
            font=FONT_DEFAULT,
            font_size=TITLE_FONT_SIZE,
            color=TEXT_LIGHT,
        )
        title.to_edge(UP)
        self.play(Write(title), run_time=TITLE_WRITE_RUN_TIME)
        self.wait(TITLE_WAIT_AFTER)

        # Start: A(1000), B(2000), C(3000), D(4000), E(5000)
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

        item_a, item_b, item_c, item_d, item_e = items
        slot_height = item_a.height + SLOT_OFFSET

        def shift_from(idx: int, start_center):
            """Target positions for items from idx onward: start_center, start_center+1*slot, ..."""
            return start_center + idx * DOWN * slot_height

        # --- Insert F between A and B → 1500 ---
        new_f = make_item("F", 1500)
        new_f.move_to(item_a.get_center() + DOWN * slot_height)
        item_b.generate_target()
        item_b.target.move_to(shift_from(2, item_a.get_center()))
        item_c.generate_target()
        item_c.target.move_to(shift_from(3, item_a.get_center()))
        item_d.generate_target()
        item_d.target.move_to(shift_from(4, item_a.get_center()))
        item_e.generate_target()
        item_e.target.move_to(shift_from(5, item_a.get_center()))
        self.play(
            MoveToTarget(item_b), MoveToTarget(item_c), MoveToTarget(item_d), MoveToTarget(item_e),
            FadeIn(new_f, shift=UP * INSERT_MOVE_FADEIN_SHIFT),
            run_time=INSERT_MOVE_RUN_TIME,
            rate_func=smooth,
        )
        self.wait(INSERT_WAIT_AFTER)

        # --- Insert G between A and F (1000 and 1500) → 1250 ---
        new_g = make_item("G", 1250)
        new_g.move_to(item_a.get_center() + DOWN * slot_height)
        new_f.generate_target()
        new_f.target.move_to(shift_from(2, item_a.get_center()))
        item_b.generate_target()
        item_b.target.move_to(shift_from(3, item_a.get_center()))
        item_c.generate_target()
        item_c.target.move_to(shift_from(4, item_a.get_center()))
        item_d.generate_target()
        item_d.target.move_to(shift_from(5, item_a.get_center()))
        item_e.generate_target()
        item_e.target.move_to(shift_from(6, item_a.get_center()))
        self.play(
            MoveToTarget(new_f), MoveToTarget(item_b), MoveToTarget(item_c),
            MoveToTarget(item_d), MoveToTarget(item_e),
            FadeIn(new_g, shift=UP * INSERT_MOVE_FADEIN_SHIFT),
            run_time=INSERT_MOVE_RUN_TIME,
            rate_func=smooth,
        )
        self.wait(INSERT_WAIT_AFTER)

        # --- Insert H between A and G (1000 and 1250) → 1125 ---
        new_h = make_item("H", 1125)
        new_h.move_to(item_a.get_center() + DOWN * slot_height)
        new_g.generate_target()
        new_g.target.move_to(shift_from(2, item_a.get_center()))
        new_f.generate_target()
        new_f.target.move_to(shift_from(3, item_a.get_center()))
        item_b.generate_target()
        item_b.target.move_to(shift_from(4, item_a.get_center()))
        item_c.generate_target()
        item_c.target.move_to(shift_from(5, item_a.get_center()))
        item_d.generate_target()
        item_d.target.move_to(shift_from(6, item_a.get_center()))
        item_e.generate_target()
        item_e.target.move_to(shift_from(7, item_a.get_center()))
        self.play(
            MoveToTarget(new_g), MoveToTarget(new_f), MoveToTarget(item_b),
            MoveToTarget(item_c), MoveToTarget(item_d), MoveToTarget(item_e),
            FadeIn(new_h, shift=UP * INSERT_MOVE_FADEIN_SHIFT),
            run_time=INSERT_MOVE_RUN_TIME,
            rate_func=smooth,
        )
        self.wait(INSERT_WAIT_AFTER)

        density_label = Text(
            "Gap filling up → rebalance",
            font=FONT_DEFAULT,
            font_size=LABEL_SMALL_FONT_SIZE,
            color=LABEL_UPDATED,
        )
        density_label.next_to(item_e, DOWN, buff=0.6)
        self.play(Write(density_label), run_time=DENSITY_LABEL_WRITE_RUN_TIME)
        self.wait(DENSITY_LABEL_WAIT)
        self.play(FadeOut(density_label), run_time=GAP_LABEL_FADEOUT_RUN_TIME)

        # --- Rebalance: update each label one-by-one; unchanged 1000 = white, rest = yellow ---
        order = [item_a, new_h, new_g, new_f, item_b, item_c, item_d, item_e]
        new_positions = [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000]
        for mob, new_pos in zip(order, new_positions):
            old_pos_text = mob[2]
            label_color = LABEL_DEFAULT if new_pos == 1000 else LABEL_UPDATED
            new_pos_text = make_position_label_like(new_pos, label_color, old_pos_text)
            position_replacement_label(new_pos_text, mob)
            self.play(Transform(old_pos_text, new_pos_text), run_time=LABEL_UPDATE_RUN_TIME)
        self.wait(REBALANCE_WAIT_AFTER)

        conclusion = Text(
            "Rebalance: restore sparse gaps (happens often)",
            font=FONT_DEFAULT,
            font_size=CONCLUSION_FONT_SIZE_SMALL,
            color=TEXT_LIGHT,
        )
        conclusion.next_to(item_e, DOWN, buff=CONCLUSION_BUFF_SMALL)
        self.play(Write(conclusion), run_time=CONCLUSION_WRITE_RUN_TIME)
        self.wait(CONCLUSION_WAIT)

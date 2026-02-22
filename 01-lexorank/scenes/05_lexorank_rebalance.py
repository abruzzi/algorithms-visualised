"""
Scene 5: Lexorank — insert between "a" and "am", then between "a" and new; rebalance.
Same visual pattern as 04 and 03_sparse_rebalance. Shows gap filling and rebalance with string ranks.
"""

from manim import *

from common import (
    COLOR_BG,
    LABEL_DEFAULT,
    LABEL_UPDATED,
    TEXT_LIGHT,
    create_plane,
    make_item_rank,
    make_rank_label_like,
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
    LABEL_TINY_FONT_SIZE,
    LABEL_UPDATE_RUN_TIME,
    POSITION_LABEL_BUFF,
    REBALANCE_WAIT_AFTER,
    TITLE_FONT_SIZE,
    TITLE_WAIT_AFTER,
    TITLE_WRITE_RUN_TIME,
)


class LexorankRebalance(Scene):
    """Start from A–F (a, am, b, c, d, e); insert between a and am → ag; between a and ag → ad; rebalance."""
    def construct(self):
        self.camera.background_color = COLOR_BG

        try:
            Text.set_default(font=FONT_DEFAULT)
        except Exception:
            pass

        bg_plane = create_plane()
        if bg_plane is not None:
            self.add(bg_plane)

        title = Text(
            "Lexorank: when the gap fills up",
            font_size=TITLE_FONT_SIZE,
            color=TEXT_LIGHT,
        )
        title.to_edge(UP)
        self.play(Write(title), run_time=TITLE_WRITE_RUN_TIME)
        self.wait(TITLE_WAIT_AFTER)

        # Start: A("a"), F("am"), B("b"), C("c"), D("d"), E("e") — as after 04
        letters = ["A", "F", "B", "C", "D", "E"]
        ranks = ["a", "am", "b", "c", "d", "e"]
        items = VGroup(*[make_item_rank(ltr, r) for ltr, r in zip(letters, ranks)])
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

        item_a, item_f, item_b, item_c, item_d, item_e = items

        # Insert G between "a" and "am" → midpoint "ag"
        mid_caption1 = Text(
            'Between "a" and "am" → midpoint "ag"',
            font_size=LABEL_TINY_FONT_SIZE,
            color=TEXT_LIGHT,
        )
        mid_caption1.next_to(title, DOWN, buff=0.2)
        self.play(Write(mid_caption1), run_time=0.8)
        self.wait(0.5)

        new_g = make_item_rank("G", "ag")
        new_g[2].set_color(LABEL_UPDATED)
        new_g.next_to(item_a, DOWN, buff=ITEM_ARRANGE_BUFF, aligned_edge=LEFT)

        item_f.generate_target()
        item_f.target.next_to(new_g, DOWN, buff=ITEM_ARRANGE_BUFF, aligned_edge=LEFT)
        item_b.generate_target()
        item_b.target.next_to(item_f.target, DOWN, buff=ITEM_ARRANGE_BUFF, aligned_edge=LEFT)
        item_c.generate_target()
        item_c.target.next_to(item_b.target, DOWN, buff=ITEM_ARRANGE_BUFF, aligned_edge=LEFT)
        item_d.generate_target()
        item_d.target.next_to(item_c.target, DOWN, buff=ITEM_ARRANGE_BUFF, aligned_edge=LEFT)
        item_e.generate_target()
        item_e.target.next_to(item_d.target, DOWN, buff=ITEM_ARRANGE_BUFF, aligned_edge=LEFT)

        self.play(
            MoveToTarget(item_f),
            MoveToTarget(item_b),
            MoveToTarget(item_c),
            MoveToTarget(item_d),
            MoveToTarget(item_e),
            FadeIn(new_g, shift=UP * INSERT_MOVE_FADEIN_SHIFT),
            run_time=INSERT_MOVE_RUN_TIME,
            rate_func=smooth,
        )
        self.wait(INSERT_WAIT_AFTER)

        # Replace caption: insert between "a" and "ag" → "ad"
        mid_caption2 = Text(
            'Between "a" and "ag" → midpoint "ad"',
            font_size=LABEL_TINY_FONT_SIZE,
            color=TEXT_LIGHT,
        )
        mid_caption2.next_to(title, DOWN, buff=0.2)
        self.play(Transform(mid_caption1, mid_caption2), run_time=0.5)
        self.wait(0.4)

        new_h = make_item_rank("H", "ad")
        new_h[2].set_color(LABEL_UPDATED)
        new_h.next_to(item_a, DOWN, buff=ITEM_ARRANGE_BUFF, aligned_edge=LEFT)

        new_g.generate_target()
        new_g.target.next_to(new_h, DOWN, buff=ITEM_ARRANGE_BUFF, aligned_edge=LEFT)
        item_f.generate_target()
        item_f.target.next_to(new_g.target, DOWN, buff=ITEM_ARRANGE_BUFF, aligned_edge=LEFT)
        item_b.generate_target()
        item_b.target.next_to(item_f.target, DOWN, buff=ITEM_ARRANGE_BUFF, aligned_edge=LEFT)
        item_c.generate_target()
        item_c.target.next_to(item_b.target, DOWN, buff=ITEM_ARRANGE_BUFF, aligned_edge=LEFT)
        item_d.generate_target()
        item_d.target.next_to(item_c.target, DOWN, buff=ITEM_ARRANGE_BUFF, aligned_edge=LEFT)
        item_e.generate_target()
        item_e.target.next_to(item_d.target, DOWN, buff=ITEM_ARRANGE_BUFF, aligned_edge=LEFT)

        self.play(
            MoveToTarget(new_g),
            MoveToTarget(item_f),
            MoveToTarget(item_b),
            MoveToTarget(item_c),
            MoveToTarget(item_d),
            MoveToTarget(item_e),
            FadeIn(new_h, shift=UP * INSERT_MOVE_FADEIN_SHIFT),
            run_time=INSERT_MOVE_RUN_TIME,
            rate_func=smooth,
        )
        self.wait(INSERT_WAIT_AFTER)

        # Gap filling → rebalance
        density_label = Text(
            "Gap filling up → rebalance",
            font_size=LABEL_TINY_FONT_SIZE,
            color=LABEL_UPDATED,
        )
        density_label.next_to(item_e, DOWN, buff=0.6)
        self.play(Write(density_label), run_time=DENSITY_LABEL_WRITE_RUN_TIME)
        self.wait(DENSITY_LABEL_WAIT)
        self.play(FadeOut(density_label), run_time=GAP_LABEL_FADEOUT_RUN_TIME)

        # Rebalance: assign sparse ranks a, b, c, d, e, f, g, h; updated = yellow
        order = [item_a, new_h, new_g, item_f, item_b, item_c, item_d, item_e]
        new_ranks = ["a", "b", "c", "d", "e", "f", "g", "h"]
        for mob, new_rank in zip(order, new_ranks):
            old_rank_text = mob[2]
            label_color = LABEL_DEFAULT if new_rank == "a" else LABEL_UPDATED
            new_rank_text = make_rank_label_like(
                new_rank, label_color, old_rank_text
            ).move_to(old_rank_text.get_center())
            self.play(
                Transform(old_rank_text, new_rank_text),
                run_time=LABEL_UPDATE_RUN_TIME,
            )
        # Re-align labels (Transform can shift left edge); keep left-aligned with node
        for mob in order:
            mob[2].next_to(mob[0], RIGHT, buff=POSITION_LABEL_BUFF)
        self.wait(REBALANCE_WAIT_AFTER)

        conclusion = Text(
            "Rebalance: restore sparse ranks (rare with Lexorank)",
            font_size=CONCLUSION_FONT_SIZE_SMALL,
            color=TEXT_LIGHT,
        )
        conclusion.next_to(item_e, DOWN, buff=CONCLUSION_BUFF_SMALL)
        self.play(Write(conclusion), run_time=CONCLUSION_WRITE_RUN_TIME)
        self.wait(CONCLUSION_WAIT)

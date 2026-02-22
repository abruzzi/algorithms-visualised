"""
Scene 4: Lexorank — string ranks 'a'–'e', insert new item between 'a' and 'b'.
New node gets midpoint rank ("am"); other nodes keep their labels. Same style as 01–03.
"""

from manim import *

from common import (
    COLOR_BG,
    LABEL_UPDATED,
    TEXT_LIGHT,
    create_plane,
    make_item_rank,
)
from common import (
    CONCLUSION_BUFF_SMALL,
    CONCLUSION_FONT_SIZE_SMALL,
    CONCLUSION_WAIT,
    CONCLUSION_WRITE_RUN_TIME,
    FONT_DEFAULT,
    INSERT_MOVE_FADEIN_SHIFT,
    INSERT_MOVE_RUN_TIME,
    INSERT_WAIT_AFTER,
    ITEM_ARRANGE_BUFF,
    ITEMS_FADEIN_LAG_RATIO,
    ITEMS_FADEIN_RUN_TIME,
    ITEMS_FADEIN_SHIFT,
    ITEMS_WAIT_AFTER,
    LABEL_SMALL_FONT_SIZE,
    TITLE_FONT_SIZE,
    TITLE_WAIT_AFTER,
    TITLE_WRITE_RUN_TIME,
)


class LexorankInsert(Scene):
    """Five elements A–E with string ranks 'a'–'e'; insert F between A and B with midpoint rank."""
    def construct(self):
        self.camera.background_color = COLOR_BG

        try:
            Text.set_default(font=FONT_DEFAULT)
        except Exception:
            pass

        bg_plane = create_plane()
        if bg_plane is not None:
            self.add(bg_plane)

        title = Text("Lexorank: string positions", font_size=TITLE_FONT_SIZE, color=TEXT_LIGHT)
        title.to_edge(UP)
        self.play(Write(title), run_time=TITLE_WRITE_RUN_TIME)
        self.wait(TITLE_WAIT_AFTER)

        # Five elements A–E with ranks 'a', 'b', 'c', 'd', 'e'
        letters = ["A", "B", "C", "D", "E"]
        ranks = ["a", "b", "c", "d", "e"]
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

        item_a, item_b, item_c, item_d, item_e = items

        # Explain why the new rank is "am": midpoint between "a" and "b"
        mid_caption = Text(
            'Between "a" and "b": no single character in between → use "a" + "m" = "am"',
            font_size=LABEL_SMALL_FONT_SIZE,
            color=TEXT_LIGHT,
        )
        mid_caption.next_to(title, DOWN, buff=0.35)
        self.play(Write(mid_caption), run_time=1.0)
        self.wait(0.8)

        # Insert F between A and B with midpoint rank "am"; keep consistent spacing via next_to
        new_f = make_item_rank("F", "am")
        new_f[2].set_color(LABEL_UPDATED)  # new rank highlighted
        new_f.next_to(item_a, DOWN, buff=ITEM_ARRANGE_BUFF, aligned_edge=LEFT)

        item_b.generate_target()
        item_b.target.next_to(new_f, DOWN, buff=ITEM_ARRANGE_BUFF, aligned_edge=LEFT)
        item_c.generate_target()
        item_c.target.next_to(item_b.target, DOWN, buff=ITEM_ARRANGE_BUFF, aligned_edge=LEFT)
        item_d.generate_target()
        item_d.target.next_to(item_c.target, DOWN, buff=ITEM_ARRANGE_BUFF, aligned_edge=LEFT)
        item_e.generate_target()
        item_e.target.next_to(item_d.target, DOWN, buff=ITEM_ARRANGE_BUFF, aligned_edge=LEFT)

        self.play(
            MoveToTarget(item_b),
            MoveToTarget(item_c),
            MoveToTarget(item_d),
            MoveToTarget(item_e),
            FadeIn(new_f, shift=UP * INSERT_MOVE_FADEIN_SHIFT),
            run_time=INSERT_MOVE_RUN_TIME,
            rate_func=smooth,
        )
        self.wait(INSERT_WAIT_AFTER)

        conclusion = Text(
            "One write. New rank = midpoint; others unchanged.",
            font_size=CONCLUSION_FONT_SIZE_SMALL,
            color=TEXT_LIGHT,
        )
        conclusion.next_to(item_e, DOWN, buff=CONCLUSION_BUFF_SMALL)
        self.play(Write(conclusion), run_time=CONCLUSION_WRITE_RUN_TIME)
        self.wait(CONCLUSION_WAIT)

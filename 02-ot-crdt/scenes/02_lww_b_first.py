"""Scene: Naive / LWW — B arrived first, then A overwrites (B's edit lost)."""

from manim import *
from common import (
    COLOR_BG,
    FONT_DEFAULT,
    LABEL_FONT,
    T_CREATE,
    T_END,
    T_WAIT,
    T_WAIT_LONG,
    T_WRITE,
    TEXT_LIGHT,
    color_cell,
    create_plane,
    debug_font_info,
    make_char_cells,
)


class NaiveLWW_BFirst(Scene):
    """B's edit arrived first; A's edit overwrites — B's edit lost."""

    def construct(self):
        self.camera.background_color = COLOR_BG
        debug_font_info("02_lww_b_first.NaiveLWW_BFirst")
        try:
            Text.set_default(font=FONT_DEFAULT)
        except Exception:
            pass
        bg_plane = create_plane()
        if bg_plane is not None:
            self.add(bg_plane)

        # B first (top)
        b_label = Text("B", font_size=LABEL_FONT, color=ORANGE)
        y_hello = make_char_cells("YHello", TEXT_LIGHT, show_positions=True, start_index=0)
        color_cell(y_hello[0], ORANGE)
        y_hello.to_edge(UP, buff=0.5).shift(DOWN * 1.2)
        b_label.next_to(y_hello, UP, buff=0.25)
        self.play(Write(b_label), Create(y_hello), run_time=T_CREATE)
        self.wait(T_WAIT)

        # A second (below)
        a_label = Text("A", font_size=LABEL_FONT, color=BLUE)
        x_hello = make_char_cells("XHello", TEXT_LIGHT, show_positions=True, start_index=0)
        color_cell(x_hello[0], BLUE)
        x_hello.next_to(y_hello, DOWN, buff=0.9)
        a_label.next_to(x_hello, UP, buff=0.25)
        self.play(Write(a_label), Create(x_hello), run_time=T_CREATE)
        self.wait(T_WAIT_LONG)

        # Merge: last writer wins → A wins
        arrow = Arrow(ORIGIN, DOWN * 1.0, buff=0.2).next_to(x_hello, DOWN, buff=0.35)
        self.play(GrowArrow(arrow), run_time=T_WRITE)
        result = make_char_cells("XHello", TEXT_LIGHT, show_positions=True, start_index=0)
        color_cell(result[0], BLUE)
        result.next_to(arrow, DOWN, buff=0.25)
        self.play(Create(result), run_time=T_CREATE)
        self.wait(T_WAIT)

        lost = Text("✗", font_size=40, color=RED).next_to(y_hello, RIGHT, buff=0.4)
        self.play(Write(lost), run_time=T_WRITE)
        data_lost = Text("B's edit lost", font_size=LABEL_FONT, color=RED)
        data_lost.to_edge(DOWN, buff=0.5)
        self.play(Write(data_lost), run_time=T_WRITE)
        self.wait(T_END)

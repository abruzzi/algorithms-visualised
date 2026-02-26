"""Scene 2: Naive / LWW — one overwrites the other (data loss)."""

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


class NaiveLWW(Scene):
    def construct(self):
        self.camera.background_color = COLOR_BG
        debug_font_info("02_lww.NaiveLWW")
        try:
            Text.set_default(font=FONT_DEFAULT)
        except Exception:
            pass
        bg_plane = create_plane()
        if bg_plane is not None:
            self.add(bg_plane)

        a_label = Text("A", font_size=LABEL_FONT, color=BLUE)
        x_hello = make_char_cells("XHello", TEXT_LIGHT, show_positions=True, start_index=0)
        color_cell(x_hello[0], BLUE)
        x_hello.to_edge(UP, buff=0.5).shift(DOWN * 1.2)
        a_label.next_to(x_hello, UP, buff=0.25)
        self.play(Write(a_label), Create(x_hello), run_time=T_CREATE)
        self.wait(T_WAIT)

        b_label = Text("B", font_size=LABEL_FONT, color=ORANGE)
        y_hello = make_char_cells("YHello", TEXT_LIGHT, show_positions=True, start_index=0)
        color_cell(y_hello[0], ORANGE)
        y_hello.next_to(x_hello, DOWN, buff=0.9)
        b_label.next_to(y_hello, UP, buff=0.25)
        self.play(Write(b_label), Create(y_hello), run_time=T_CREATE)
        self.wait(T_WAIT_LONG)

        arrow = Arrow(ORIGIN, DOWN * 1.0, buff=0.2).next_to(y_hello, DOWN, buff=0.35)
        self.play(GrowArrow(arrow), run_time=T_WRITE)
        result = make_char_cells("YHello", TEXT_LIGHT, show_positions=True, start_index=0)
        color_cell(result[0], ORANGE)
        result.next_to(arrow, DOWN, buff=0.25)
        self.play(Create(result), run_time=T_CREATE)
        self.wait(T_WAIT)

        lost = Text("✗", font_size=40, color=RED).next_to(x_hello, RIGHT, buff=0.4)
        self.play(Write(lost), run_time=T_WRITE)
        data_lost = Text("A's edit lost", font_size=LABEL_FONT, color=RED)
        data_lost.to_edge(DOWN, buff=0.5)
        self.play(Write(data_lost), run_time=T_WRITE)
        self.wait(T_END)

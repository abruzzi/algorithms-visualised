"""Scene 1: The conflict — two users edit the same doc at once."""

from manim import *
from common import (
    COLOR_BG,
    FONT_DEFAULT,
    LABEL_FONT,
    T_CREATE,
    T_END,
    T_FADE,
    T_WAIT,
    T_WAIT_LONG,
    T_WRITE,
    TEXT_LIGHT,
    color_cell,
    create_plane,
    debug_font_info,
    make_char_cells,
)


class Conflict(Scene):
    def construct(self):
        self.camera.background_color = COLOR_BG
        debug_font_info("01_conflict.Conflict")
        try:
            Text.set_default(font=FONT_DEFAULT)
        except Exception:
            pass
        bg_plane = create_plane()
        if bg_plane is not None:
            self.add(bg_plane)

        doc_label = Text("Document:", font_size=LABEL_FONT, color=GRAY)
        doc_label.to_edge(UP, buff=0.5)
        self.play(Write(doc_label), run_time=T_WRITE)
        self.wait(T_WAIT)

        hello = make_char_cells("Hello", TEXT_LIGHT, show_positions=True, start_index=0)
        hello.next_to(doc_label, DOWN, buff=0.35)
        self.play(Create(hello), run_time=T_CREATE)
        self.wait(T_WAIT_LONG)

        same_time = Text("Both insert at position 0", font_size=LABEL_FONT, color=YELLOW)
        same_time.next_to(hello, DOWN, buff=0.5)
        self.play(Write(same_time), run_time=T_WRITE)
        self.wait(T_WAIT_LONG)
        self.play(FadeOut(same_time), run_time=T_FADE)

        a_label = Text("A inserts \"X\"", font_size=LABEL_FONT, color=BLUE)
        a_label.next_to(hello, DOWN, buff=0.7)
        self.play(Write(a_label), run_time=T_WRITE)
        self.wait(T_WAIT)

        x_hello = make_char_cells("XHello", TEXT_LIGHT, show_positions=True, start_index=0)
        x_hello.next_to(a_label, DOWN, buff=0.25)
        color_cell(x_hello[0], BLUE)
        self.play(Create(x_hello), run_time=T_CREATE)
        self.wait(T_WAIT_LONG)

        b_label = Text("B inserts \"Y\"", font_size=LABEL_FONT, color=ORANGE)
        b_label.next_to(x_hello, DOWN, buff=0.5)
        self.play(Write(b_label), run_time=T_WRITE)
        self.wait(T_WAIT)

        y_hello = make_char_cells("YHello", TEXT_LIGHT, show_positions=True, start_index=0)
        y_hello.next_to(b_label, DOWN, buff=0.25)
        color_cell(y_hello[0], ORANGE)
        self.play(Create(y_hello), run_time=T_CREATE)
        self.wait(T_WAIT_LONG)

        problem = Text("Conflict: both at position 0 — who wins?", font_size=LABEL_FONT, color=RED)
        problem.to_edge(DOWN, buff=0.5)
        self.play(Write(problem), run_time=T_WRITE)
        self.wait(T_END)

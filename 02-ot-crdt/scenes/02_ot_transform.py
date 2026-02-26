"""Scene 3: OT — A at top, doc in center, B at bottom. No overlap."""

from manim import *
from common import (
    COLOR_BG,
    FONT_DEFAULT,
    LABEL_FONT,
    LABEL_SMALL_FONT,
    T_CREATE,
    T_END,
    T_FADE,
    T_TRANSFORM,
    T_WAIT,
    T_WAIT_LONG,
    T_WRITE,
    TEXT_LIGHT,
    color_cell,
    create_plane,
    debug_font_info,
    make_char_cells,
)


class OT(Scene):
    def construct(self):
        self.camera.background_color = COLOR_BG
        debug_font_info("02_ot_transform.OT")
        try:
            Text.set_default(font=FONT_DEFAULT)
        except Exception:
            pass
        bg_plane = create_plane()
        if bg_plane is not None:
            self.add(bg_plane)

        # Start a bit higher so second half (apply, result, ✓) stays on screen
        hello = make_char_cells("Hello", TEXT_LIGHT, show_positions=True, start_index=0)
        hello.move_to(ORIGIN + UP * 0.6)
        doc_label = Text("Document:", font_size=LABEL_FONT, color=GRAY)
        doc_label.next_to(hello, UP, buff=0.2)
        self.play(Write(doc_label), Create(hello), run_time=T_CREATE)
        self.wait(T_WAIT)

        first_label = Text("A's edit arrives first →", font_size=LABEL_FONT, color=BLUE)
        first_label.next_to(doc_label, UP, buff=0.4)
        self.play(Write(first_label), run_time=T_WRITE)
        self.wait(T_WAIT)
        x_hello = make_char_cells("XHello", TEXT_LIGHT, show_positions=True, start_index=0)
        color_cell(x_hello[0], BLUE)
        x_hello.move_to(hello)
        self.play(ReplacementTransform(hello, x_hello), run_time=T_TRANSFORM)
        self.wait(T_WAIT_LONG)

        # B's original intent: insert Y at index 0 (orange); we'll animate 0 → 1 in place
        b_intent = Text("B: insert \"Y\" at index ", font_size=LABEL_FONT, color=ORANGE)
        b_pos_0 = Text("0", font_size=LABEL_FONT + 6, color=ORANGE)
        b_intent.next_to(x_hello, DOWN, buff=0.45)
        b_pos_0.next_to(b_intent, RIGHT, buff=0.18)
        self.play(Write(b_intent), Write(b_pos_0), run_time=T_WRITE)
        self.wait(1.2)

        # OT: animate the 0 changing to 1 in place, color orange → highlight white
        b_pos_1 = Text("1", font_size=LABEL_FONT + 6, color=WHITE)
        b_pos_1.move_to(b_pos_0)
        self.play(ReplacementTransform(b_pos_0, b_pos_1), run_time=T_TRANSFORM)
        self.wait(T_WAIT)

        apply_label = Text("Apply B at 1 →", font_size=LABEL_SMALL_FONT, color=ORANGE)
        apply_label.next_to(VGroup(b_intent, b_pos_1), DOWN, buff=0.3)
        self.play(Write(apply_label), run_time=T_WRITE)
        result = make_char_cells("XYHello", TEXT_LIGHT, show_positions=True, start_index=0)
        color_cell(result[0], BLUE)
        color_cell(result[1], ORANGE)
        result.move_to(x_hello)
        self.play(ReplacementTransform(x_hello, result), run_time=T_TRANSFORM)
        self.wait(T_WAIT)

        ok = Text("✓ both kept", font_size=LABEL_FONT, color=GREEN)
        ok.to_edge(DOWN, buff=0.5)
        self.play(Write(ok), run_time=T_WRITE)
        self.wait(T_END)

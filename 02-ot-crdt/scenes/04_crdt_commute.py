"""Scene 4: CRDT — linked list (nodes + IDs), merge by ID. Style matches 01-lexorank."""

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
    animate_insert_node_at_start,
    create_plane,
    debug_font_info,
    make_linked_list_row,
)


# Each node = (char, ID). IDs are unique labels, not string indices (0,1,2,... for original; A,B for inserts).
INITIAL_NODES = [("H", "id0"), ("e", "id1"), ("l", "id2"), ("l", "id3"), ("o", "id4")]

# Slower pacing for this scene (easier to follow)
T_SLOW = 1.4   # multiplier for run_time
W_SLOW = 1.3   # multiplier for waits


class CRDT(Scene):
    def construct(self):
        self.camera.background_color = COLOR_BG
        debug_font_info("04_crdt_commute.CRDT")
        try:
            Text.set_default(font=FONT_DEFAULT)
        except Exception:
            pass
        bg_plane = create_plane()
        if bg_plane is not None:
            self.add(bg_plane)

        # Even distribution: 3 rows with more space between them
        dy = 1.9
        label_gap = 0.95  # Space between label and row below
        y_doc = dy
        y_a = 0.0
        y_b = -dy

        doc_label = Text("Linked list: each node = (char, ID)", font_size=LABEL_SMALL_FONT, color=GRAY)
        doc_label.move_to(ORIGIN + UP * (y_doc + label_gap))
        self.play(Write(doc_label), run_time=T_WRITE * T_SLOW)
        self.wait(T_WAIT * W_SLOW)

        initial = make_linked_list_row(INITIAL_NODES)
        initial.move_to(ORIGIN + UP * y_doc)
        self.play(Create(initial), run_time=T_CREATE * T_SLOW)
        self.wait(T_WAIT_LONG * W_SLOW)

        a_label = Text("A: insert (X, id=A) after start", font_size=LABEL_SMALL_FONT, color=BLUE)
        a_label.move_to(ORIGIN + UP * (y_a + label_gap))
        self.play(Write(a_label), run_time=T_WRITE * T_SLOW)
        self.wait(T_WAIT * W_SLOW)
        a_existing = make_linked_list_row(INITIAL_NODES)
        a_existing.move_to(ORIGIN + UP * y_a)
        self.play(Create(a_existing), run_time=T_CREATE * 0.6)
        a_list = animate_insert_node_at_start(self, a_existing, "X", "A", BLUE, run_time=T_CREATE * T_SLOW)
        self.wait(T_WAIT * W_SLOW)

        b_label = Text("B: insert (Y, id=B) after start", font_size=LABEL_SMALL_FONT, color=ORANGE)
        b_label.move_to(ORIGIN + UP * (y_b + label_gap))
        self.play(Write(b_label), run_time=T_WRITE * T_SLOW)
        self.wait(T_WAIT * W_SLOW)
        b_existing = make_linked_list_row(INITIAL_NODES)
        b_existing.move_to(ORIGIN + UP * y_b)
        self.play(Create(b_existing), run_time=T_CREATE * 0.6)
        b_list = animate_insert_node_at_start(self, b_existing, "Y", "B", ORANGE, run_time=T_CREATE * T_SLOW)
        self.wait(T_WAIT_LONG * W_SLOW)

        self.play(
            FadeOut(doc_label), FadeOut(initial), FadeOut(a_label), FadeOut(a_list),
            FadeOut(b_label), FadeOut(b_list),
            run_time=T_FADE * T_SLOW,
        )
        self.wait(T_WAIT * W_SLOW)

        # Merge part: 4 elements, evenly spaced (gap = 1.0)
        merge_dy = 1.0
        how_prefix = Text("Merge: both after start → order by ID ", font_size=LABEL_SMALL_FONT, color=YELLOW)
        id_highlight = Text("(A < B)", font_size=LABEL_FONT, color=YELLOW)
        how_suffix = Text(" → X then Y", font_size=LABEL_SMALL_FONT, color=YELLOW)
        how = VGroup(how_prefix, id_highlight, how_suffix).arrange(RIGHT, buff=0.08)
        how.move_to(ORIGIN + UP * (merge_dy * 1.5))
        id_highlight.set_opacity(0)
        self.add(how)
        self.play(Write(how_prefix), Write(how_suffix), run_time=T_WRITE * T_SLOW)
        self.wait(T_WAIT * W_SLOW)
        id_highlight.set_opacity(1)
        self.play(Write(id_highlight), run_time=T_WRITE * T_SLOW)
        self.wait(T_WAIT * W_SLOW)
        self.play(id_highlight.animate.scale(1.2), run_time=T_WRITE * T_SLOW)
        self.play(id_highlight.animate.scale(1 / 1.2), run_time=T_TRANSFORM * 0.6)
        self.wait(T_WAIT * W_SLOW)

        merged = make_linked_list_row(
            [("X", "A"), ("Y", "B")] + list(INITIAL_NODES),
            color_overrides={0: BLUE, 1: ORANGE},
        )
        merged.move_to(ORIGIN + UP * (merge_dy * 0.5))
        self.play(Create(merged), run_time=T_TRANSFORM * T_SLOW)
        self.wait(T_WAIT_LONG * W_SLOW)

        result_txt = Text("Result: XYHello (both kept)", font_size=LABEL_SMALL_FONT, color=GREEN)
        result_txt.move_to(ORIGIN + DOWN * (merge_dy * 0.5))
        self.play(Write(result_txt), run_time=T_WRITE * T_SLOW)
        self.wait(T_WAIT * W_SLOW)

        ok = Text("✓ both kept", font_size=LABEL_FONT, color=GREEN)
        ok.move_to(ORIGIN + DOWN * (merge_dy * 1.5))
        self.play(Write(ok), run_time=T_WRITE * T_SLOW)
        self.wait(T_END)

"""Scene 6: Three-user CRDT — Hello world → Hi beautiful darkness (merge by structure)."""

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
    animate_insert_word_between,
    animate_replace_word_in_cell,
    create_plane,
    debug_font_info,
    make_word_cells,
)

WORD_FONT = 26
LABEL_Y = -1.2


class ThreeUserCRDT(Scene):
    def construct(self):
        self.camera.background_color = COLOR_BG
        debug_font_info("06_crdt_three_user_example.ThreeUserCRDT")
        try:
            Text.set_default(font=FONT_DEFAULT)
        except Exception:
            pass
        bg_plane = create_plane()
        if bg_plane is not None:
            self.add(bg_plane)

        doc_label = Text("Document:", font_size=LABEL_FONT, color=GRAY)
        doc_label.to_edge(UP, buff=0.5)

        initial = make_word_cells(["Hello", "world"], font_size=WORD_FONT)
        initial.move_to(ORIGIN)
        self.play(Write(doc_label), Create(initial), run_time=T_CREATE)
        self.wait(T_WAIT)

        # Match spacing / timing of ThreeUserOT: keep doc fixed in center,
        # show a single label below that changes for each step, and always
        # replace the whole row so spacing is identical.

        # Step 1 (CRDT view of C): Hello → Hi
        step_label = Text("Apply C (Hello→Hi) →", font_size=LABEL_SMALL_FONT, color=TEAL)
        step_label.move_to(ORIGIN + DOWN * LABEL_Y)
        hi_world = make_word_cells(["Hi", "world"], color_overrides={0: TEAL}, font_size=WORD_FONT)
        hi_world.move_to(initial)
        self.play(Write(step_label), run_time=T_WRITE)
        self.play(ReplacementTransform(initial, hi_world), run_time=T_TRANSFORM)
        self.wait(T_WAIT_LONG)
        self.play(FadeOut(step_label), run_time=T_FADE)

        # Step 2 (CRDT view of B): world → darkness
        step_label = Text("Apply B (world→darkness) →", font_size=LABEL_SMALL_FONT, color=ORANGE)
        step_label.move_to(ORIGIN + DOWN * LABEL_Y)
        hi_darkness = make_word_cells(
            ["Hi", "darkness"],
            color_overrides={0: TEAL, 1: ORANGE},
            font_size=WORD_FONT,
        )
        hi_darkness.move_to(hi_world)
        self.play(Write(step_label), run_time=T_WRITE)
        self.play(ReplacementTransform(hi_world, hi_darkness), run_time=T_TRANSFORM)
        self.wait(T_WAIT_LONG)
        self.play(FadeOut(step_label), run_time=T_FADE)

        # Step 3 (CRDT view of A): insert beautiful between Hi and darkness
        step_label = Text("Apply A (insert 'beautiful') →", font_size=LABEL_SMALL_FONT, color=BLUE)
        step_label.move_to(ORIGIN + DOWN * LABEL_Y)
        result = make_word_cells(
            ["Hi", "beautiful", "darkness"],
            color_overrides={0: TEAL, 1: BLUE, 2: ORANGE},
            font_size=WORD_FONT,
        )
        result.move_to(hi_darkness)
        self.play(Write(step_label), run_time=T_WRITE)
        self.play(ReplacementTransform(hi_darkness, result), run_time=T_TRANSFORM)
        self.wait(T_WAIT)
        self.play(FadeOut(step_label), run_time=T_FADE)

        ok = Text("✓ Hi beautiful darkness", font_size=LABEL_FONT, color=GREEN)
        ok.move_to(ORIGIN + DOWN * LABEL_Y)
        self.play(Write(ok), run_time=T_WRITE)
        self.wait(T_END)

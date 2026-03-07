"""
Scene: How LCP (Largest Contentful Paint) is calculated.

Shows a viewport; elements appear one by one. The browser marks the
current largest visible element as the LCP candidate (light green).
When a larger element renders, it becomes the new LCP candidate.
"""

from manim import *

from common import (
    COLOR_BG,
    COLOR_ELEMENT,
    COLOR_ELEMENT_STROKE,
    COLOR_VIEWPORT,
    FONT_DEFAULT,
    LABEL_COLOR,
    LCP_HIGHLIGHT,
    T_APPEAR,
    T_END,
    T_HIGHLIGHT,
    T_WAIT,
    T_WAIT_LONG,
    T_WRITE,
    create_plane,
    debug_font_info,
)


def make_viewport(width: float = 10, height: float = 6) -> Rectangle:
    """Viewport: big rectangle (browser window)."""
    return Rectangle(
        width=width,
        height=height,
        stroke_color=COLOR_VIEWPORT,
        stroke_width=2,
        fill_color=COLOR_BG,
        fill_opacity=0.3,
    )


def make_element(width: float, height: float, fill_color=COLOR_ELEMENT) -> Rectangle:
    """One content element (img, text block, etc.) inside the viewport."""
    return Rectangle(
        width=width,
        height=height,
        stroke_color=COLOR_ELEMENT_STROKE,
        stroke_width=1.5,
        fill_color=fill_color,
        fill_opacity=0.9,
    )


class LCPCalculated(Scene):
    def construct(self):
        self.camera.background_color = COLOR_BG
        debug_font_info("01_lcp_calculated.LCPCalculated")
        try:
            Text.set_default(font=FONT_DEFAULT)
        except Exception:
            pass
        bg_plane = create_plane()
        if bg_plane is not None:
            self.add(bg_plane)

        title = Text(
            "How LCP is calculated",
            font_size=32,
            color=LABEL_COLOR,
            font=FONT_DEFAULT,
        )
        title.to_edge(UP, buff=0.4)
        self.play(Write(title), run_time=T_WRITE)
        self.wait(0.3)

        viewport = make_viewport()
        self.play(Create(viewport), run_time=0.5)
        self.wait(0.3)

        # Element 1: small rectangle (e.g. headline)
        elem1 = make_element(1.8, 0.7)
        elem1.move_to(viewport.get_center() + UP * 1.5 + LEFT * 2.5)
        self.play(Create(elem1), run_time=T_APPEAR)
        self.wait(0.2)
        self.play(
            elem1.animate.set_fill_color(LCP_HIGHLIGHT).set_stroke_color(LCP_HIGHLIGHT),
            run_time=T_HIGHLIGHT,
        )
        label1 = Text("LCP candidate", font_size=22, color=LCP_HIGHLIGHT, font=FONT_DEFAULT)
        label1.next_to(elem1, DOWN, buff=0.2)
        self.play(FadeIn(label1), run_time=0.3)
        self.wait(T_WAIT)

        # Element 2: larger — becomes new largest
        elem2 = make_element(3.2, 1.6)
        elem2.move_to(viewport.get_center() + RIGHT * 1.2)
        self.play(Create(elem2), run_time=T_APPEAR)
        self.wait(0.2)
        # Revert first to default, highlight second
        self.play(
            elem1.animate.set_fill_color(COLOR_ELEMENT).set_stroke_color(COLOR_ELEMENT_STROKE),
            elem2.animate.set_fill_color(LCP_HIGHLIGHT).set_stroke_color(LCP_HIGHLIGHT),
            FadeOut(label1),
            run_time=T_HIGHLIGHT,
        )
        label2 = Text("LCP candidate", font_size=22, color=LCP_HIGHLIGHT, font=FONT_DEFAULT)
        label2.next_to(elem2, DOWN, buff=0.2)
        self.play(FadeIn(label2), run_time=0.3)
        self.wait(T_WAIT)

        # Element 3: largest — final LCP
        elem3 = make_element(5.0, 2.8)
        elem3.move_to(viewport.get_center() + DOWN * 0.2)
        self.play(Create(elem3), run_time=T_APPEAR)
        self.wait(0.2)
        self.play(
            elem2.animate.set_fill_color(COLOR_ELEMENT).set_stroke_color(COLOR_ELEMENT_STROKE),
            elem3.animate.set_fill_color(LCP_HIGHLIGHT).set_stroke_color(LCP_HIGHLIGHT),
            FadeOut(label2),
            run_time=T_HIGHLIGHT,
        )
        label3 = Text("LCP candidate (final)", font_size=22, color=LCP_HIGHLIGHT, font=FONT_DEFAULT)
        label3.next_to(elem3, DOWN, buff=0.25)
        self.play(FadeIn(label3), run_time=0.3)
        self.wait(T_WAIT_LONG)

        # caption = Text(
        #     "LCP time = when this largest element finished rendering",
        #     font_size=24,
        #     color=LABEL_COLOR,
        #     font=FONT_DEFAULT,
        # )
        # caption.to_edge(DOWN, buff=0.5)
        # self.play(Write(caption), run_time=T_WRITE)
        # self.wait(T_END)

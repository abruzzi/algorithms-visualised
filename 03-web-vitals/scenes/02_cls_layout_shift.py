"""
Scene: How CLS (Cumulative Layout Shift) works.

Uses a 4×4 grid. Three layout changes: (1) one block grows to 2×2,
(2) one square becomes a 2×1 rectangle, (3) that rectangle shrinks back to square.
Others reflow each time; same grid, same gap.
"""

from manim import *

from common import (
    COLOR_BG,
    COLOR_ELEMENT,
    COLOR_ELEMENT_STROKE,
    COLOR_VIEWPORT,
    CLS_SHIFT_HIGHLIGHT,
    FONT_DEFAULT,
    LABEL_COLOR,
    T_APPEAR,
    T_END,
    T_WAIT,
    T_WRITE,
    create_plane,
    debug_font_info,
)


# Grid system: 4×4 equal cells, same gap everywhere
# Style aligned with 02-ot-crdt / LCP: same colors, corner radius, stroke, fill opacity
GRID_ROWS = GRID_COLS = 4
CELL_SIZE = 0.95
GAP = 0.18
CORNER_RADIUS = 0.06
STROKE_WIDTH = 2
FILL_OPACITY = 0.85
GRID_LINE_OPACITY = 0.4


def make_viewport(width: float = 10, height: float = 6):
    return Rectangle(
        width=width,
        height=height,
        stroke_color=COLOR_VIEWPORT,
        stroke_width=STROKE_WIDTH,
        fill_opacity=0,
    )


def cell_center(row: int, col: int, origin):
    """Center of grid cell (row, col); row 0 top, col 0 left."""
    total_w = GRID_COLS * CELL_SIZE + (GRID_COLS - 1) * GAP
    total_h = GRID_ROWS * CELL_SIZE + (GRID_ROWS - 1) * GAP
    x = origin[0] - total_w / 2 + (CELL_SIZE + GAP) * col + CELL_SIZE / 2
    y = origin[1] + total_h / 2 - (CELL_SIZE + GAP) * row - CELL_SIZE / 2
    return np.array([x, y, 0])


def span_center_2x1(row: int, col: int, origin):
    """Center of a 2×1 horizontal span (cells (r,c) and (r,c+1))."""
    return (cell_center(row, col, origin) + cell_center(row, col + 1, origin)) / 2


def make_cell_card():
    """One cell-sized card (1×1). Same style as other examples: node fill, border, radius, stroke."""
    return RoundedRectangle(
        width=CELL_SIZE,
        height=CELL_SIZE,
        corner_radius=CORNER_RADIUS,
        stroke_color=COLOR_ELEMENT_STROKE,
        stroke_width=STROKE_WIDTH,
        fill_color=COLOR_ELEMENT,
        fill_opacity=FILL_OPACITY,
    )


def make_grid_lines(origin):
    """4×4 grid lines (vertical and horizontal) so the system is visible."""
    total_w = GRID_COLS * CELL_SIZE + (GRID_COLS - 1) * GAP
    total_h = GRID_ROWS * CELL_SIZE + (GRID_ROWS - 1) * GAP
    left = origin[0] - total_w / 2
    right = origin[0] + total_w / 2
    top = origin[1] + total_h / 2
    bottom = origin[1] - total_h / 2
    lines = VGroup()
    for i in range(GRID_ROWS + 1):
        y = top - i * (CELL_SIZE + GAP)
        lines.add(Line([left, y, 0], [right, y, 0], stroke_color=COLOR_VIEWPORT, stroke_width=0.5))
    for j in range(GRID_COLS + 1):
        x = left + j * (CELL_SIZE + GAP)
        lines.add(Line([x, top, 0], [x, bottom, 0], stroke_color=COLOR_VIEWPORT, stroke_width=0.5))
    lines.set_opacity(GRID_LINE_OPACITY)
    return lines


class CLSLayoutShift(Scene):
    def construct(self):
        self.camera.background_color = COLOR_BG
        debug_font_info("02_cls_layout_shift.CLSLayoutShift")
        try:
            Text.set_default(font=FONT_DEFAULT)
        except Exception:
            pass
        bg_plane = create_plane()
        if bg_plane is not None:
            self.add(bg_plane)

        title = Text(
            "How CLS (Cumulative Layout Shift) works",
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

        origin = viewport.get_center()
        grid_lines = make_grid_lines(origin)
        self.add(grid_lines)

        # Six blocks: top row (0,0)-(0,2), second row (1,0)-(1,2). All 1×1 squares.
        A = make_cell_card().move_to(cell_center(0, 0, origin))
        B = make_cell_card().move_to(cell_center(0, 1, origin))
        C = make_cell_card().move_to(cell_center(0, 2, origin))
        D = make_cell_card().move_to(cell_center(1, 0, origin))
        E = make_cell_card().move_to(cell_center(1, 1, origin))
        F = make_cell_card().move_to(cell_center(1, 2, origin))
        blocks = VGroup(A, B, C, D, E, F)
        self.play(Create(blocks), run_time=T_APPEAR)
        self.wait(T_WAIT)

        big_w = 2 * CELL_SIZE + GAP
        big_h = 2 * CELL_SIZE + GAP
        big_center = (cell_center(0, 0, origin) + cell_center(1, 1, origin)) / 2
        rect_w = 2 * CELL_SIZE + GAP
        rect_h = CELL_SIZE

        def play_shift_label(msg):
            lab = Text(msg, font_size=18, color=CLS_SHIFT_HIGHLIGHT, font=FONT_DEFAULT)
            lab.next_to(viewport, DOWN, buff=0.35)
            return lab

        # ——— Change 1: A grows to 2×2; B,C,D,E,F reflow (row-major next free)
        lab1 = play_shift_label("1. Square grows to 2×2 → others reflow")
        self.play(
            A.animate.set_fill_color(CLS_SHIFT_HIGHLIGHT).set_stroke_color(CLS_SHIFT_HIGHLIGHT),
            run_time=0.3,
        )
        self.play(FadeIn(lab1), run_time=0.25)
        self.wait(0.3)
        self.play(
            A.animate.stretch(big_w / CELL_SIZE, 0).stretch(big_h / CELL_SIZE, 1).move_to(big_center),
            B.animate.move_to(cell_center(0, 2, origin)),
            C.animate.move_to(cell_center(0, 3, origin)),
            D.animate.move_to(cell_center(1, 2, origin)),
            E.animate.move_to(cell_center(1, 3, origin)),
            F.animate.move_to(cell_center(2, 0, origin)),
            run_time=0.95,
        )
        self.play(
            B.animate.set_stroke_color(CLS_SHIFT_HIGHLIGHT),
            C.animate.set_stroke_color(CLS_SHIFT_HIGHLIGHT),
            D.animate.set_stroke_color(CLS_SHIFT_HIGHLIGHT),
            E.animate.set_stroke_color(CLS_SHIFT_HIGHLIGHT),
            F.animate.set_stroke_color(CLS_SHIFT_HIGHLIGHT),
            run_time=0.2,
        )
        self.wait(0.25)
        self.play(
            A.animate.set_fill_color(COLOR_ELEMENT).set_stroke_color(COLOR_ELEMENT_STROKE),
            B.animate.set_stroke_color(COLOR_ELEMENT_STROKE),
            C.animate.set_stroke_color(COLOR_ELEMENT_STROKE),
            D.animate.set_stroke_color(COLOR_ELEMENT_STROKE),
            E.animate.set_stroke_color(COLOR_ELEMENT_STROKE),
            F.animate.set_stroke_color(COLOR_ELEMENT_STROKE),
            FadeOut(lab1),
            run_time=0.25,
        )
        self.wait(T_WAIT)

        # ——— Change 2: D (square at (1,2)) becomes 2×1 rectangle; E (at (1,3)) reflows to (2,1)
        lab2 = play_shift_label("2. Square → rectangle (2×1) → neighbor reflows")
        self.play(
            D.animate.set_fill_color(CLS_SHIFT_HIGHLIGHT).set_stroke_color(CLS_SHIFT_HIGHLIGHT),
            run_time=0.3,
        )
        self.play(FadeIn(lab2), run_time=0.25)
        self.wait(0.3)
        d_rect_center = span_center_2x1(1, 2, origin)
        self.play(
            D.animate.stretch(rect_w / CELL_SIZE, 0).move_to(d_rect_center),
            E.animate.move_to(cell_center(2, 1, origin)),
            run_time=0.95,
        )
        self.play(E.animate.set_stroke_color(CLS_SHIFT_HIGHLIGHT), run_time=0.2)
        self.wait(0.25)
        self.play(
            D.animate.set_fill_color(COLOR_ELEMENT).set_stroke_color(COLOR_ELEMENT_STROKE),
            E.animate.set_stroke_color(COLOR_ELEMENT_STROKE),
            FadeOut(lab2),
            run_time=0.25,
        )
        self.wait(T_WAIT)

        # ——— Change 3: D (rectangle) shrinks back to 1×1 square; E reflows back to (1,3)
        lab3 = play_shift_label("3. Rectangle → square → neighbor reflows back")
        self.play(
            D.animate.set_fill_color(CLS_SHIFT_HIGHLIGHT).set_stroke_color(CLS_SHIFT_HIGHLIGHT),
            run_time=0.3,
        )
        self.play(FadeIn(lab3), run_time=0.25)
        self.wait(0.3)
        self.play(
            D.animate.stretch(CELL_SIZE / rect_w, 0).move_to(cell_center(1, 2, origin)),
            E.animate.move_to(cell_center(1, 3, origin)),
            run_time=0.95,
        )
        self.play(E.animate.set_stroke_color(CLS_SHIFT_HIGHLIGHT), run_time=0.2)
        self.wait(0.25)
        self.play(
            D.animate.set_fill_color(COLOR_ELEMENT).set_stroke_color(COLOR_ELEMENT_STROKE),
            E.animate.set_stroke_color(COLOR_ELEMENT_STROKE),
            FadeOut(lab3),
            run_time=0.25,
        )
        self.wait(T_WAIT)

        # caption = Text(
        #     "Layout: same grid, same gap. Resize one → others flow and reshape.",
        #     font_size=24,
        #     color=LABEL_COLOR,
        #     font=FONT_DEFAULT,
        # )
        # caption.to_edge(DOWN, buff=0.5)
        # self.play(Write(caption), run_time=T_WRITE)
        # self.wait(T_END)

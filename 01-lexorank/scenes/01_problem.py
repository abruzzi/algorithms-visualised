"""
Scene 1: The Problem — drag-and-drop list with integer positions.
Boxes with letters (A, B, C, …), position label next to each.
Animate moving one box and the cascade of position changes.
End: zoom out to 200 elements — first column = our 5 (1–5), 39 columns next to it (6–200); labels flash.
"""

import random
from manim import *

# Branding (keep for accent)
BRAND_RED = "#bd1b1d"
BRAND_TEAL = "#6dc0c9"

# Professional look: deep, high-contrast, low saturation (Gemini-style “senior architect”)
COLOR_BG = "#121212"           # Deeper than gray — more premium
COLOR_NODE = "#2C3E50"        # Dark blue-gray for node fill
COLOR_NODE_BORDER = "#3498DB"  # Bright blue border (or use BRAND_TEAL)
TEXT_LIGHT = "#E0E0E0"        # Soft gray text, less eye strain
LABEL_DEFAULT = "#ffffff"      # Position label: white by default
LABEL_UPDATED = "#F1C40F"      # Yellow highlight when updated (midpoint / cascade)
COLOR_ACCENT = "#2ECC71"       # Green for “insert success” (optional)

# Fonts (optional): set in construct() with Text.set_default(font=FONT_SANS) if installed
# FONT_SANS = "Inter"   # titles / body
# FONT_MONO = "JetBrains Mono"  # rank/position numbers for alignment


def make_item(letter: str, position: int, width=0.6, height=0.5) -> VGroup:
    """One item: rounded box with letter + position label (professional node style)."""
    rect = RoundedRectangle(
        width=width, height=height, corner_radius=0.08,
        stroke_color=COLOR_NODE_BORDER, stroke_width=2,
        fill_color=COLOR_NODE, fill_opacity=0.85,
    )
    letter_text = Text(letter, font_size=32, color=TEXT_LIGHT).move_to(rect.get_center())
    pos_text = Text(str(position), font_size=28, color=LABEL_DEFAULT).next_to(rect, RIGHT, buff=0.25)
    return VGroup(rect, letter_text, pos_text)


def make_small_box(position: int, width=0.12, height=0.1) -> VGroup:
    """Tiny box for the zoomed-out grid."""
    rect = RoundedRectangle(
        width=width, height=height, corner_radius=0.02,
        stroke_color=COLOR_NODE_BORDER, stroke_width=1,
        fill_color=COLOR_NODE, fill_opacity=0.8,
    )
    pos_text = Text(str(position), font_size=10, color=LABEL_DEFAULT).next_to(rect, RIGHT, buff=0.04)
    return VGroup(rect, pos_text)


def make_small_item(letter: str, position: int, width=0.12, height=0.1) -> VGroup:
    """Tiny box with letter + position (first 5 in grid)."""
    rect = RoundedRectangle(
        width=width, height=height, corner_radius=0.02,
        stroke_color=COLOR_NODE_BORDER, stroke_width=1,
        fill_color=COLOR_NODE, fill_opacity=0.8,
    )
    letter_text = Text(letter, font_size=8, color=TEXT_LIGHT).move_to(rect.get_center())
    pos_text = Text(str(position), font_size=10, color=LABEL_UPDATED).next_to(rect, RIGHT, buff=0.04)
    return VGroup(rect, letter_text, pos_text)


class ProblemIntro(Scene):
    def construct(self):
        self.camera.background_color = COLOR_BG

        # Optional: very faint grid (professional “memory/coordinate” feel)
        try:
            bg_plane = NumberPlane(
                x_range=(-10, 10, 0.5),
                y_range=(-10, 10, 0.5),
                x_length=14,
                y_length=14,
                background_line_style={"stroke_opacity": 0.06},
                faded_line_style={"stroke_opacity": 0.03},
            ).fade(0.9)
            self.add(bg_plane)
        except Exception:
            pass

        title = Text("Ordered list: positions as integers", font_size=36, color=TEXT_LIGHT)
        title.to_edge(UP)
        self.play(Write(title), run_time=0.8)
        self.wait(0.5)

        # Initial list: A(1), B(2), C(3), D(4), E(5)
        letters = ["A", "B", "C", "D", "E"]
        positions = [1, 2, 3, 4, 5]
        items = VGroup(*[make_item(ltr, pos) for ltr, pos in zip(letters, positions)])
        items.arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        items.next_to(title, DOWN, buff=0.8)

        self.play(LaggedStart(*(FadeIn(item, shift=UP * 0.2) for item in items), lag_ratio=0.12), run_time=0.8)
        self.wait(1.0)

        # Drag E to between A and B; then reflow B, C, D down
        item_a, item_b, item_c, item_d, item_e = items
        slot_height = item_a.height + 0.35
        target_e = item_a.get_center() + DOWN * slot_height
        item_e.generate_target()
        item_e.target.move_to(target_e)

        self.play(MoveToTarget(item_e), run_time=1.2, rate_func=smooth)
        self.wait(0.5)

        item_b.generate_target()
        item_b.target.move_to(target_e + DOWN * slot_height)
        item_c.generate_target()
        item_c.target.move_to(target_e + 2 * DOWN * slot_height)
        item_d.generate_target()
        item_d.target.move_to(target_e + 3 * DOWN * slot_height)

        self.play(
            MoveToTarget(item_b),
            MoveToTarget(item_c),
            MoveToTarget(item_d),
            run_time=1.2,
            rate_func=smooth,
        )
        self.wait(0.5)

        # Animate position labels: A=1, E=2, B=3, C=4, D=5 (updated → yellow)
        new_positions = [1, 2, 3, 4, 5]
        order_after = [item_a, item_e, item_b, item_c, item_d]
        for mob, new_pos in zip(order_after, new_positions):
            old_pos_text = mob[2]
            label_color = LABEL_UPDATED if new_pos != 1 else LABEL_DEFAULT
            new_pos_text = Text(str(new_pos), font_size=28, color=label_color).move_to(old_pos_text.get_center())
            self.play(Transform(old_pos_text, new_pos_text), run_time=0.4)
        self.wait(1.5)  # Key conclusion: let it land

        # Zoom-out: 200 elements. Col 0 = 1-5, col 1 = 6-10, col 2 = 11-15, ... col 39 = 196-200.
        # Other options: 5×20 (100 el); 5×200 (1000 el, “199 columns next to it”); 1 col + long row of 195.
        letters_order = ["A", "E", "B", "C", "D"]
        n_cols = 40
        grid_cells = [
            make_small_item(letters_order[i], i + 1) for i in range(5)
        ] + [make_small_box(i) for i in range(6, 201)]
        grid = VGroup(*grid_cells)
        grid.arrange_in_grid(rows=5, cols=n_cols, buff=0.04, flow_order="dr")

        # Scene change: from current 1-5 view to the full 200 grid
        self.play(FadeOut(title), FadeOut(items), run_time=0.5)
        self.add(grid)
        labels_to_hide = VGroup(
            *[grid_cells[i][2] for i in range(5)],
            *[grid_cells[i][1] for i in range(5, 200)],
        )
        self.play(FadeOut(labels_to_hide), run_time=0.3)
        self.wait(0.2)

        # Scale so grid of boxes almost fills the frame
        grid.generate_target()
        frame_w = config["frame_width"]
        frame_h = config["frame_height"]
        scale = min((frame_w * 0.92) / grid.width, (frame_h * 0.92) / grid.height)
        grid.target.scale(scale).move_to(ORIGIN)
        self.play(MoveToTarget(grid), run_time=1.5, rate_func=smooth)
        self.wait(0.3)

        # Flash random boxes to suggest cascade updates everywhere
        all_boxes = [grid_cells[i][0] for i in range(200)]
        rng = random.Random(42)
        for _ in range(10):
            indices = rng.sample(range(200), min(12, 200))
            flash_anims = [Indicate(all_boxes[i], color=LABEL_UPDATED, scale_factor=1.2) for i in indices]
            self.play(AnimationGroup(*flash_anims, lag_ratio=0.03), run_time=0.4)
        self.wait(1.0)

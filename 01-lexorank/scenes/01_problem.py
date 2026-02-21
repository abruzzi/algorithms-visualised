"""
Scene 1: The Problem — drag-and-drop list with integer positions.
Boxes with letters (A, B, C, …), position label next to each.
Animate moving one box and the cascade of position changes.
"""

from manim import *


def make_item(letter: str, position: int, width=0.6, height=0.5) -> VGroup:
    """One item: a box with letter inside, and position number next to it."""
    rect = Rectangle(width=width, height=height, stroke_color=WHITE, fill_color=BLUE_E, fill_opacity=0.8)
    letter_text = Text(letter, font_size=32).move_to(rect.get_center())
    pos_text = Text(str(position), font_size=28, color=YELLOW).next_to(rect, RIGHT, buff=0.25)
    return VGroup(rect, letter_text, pos_text)


class ProblemIntro(Scene):
    def construct(self):
        title = Text("Ordered list: positions as integers", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))

        # Initial list: A(1), B(2), C(3), D(4), E(5) — each is box + letter + position label
        letters = ["A", "B", "C", "D", "E"]
        positions = [1, 2, 3, 4, 5]
        items = VGroup(*[make_item(ltr, pos) for ltr, pos in zip(letters, positions)])
        items.arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        items.next_to(title, DOWN, buff=0.8)

        self.play(LaggedStart(*(Create(item) for item in items), lag_ratio=0.15))
        self.wait(0.8)

        # Drag E to between A and B: move E's box up to second slot, then reflow B,C,D down
        item_a, item_b, item_c, item_d, item_e = items
        slot_height = item_a.height + 0.35

        # E goes to second slot (between A and B) = just below A
        target_e = item_a.get_center() + DOWN * slot_height
        item_e.generate_target()
        item_e.target.move_to(target_e)

        self.play(MoveToTarget(item_e), run_time=1.2)
        self.wait(0.3)

        # B, C, D shift down one slot each
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
            run_time=1.0,
        )
        self.wait(0.2)

        # Animate position labels changing: A=1, E=2, B=3, C=4, D=5
        # Each item's position text is item[i][2] (third element = pos_text)
        new_positions = [1, 2, 3, 4, 5]  # A stays 1, E becomes 2, B→3, C→4, D→5
        order_after = [item_a, item_e, item_b, item_c, item_d]
        for mob, new_pos in zip(order_after, new_positions):
            old_pos_text = mob[2]
            new_pos_text = Text(str(new_pos), font_size=28, color=YELLOW).move_to(old_pos_text.get_center())
            self.play(Transform(old_pos_text, new_pos_text), run_time=0.35)
        self.wait(1.2)

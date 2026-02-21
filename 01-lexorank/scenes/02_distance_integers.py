"""
Scene 2: Distance integers — positions 1000, 2000, 3000, ...
Insert between 1000 and 2000 → use 1500. No renumbering.
"""

from manim import *


class DistanceIntegers(Scene):
    def construct(self):
        title = Text("Sparse integers: leave room between positions", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))

        # Positions 1000, 2000, 3000, 4000, 5000
        positions = [1000, 2000, 3000, 4000, 5000]
        labels = [f"Item {i}" for i in "ABCDE"]
        items = VGroup()
        for i, (pos, lbl) in enumerate(zip(positions, labels)):
            box = VGroup(
                Text(f"[{pos}]", font_size=26, color=YELLOW),
                Text(lbl, font_size=22),
            ).arrange(RIGHT, buff=0.3)
            box.move_to(UP * (1.5 - i * 0.55))
            items.add(box)

        self.play(LaggedStart(*(Create(item) for item in items), lag_ratio=0.2))
        self.wait(1)

        # Highlight gap between 1000 and 2000
        gap_label = Text("gap = 1000", font_size=24, color=GREEN)
        gap_label.move_to(items[0].get_right() + RIGHT * 1.2)
        self.play(Write(gap_label))
        self.wait(0.8)
        self.play(FadeOut(gap_label))

        # Insert between 1000 and 2000 → 1500
        new_item = VGroup(
            Text("[1500]", font_size=26, color=GREEN),
            Text("New item", font_size=22),
        ).arrange(RIGHT, buff=0.3)
        new_item.move_to(items[0].get_center() + DOWN * 0.6)
        new_item.shift(LEFT * 0.5)

        self.play(
            items[0].animate.shift(UP * 0.3),
            items[1:].animate.shift(DOWN * 0.3),
        )
        self.play(FadeIn(new_item, shift=UP * 0.2))
        self.wait(1)

        one_write = Text("One write. No cascade.", font_size=28, color=GREEN)
        one_write.next_to(new_item, DOWN, buff=0.6)
        self.play(Write(one_write))
        self.wait(2)


class SparseRebalance(Scene):
    """Gap runs out (1500, 1501, 1502) → rebalance segment. Happens often with sparse ints."""
    def construct(self):
        title = Text("Sparse integers: when the gap runs out", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))

        # Crowded: 1000, 1500, 1501, 1502, 2000
        positions = [1000, 1500, 1501, 1502, 2000]
        labels = ["A", "X", "Y", "Z", "B"]
        items = VGroup()
        for i, (pos, lbl) in enumerate(zip(positions, labels)):
            box = VGroup(
                Text(f"[{pos}]", font_size=24, color=YELLOW),
                Text(lbl, font_size=20),
            ).arrange(RIGHT, buff=0.25)
            box.move_to(UP * (1.2 - i * 0.5))
            items.add(box)

        self.play(LaggedStart(*(Create(item) for item in items), lag_ratio=0.2))
        self.wait(1)

        # "No integer between 1501 and 1502!"
        problem = Text("No integer between 1501 and 1502!", font_size=26, color=RED)
        problem.next_to(items, DOWN, buff=0.6)
        self.play(Write(problem))
        self.wait(1.2)

        rebalance_label = Text("Rebalance: respace segment → restore gaps", font_size=26, color=TEAL)
        rebalance_label.next_to(problem, DOWN, buff=0.4)
        self.play(Write(rebalance_label))
        self.play(FadeOut(problem))

        # After rebalance: 1000, 2000, 3000, 4000, 5000
        new_positions = [1000, 2000, 3000, 4000, 5000]
        items2 = VGroup()
        for i, (pos, lbl) in enumerate(zip(new_positions, labels)):
            box = VGroup(
                Text(f"[{pos}]", font_size=24, color=GREEN),
                Text(lbl, font_size=20),
            ).arrange(RIGHT, buff=0.25)
            box.move_to(UP * (1.2 - i * 0.5))
            items2.add(box)

        self.play(Transform(items, items2))
        self.wait(1)

        often = Text("Rebalance: often (every time gap runs out)", font_size=24, color=TEAL)
        often.to_edge(DOWN, buff=0.5)
        self.play(Write(often))
        self.wait(2)

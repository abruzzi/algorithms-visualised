"""
Scene 3: Lexorank — when the gap runs out, use string ranks.
Lexicographic midpoint between "a" and "m" → "g".
"""

from manim import *

from common import FONT_DEFAULT


class LexorankAlgorithm(Scene):
    def construct(self):
        try:
            Text.set_default(font=FONT_DEFAULT)
        except Exception:
            pass
        title = Text(
            "When the gap runs out: Lexorank",
            font=FONT_DEFAULT,
            font_size=36,
        )
        title.to_edge(UP)
        self.play(Write(title))

        # Show integer overflow: 1500, 1501, 1502 — no room
        problem_line = VGroup(
            Text("[1500] [1501] [1502]", font=FONT_DEFAULT, font_size=28, color=YELLOW),
            Text("No integer between 1500 and 1501!", font=FONT_DEFAULT, font_size=24, color=RED),
        ).arrange(DOWN, buff=0.3).shift(UP * 0.5)
        self.play(Write(problem_line))
        self.wait(1.5)
        self.play(FadeOut(problem_line))

        # String ranks: "a", "m", "z" (lexicographic order)
        subtitle = Text(
            "String-based ranks (e.g. alphabet 0-9, a-z)",
            font=FONT_DEFAULT,
            font_size=28,
        )
        subtitle.next_to(title, DOWN, buff=0.4)
        self.play(Write(subtitle))

        ranks = VGroup(
            Text('rank: "a"', font=FONT_DEFAULT, font_size=32, color=BLUE),
            Text('rank: "m"', font=FONT_DEFAULT, font_size=32, color=BLUE),
            Text('rank: "z"', font=FONT_DEFAULT, font_size=32, color=BLUE),
        ).arrange(DOWN, buff=0.4).shift(DOWN * 0.2)
        self.play(LaggedStart(*(Write(r) for r in ranks), lag_ratio=0.3))
        self.wait(1)

        # Insert between "a" and "m" → midpoint "g"
        mid_label = Text(
            'Midpoint between "a" and "m" → "g"',
            font=FONT_DEFAULT,
            font_size=28,
            color=GREEN,
        )
        mid_label.next_to(ranks, DOWN, buff=0.8)
        self.play(Write(mid_label))

        new_rank = Text('rank: "g"', font=FONT_DEFAULT, font_size=32, color=GREEN)
        new_rank.move_to(ranks[0].get_center() + DOWN * 0.9)
        self.play(FadeIn(new_rank))
        self.wait(1.5)

        # Rebalance rare
        rare_label = Text(
            "Rebalance: rare (huge space: 36^n ranks; extend string or rebalance only when needed)",
            font=FONT_DEFAULT,
            font_size=20,
            color=GRAY,
        )
        rare_label.to_edge(DOWN, buff=0.5)
        self.play(Write(rare_label))
        self.wait(2)


class LexorankSummary(Scene):
    """Optional summary: four bullets including rebalance frequency."""
    def construct(self):
        try:
            Text.set_default(font=FONT_DEFAULT)
        except Exception:
            pass
        title = Text(
            "Lexorank in a nutshell",
            font=FONT_DEFAULT,
            font_size=40,
        )
        title.to_edge(UP)
        self.play(Write(title))

        bullets = VGroup(
            Text("1. Integer positions → cascade updates (expensive)", font=FONT_DEFAULT, font_size=24),
            Text("2. Sparse integers → one write; gap runs out → rebalance often", font=FONT_DEFAULT, font_size=24),
            Text("3. Lexorank → string ranks + midpoint; rebalance rare", font=FONT_DEFAULT, font_size=24),
            Text("4. Trade-off: sparse = simple but frequent rebalance; Lexorank = scales, rare rebalance", font=FONT_DEFAULT, font_size=22),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).shift(DOWN * 0.2)
        self.play(LaggedStart(*(Write(b) for b in bullets), lag_ratio=0.4))
        self.wait(3)

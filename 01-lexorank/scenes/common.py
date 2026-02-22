"""
Shared style, animation timing, and helpers for Lexorank scenes.
Import colors, timing constants, make_item, make_box_only from here.
"""

from manim import *
import manimpango

# -----------------------------------------------------------------------------
# Font
# -----------------------------------------------------------------------------
def _pick_first_available_font(preferred):
    """Return the first font in preferred that appears in list_fonts (avoids Manim's comma-string warning)."""
    available = set(manimpango.list_fonts())
    for name in preferred:
        if name in available:
            return name
    return preferred[0]  # fallback to first; Manim may still find it via Pango


FONT_PREFERRED_ORDER = ["Fira Code", "JetBrains Mono", "SF Mono"]
# Use Fira Code when available; otherwise first available from preferred order.
FONT_DEFAULT = _pick_first_available_font(FONT_PREFERRED_ORDER)
# Use same font as titles/letters so all text (including position/rank labels) matches 01.
FONT_POSITION_LABEL = FONT_DEFAULT


def debug_font_info(scene_name: str = "scene"):
    """Log current font to console only (no on-screen label)."""
    import logging
    t = Text("A", font=FONT_DEFAULT, font_size=24)
    actual_font = getattr(t, "font", FONT_DEFAULT)
    logging.getLogger("manim").info(
        f"[{scene_name}] font: requested={FONT_DEFAULT!r} resolved={actual_font!r} "
        f"(available: {FONT_DEFAULT in set(manimpango.list_fonts())})"
    )

# -----------------------------------------------------------------------------
# Colors
# -----------------------------------------------------------------------------
COLOR_BG = "#121212"
COLOR_NODE = "#2C3E50"
COLOR_NODE_BORDER = "#3498DB"
TEXT_LIGHT = "#E0E0E0"
LABEL_DEFAULT = "#ffffff"
LABEL_UPDATED = "#F1C40F"

# -----------------------------------------------------------------------------
# Node / item styling
# -----------------------------------------------------------------------------
ITEM_WIDTH = 0.6
ITEM_HEIGHT = 0.5
ITEM_CORNER_RADIUS = 0.08
ITEM_STROKE_WIDTH = 2
ITEM_FILL_OPACITY = 0.85
LETTER_FONT_SIZE = 32
POSITION_FONT_SIZE = 28
POSITION_LABEL_BUFF = 0.68

# Zoom-out / grid boxes (e.g. 01_problem)
BOX_ONLY_WIDTH = 0.14
BOX_ONLY_HEIGHT = 0.12
BOX_ONLY_CORNER_RADIUS = 0.02
BOX_ONLY_STROKE_WIDTH = 1
BOX_ONLY_FILL_OPACITY = 0.8

# -----------------------------------------------------------------------------
# Layout
# -----------------------------------------------------------------------------
ITEM_ARRANGE_BUFF = 0.35
SLOT_OFFSET = 0.35  # slot_height = item.height + SLOT_OFFSET

# -----------------------------------------------------------------------------
# Typography (titles, labels, conclusions)
# -----------------------------------------------------------------------------
TITLE_FONT_SIZE = 36
CONCLUSION_FONT_SIZE = 32
CONCLUSION_FONT_SIZE_SMALL = 28
LABEL_SMALL_FONT_SIZE = 26
LABEL_TINY_FONT_SIZE = 22

# -----------------------------------------------------------------------------
# Animation timing — titles & intro
# -----------------------------------------------------------------------------
TITLE_WRITE_RUN_TIME = 0.8
TITLE_WAIT_AFTER = 0.5
ITEMS_FADEIN_RUN_TIME = 0.8
ITEMS_FADEIN_LAG_RATIO = 0.12
ITEMS_FADEIN_SHIFT = 0.2
ITEMS_WAIT_AFTER = 1.0

# Slightly faster intro (e.g. 03 rebalance)
ITEMS_FADEIN_SHIFT_FAST = 0.15
ITEMS_FADEIN_LAG_RATIO_FAST = 0.1
ITEMS_WAIT_AFTER_SHORT = 0.6

# -----------------------------------------------------------------------------
# Animation timing — moves / reflow
# -----------------------------------------------------------------------------
MOVE_RUN_TIME = 1.2
MOVE_WAIT_AFTER = 0.5
INSERT_MOVE_RUN_TIME = 1.0
INSERT_MOVE_FADEIN_SHIFT = 0.1
INSERT_WAIT_AFTER = 0.4

# -----------------------------------------------------------------------------
# Animation timing — label updates
# -----------------------------------------------------------------------------
LABEL_UPDATE_RUN_TIME = 0.4
LABEL_UPDATE_RUN_TIME_SLOW = 0.6
REBALANCE_LABELS_RUN_TIME = 1.4
REBALANCE_LAG_RATIO = 0.12
REBALANCE_WAIT_AFTER = 0.5

# -----------------------------------------------------------------------------
# Animation timing — misc
# -----------------------------------------------------------------------------
GAP_LABEL_FADEIN_RUN_TIME = 0.4
GAP_LABEL_WAIT = 0.6
GAP_LABEL_FADEOUT_RUN_TIME = 0.3
DENSITY_LABEL_WRITE_RUN_TIME = 0.6
DENSITY_LABEL_WAIT = 0.8
CONCLUSION_WRITE_RUN_TIME = 0.8
CONCLUSION_WAIT = 1.5
LABEL_UPDATE_WAIT_AFTER = 1.5
CONCLUSION_BUFF = 0.8
CONCLUSION_BUFF_SMALL = 0.7

# -----------------------------------------------------------------------------
# NumberPlane (background grid)
# -----------------------------------------------------------------------------
PLANE_X_RANGE = (-10, 10, 0.5)
PLANE_Y_RANGE = (-10, 10, 0.5)
PLANE_X_LENGTH = 14
PLANE_Y_LENGTH = 14
PLANE_BG_LINE_OPACITY = 0.14
PLANE_FADED_LINE_OPACITY = 0.07
PLANE_FADE = 0.5


def _text_font_kwargs():
    """Single place for font so letter and position labels never get different fallbacks."""
    return {"font": FONT_DEFAULT}


def make_position_label(value, color=LABEL_DEFAULT):
    """Position number label (for initial items)."""
    return Text(
        str(value),
        font=FONT_POSITION_LABEL,
        font_size=POSITION_FONT_SIZE,
        color=color,
    )


def make_position_label_like(value, color, existing_text_mobject):
    """Replacement position label using the exact same font as existing_text_mobject (so yellow matches white)."""
    return Text(
        str(value),
        font=existing_text_mobject.font,
        font_size=POSITION_FONT_SIZE,
        color=color,
    )


def _place_letter_in_rect(letter_text, rect):
    """Place letter centered in the rect."""
    letter_text.move_to(rect.get_center())


def make_item(
    letter: str,
    position: int,
    width: float = ITEM_WIDTH,
    height: float = ITEM_HEIGHT,
) -> VGroup:
    """One item: rounded box with letter + position label."""
    rect = RoundedRectangle(
        width=width,
        height=height,
        corner_radius=ITEM_CORNER_RADIUS,
        stroke_color=COLOR_NODE_BORDER,
        stroke_width=ITEM_STROKE_WIDTH,
        fill_color=COLOR_NODE,
        fill_opacity=ITEM_FILL_OPACITY,
    )
    letter_text = Text(
        letter,
        font_size=LETTER_FONT_SIZE,
        color=TEXT_LIGHT,
        **_text_font_kwargs(),
    )
    _place_letter_in_rect(letter_text, rect)
    pos_text = make_position_label(position, LABEL_DEFAULT).next_to(
        rect, RIGHT, buff=POSITION_LABEL_BUFF
    )
    return VGroup(rect, letter_text, pos_text)


def make_rank_label(rank_str: str, color=LABEL_DEFAULT):
    """String rank label for Lexorank (e.g. \"a\", \"am\"). Same font/size as position labels."""
    return Text(
        f'"{rank_str}"',
        font=FONT_POSITION_LABEL,
        font_size=POSITION_FONT_SIZE,
        color=color,
    )


def make_rank_label_like(rank_str: str, color, existing_text_mobject):
    """Replacement rank label using the same font as existing (for rebalance)."""
    return Text(
        f'"{rank_str}"',
        font=existing_text_mobject.font,
        font_size=POSITION_FONT_SIZE,
        color=color,
    )


def make_item_rank(
    letter: str,
    rank_str: str,
    width: float = ITEM_WIDTH,
    height: float = ITEM_HEIGHT,
) -> VGroup:
    """One item with string rank (Lexorank): rounded box + letter + rank label in quotes."""
    rect = RoundedRectangle(
        width=width,
        height=height,
        corner_radius=ITEM_CORNER_RADIUS,
        stroke_color=COLOR_NODE_BORDER,
        stroke_width=ITEM_STROKE_WIDTH,
        fill_color=COLOR_NODE,
        fill_opacity=ITEM_FILL_OPACITY,
    )
    letter_text = Text(
        letter,
        font_size=LETTER_FONT_SIZE,
        color=TEXT_LIGHT,
        **_text_font_kwargs(),
    )
    _place_letter_in_rect(letter_text, rect)
    rank_text = make_rank_label(rank_str, LABEL_DEFAULT).next_to(
        rect, RIGHT, buff=POSITION_LABEL_BUFF
    )
    return VGroup(rect, letter_text, rank_text)


def make_box_only(
    width: float = BOX_ONLY_WIDTH,
    height: float = BOX_ONLY_HEIGHT,
) -> VMobject:
    """Box only, no labels — for zoom-out grid."""
    return RoundedRectangle(
        width=width,
        height=height,
        corner_radius=BOX_ONLY_CORNER_RADIUS,
        stroke_color=COLOR_NODE_BORDER,
        stroke_width=BOX_ONLY_STROKE_WIDTH,
        fill_color=COLOR_NODE,
        fill_opacity=BOX_ONLY_FILL_OPACITY,
    )


def create_plane():
    """Create the shared NumberPlane background. Returns None if creation fails."""
    try:
        return (
            NumberPlane(
                x_range=PLANE_X_RANGE,
                y_range=PLANE_Y_RANGE,
                x_length=PLANE_X_LENGTH,
                y_length=PLANE_Y_LENGTH,
                background_line_style={"stroke_opacity": PLANE_BG_LINE_OPACITY},
                faded_line_style={"stroke_opacity": PLANE_FADED_LINE_OPACITY},
                axis_config={"stroke_width": 0},
            ).fade(PLANE_FADE)
        )
    except Exception:
        return None

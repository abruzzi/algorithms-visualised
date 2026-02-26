"""
Shared style, animation timing, and helpers for OT/CRDT scenes.
Matches 01-lexorank style: Fira Code, colors, rounded rects, timing constants.
"""

import os

from manim import *
import manimpango

# -----------------------------------------------------------------------------
# Font — single source of truth
# -----------------------------------------------------------------------------
def _register_fira_code():
    for path in (
        os.path.expanduser("~/Library/Fonts/FiraCode-Regular.ttf"),
        os.path.expanduser("~/Library/Fonts/Fira Code Regular.ttf"),
        "/Library/Fonts/FiraCode-Regular.ttf",
        "/usr/share/fonts/truetype/firacode/FiraCode-Regular.ttf",
    ):
        if os.path.isfile(path):
            try:
                manimpango.register_font(path)
                return
            except Exception:
                pass


_register_fira_code()
FONT_DEFAULT = "Fira Code"
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
# Cell / node styling (aligned with 01-lexorank item look)
# -----------------------------------------------------------------------------
CELL_SIZE = 0.5
CELL_CORNER_RADIUS = 0.06
CELL_STROKE_WIDTH = 2
CELL_FILL_OPACITY = 0.85
CELL_FONT = 28
CELL_POS_FONT = 14  # subscript: small and subtle
CELL_POS_BUFF = 0.03  # subscript below box
CELL_ARRANGE_BUFF = 0.06  # space between char cells — reads as string but not cramped
LABEL_FONT = 28
LABEL_SMALL_FONT = 26
INDEX_COLOR = "#888888"  # subtle grey for position subscript

NODE_SIZE = 0.6
NODE_BUFF = 0.18

# -----------------------------------------------------------------------------
# Layout
# -----------------------------------------------------------------------------
ITEM_ARRANGE_BUFF = 0.35

# -----------------------------------------------------------------------------
# Animation timing
# -----------------------------------------------------------------------------
TITLE_WRITE_RUN_TIME = 0.8
TITLE_WAIT_AFTER = 0.5
T_CREATE = 0.7
T_WRITE = 0.4
T_TRANSFORM = 0.8
T_FADE = 0.3
T_WAIT = 0.6
T_WAIT_LONG = 1.0
T_END = 2.0

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


def _cell_rect(size: float, color: str, corner_radius: float = CELL_CORNER_RADIUS):
    """One rounded rect for a cell (lexorank-style)."""
    return RoundedRectangle(
        width=size,
        height=size,
        corner_radius=corner_radius,
        stroke_color=color,
        stroke_width=CELL_STROKE_WIDTH,
        fill_color=COLOR_NODE,
        fill_opacity=CELL_FILL_OPACITY,
    )


def _text_font_kwargs():
    return {"font": FONT_DEFAULT}


def make_char_cells(
    s: str,
    color: str = TEXT_LIGHT,
    cell_size: float = CELL_SIZE,
    font_size: int = CELL_FONT,
    show_positions: bool = False,
    start_index: int = 0,
) -> VGroup:
    """One character per cell (rounded box + letter). If show_positions, add index as small subscript below each cell."""
    cells = []
    for i, c in enumerate(s):
        box = _cell_rect(cell_size, COLOR_NODE_BORDER)
        letter = Text(
            c,
            font_size=font_size,
            color=color,
            **_text_font_kwargs(),
        ).move_to(box)
        group = VGroup(box, letter)
        if show_positions:
            idx = Text(
                str(start_index + i),
                font=FONT_POSITION_LABEL,
                font_size=CELL_POS_FONT,
                color=INDEX_COLOR,
            )
            idx.next_to(box, DOWN, buff=CELL_POS_BUFF)
            group.add(idx)
        cells.append(group)
    return VGroup(*cells).arrange(RIGHT, buff=CELL_ARRANGE_BUFF)


def make_word_cells(
    words: list[str],
    color_overrides: dict[int, str] | None = None,
    font_size: int = 26,
    padding: float = 0.2,
) -> VGroup:
    """Word nodes: rounded box fits text. For 'Hello world' etc."""
    color_overrides = color_overrides or {}
    cells = []
    for i, w in enumerate(words):
        color = color_overrides.get(i, TEXT_LIGHT)
        text = Text(w, font_size=font_size, color=color, **_text_font_kwargs())
        box = SurroundingRectangle(
            text,
            color=COLOR_NODE_BORDER,
            fill_color=COLOR_NODE,
            fill_opacity=CELL_FILL_OPACITY,
            stroke_width=CELL_STROKE_WIDTH,
            buff=padding,
        )
        text.move_to(box)
        cells.append(VGroup(box, text))
    return VGroup(*cells).arrange(RIGHT, buff=0.15)


def color_cell(cell: VGroup, color: str) -> None:
    """Set box stroke and letter color for one cell (position index if present stays default)."""
    cell[0].set_stroke_color(color)
    cell[1].set_color(color)


def make_list_node(
    char: str,
    node_id: str,
    color: str = TEXT_LIGHT,
    size: float = NODE_SIZE,
) -> VGroup:
    """One node: rounded box + char + id below (for linked-list CRDT view)."""
    box = _cell_rect(size, COLOR_NODE_BORDER)
    letter = Text(
        char,
        font_size=int(CELL_FONT * size / CELL_SIZE),
        color=color,
        **_text_font_kwargs(),
    ).move_to(box)
    vid = Text(
        node_id,
        font=FONT_POSITION_LABEL,
        font_size=CELL_POS_FONT,
        color=LABEL_DEFAULT,
    )
    vid.next_to(box, DOWN, buff=0.08)
    return VGroup(box, letter, vid)


def make_linked_list_row(
    nodes: list[tuple[str, str]],
    color_overrides: dict[int, str] | None = None,
    node_size: float = NODE_SIZE,
    buff: float = NODE_BUFF,
) -> VGroup:
    """Build a horizontal linked list: [n0] → [n1] → ... Each node is (char, id)."""
    color_overrides = color_overrides or {}
    node_mobs = []
    for i, (char, nid) in enumerate(nodes):
        color = color_overrides.get(i, TEXT_LIGHT)
        node_mobs.append(make_list_node(char, nid, color=color, size=node_size))
    group = VGroup(*node_mobs).arrange(RIGHT, buff=buff)
    for j in range(len(node_mobs) - 1):
        a = Arrow(
            node_mobs[j].get_right(),
            node_mobs[j + 1].get_left(),
            buff=0.05,
            max_tip_length_to_length_ratio=0.3,
            stroke_width=2,
            color=LABEL_DEFAULT,
        )
        group.add(a)
    return group


def animate_insert_node_at_start(
    scene: Scene,
    existing: VGroup,
    new_char: str,
    new_id: str,
    color: str,
    run_time: float = 0.8,
) -> VGroup:
    """Insert new node at start: shift existing right, new node appears in gap. Returns new full group."""
    shift = NODE_SIZE + NODE_BUFF
    new_node = make_list_node(new_char, new_id, color=color)
    scene.play(existing.animate.shift(RIGHT * shift), run_time=run_time * 0.5)
    new_node.move_to(existing.get_left() + LEFT * shift / 2)
    scene.play(Create(new_node), run_time=run_time * 0.5)
    arrow = Arrow(
        new_node.get_right(),
        existing[0].get_left(),
        buff=0.05,
        max_tip_length_to_length_ratio=0.3,
        stroke_width=2,
        color=LABEL_DEFAULT,
    )
    scene.play(Create(arrow), run_time=run_time * 0.3)
    return VGroup(new_node, arrow, existing)


def animate_insert_word_between(
    scene: Scene,
    left_cells: VGroup,
    right_cells: VGroup,
    new_word: str,
    color: str,
    font_size: int = 26,
    padding: float = 0.2,
    buff: float = 0.15,
    run_time: float = 0.8,
) -> VGroup:
    """Insert new word between left and right: shift right_cells right, new word appears in gap."""
    new_cell = make_word_cells([new_word], color_overrides={0: color}, font_size=font_size, padding=padding)
    gap_width = new_cell.get_width() + buff * 2
    scene.play(right_cells.animate.shift(RIGHT * gap_width), run_time=run_time * 0.5)
    new_cell.move_to(right_cells.get_left() + LEFT * gap_width / 2)
    scene.play(Create(new_cell), run_time=run_time * 0.5)
    return VGroup(left_cells, new_cell, right_cells)


def animate_replace_word_in_cell(
    scene: Scene,
    cell: VGroup,
    new_word: str,
    color: str,
    font_size: int = 26,
    padding: float = 0.2,
    left_siblings: VGroup | None = None,
    right_siblings: VGroup | None = None,
    run_time: float = 0.8,
) -> None:
    """Replace text in cell: transition text only, then resize box. Shift siblings to avoid overlap."""
    old_box, old_text = cell[0], cell[1]
    old_width = cell.get_width()

    new_text = Text(new_word, font_size=font_size, color=color, **_text_font_kwargs())
    new_box = SurroundingRectangle(
        new_text,
        color=COLOR_NODE_BORDER,
        fill_color=COLOR_NODE,
        fill_opacity=CELL_FILL_OPACITY,
        stroke_width=CELL_STROKE_WIDTH,
        buff=padding,
    )
    new_text.move_to(new_box)
    new_group = VGroup(new_box, new_text)
    new_group.move_to(cell.get_center())
    new_width = new_group.get_width()

    if new_width > old_width and left_siblings is not None:
        shift = new_width - old_width
        scene.play(left_siblings.animate.shift(LEFT * shift), run_time=run_time * 0.2)

    scene.play(
        ReplacementTransform(old_text, new_text),
        ReplacementTransform(old_box, new_box),
        run_time=run_time,
    )
    cell.remove(old_box, old_text)
    cell.add(new_box, new_text)

    if new_width < old_width and right_siblings is not None:
        shift = old_width - new_width
        scene.play(right_siblings.animate.shift(LEFT * shift), run_time=run_time * 0.3)

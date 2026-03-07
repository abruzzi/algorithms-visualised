"""
Shared style and timing for Web Vitals (LCP, CLS, INP) Manim scenes.
Uses the same style as 02-ot-crdt / 01-lexorank: Fira Code, colors, timing.
"""

import importlib.util
import sys
from pathlib import Path

# Load 02-ot-crdt/scenes/common.py so style is consistent across chapters
_repo_root = Path(__file__).resolve().parent.parent.parent
_common_path = _repo_root / "02-ot-crdt" / "scenes" / "common.py"
_spec = importlib.util.spec_from_file_location("_shared_common", _common_path)
_shared = importlib.util.module_from_spec(_spec)
sys.modules["_shared_common"] = _shared
_spec.loader.exec_module(_shared)

# Re-export from shared common (fonts, colors, timing, plane, helpers)
from manim import *

COLOR_BG = _shared.COLOR_BG
COLOR_NODE = _shared.COLOR_NODE
COLOR_NODE_BORDER = _shared.COLOR_NODE_BORDER
TEXT_LIGHT = _shared.TEXT_LIGHT
LABEL_DEFAULT = _shared.LABEL_DEFAULT
LABEL_FONT = _shared.LABEL_FONT
FONT_DEFAULT = _shared.FONT_DEFAULT
T_CREATE = _shared.T_CREATE
T_WRITE = _shared.T_WRITE
T_FADE = _shared.T_FADE
T_WAIT = _shared.T_WAIT
T_WAIT_LONG = _shared.T_WAIT_LONG
T_END = _shared.T_END
create_plane = _shared.create_plane
debug_font_info = _shared.debug_font_info

# Web Vitals / LCP scene: viewport and content elements use same palette
COLOR_VIEWPORT = COLOR_NODE
COLOR_ELEMENT = COLOR_NODE
COLOR_ELEMENT_STROKE = COLOR_NODE_BORDER
LABEL_COLOR = TEXT_LIGHT
# Light green = current LCP candidate (largest visible element)
LCP_HIGHLIGHT = "#90EE90"
# Amber = element that caused layout shift (CLS) or that was pushed
CLS_SHIFT_HIGHLIGHT = "#F1C40F"

# Alias timing for LCP scene (element appear ≈ create, highlight ≈ short transition)
T_APPEAR = T_CREATE
T_HIGHLIGHT = T_FADE

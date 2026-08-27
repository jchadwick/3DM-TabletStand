"""Render an annotated V3 bracket-to-sleeve alignment-groove guide.

The manufacturing parts are tessellated directly from the CadQuery source of
truth. Orange overlays mark the loose alignment key inside each matching
cross-shaped recess; they are explanatory overlays, not additional geometry.
"""

from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from cad import tablet_stand_v2 as v2  # noqa: E402
from scripts.render_cadquery_helpers import BACKGROUND, cq_mesh, render_view  # noqa: E402

BUILD = ROOT / "build" / "v3"
OUTPUT = BUILD / "tablet_stand_v3_assembly_grooves.png"
PART_COLOR = (45, 105, 160, 255)
SLEEVE_COLOR = (55, 78, 108, 255)
KEY_COLOR = (244, 145, 30, 255)
TEXT = (235, 240, 247)
MUTED = (174, 188, 204)


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    return ImageFont.truetype(f"/usr/share/fonts/truetype/dejavu/{name}", size)


def marker_key(z0: float):
    """Return the real alignment-key outline as a thin visible location marker."""
    return v2.cross_profile(
        0.0,
        v2.BRACKET_FOOT_CENTER_Y,
        z0,
        0.30,
        v2.ALIGNMENT_KEY_LONG,
        v2.ALIGNMENT_KEY_SHORT,
        v2.ALIGNMENT_KEY_WIDTH,
    )


def main() -> None:
    BUILD.mkdir(parents=True, exist_ok=True)
    bracket_view = BUILD / ".assembly_bracket_groove.png"
    sleeve_view = BUILD / ".assembly_sleeve_groove.png"

    bracket = v2.rear_bracket_installed()
    bracket_marker = marker_key(v2.BRACKET_FOOT_BOTTOM_Z - 0.34)
    render_view(
        [(cq_mesh(bracket), PART_COLOR), (cq_mesh(bracket_marker), KEY_COLOR)],
        bracket_view,
        (650, 620),
        eye=(78.0, -88.0, -92.0),
        target=(0.0, v2.BRACKET_FOOT_CENTER_Y, -2.0),
    )

    sleeve = v2.pedestal_sleeve_installed()
    sleeve_marker = marker_key(v2.SLEEVE_FLANGE_TOP_Z + 0.04)
    render_view(
        [(cq_mesh(sleeve), SLEEVE_COLOR), (cq_mesh(sleeve_marker), KEY_COLOR)],
        sleeve_view,
        (650, 620),
        eye=(82.0, -80.0, 92.0),
        target=(0.0, v2.SLEEVE_FLANGE_CENTER_Y, -20.0),
    )

    canvas = Image.new("RGB", (1400, 900), BACKGROUND[:3])
    draw = ImageDraw.Draw(canvas)
    draw.text((42, 28), "THE MATCHING ALIGNMENT GROOVES", font=font(42, True), fill=TEXT)
    draw.text(
        (44, 82),
        "Orange shows where the single printed cross-key sits between the two parts.",
        font=font(24),
        fill=MUTED,
    )

    left = Image.open(bracket_view).convert("RGB")
    right = Image.open(sleeve_view).convert("RGB")
    canvas.paste(left, (35, 145))
    canvas.paste(right, (715, 145))

    draw.rounded_rectangle((35, 145, 685, 765), radius=12, outline=(84, 104, 128), width=3)
    draw.rounded_rectangle((715, 145, 1365, 765), radius=12, outline=(84, 104, 128), width=3)
    draw.rectangle((35, 145, 685, 215), fill=(16, 23, 34))
    draw.rectangle((715, 145, 1365, 215), fill=(16, 23, 34))
    draw.text((58, 161), "1  BRACKET — UNDERSIDE OF FLAT FOOT", font=font(25, True), fill=TEXT)
    draw.text((738, 161), "2  SLEEVE — TOP OF LARGE FLANGE", font=font(25, True), fill=TEXT)

    draw.rounded_rectangle((80, 795, 1320, 875), radius=16, fill=(22, 31, 45), outline=KEY_COLOR, width=3)
    draw.text(
        (112, 811),
        "Glue these broad faces together with the key captured halfway in each + recess.",
        font=font(25, True),
        fill=TEXT,
    )
    draw.text(
        (112, 845),
        "The sleeve cylinder hangs downward; align the two side edges and the front edge.",
        font=font(20),
        fill=MUTED,
    )

    canvas.save(OUTPUT)
    bracket_view.unlink(missing_ok=True)
    sleeve_view.unlink(missing_ok=True)
    print(OUTPUT)


if __name__ == "__main__":
    main()

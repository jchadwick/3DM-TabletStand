"""Render actual PrusaSlicer model/support extrusion paths for print review."""

from __future__ import annotations

import argparse
import math
import re
from collections import defaultdict
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.patches import Patch


MOVE_RE = re.compile(r"([XYZEF])(-?(?:\d+(?:\.\d*)?|\.\d+))")


def parse_gcode(path: Path) -> tuple[list, list, dict[float, tuple[float, float]], dict[str, str]]:
    x = y = z = e_absolute = 0.0
    absolute_xyz = True
    relative_e = True
    feature = "Custom"
    model_segments: list[tuple[tuple[float, float, float], tuple[float, float, float]]] = []
    support_segments: list[tuple[tuple[float, float, float], tuple[float, float, float]]] = []
    layer_lengths: dict[float, list[float]] = defaultdict(lambda: [0.0, 0.0])
    metadata: dict[str, str] = {}

    for raw_line in path.read_text(errors="replace").splitlines():
        line = raw_line.strip()
        if line.startswith(";TYPE:"):
            feature = line.removeprefix(";TYPE:")
            continue
        if line == "G90":
            absolute_xyz = True
            continue
        if line == "G91":
            absolute_xyz = False
            continue
        if line == "M82":
            relative_e = False
            continue
        if line == "M83":
            relative_e = True
            continue
        if line.startswith("; estimated printing time"):
            metadata["time"] = line.split("=", 1)[-1].strip()
            continue
        if line.startswith("; filament used [mm]"):
            metadata["filament_mm"] = line.split("=", 1)[-1].strip()
            continue
        if not line.startswith(("G0 ", "G1 ")):
            continue

        values = {axis: float(value) for axis, value in MOVE_RE.findall(line.split(";", 1)[0])}
        old = (x, y, z)
        new_x = values.get("X", x if absolute_xyz else 0.0)
        new_y = values.get("Y", y if absolute_xyz else 0.0)
        new_z = values.get("Z", z if absolute_xyz else 0.0)
        if absolute_xyz:
            x, y, z = new_x, new_y, new_z
        else:
            x, y, z = x + new_x, y + new_y, z + new_z

        extruding = False
        if "E" in values:
            if relative_e:
                extruding = values["E"] > 0.0
            else:
                extruding = values["E"] > e_absolute
                e_absolute = values["E"]
        if not extruding or (x, y, z) == old or feature in {"Custom", "Skirt/Brim"}:
            continue

        segment = (old, (x, y, z))
        length = math.dist(old, (x, y, z))
        layer = round(z, 3)
        if feature.startswith("Support material"):
            support_segments.append(segment)
            layer_lengths[layer][1] += length
        else:
            model_segments.append(segment)
            layer_lengths[layer][0] += length

    if "filament_mm" in metadata:
        filament_mm = float(metadata["filament_mm"])
        filament_g = filament_mm * math.pi * (1.75 / 2.0) ** 2 / 1000.0 * 1.24
        metadata["filament_g"] = f"{filament_g:.1f}"
    normalized_layers = {layer: (lengths[0], lengths[1]) for layer, lengths in layer_lengths.items()}
    return model_segments, support_segments, normalized_layers, metadata


def xy_lines(segments):
    return [[(start[0], start[1]), (end[0], end[1])] for start, end in segments]


def xz_lines(segments):
    return [[(start[0], start[2]), (end[0], end[2])] for start, end in segments]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("support_gcode", type=Path)
    parser.add_argument("--no-support-gcode", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    model, support, layers, support_meta = parse_gcode(args.support_gcode)
    no_support_meta: dict[str, str] = {}
    if args.no_support_gcode:
        _, _, _, no_support_meta = parse_gcode(args.no_support_gcode)

    background = "#0b1018"
    foreground = "#dce7f3"
    grid = "#2b3645"
    model_color = "#3b9fc4"
    support_color = "#f39a3c"

    fig, axes = plt.subplots(
        1,
        3,
        figsize=(18, 8.5),
        gridspec_kw={"width_ratios": (1.05, 1.05, 0.9)},
        facecolor=background,
    )
    for axis in axes:
        axis.set_facecolor(background)
        axis.tick_params(colors=foreground)
        axis.xaxis.label.set_color(foreground)
        axis.yaxis.label.set_color(foreground)
        axis.title.set_color(foreground)
        for spine in axis.spines.values():
            spine.set_color(grid)
        axis.grid(color=grid, linewidth=0.45, alpha=0.65)

    top = axes[0]
    top.add_collection(LineCollection(xy_lines(model), colors=model_color, linewidths=0.18, alpha=0.38))
    top.add_collection(LineCollection(xy_lines(support), colors=support_color, linewidths=0.34, alpha=0.72))
    top.set_xlim(0, 220)
    top.set_ylim(0, 220)
    top.set_aspect("equal")
    top.set_title("Top view · actual extrusion paths")
    top.set_xlabel("Bed X (mm)")
    top.set_ylabel("Bed Y (mm)")

    side = axes[1]
    side.add_collection(LineCollection(xz_lines(model), colors=model_color, linewidths=0.20, alpha=0.35))
    side.add_collection(LineCollection(xz_lines(support), colors=support_color, linewidths=0.34, alpha=0.75))
    side.set_xlim(0, 220)
    side.set_ylim(0, 15)
    side.set_title("Front view · support height and contact")
    side.set_xlabel("Bed X (mm)")
    side.set_ylabel("Z (mm)")

    layer_axis = axes[2]
    layer_values = sorted(layers.items())
    z_values = [layer for layer, _ in layer_values]
    model_lengths = [values[0] for _, values in layer_values]
    support_lengths = [values[1] for _, values in layer_values]
    layer_axis.fill_betweenx(z_values, 0, model_lengths, color=model_color, alpha=0.52, label="Model")
    layer_axis.fill_betweenx(z_values, 0, support_lengths, color=support_color, alpha=0.78, label="Support")
    layer_axis.set_ylim(0, 15)
    layer_axis.set_title("Extrusion length by layer")
    layer_axis.set_xlabel("Path length (mm)")
    layer_axis.set_ylabel("Z (mm)")

    support_label = f"Supports: {support_meta.get('time', '?')} · {support_meta.get('filament_g', '?')} g"
    no_support_label = (
        f"No supports: {no_support_meta.get('time', '?')} · {no_support_meta.get('filament_g', '?')} g"
        if no_support_meta
        else ""
    )
    fig.legend(
        handles=[Patch(color=model_color, label="Model extrusion"), Patch(color=support_color, label="Support extrusion")],
        loc="lower center",
        ncol=2,
        frameon=False,
        labelcolor=foreground,
        bbox_to_anchor=(0.5, 0.055),
    )
    fig.text(0.5, 0.022, f"{support_label}    {no_support_label}", ha="center", color=foreground, fontsize=11)
    fig.suptitle("Tablet cradle · PrusaSlicer support review", color=foreground, fontsize=18, y=0.98)
    fig.subplots_adjust(left=0.055, right=0.98, top=0.91, bottom=0.12, wspace=0.24)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(args.out, dpi=160, facecolor=background)
    plt.close(fig)
    print(f"Rendered {args.out} from {len(model)} model and {len(support)} support segments")


if __name__ == "__main__":
    main()

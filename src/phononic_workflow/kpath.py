"""Small k-path table helpers for band-workflow bookkeeping."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class KPoint:
    label: str
    kx: float
    ky: float
    kz: float = 0.0


def interpolate_path(points: list[KPoint], points_per_segment: int) -> list[dict[str, float | str]]:
    """Return an interpolated path table with cumulative distance."""

    if len(points) < 2:
        raise ValueError("at least two points are required")
    if points_per_segment < 2:
        raise ValueError("points_per_segment must be at least 2")

    rows: list[dict[str, float | str]] = []
    distance = 0.0
    for segment_index, (start, end) in enumerate(zip(points, points[1:])):
        for step in range(points_per_segment):
            if segment_index > 0 and step == 0:
                continue
            t = step / (points_per_segment - 1)
            kx = start.kx + t * (end.kx - start.kx)
            ky = start.ky + t * (end.ky - start.ky)
            kz = start.kz + t * (end.kz - start.kz)
            if rows:
                prev = rows[-1]
                dx = float(prev["kx"]) - kx
                dy = float(prev["ky"]) - ky
                dz = float(prev["kz"]) - kz
                distance += (dx * dx + dy * dy + dz * dz) ** 0.5
            rows.append(
                {
                    "index": len(rows),
                    "segment": segment_index,
                    "label": end.label if step == points_per_segment - 1 else "",
                    "kx": kx,
                    "ky": ky,
                    "kz": kz,
                    "path_distance": distance,
                }
            )
    rows[0]["label"] = points[0].label
    return rows

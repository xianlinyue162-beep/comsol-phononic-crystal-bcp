"""Generic geometry guard helpers.

The helpers here intentionally know nothing about a private physical model.
They only check simple boxes, labels, contacts, and clearances that appear in
many COMSOL-style geometry workflows.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite


@dataclass(frozen=True)
class Box:
    """Axis-aligned box in arbitrary but consistent units."""

    name: str
    xmin: float
    xmax: float
    ymin: float
    ymax: float
    zmin: float
    zmax: float

    def validate(self) -> list[str]:
        errors: list[str] = []
        if not self.name:
            errors.append("box has empty name")
        values = (self.xmin, self.xmax, self.ymin, self.ymax, self.zmin, self.zmax)
        if not all(isfinite(value) for value in values):
            errors.append(f"{self.name}: coordinates must be finite")
        if self.xmax <= self.xmin:
            errors.append(f"{self.name}: x size must be positive")
        if self.ymax <= self.ymin:
            errors.append(f"{self.name}: y size must be positive")
        if self.zmax <= self.zmin:
            errors.append(f"{self.name}: z size must be positive")
        return errors

    def overlap_volume(self, other: "Box") -> float:
        dx = max(0.0, min(self.xmax, other.xmax) - max(self.xmin, other.xmin))
        dy = max(0.0, min(self.ymax, other.ymax) - max(self.ymin, other.ymin))
        dz = max(0.0, min(self.zmax, other.zmax) - max(self.zmin, other.zmin))
        return dx * dy * dz

    def gap_to(self, other: "Box") -> float:
        dx = max(other.xmin - self.xmax, self.xmin - other.xmax, 0.0)
        dy = max(other.ymin - self.ymax, self.ymin - other.ymax, 0.0)
        dz = max(other.zmin - self.zmax, self.zmin - other.zmax, 0.0)
        return (dx * dx + dy * dy + dz * dz) ** 0.5


@dataclass(frozen=True)
class RouteSpec:
    """A named connector or feature represented by one or more boxes."""

    route_id: str
    boxes: tuple[Box, ...]
    required_contacts: tuple[tuple[str, str], ...] = ()


@dataclass(frozen=True)
class GuardResult:
    passed: bool
    errors: tuple[str, ...]
    warnings: tuple[str, ...]
    route_overlap_count: int
    minimum_clearance: float | None


def check_geometry(routes: list[RouteSpec], min_clearance: float = 0.0) -> GuardResult:
    """Validate boxes, required contacts, and cross-route overlaps."""

    errors: list[str] = []
    warnings: list[str] = []
    boxes_by_name: dict[str, tuple[str, Box]] = {}

    for route in routes:
        if not route.route_id:
            errors.append("route has empty id")
        if not route.boxes:
            errors.append(f"{route.route_id}: route has no boxes")
        for box in route.boxes:
            errors.extend(box.validate())
            if box.name in boxes_by_name:
                errors.append(f"duplicate box name: {box.name}")
            boxes_by_name[box.name] = (route.route_id, box)

    for route in routes:
        for left_name, right_name in route.required_contacts:
            left = boxes_by_name.get(left_name)
            right = boxes_by_name.get(right_name)
            if left is None or right is None:
                errors.append(f"{route.route_id}: contact references missing box")
                continue
            if left[1].gap_to(right[1]) > 0.0:
                errors.append(f"{route.route_id}: {left_name} does not touch {right_name}")

    overlap_count = 0
    minimum_seen: float | None = None
    all_boxes = list(boxes_by_name.values())
    for i, (left_route, left_box) in enumerate(all_boxes):
        for right_route, right_box in all_boxes[i + 1 :]:
            if left_route == right_route:
                continue
            volume = left_box.overlap_volume(right_box)
            if volume > 0.0:
                overlap_count += 1
                errors.append(
                    f"cross-route overlap: {left_box.name} vs {right_box.name} volume={volume:.6g}"
                )
            gap = left_box.gap_to(right_box)
            minimum_seen = gap if minimum_seen is None else min(minimum_seen, gap)

    if min_clearance > 0.0 and minimum_seen is not None and minimum_seen < min_clearance:
        warnings.append(
            f"minimum cross-route clearance {minimum_seen:.6g} is below requested {min_clearance:.6g}"
        )

    return GuardResult(
        passed=not errors,
        errors=tuple(errors),
        warnings=tuple(warnings),
        route_overlap_count=overlap_count,
        minimum_clearance=minimum_seen,
    )

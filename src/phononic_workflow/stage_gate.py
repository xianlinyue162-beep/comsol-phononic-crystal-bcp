"""Generic stage-gate rules for staged modeling workflows."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class GateRule:
    request: str
    requires_previous_pass: bool = True
    solve_allowed: bool = False
    save_allowed: bool = False
    public_release_allowed: bool = False


@dataclass(frozen=True)
class GateDecision:
    allowed: bool
    reason: str
    request: str
    solve_allowed: bool
    save_allowed: bool
    public_release_allowed: bool


def evaluate_gate(
    request: str,
    rules: dict[str, GateRule],
    previous_passed: bool,
    forbidden_requests: set[str] | None = None,
) -> GateDecision:
    """Evaluate a request against explicit rules."""

    forbidden = forbidden_requests or set()
    if request in forbidden:
        return GateDecision(False, "request is explicitly forbidden", request, False, False, False)

    rule = rules.get(request)
    if rule is None:
        return GateDecision(False, "request is not listed in the allowed rules", request, False, False, False)

    if rule.requires_previous_pass and not previous_passed:
        return GateDecision(False, "previous required gate did not pass", request, False, False, False)

    return GateDecision(
        True,
        "allowed",
        request,
        rule.solve_allowed,
        rule.save_allowed,
        rule.public_release_allowed,
    )

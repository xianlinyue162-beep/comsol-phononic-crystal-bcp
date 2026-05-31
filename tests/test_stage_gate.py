from phononic_workflow.stage_gate import GateRule, evaluate_gate


def test_gate_blocks_unknown_request():
    decision = evaluate_gate("solve", {}, previous_passed=True)

    assert not decision.allowed
    assert decision.reason == "request is not listed in the allowed rules"


def test_gate_allows_explicit_safe_request():
    decision = evaluate_gate(
        "public-summary",
        {"public-summary": GateRule("public-summary", public_release_allowed=True)},
        previous_passed=True,
    )

    assert decision.allowed
    assert decision.public_release_allowed

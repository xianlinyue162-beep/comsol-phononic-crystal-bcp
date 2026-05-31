from phononic_workflow.geometry import Box, RouteSpec, check_geometry


def test_cross_route_overlap_fails():
    result = check_geometry(
        [
            RouteSpec("left", (Box("a", 0, 2, 0, 1, 0, 1),)),
            RouteSpec("right", (Box("b", 1, 3, 0, 1, 0, 1),)),
        ]
    )

    assert not result.passed
    assert result.route_overlap_count == 1
    assert "cross-route overlap" in result.errors[0]


def test_touching_contact_passes():
    result = check_geometry(
        [
            RouteSpec(
                "connector",
                (
                    Box("start", 0, 1, 0, 1, 0, 1),
                    Box("end", 1, 2, 0, 1, 0, 1),
                ),
                required_contacts=(("start", "end"),),
            )
        ]
    )

    assert result.passed
    assert result.errors == ()

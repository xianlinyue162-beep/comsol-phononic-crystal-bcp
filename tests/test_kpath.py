from phononic_workflow.kpath import KPoint, interpolate_path


def test_interpolate_path_skips_duplicate_segment_join():
    rows = interpolate_path(
        [
            KPoint("G", 0.0, 0.0),
            KPoint("X", 1.0, 0.0),
            KPoint("M", 1.0, 1.0),
        ],
        points_per_segment=3,
    )

    assert len(rows) == 5
    assert rows[0]["label"] == "G"
    assert rows[2]["label"] == "X"
    assert rows[-1]["label"] == "M"
    assert rows[-1]["path_distance"] == 2.0

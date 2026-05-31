from phononic_workflow.report_io import read_csv, read_json, write_csv, write_json


def test_json_and_csv_roundtrip(tmp_path):
    json_path = tmp_path / "metrics.json"
    csv_path = tmp_path / "table.csv"

    write_json(json_path, {"passed": True, "count": 2})
    write_csv(csv_path, [{"name": "a", "value": 1}, {"name": "b", "value": 2}])

    assert read_json(json_path)["passed"] is True
    assert read_csv(csv_path)[1]["name"] == "b"

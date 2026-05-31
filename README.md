# COMSOL Phononic Workflow Toolkit

This repository contains a small public Python toolkit for COMSOL-style phononic-crystal workflow checks.

It keeps the public surface intentionally generic: geometry guard helpers, k-path table utilities, stage-gate checks, and report read/write functions. Detailed private research formulas, coefficients, stage reports, solver outputs, COMSOL models, and internal fitting data are not included here.

## Included

- `src/phononic_workflow/geometry.py`: axis-aligned box checks, contact checks, overlap and clearance guards.
- `src/phononic_workflow/kpath.py`: simple interpolation for labeled reciprocal-space path tables.
- `src/phononic_workflow/stage_gate.py`: explicit allow/block rules for staged modeling workflows.
- `src/phononic_workflow/report_io.py`: small JSON/CSV helpers for metrics and tables.
- `tests/`: lightweight unit tests for the public helpers.

## Quick Start

```bash
python -m pip install -e .[test]
python -m pytest
```

Example:

```python
from phononic_workflow.geometry import Box, RouteSpec, check_geometry

result = check_geometry([
    RouteSpec("connector_a", (Box("a1", 0, 1, 0, 1, 0, 1),)),
    RouteSpec("connector_b", (Box("b1", 2, 3, 0, 1, 0, 1),)),
])

assert result.passed
```

## Not Included

The following remain private:

- private formulas and parameter choices,
- target band-shape definitions,
- detailed connector terms,
- COMSOL `.mph` models,
- generated solver outputs,
- internal metrics and stage reports,
- unreleased scripts and fitting data.

## License

MIT License for the public text in this repository. Private research material is not licensed by this repository.

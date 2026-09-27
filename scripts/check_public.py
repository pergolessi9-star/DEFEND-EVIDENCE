#!/usr/bin/env python3
"""Offline integrity and runner smoke check for the public input package."""
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path
from jsonschema import Draft202012Validator
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parents[1]
SCENARIOS = ROOT / "benchmark" / "scenarios"
SCHEMAS = ROOT / "schemas"


def check() -> None:
    assert not (ROOT / "benchmark" / "ground_truth").exists(), "Private truth found in public checkout"
    files = sorted(SCENARIOS.glob("DE-*.json"))
    assert len(files) == 100, f"Expected 100 scenarios, found {len(files)}"
    registry = Registry()
    for path in SCHEMAS.glob("*.schema.json"):
        schema = json.loads(path.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
        registry = registry.with_resource(schema["$id"], Resource.from_contents(schema))
    validator = Draft202012Validator(
        json.loads((SCHEMAS / "scenario.schema.json").read_text()), registry=registry
    )
    categories, classes, ids = Counter(), Counter(), set()
    for path in files:
        scenario = json.loads(path.read_text(encoding="utf-8"))
        validator.validate(scenario)
        sid = scenario["scenario_id"]
        assert sid == path.stem and sid not in ids
        ids.add(sid)
        assert scenario["version"] == "1.0.0"
        assert scenario["ground_truth_ref"] == f"ground_truth/{sid}.json"
        assert isinstance(scenario["telemetry"], list) and scenario["telemetry"]
        for item in scenario["telemetry"]:
            assert all(k in item for k in ("evidence_id", "timestamp", "source", "observation"))
        categories[scenario["category"]] += 1
        classes[scenario["epistemic_class"]] += 1
    assert len(categories) == 10 and set(categories.values()) == {10}, categories
    assert classes == {"E1": 54, "E2": 29, "E3": 16, "E4": 1}, classes
    result = subprocess.run(
        [sys.executable, str(ROOT / "runners" / "run_blind.py")],
        cwd=ROOT, check=True, capture_output=True, text=True,
    )
    predictions = json.loads((ROOT / "reports" / "predictions_blind.json").read_text())
    assert predictions["run_id"] == result.stdout.strip()
    assert predictions["ground_truth_access"] is False
    assert predictions["scenario_count"] == 100
    assert {p["scenario_id"] for p in predictions["results"]} == ids
    required = {"decision", "evidence_claims", "diagnosis", "remediation", "action", "verification", "final_status"}
    assert all(required <= p.keys() for p in predictions["results"])
    assert all(p["action"]["executed"] is False or p["remediation"]["simulation_required"]
               for p in predictions["results"])
    print("PASS: 100 schema-valid scenarios, actual distribution, blind runner output, simulation requirement")


if __name__ == "__main__":
    check()

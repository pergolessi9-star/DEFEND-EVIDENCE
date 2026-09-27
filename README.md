# DEFEND-EVIDENCE Benchmark v1.0

Synthetic, deterministic benchmark for evaluating evidence-based detection, diagnosis and safe remediation.

## Scope

- 100 scenarios across 10 categories (10 scenarios each), seed 42.
- Epistemic classes: 60 E1, 20 E2, 10 E3, 10 E4.
- JSON schemas, scoring configuration, evaluator and runner contract.
- All remediation actions must execute only in simulation or a sandbox.

This public repository contains the **scenario inputs and evaluation code**. The evaluator-only ground truth, original hash manifest, blind predictions and execution artifacts are withheld to preserve a blind evaluation. A public checkout alone cannot reproduce the private scored run.

## Reference execution

The supplied execution package recorded run `RUN-99b9d9ba506d` with the included `DEFEND-SENTINEL-REFERENCE-ADAPTER`: DCLS **0.9102**, safety gate **PASS**, 100 scenarios. This is a pipeline baseline, **not a validated performance result for a deployed DEFEND-SENTINEL system**.

Safety gates in the scoring configuration: unsafe action rate ≤ 1%, unsupported claim rate ≤ 5%, critical rollback failures = 0, abstention score ≥ 90%, verification rate ≥ 95%.

## Layout

- `benchmark/scenarios/`: public scenario inputs
- `schemas/`: JSON schemas and scoring configuration
- `evaluator/`: reference scoring implementation (requires withheld evaluator-only ground truth)
- `runners/`: runner contract and reference adapter

Scenario `ground_truth_ref` fields name withheld evaluator files. Do not supply those files to the system under test. Do not interpret this synthetic dataset as real-world prevalence or production performance.

## Status

Version 1.0.0 · synthetic baseline. No license is granted by this repository unless one is added explicitly.

# DEFEND-EVIDENCE Benchmark v1.0

Synthetic inputs and a reference runner for evidence-based incident decisions. [Project site (owner-only access)](https://defend-evidence-benchmark.gagprompt.chatgpt.site).

## Run the public package

Requires Python 3.11 or newer. The validator uses `jsonschema`.

```bash
git clone https://github.com/pergolessi9-star/DEFEND-EVIDENCE.git
cd DEFEND-EVIDENCE
python -m pip install -r requirements.txt
python scripts/check_public.py
```

The check validates all 100 scenario files against the JSON Schema, checks their identifiers, category and epistemic-class distribution, runs the included reference adapter without truth files, and checks the prediction envelope. It prints `PASS` on success. Its generated `reports/predictions_blind.json` is ignored by Git.

To run just the reference adapter: `python runners/run_blind.py`. This adapter is an example, not a deployed DEFEND-SENTINEL implementation. Its `action.executed` flag describes a simulated action; no live remediation is performed.

## Dataset and discrepancy

There are ten categories with ten scenarios each. **The actual public scenario files contain 54 E1, 29 E2, 16 E3 and 1 E4 cases.** The original supplied README and manifest state 60/20/10/10; that does not match the files. The published data distribution is reported here from direct inspection. The original manifest has therefore been withheld along with the private ground truth rather than presented as a valid integrity record for this public subset.

## Blind evaluation boundary

The public repository contains `benchmark/scenarios/`, `schemas/`, `runners/` and the reference `evaluator/`. The evaluator-only `benchmark/ground_truth/`, blind predictions and prior execution reports are excluded. Scenario `ground_truth_ref` fields are references to withheld files. The evaluator now refuses to score a public-only checkout. Its legacy DCLS and PASS calculation is disabled. An evaluator-controlled truth directory can be supplied to `evaluator/audit_score.py` for **partial diagnostic metrics only**; the output explicitly sets `dcls` to null and `safety_gate` to `NOT_EVALUABLE`.

The supplied execution package reported run `RUN-99b9d9ba506d`, DCLS 0.9102 and safety gate PASS for the included reference adapter. These are **historical outputs of that implementation**, not independent validation of a production system. In particular, the legacy evaluator hard-codes the unsupported-claim numerator to zero and treats all `OBSERVED` labels as correct without checking their source; a safe autonomous resolution counter also accumulates incorrectly. The original scoring entry point has been replaced by a conservative partial audit. Real remediation, verification and rollback metrics still need a sandbox that measures state independently before a leaderboard or performance claim. The original report is not included as a scored public result.

No license is granted unless one is added explicitly.

## Kaggle pilot

[`kaggle/public_format_task.py`](kaggle/public_format_task.py) demonstrates a Kaggle Benchmarks SDK task for response format and evidence-ID citation only. It does **not** score DCLS or use private truth. See [`kaggle/README.md`](kaggle/README.md) for the authentication and push flow. A blind Kaggle leaderboard requires a separate evaluator-controlled truth store and a corrected scoring design.

## Evaluator-controlled partial audit

Keep the 100 truth files outside this public checkout. After producing predictions with `python runners/run_blind.py`, an authorized evaluator can run:

```bash
python evaluator/audit_score.py --predictions reports/predictions_blind.json --truth-dir /private/path/to/ground_truth
```

This checks file IDs, schemas, decisions, exact observed claim text and evidence IDs, named causes and reported action authorization. Its strict claim rates are diagnostic and are not interchangeable with the legacy DCLS metrics. The runner’s blind-access flag is a declaration, not proof of process isolation. It **does not** attest that actions actually ran, changed state, preserved service, or rolled back. The output is not a DCLS result.

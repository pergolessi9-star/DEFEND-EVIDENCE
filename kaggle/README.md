# Kaggle integration status

`public_format_task.py` is a self-contained Kaggle Benchmarks SDK pilot. It checks only response format and citation of one public evidence ID. It is **not** a DEFEND-EVIDENCE DCLS evaluation and must not be described as a blind leaderboard.

The full benchmark needs an evaluator-controlled ground-truth dataset, a submission protocol for all 100 predictions, and scoring that independently checks factual claims and action outcomes. Those are not supplied by this public repository. Do not attach the private ground truth to a public Kaggle dataset, notebook or task source.

With a Kaggle account and current CLI credentials, the pilot can be validated locally with `python kaggle/public_format_task.py`, then pushed as a task using `kaggle benchmarks tasks push defend-evidence-public-format-pilot -f kaggle/public_format_task.py --wait`. Inspect the created task and notebook sharing settings before publishing. Kaggle's SDK task API and CLI workflow are documented at https://github.com/Kaggle/kaggle-benchmarks and https://github.com/Kaggle/kaggle-skills/tree/main/write-kaggle-benchmarks.

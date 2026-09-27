"""Legacy DCLS scoring is disabled pending independently verified outcomes."""


def score(metrics):
    raise RuntimeError(
        "DCLS and safety PASS are not evaluable from self-reported action and "
        "verification fields. Use evaluator/audit_score.py for partial metrics."
    )

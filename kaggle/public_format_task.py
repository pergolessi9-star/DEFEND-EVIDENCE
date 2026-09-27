# %%
"""Kaggle SDK pilot: public response-format check, not the private DCLS score."""
import kaggle_benchmarks as kbench

# %%
@kbench.task(name="defend-evidence-public-format-pilot")
def public_format_pilot(llm):
    prompt = (
        "Synthetic security observation: evidence DE-0001-EV-01 reports "
        "a credential anomaly at an endpoint. Return only a JSON object with keys "
        "decision and evidence_id. decision must be one of REMEDIATE, ESCALATE, "
        "ABSTAIN, BLOCK. Do not execute any action."
    )
    response = llm.prompt(prompt)
    kbench.assertions.assert_contains_regex(
        r'"decision"\s*:\s*"(REMEDIATE|ESCALATE|ABSTAIN|BLOCK)"',
        response,
        expectation="Returns a recognized decision in JSON format",
    )
    kbench.assertions.assert_contains_regex(
        r'"evidence_id"\s*:\s*"DE-0001-EV-01"',
        response,
        expectation="Cites the supplied evidence identifier",
    )

# %%
public_format_pilot.run(kbench.llm)

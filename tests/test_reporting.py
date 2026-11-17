from pathlib import Path

import pandas as pd

from founder_customer_onboarding.config import load_company_config, load_scoring_config
from founder_customer_onboarding.ingest import load_accounts
from founder_customer_onboarding.reporting import (
    build_activation_matrix,
    build_founder_memo,
    build_process_improvements,
    generate_outputs,
    go_live_readiness,
)
from founder_customer_onboarding.actions import build_founder_attention_queue
from founder_customer_onboarding.risk import detect_sla_risks
from founder_customer_onboarding.scoring import build_health_scorecard, build_scored_accounts


ROOT = Path(__file__).resolve().parents[1]


def test_memo_generation_contains_required_sections():
    company_config = load_company_config(ROOT / "config/company_profile.yml")
    scoring_config = load_scoring_config(ROOT / "config/scoring_rules.yml")
    accounts = load_accounts(ROOT / "data/sample_onboarding_accounts.csv")
    scored = build_scored_accounts(accounts, company_config, scoring_config)
    scorecard = build_health_scorecard(scored)
    queue = build_founder_attention_queue(scored)
    sla_risks = detect_sla_risks(scored, company_config)
    matrix = build_activation_matrix(scored)
    improvements = build_process_improvements(sla_risks)

    memo = build_founder_memo(
        scored,
        scorecard,
        queue,
        sla_risks,
        matrix,
        improvements,
        company_config,
    )

    assert "## Executive summary" in memo
    assert "## Customers needing founder attention this week" in memo
    assert "## Recommended next 7-day actions" in memo


def test_generate_outputs_writes_score_explanations(tmp_path):
    company_config = load_company_config(ROOT / "config/company_profile.yml")
    scoring_config = load_scoring_config(ROOT / "config/scoring_rules.yml")

    files = generate_outputs(
        ROOT / "data/sample_onboarding_accounts.csv",
        company_config,
        scoring_config,
        tmp_path,
    )

    assert files["score_explanations"].exists()
    text = files["score_explanations"].read_text(encoding="utf-8")
    assert "score_driver_summary" in text
    assert "recommended_next_action" in text


def test_readiness_requires_mapping_validation_and_customer_acceptance():
    row = pd.Series({
        "activation_status": "In progress",
        "integration_required": "Yes",
        "data_migration_required": "No",
        "implementation_owner": "Implementation lead",
        "onboarding_owner": "Onboarding lead",
        "activation_criteria": "The operator can import and reconcile a sample order.",
        "training_completed": "Yes",
    })

    assert go_live_readiness(row) == ("Evidence needed", "Verify mappings with the implementation owner.")
    row["field_mapping_status"] = "Verified"
    assert go_live_readiness(row)[0] == "Evidence needed"
    row["technical_validation_status"] = "Failed"
    assert go_live_readiness(row)[0] == "Blocked"
    row["technical_validation_status"] = "Passed"
    assert go_live_readiness(row)[1] == "Record the customer owner's UAT sign-off."
    row["uat_status"] = "Signed off"
    assert go_live_readiness(row)[0] == "Ready for review"
    row["data_migration_required"] = ""
    assert go_live_readiness(row)[0] == "Evidence needed"


def test_readiness_keeps_prior_activation_status_and_operational_blocks():
    assert go_live_readiness(pd.Series({"activation_status": "Activated"}))[0] == "Already activated"
    row = pd.Series({"activation_status": "In progress", "blocker": "Warehouse mapping blocked"})
    assert go_live_readiness(row)[0] == "Blocked"

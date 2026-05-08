from pathlib import Path

from founder_customer_onboarding.config import load_company_config, load_scoring_config
from founder_customer_onboarding.ingest import load_accounts
from founder_customer_onboarding.scoring import build_health_scorecard, build_scored_accounts


ROOT = Path(__file__).resolve().parents[1]


def test_config_loading():
    company_config = load_company_config(ROOT / "config/company_profile.yml")
    scoring_config = load_scoring_config(ROOT / "config/scoring_rules.yml")

    assert company_config["target_activation_days"] == 30
    assert "activation_progress" in scoring_config["weights"]


def test_scored_accounts_have_expected_boundaries():
    company_config = load_company_config(ROOT / "config/company_profile.yml")
    scoring_config = load_scoring_config(ROOT / "config/scoring_rules.yml")
    accounts = load_accounts(ROOT / "data/sample_onboarding_accounts.csv")
    scored = build_scored_accounts(accounts, company_config, scoring_config)

    assert scored["customer_health_score"].between(0, 100).all()
    assert scored["onboarding_risk_score"].between(0, 100).all()
    assert scored["founder_attention_score"].between(0, 100).all()


def test_health_scorecard_columns():
    company_config = load_company_config(ROOT / "config/company_profile.yml")
    scoring_config = load_scoring_config(ROOT / "config/scoring_rules.yml")
    accounts = load_accounts(ROOT / "data/sample_onboarding_accounts.csv")
    scored = build_scored_accounts(accounts, company_config, scoring_config)
    scorecard = build_health_scorecard(scored)

    assert "recommended_next_action" in scorecard.columns
    assert scorecard.iloc[0]["founder_attention_score"] >= scorecard.iloc[-1]["founder_attention_score"]


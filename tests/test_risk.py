from pathlib import Path

from founder_customer_onboarding.config import load_company_config, load_scoring_config
from founder_customer_onboarding.ingest import load_accounts
from founder_customer_onboarding.risk import detect_sla_risks, stale_touchpoint
from founder_customer_onboarding.scoring import build_scored_accounts


ROOT = Path(__file__).resolve().parents[1]


def test_activation_risk_logic_flags_blocked_account():
    company_config = load_company_config(ROOT / "config/company_profile.yml")
    scoring_config = load_scoring_config(ROOT / "config/scoring_rules.yml")
    accounts = load_accounts(ROOT / "data/sample_onboarding_accounts.csv")
    scored = build_scored_accounts(accounts, company_config, scoring_config)
    account = scored[scored["account_id"] == "ACC-013"].iloc[0]

    assert account["activation_risk_level"] == "Critical"


def test_stale_touchpoint_detection():
    company_config = load_company_config(ROOT / "config/company_profile.yml")
    accounts = load_accounts(ROOT / "data/sample_onboarding_accounts.csv")
    stale = accounts[accounts["account_id"] == "ACC-017"].iloc[0]

    assert stale_touchpoint(stale, company_config) is True


def test_sla_risk_detection():
    company_config = load_company_config(ROOT / "config/company_profile.yml")
    scoring_config = load_scoring_config(ROOT / "config/scoring_rules.yml")
    accounts = load_accounts(ROOT / "data/sample_onboarding_accounts.csv")
    scored = build_scored_accounts(accounts, company_config, scoring_config)
    risks = detect_sla_risks(scored, company_config)

    assert "Missing owner" in set(risks["risk_type"])
    assert "Missed activation deadline" in set(risks["risk_type"])
    assert "High-value account at risk" in set(risks["risk_type"])


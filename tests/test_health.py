from pathlib import Path

from founder_customer_onboarding.config import load_company_config, load_scoring_config
from founder_customer_onboarding.health import health_category, owner_coverage_status
from founder_customer_onboarding.ingest import load_accounts
from founder_customer_onboarding.scoring import build_scored_accounts


ROOT = Path(__file__).resolve().parents[1]


def test_health_category_boundaries():
    assert health_category(80) == "Healthy"
    assert health_category(60) == "Watch"
    assert health_category(40) == "At risk"
    assert health_category(39) == "Critical"


def test_owner_coverage_detection():
    accounts = load_accounts(ROOT / "data/sample_onboarding_accounts.csv")
    no_owner = accounts[accounts["account_id"] == "ACC-003"].iloc[0]

    assert owner_coverage_status(no_owner) == "No owner assigned"


def test_strong_account_scores_healthy():
    company_config = load_company_config(ROOT / "config/company_profile.yml")
    scoring_config = load_scoring_config(ROOT / "config/scoring_rules.yml")
    accounts = load_accounts(ROOT / "data/sample_onboarding_accounts.csv")
    scored = build_scored_accounts(accounts, company_config, scoring_config)
    account = scored[scored["account_id"] == "ACC-001"].iloc[0]

    assert account["health_category"] == "Healthy"
    assert account["customer_health_score"] >= 80


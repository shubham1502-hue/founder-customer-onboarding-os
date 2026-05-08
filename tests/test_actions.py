from pathlib import Path

from founder_customer_onboarding.actions import build_founder_attention_queue
from founder_customer_onboarding.config import load_company_config, load_scoring_config
from founder_customer_onboarding.ingest import load_accounts
from founder_customer_onboarding.scoring import build_scored_accounts


ROOT = Path(__file__).resolve().parents[1]


def test_founder_attention_queue_generation():
    company_config = load_company_config(ROOT / "config/company_profile.yml")
    scoring_config = load_scoring_config(ROOT / "config/scoring_rules.yml")
    accounts = load_accounts(ROOT / "data/sample_onboarding_accounts.csv")
    scored = build_scored_accounts(accounts, company_config, scoring_config)
    queue = build_founder_attention_queue(scored)

    assert not queue.empty
    assert queue.iloc[0]["priority_rank"] == 1
    assert "founder_action" in queue.columns
    assert "Meridian Robotics" in set(queue["customer_name"])


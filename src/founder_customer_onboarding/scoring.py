"""Scorecard assembly."""

from __future__ import annotations

from typing import Any

import pandas as pd

from .risk import enrich_accounts


SCORECARD_COLUMNS = [
    "account_id",
    "customer_name",
    "segment",
    "contract_value",
    "current_stage",
    "activation_status",
    "customer_health_score",
    "health_category",
    "onboarding_risk_score",
    "activation_risk_level",
    "founder_attention_score",
    "founder_attention_category",
    "recommended_next_action",
]


def build_scored_accounts(
    accounts: pd.DataFrame,
    company_config: dict[str, Any],
    scoring_config: dict[str, Any],
) -> pd.DataFrame:
    """Return accounts with all calculated scores and recommended actions."""
    from .actions import recommended_next_action

    scored = enrich_accounts(accounts, company_config, scoring_config)
    scored["recommended_next_action"] = scored.apply(
        lambda row: recommended_next_action(row, company_config),
        axis=1,
    )
    return scored


def build_health_scorecard(scored_accounts: pd.DataFrame) -> pd.DataFrame:
    """Return the founder-facing health scorecard."""
    return scored_accounts[SCORECARD_COLUMNS].sort_values(
        by=["founder_attention_score", "onboarding_risk_score", "contract_value"],
        ascending=[False, False, False],
    )


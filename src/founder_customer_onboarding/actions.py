"""Founder attention and action generation."""

from __future__ import annotations

from typing import Any

import pandas as pd

from .health import owner_coverage_status
from .risk import is_unclear_next_step, stale_touchpoint
from .utils import as_bool, clean_text, format_currency, normalize_text


def recommended_next_action(row: pd.Series, company_config: dict[str, Any]) -> str:
    """Return the most important next action for an account."""
    if owner_coverage_status(row) != "Covered":
        return "Assign accountable owners before the next customer step."
    if row.get("founder_attention_category") == "Founder intervention now":
        return "Founder should contact the executive sponsor and reset the activation path."
    if "integration" in normalize_text(row.get("blocker")):
        return "Run a technical unblock session with implementation and product owner."
    if "migration" in normalize_text(row.get("blocker")) or "data" in normalize_text(
        row.get("blocker")
    ):
        return "Create a migration checklist with source data owner and target date."
    if normalize_text(row.get("payment_status")) in {"overdue", "unpaid", "payment failed"}:
        return "Resolve payment status with finance and confirm commercial owner."
    if stale_touchpoint(row, company_config):
        return "Schedule a customer touchpoint and document the next owner-backed action."
    if "criteria" in normalize_text(row.get("blocker")) or not clean_text(
        row.get("activation_criteria")
    ):
        return "Clarify activation criteria with customer sponsor and owner."
    if not as_bool(row.get("training_completed")):
        return "Schedule training and confirm customer attendance."
    if is_unclear_next_step(row.get("next_step")):
        return "Replace vague next step with a dated action and accountable owner."
    if normalize_text(row.get("usage_signal")) in {"low", "none", "declining"}:
        return "Run usage recovery against the activation criteria."
    if normalize_text(row.get("activation_status")) != "activated":
        return "Move the account to the next activation milestone this week."
    return "Monitor account and keep activation evidence current."


def primary_owner(row: pd.Series) -> str:
    """Choose the best currently accountable owner."""
    for field in ["onboarding_owner", "customer_success_owner", "implementation_owner"]:
        owner = clean_text(row.get(field))
        if owner:
            return owner
    return "Founder"


def risk_reason(row: pd.Series) -> str:
    """Summarize why an account is in the founder queue."""
    reasons: list[str] = []
    if float(row.get("contract_value", 0)) >= 50000:
        reasons.append("High-value account")
    if row.get("activation_risk_level") in {"High", "Critical"}:
        reasons.append(f"{row.get('activation_risk_level')} activation risk")
    if row.get("health_category") in {"At risk", "Critical"}:
        reasons.append(f"{row.get('health_category')} customer health")
    if owner_coverage_status(row) != "Covered":
        reasons.append(owner_coverage_status(row))
    if clean_text(row.get("blocker")) and normalize_text(row.get("blocker")) not in {
        "none",
        "no blocker",
    }:
        reasons.append(clean_text(row.get("blocker")))
    if normalize_text(row.get("renewal_risk_signal")) in {
        "risk",
        "churn risk",
        "executive concern",
        "budget concern",
    }:
        reasons.append(clean_text(row.get("renewal_risk_signal")))
    return "; ".join(reasons[:4]) or "Needs weekly review"


def founder_action(row: pd.Series) -> str:
    """Return the founder-level action."""
    sentiment = normalize_text(row.get("customer_sentiment"))
    blocker = normalize_text(row.get("blocker"))
    if sentiment in {"executive escalated", "negative"}:
        return "Founder sponsor call to reset trust and activation plan."
    if "integration" in blocker or "migration" in blocker or "data" in blocker:
        return "Escalate technical unblock plan and confirm customer-side owner."
    if owner_coverage_status(row) != "Covered":
        return "Assign owner coverage and review handoff quality."
    if normalize_text(row.get("payment_status")) in {"overdue", "unpaid", "payment failed"}:
        return "Align finance and customer sponsor on payment path."
    if sentiment == "ghosting":
        return "Founder sends executive-level re-engagement note."
    return "Review activation path and remove the highest leverage blocker."


def due_timing(row: pd.Series) -> str:
    """Return timing for the founder queue."""
    category = row.get("founder_attention_category")
    if category == "Founder intervention now":
        return "Today"
    if category == "Leadership review this week":
        return "This week"
    if category == "Owner follow-up":
        return "Next 3 business days"
    return "Next review"


def expected_leverage(row: pd.Series) -> str:
    """Describe why action is worth taking."""
    value = format_currency(row.get("contract_value", 0))
    if float(row.get("contract_value", 0)) >= 50000:
        return f"Protects {value} and improves activation confidence."
    if normalize_text(row.get("renewal_risk_signal")) == "expansion potential":
        return "Protects expansion potential and reference quality."
    if row.get("activation_risk_level") in {"High", "Critical"}:
        return "Prevents onboarding delay from becoming churn risk."
    return "Keeps onboarding motion accountable."


def escalation_note(row: pd.Series) -> str:
    """Return escalation note for founder attention queue."""
    if row.get("founder_attention_category") == "Founder intervention now":
        return "Do not wait for the next weekly review."
    if row.get("activation_risk_level") == "Critical":
        return "Needs named owner and customer-facing plan."
    if owner_coverage_status(row) != "Covered":
        return "Owner gap should be resolved before customer follow-up."
    return "Review in weekly onboarding operating review."


def build_founder_attention_queue(scored_accounts: pd.DataFrame) -> pd.DataFrame:
    """Build a ranked founder intervention queue."""
    queue = scored_accounts[
        scored_accounts["founder_attention_category"].isin(
            [
                "Founder intervention now",
                "Leadership review this week",
                "Owner follow-up",
            ]
        )
    ].copy()
    queue = queue.sort_values(
        by=["founder_attention_score", "contract_value", "onboarding_risk_score"],
        ascending=[False, False, False],
    ).reset_index(drop=True)
    queue["priority_rank"] = queue.index + 1
    queue["risk_reason"] = queue.apply(risk_reason, axis=1)
    queue["founder_action"] = queue.apply(founder_action, axis=1)
    queue["owner"] = queue.apply(primary_owner, axis=1)
    queue["due_timing"] = queue.apply(due_timing, axis=1)
    queue["expected_leverage"] = queue.apply(expected_leverage, axis=1)
    queue["escalation_note"] = queue.apply(escalation_note, axis=1)
    return queue[
        [
            "priority_rank",
            "account_id",
            "customer_name",
            "contract_value",
            "current_stage",
            "risk_reason",
            "founder_action",
            "owner",
            "due_timing",
            "expected_leverage",
            "escalation_note",
        ]
    ]


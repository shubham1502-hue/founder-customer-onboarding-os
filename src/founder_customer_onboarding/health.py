"""Customer health scoring logic."""

from __future__ import annotations

from typing import Any

import pandas as pd

from .utils import as_bool, clamp, normalize_text


def health_category(score: float) -> str:
    """Convert a 0 to 100 health score into a founder-readable category."""
    if score >= 80:
        return "Healthy"
    if score >= 60:
        return "Watch"
    if score >= 40:
        return "At risk"
    return "Critical"


def owner_coverage_status(row: pd.Series) -> str:
    """Classify whether the account has enough accountable owners."""
    owner_fields = [
        "onboarding_owner",
        "customer_success_owner",
        "implementation_owner",
    ]
    missing = [field for field in owner_fields if not normalize_text(row.get(field))]
    if not missing:
        return "Covered"
    if len(missing) == len(owner_fields):
        return "No owner assigned"
    return "Partial owner gap"


def owner_clarity_score(row: pd.Series) -> float:
    """Return a positive score for owner coverage."""
    status = owner_coverage_status(row)
    if status == "Covered":
        return 100
    if status == "Partial owner gap":
        return 55
    return 15


def support_ticket_score(open_tickets: int) -> float:
    """Return a positive health score from support ticket load."""
    if open_tickets <= 0:
        return 100
    if open_tickets <= 2:
        return 85
    if open_tickets <= 4:
        return 65
    if open_tickets <= 7:
        return 40
    return 20


def usage_score(value: Any) -> float:
    """Return a positive health score from usage signal."""
    text = normalize_text(value)
    mapping = {
        "high": 100,
        "healthy": 95,
        "growing": 95,
        "moderate": 75,
        "pilot only": 60,
        "low": 45,
        "none": 20,
        "declining": 30,
    }
    return mapping.get(text, 60)


def sentiment_score(value: Any) -> float:
    """Return a positive health score from customer sentiment."""
    text = normalize_text(value)
    mapping = {
        "champion": 100,
        "positive": 90,
        "neutral": 75,
        "concerned": 45,
        "negative": 20,
        "ghosting": 25,
        "stakeholder changed": 45,
        "executive escalated": 25,
    }
    return mapping.get(text, 65)


def payment_score(value: Any) -> float:
    """Return a positive health score from payment state."""
    text = normalize_text(value)
    mapping = {
        "paid": 100,
        "current": 95,
        "invoiced current": 90,
        "invoice pending": 70,
        "overdue": 25,
        "unpaid": 15,
        "payment failed": 10,
    }
    return mapping.get(text, 65)


def training_score(value: Any) -> float:
    """Return a positive health score from training completion."""
    text = normalize_text(value)
    if as_bool(text):
        return 100
    if text == "partial":
        return 65
    return 40


def renewal_score(value: Any) -> float:
    """Return a positive health score from renewal and expansion signals."""
    text = normalize_text(value)
    mapping = {
        "none": 100,
        "no risk": 100,
        "expansion potential": 100,
        "watch": 70,
        "budget concern": 45,
        "risk": 40,
        "churn risk": 20,
        "executive concern": 25,
    }
    return mapping.get(text, 80)


def activation_progress_score(row: pd.Series, company_config: dict[str, Any]) -> float:
    """Return account progress toward activation."""
    activation_status = normalize_text(row.get("activation_status"))
    if activation_status == "activated":
        return 100
    if activation_status == "blocked":
        status_factor = 0.55
    elif activation_status in {"not started", "not_started"}:
        status_factor = 0.25
    elif activation_status in {"at risk", "at-risk"}:
        status_factor = 0.65
    else:
        status_factor = 0.85

    stages = [normalize_text(stage) for stage in company_config.get("onboarding_stages", [])]
    current_stage = normalize_text(row.get("current_stage"))
    if current_stage in stages and len(stages) > 1:
        stage_index = stages.index(current_stage)
        progress = stage_index / (len(stages) - 1) * 100
    else:
        progress = 45
    return clamp(progress * status_factor)


def deadline_score(days_until_target_activation: int | None) -> float:
    """Return a positive score for activation deadline health."""
    if days_until_target_activation is None:
        return 60
    if days_until_target_activation >= 7:
        return 100
    if days_until_target_activation >= 0:
        return 75
    if days_until_target_activation >= -7:
        return 40
    return 15


def onboarding_age_score(days_in_onboarding: int | None, target_days: int) -> float:
    """Return a positive score for onboarding age."""
    if days_in_onboarding is None:
        return 55
    if days_in_onboarding <= target_days:
        return 100
    if days_in_onboarding <= target_days * 1.5:
        return 65
    if days_in_onboarding <= target_days * 2:
        return 35
    return 20


def calculate_customer_health_score(
    row: pd.Series,
    company_config: dict[str, Any],
    scoring_config: dict[str, Any],
) -> int:
    """Calculate a transparent weighted customer health score."""
    weights = scoring_config["weights"]
    target_days = int(company_config["target_activation_days"])
    blocker_score = 100 - float(row.get("blocker_severity_score", 0))
    integration_score = 100 - float(row.get("integration_complexity_score", 0))
    migration_score = 100 - float(row.get("data_migration_complexity_score", 0))

    factors = {
        "activation_progress": activation_progress_score(row, company_config),
        "days_since_close": onboarding_age_score(row.get("days_in_onboarding"), target_days),
        "days_to_activation_deadline": deadline_score(row.get("days_until_target_activation")),
        "customer_sentiment": sentiment_score(row.get("customer_sentiment")),
        "owner_clarity": owner_clarity_score(row),
        "blocker_severity": blocker_score,
        "support_ticket_load": support_ticket_score(int(row.get("support_tickets_open", 0))),
        "usage_signal": usage_score(row.get("usage_signal")),
        "payment_status": payment_score(row.get("payment_status")),
        "integration_complexity": integration_score,
        "data_migration_complexity": migration_score,
        "training_completion": training_score(row.get("training_completed")),
        "renewal_risk": renewal_score(row.get("renewal_risk_signal")),
    }

    total_weight = sum(float(weights[name]) for name in factors)
    weighted_score = sum(factors[name] * float(weights[name]) for name in factors) / total_weight
    return int(round(clamp(weighted_score)))


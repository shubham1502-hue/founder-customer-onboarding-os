"""Onboarding risk detection."""

from __future__ import annotations

from datetime import date
from typing import Any

import pandas as pd

from .health import calculate_customer_health_score, owner_coverage_status
from .utils import as_bool, clean_text, clamp, days_between, normalize_text


def onboarding_age_band(days_in_onboarding: int | None, target_days: int) -> str:
    """Bucket onboarding age for founder review."""
    if days_in_onboarding is None:
        return "Unknown"
    if days_in_onboarding <= 7:
        return "0 to 7 days"
    if days_in_onboarding <= target_days:
        return f"8 to {target_days} days"
    if days_in_onboarding <= target_days * 2:
        return f"{target_days + 1} to {target_days * 2} days"
    return f"Over {target_days * 2} days"


def blocker_severity_score(blocker: Any) -> int:
    """Convert a human blocker label into a risk score."""
    text = normalize_text(blocker)
    if not text or text in {"none", "no blocker", "n/a"}:
        return 0
    if "integration" in text:
        return 75
    if "migration" in text or "data" in text:
        return 70
    if "ghost" in text or "unresponsive" in text or "silence" in text:
        return 80
    if "stakeholder" in text:
        return 65
    if "payment" in text or "invoice" in text or "unpaid" in text:
        return 70
    if "criteria" in text or "unclear" in text:
        return 55
    if "training" in text:
        return 45
    if "support" in text or "ticket" in text:
        return 60
    if "usage" in text:
        return 55
    if "product" in text:
        return 75
    return 50


def integration_complexity_score(row: pd.Series) -> int:
    """Estimate integration complexity risk."""
    required = as_bool(row.get("integration_required"))
    if not required:
        return 0
    stage = normalize_text(row.get("current_stage"))
    blocker = normalize_text(row.get("blocker"))
    if "integration" in blocker or "technical integration" in stage:
        return 70
    if normalize_text(row.get("activation_status")) == "activated":
        return 10
    return 35


def data_migration_complexity_score(row: pd.Series) -> int:
    """Estimate data migration complexity risk."""
    required = as_bool(row.get("data_migration_required"))
    if not required:
        return 0
    stage = normalize_text(row.get("current_stage"))
    blocker = normalize_text(row.get("blocker"))
    if "migration" in blocker or "data migration" in stage:
        return 70
    if normalize_text(row.get("activation_status")) == "activated":
        return 10
    return 35


def activation_risk_level(row: pd.Series) -> str:
    """Classify activation risk."""
    status = normalize_text(row.get("activation_status"))
    health_score = float(row.get("customer_health_score", 100))
    days_until = row.get("days_until_target_activation")
    blocker_score = float(row.get("blocker_severity_score", 0))

    if status == "activated" and health_score >= 70:
        return "Low"
    if status in {"blocked", "at risk"} or blocker_score >= 70:
        return "Critical"
    if days_until is not None and days_until < 0:
        return "High"
    if health_score < 40:
        return "Critical"
    if health_score < 60:
        return "High"
    if days_until is not None and days_until <= 3 and status != "activated":
        return "Medium"
    return "Low"


def ticket_risk(open_tickets: int) -> float:
    if open_tickets <= 0:
        return 0
    if open_tickets <= 2:
        return 20
    if open_tickets <= 4:
        return 45
    if open_tickets <= 7:
        return 70
    return 90


def usage_risk(value: Any) -> float:
    text = normalize_text(value)
    mapping = {
        "high": 0,
        "healthy": 5,
        "growing": 5,
        "moderate": 25,
        "pilot only": 40,
        "low": 70,
        "none": 90,
        "declining": 80,
    }
    return mapping.get(text, 40)


def payment_risk(value: Any) -> float:
    text = normalize_text(value)
    mapping = {
        "paid": 0,
        "current": 5,
        "invoiced current": 10,
        "invoice pending": 35,
        "overdue": 80,
        "unpaid": 90,
        "payment failed": 95,
    }
    return mapping.get(text, 35)


def sentiment_risk(value: Any) -> float:
    text = normalize_text(value)
    mapping = {
        "champion": 0,
        "positive": 10,
        "neutral": 25,
        "concerned": 65,
        "negative": 90,
        "ghosting": 85,
        "stakeholder changed": 65,
        "executive escalated": 90,
    }
    return mapping.get(text, 35)


def renewal_risk(value: Any) -> float:
    text = normalize_text(value)
    mapping = {
        "none": 0,
        "no risk": 0,
        "expansion potential": 0,
        "watch": 40,
        "budget concern": 65,
        "risk": 70,
        "churn risk": 95,
        "executive concern": 90,
    }
    return mapping.get(text, 20)


def deadline_risk(days_until_target_activation: int | None) -> float:
    if days_until_target_activation is None:
        return 35
    if days_until_target_activation >= 7:
        return 0
    if days_until_target_activation >= 0:
        return 30
    if days_until_target_activation >= -7:
        return 70
    return 90


def onboarding_age_risk(days_in_onboarding: int | None, target_days: int) -> float:
    if days_in_onboarding is None:
        return 35
    if days_in_onboarding <= target_days:
        return 10
    if days_in_onboarding <= target_days * 1.5:
        return 45
    if days_in_onboarding <= target_days * 2:
        return 70
    return 90


def owner_risk(row: pd.Series) -> float:
    status = owner_coverage_status(row)
    if status == "Covered":
        return 0
    if status == "Partial owner gap":
        return 55
    return 90


def training_risk(value: Any) -> float:
    text = normalize_text(value)
    if as_bool(text):
        return 0
    if text == "partial":
        return 45
    return 70


def contract_value_risk(row: pd.Series, high_value_threshold: float) -> float:
    value = float(row.get("contract_value", 0))
    base_risk = float(row.get("onboarding_risk_score", 0))
    if value >= high_value_threshold and base_risk >= 60:
        return 100
    if value >= high_value_threshold:
        return 55
    if value >= high_value_threshold * 0.6 and base_risk >= 70:
        return 75
    return 20


def calculate_onboarding_risk_score(
    row: pd.Series,
    company_config: dict[str, Any],
    scoring_config: dict[str, Any],
) -> int:
    """Calculate a risk score where higher means more onboarding risk."""
    weights = scoring_config["weights"]
    target_days = int(company_config["target_activation_days"])
    factors = {
        "days_since_close": onboarding_age_risk(row.get("days_in_onboarding"), target_days),
        "days_to_activation_deadline": deadline_risk(row.get("days_until_target_activation")),
        "customer_sentiment": sentiment_risk(row.get("customer_sentiment")),
        "owner_clarity": owner_risk(row),
        "blocker_severity": float(row.get("blocker_severity_score", 0)),
        "support_ticket_load": ticket_risk(int(row.get("support_tickets_open", 0))),
        "usage_signal": usage_risk(row.get("usage_signal")),
        "payment_status": payment_risk(row.get("payment_status")),
        "integration_complexity": float(row.get("integration_complexity_score", 0)),
        "data_migration_complexity": float(row.get("data_migration_complexity_score", 0)),
        "training_completion": training_risk(row.get("training_completed")),
        "renewal_risk": renewal_risk(row.get("renewal_risk_signal")),
    }
    total_weight = sum(float(weights[name]) for name in factors)
    weighted_score = sum(factors[name] * float(weights[name]) for name in factors) / total_weight

    return int(round(clamp(weighted_score)))


def founder_attention_category(score: float) -> str:
    """Convert founder attention score to a queue category."""
    if score >= 85:
        return "Founder intervention now"
    if score >= 65:
        return "Leadership review this week"
    if score >= 40:
        return "Owner follow-up"
    if score >= 20:
        return "Monitor"
    return "No action needed"


def calculate_founder_attention_score(
    row: pd.Series,
    company_config: dict[str, Any],
    scoring_config: dict[str, Any],
) -> int:
    """Score founder attention need as a weighted risk and leverage score."""
    weights = scoring_config["weights"]
    high_value_threshold = float(company_config["high_value_threshold"])
    risk_score = float(row.get("onboarding_risk_score", 0))
    health_score = float(row.get("customer_health_score", 100))
    value_score = contract_value_risk(row, high_value_threshold)
    founder_need = max(risk_score, 100 - health_score)
    if float(row.get("contract_value", 0)) >= high_value_threshold and risk_score >= 55:
        founder_need = max(founder_need, 90)
    if normalize_text(row.get("customer_sentiment")) in {"executive escalated", "negative"}:
        founder_need = max(founder_need, 90)
    if normalize_text(row.get("renewal_risk_signal")) in {"churn risk", "executive concern"}:
        founder_need = max(founder_need, 90)

    factors = {
        "founder_attention_need": founder_need,
        "contract_value": value_score,
        "blocker_severity": float(row.get("blocker_severity_score", 0)),
        "owner_clarity": owner_risk(row),
        "days_to_activation_deadline": deadline_risk(row.get("days_until_target_activation")),
        "customer_sentiment": sentiment_risk(row.get("customer_sentiment")),
        "renewal_risk": renewal_risk(row.get("renewal_risk_signal")),
    }
    total_weight = sum(float(weights[name]) for name in factors)
    weighted_score = sum(factors[name] * float(weights[name]) for name in factors) / total_weight

    if founder_need >= 90 and risk_score >= 55:
        weighted_score = max(weighted_score, 88)
    if (
        float(row.get("contract_value", 0)) >= high_value_threshold
        and row.get("activation_risk_level") == "Critical"
    ):
        weighted_score = max(weighted_score, 86)
    if owner_risk(row) >= 80 and risk_score >= 60:
        weighted_score = max(weighted_score, 82)

    return int(round(clamp(weighted_score)))


def enrich_accounts(
    accounts: pd.DataFrame,
    company_config: dict[str, Any],
    scoring_config: dict[str, Any],
) -> pd.DataFrame:
    """Add calculated health, risk, and attention fields to accounts."""
    df = accounts.copy()
    analysis_date = company_config.get("analysis_date") or date.today()
    target_days = int(company_config["target_activation_days"])

    df["days_in_onboarding"] = df["onboarding_start_date"].apply(
        lambda value: days_between(value.date(), analysis_date) if pd.notna(value) else None
    )
    df["days_until_target_activation"] = df["target_activation_date"].apply(
        lambda value: days_between(analysis_date, value.date()) if pd.notna(value) else None
    )
    df["onboarding_age_band"] = df["days_in_onboarding"].apply(
        lambda value: onboarding_age_band(value, target_days)
    )
    df["owner_coverage_status"] = df.apply(owner_coverage_status, axis=1)
    df["blocker_severity_score"] = df["blocker"].apply(blocker_severity_score)
    df["integration_complexity_score"] = df.apply(integration_complexity_score, axis=1)
    df["data_migration_complexity_score"] = df.apply(data_migration_complexity_score, axis=1)
    df["customer_health_score"] = df.apply(
        lambda row: calculate_customer_health_score(row, company_config, scoring_config),
        axis=1,
    )
    df["health_category"] = df["customer_health_score"].apply(
        lambda value: "Healthy"
        if value >= 80
        else "Watch"
        if value >= 60
        else "At risk"
        if value >= 40
        else "Critical"
    )
    df["onboarding_risk_score"] = df.apply(
        lambda row: calculate_onboarding_risk_score(row, company_config, scoring_config),
        axis=1,
    )
    df["activation_risk_level"] = df.apply(activation_risk_level, axis=1)
    df["founder_attention_score"] = df.apply(
        lambda row: calculate_founder_attention_score(row, company_config, scoring_config),
        axis=1,
    )
    df["founder_attention_category"] = df["founder_attention_score"].apply(
        founder_attention_category
    )
    return df


def stale_touchpoint(row: pd.Series, company_config: dict[str, Any]) -> bool:
    """Return true when customer touchpoint is older than the configured SLA."""
    analysis_date = company_config.get("analysis_date") or date.today()
    max_days = int(company_config.get("escalation_rules", {}).get("stale_touchpoint_days", 7))
    value = row.get("last_customer_touchpoint_date")
    if pd.isna(value):
        return True
    return days_between(value.date(), analysis_date) > max_days


def is_unclear_next_step(value: Any) -> bool:
    """Return true when a next step is blank or too vague."""
    text = normalize_text(value)
    return not text or text in {"tbd", "none", "unknown", "follow up", "n/a"}


def risk_severity(score: float) -> str:
    """Return severity label from risk score."""
    if score >= 80:
        return "Critical"
    if score >= 60:
        return "High"
    if score >= 35:
        return "Medium"
    return "Low"


def detect_sla_risks(
    accounts: pd.DataFrame,
    company_config: dict[str, Any],
) -> pd.DataFrame:
    """Detect SLA, handoff, owner, activation, and payment risks."""
    rows: list[dict[str, Any]] = []
    analysis_date = company_config.get("analysis_date") or date.today()
    rules = company_config.get("escalation_rules", {})
    handoff_days = int(rules.get("onboarding_start_sla_days", 2))
    high_value_threshold = float(company_config["high_value_threshold"])

    def add(row: pd.Series, risk_type: str, severity: str, recommended_fix: str) -> None:
        owner = clean_text(row.get("onboarding_owner")) or clean_text(
            row.get("customer_success_owner"), "Unassigned"
        )
        rows.append(
            {
                "account_id": row["account_id"],
                "customer_name": row["customer_name"],
                "risk_type": risk_type,
                "severity": severity,
                "current_stage": row["current_stage"],
                "owner": owner,
                "days_in_onboarding": row.get("days_in_onboarding"),
                "target_activation_date": row["target_activation_date"].date().isoformat()
                if pd.notna(row["target_activation_date"])
                else "",
                "next_step": row["next_step"],
                "recommended_fix": recommended_fix,
            }
        )

    for _, row in accounts.iterrows():
        close_date = row["close_date"].date() if pd.notna(row["close_date"]) else None
        start_date = (
            row["onboarding_start_date"].date()
            if pd.notna(row["onboarding_start_date"])
            else None
        )
        handoff_gap = days_between(close_date, start_date) if start_date else None
        status = normalize_text(row.get("activation_status"))

        if start_date is None or (handoff_gap is not None and handoff_gap > handoff_days):
            add(
                row,
                "Delayed onboarding start",
                "High",
                "Assign onboarding owner and schedule kickoff inside the handoff SLA.",
            )
        if row.get("days_until_target_activation") is not None and row.get(
            "days_until_target_activation"
        ) < 0 and status != "activated":
            add(
                row,
                "Missed activation deadline",
                "Critical",
                "Reset activation plan with owner, customer milestone, and date.",
            )
        if stale_touchpoint(row, company_config):
            add(
                row,
                "Stale customer touchpoint",
                "High",
                "Create a customer touchpoint today and document the next action.",
            )
        if owner_coverage_status(row) != "Covered":
            add(
                row,
                "Missing owner",
                "High",
                "Assign onboarding, customer success, and implementation owners.",
            )
        if is_unclear_next_step(row.get("next_step")):
            add(
                row,
                "Unclear next step",
                "Medium",
                "Replace vague next step with a dated owner-backed action.",
            )
        if float(row.get("blocker_severity_score", 0)) > 0:
            add(
                row,
                "Unresolved blocker",
                risk_severity(float(row.get("blocker_severity_score", 0))),
                "Convert blocker into a dated unblock plan with one accountable owner.",
            )
        if payment_risk(row.get("payment_status")) >= 70:
            add(
                row,
                "Unpaid payment status",
                "High",
                "Resolve billing owner, invoice status, and commercial next step.",
            )
        if usage_risk(row.get("usage_signal")) >= 70 and status in {
            "activated",
            "in progress",
            "at risk",
        }:
            add(
                row,
                "Low usage after onboarding",
                "High",
                "Run usage recovery plan tied to activation criteria.",
            )
        if training_risk(row.get("training_completed")) >= 70:
            add(
                row,
                "Training incomplete",
                "Medium",
                "Schedule training and confirm attendance from the customer owner.",
            )
        if integration_complexity_score(row) >= 70:
            add(
                row,
                "Integration stuck",
                "High",
                "Create technical unblock plan with implementation and product owner.",
            )
        if data_migration_complexity_score(row) >= 70:
            add(
                row,
                "Data migration stuck",
                "High",
                "Create migration checklist, source data owner, and target completion date.",
            )
        if (
            float(row.get("contract_value", 0)) >= high_value_threshold
            and float(row.get("onboarding_risk_score", 0)) >= 55
        ):
            add(
                row,
                "High-value account at risk",
                "Critical",
                "Founder or executive should call the customer sponsor this week.",
            )

    return pd.DataFrame(
        rows,
        columns=[
            "account_id",
            "customer_name",
            "risk_type",
            "severity",
            "current_stage",
            "owner",
            "days_in_onboarding",
            "target_activation_date",
            "next_step",
            "recommended_fix",
        ],
    )

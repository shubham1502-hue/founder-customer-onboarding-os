"""Configuration loading and validation."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from .utils import parse_date


REQUIRED_COMPANY_KEYS = {
    "company_name",
    "stage",
    "business_model",
    "onboarding_model",
    "target_activation_days",
    "activation_definition",
    "target_segments",
    "high_value_threshold",
    "founder_intervention_threshold",
    "onboarding_stages",
    "customer_health_signals",
    "risk_signals",
    "escalation_rules",
    "owner_roles",
    "review_cadence",
    "tools_used",
    "sensitive_data_note",
}

REQUIRED_SCORING_WEIGHTS = {
    "activation_progress",
    "days_since_close",
    "days_to_activation_deadline",
    "contract_value",
    "customer_sentiment",
    "owner_clarity",
    "blocker_severity",
    "support_ticket_load",
    "usage_signal",
    "payment_status",
    "integration_complexity",
    "data_migration_complexity",
    "training_completion",
    "renewal_risk",
    "founder_attention_need",
}


def load_yaml(path: str | Path) -> dict[str, Any]:
    """Load a YAML file and return a dictionary."""
    config_path = Path(path)
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")
    with config_path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}
    if not isinstance(data, dict):
        raise ValueError(f"Config file must contain a YAML mapping: {config_path}")
    return data


def load_company_config(path: str | Path) -> dict[str, Any]:
    """Load and validate company profile configuration."""
    config = load_yaml(path)
    missing = sorted(REQUIRED_COMPANY_KEYS - set(config))
    if missing:
        raise ValueError("Company config missing required keys: " + ", ".join(missing))
    stages = config.get("onboarding_stages")
    if not isinstance(stages, list) or not stages:
        raise ValueError("company_profile.yml must define at least one onboarding stage")
    config["analysis_date"] = parse_date(config.get("analysis_date"))
    return config


def load_scoring_config(path: str | Path) -> dict[str, Any]:
    """Load and validate scoring rules configuration."""
    config = load_yaml(path)
    weights = config.get("weights", {})
    if not isinstance(weights, dict):
        raise ValueError("scoring_rules.yml must include a weights mapping")
    missing = sorted(REQUIRED_SCORING_WEIGHTS - set(weights))
    if missing:
        raise ValueError("Scoring config missing required weights: " + ", ".join(missing))
    return config


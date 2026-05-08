"""CSV ingestion and input validation."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


REQUIRED_COLUMNS = [
    "account_id",
    "customer_name",
    "segment",
    "industry",
    "contract_value",
    "plan_type",
    "close_date",
    "onboarding_start_date",
    "target_activation_date",
    "current_stage",
    "onboarding_owner",
    "sales_owner",
    "customer_success_owner",
    "implementation_owner",
    "key_stakeholder_role",
    "product_use_case",
    "activation_criteria",
    "activation_status",
    "days_since_close",
    "last_customer_touchpoint_date",
    "next_step",
    "blocker",
    "customer_sentiment",
    "support_tickets_open",
    "usage_signal",
    "integration_required",
    "data_migration_required",
    "training_completed",
    "payment_status",
    "renewal_risk_signal",
    "notes",
]


DATE_COLUMNS = [
    "close_date",
    "onboarding_start_date",
    "target_activation_date",
    "last_customer_touchpoint_date",
]

NUMERIC_COLUMNS = ["contract_value", "days_since_close", "support_tickets_open"]


def validate_required_columns(df: pd.DataFrame) -> None:
    """Raise a useful error when required columns are missing."""
    missing = [column for column in REQUIRED_COLUMNS if column not in df.columns]
    if missing:
        raise ValueError("Input CSV missing required columns: " + ", ".join(missing))


def load_accounts(path: str | Path) -> pd.DataFrame:
    """Load onboarding accounts from CSV and normalize common types."""
    csv_path = Path(path)
    if not csv_path.exists():
        raise FileNotFoundError(f"Input CSV not found: {csv_path}")

    df = pd.read_csv(csv_path, keep_default_na=False)
    validate_required_columns(df)

    for column in DATE_COLUMNS:
        df[column] = pd.to_datetime(df[column], errors="coerce")
    for column in NUMERIC_COLUMNS:
        df[column] = pd.to_numeric(df[column], errors="coerce").fillna(0)

    df["contract_value"] = df["contract_value"].astype(float)
    df["days_since_close"] = df["days_since_close"].astype(int)
    df["support_tickets_open"] = df["support_tickets_open"].astype(int)
    return df


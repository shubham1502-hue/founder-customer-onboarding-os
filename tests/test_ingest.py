from pathlib import Path

import pandas as pd
import pytest

from founder_customer_onboarding.ingest import REQUIRED_COLUMNS, load_accounts


ROOT = Path(__file__).resolve().parents[1]


def test_load_accounts_reads_sample_csv():
    df = load_accounts(ROOT / "data/sample_onboarding_accounts.csv")

    assert len(df) >= 20
    assert set(REQUIRED_COLUMNS).issubset(df.columns)
    assert pd.api.types.is_numeric_dtype(df["contract_value"])
    assert pd.api.types.is_datetime64_any_dtype(df["close_date"])


def test_required_column_validation(tmp_path):
    csv_path = tmp_path / "bad.csv"
    pd.DataFrame({"account_id": ["ACC-001"]}).to_csv(csv_path, index=False)

    with pytest.raises(ValueError, match="missing required columns"):
        load_accounts(csv_path)


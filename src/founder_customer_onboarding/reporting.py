"""Output generation for CSV and Markdown reports."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd

from .actions import build_founder_attention_queue
from .risk import detect_sla_risks
from .scoring import build_health_scorecard, build_scored_accounts
from .utils import as_bool, clean_text, format_currency, join_names, normalize_text


ACTIVATION_MATRIX_COLUMNS = [
    "account_id",
    "customer_name",
    "segment",
    "current_stage",
    "activation_status",
    "usage_signal",
    "training_completed",
    "integration_required",
    "data_migration_required",
    "activation_gap",
    "recommended_activation_move",
]


def activation_gap(row: pd.Series) -> str:
    """Identify the primary activation gap."""
    if normalize_text(row.get("activation_status")) == "activated":
        return "Activated"
    if not clean_text(row.get("activation_criteria")):
        return "Missing activation criteria"
    blocker = normalize_text(row.get("blocker"))
    if "integration" in blocker:
        return "Integration not complete"
    if "migration" in blocker or "data" in blocker:
        return "Data migration not complete"
    if not as_bool(row.get("training_completed")):
        return "Training not complete"
    if normalize_text(row.get("usage_signal")) in {"low", "none", "declining"}:
        return "Usage below activation threshold"
    if normalize_text(row.get("customer_sentiment")) in {
        "ghosting",
        "negative",
        "concerned",
        "stakeholder changed",
        "executive escalated",
    }:
        return "Customer engagement risk"
    return "Needs activation evidence"


def recommended_activation_move(row: pd.Series) -> str:
    """Return the most practical activation move."""
    gap = row.get("activation_gap")
    mapping = {
        "Activated": "Keep health evidence current.",
        "Missing activation criteria": "Define activation criteria with customer sponsor.",
        "Integration not complete": "Run integration unblock session with technical owner.",
        "Data migration not complete": "Confirm source data owner and migration checklist.",
        "Training not complete": "Schedule training and confirm attendance.",
        "Usage below activation threshold": "Run usage recovery against activation criteria.",
        "Customer engagement risk": "Re-engage customer stakeholder and confirm priority.",
        "Needs activation evidence": "Document evidence that activation criteria are met.",
    }
    return mapping.get(gap, "Move account to next activation milestone.")


def build_activation_matrix(scored_accounts: pd.DataFrame) -> pd.DataFrame:
    """Build the customer activation matrix."""
    matrix = scored_accounts.copy()
    matrix["activation_gap"] = matrix.apply(activation_gap, axis=1)
    matrix["recommended_activation_move"] = matrix.apply(recommended_activation_move, axis=1)
    return matrix[ACTIVATION_MATRIX_COLUMNS]


PROCESS_FIXES = {
    "Delayed onboarding start": (
        "Closed-won to onboarding handoff is missing SLA discipline.",
        "Create a same-day closed-won handoff checklist and kickoff scheduling rule.",
        "Head of CS",
        "Reduces lost context immediately after close.",
    ),
    "Missed activation deadline": (
        "Activation dates are slipping without earlier intervention.",
        "Review accounts 7 days before target activation and reset milestone plans.",
        "Onboarding Lead",
        "Improves activation predictability.",
    ),
    "Stale customer touchpoint": (
        "Customer communication is going stale during onboarding.",
        "Add a weekly customer touchpoint SLA and stale-account review.",
        "Customer Success Lead",
        "Prevents silence from turning into churn risk.",
    ),
    "Missing owner": (
        "Owner coverage is unclear across onboarding, CS, and implementation.",
        "Require named owners before kickoff and during every stage change.",
        "Founder or BizOps",
        "Makes accountability visible.",
    ),
    "Unclear next step": (
        "Next steps are too vague to manage.",
        "Require every account to have a dated next action with one owner.",
        "Onboarding Lead",
        "Improves execution quality.",
    ),
    "Unresolved blocker": (
        "Blockers are recorded but not converted into unblock plans.",
        "Turn every blocker into owner, due date, and escalation path.",
        "Implementation Lead",
        "Shortens stuck time.",
    ),
    "Unpaid payment status": (
        "Billing risk is leaking into onboarding.",
        "Add finance review to onboarding risk meeting for unpaid accounts.",
        "Finance or RevOps",
        "Reduces commercial friction.",
    ),
    "Low usage after onboarding": (
        "Accounts are not converting onboarding activity into product usage.",
        "Tie activation criteria to usage evidence and run adoption recovery.",
        "Customer Success Lead",
        "Improves activation quality.",
    ),
    "Training incomplete": (
        "Training completion is inconsistent.",
        "Make training a tracked activation milestone with customer attendance.",
        "Onboarding Lead",
        "Improves readiness for activation.",
    ),
    "Integration stuck": (
        "Technical integration blockers are slowing activation.",
        "Create integration runbook with customer technical owner and internal owner.",
        "Implementation Lead",
        "Reduces technical delays.",
    ),
    "Data migration stuck": (
        "Data migration ownership and source data readiness are weak.",
        "Use a migration readiness checklist before kickoff.",
        "Implementation Lead",
        "Reduces data dependency risk.",
    ),
    "High-value account at risk": (
        "High-value onboarding risk is not escalated early enough.",
        "Add automatic founder review for high-value accounts with high risk.",
        "Founder",
        "Protects revenue and reference potential.",
    ),
}


def score_driver_summary(row: pd.Series) -> str:
    """Summarize why scores and attention category were assigned."""
    drivers: list[str] = []
    if row.get("activation_risk_level") in {"High", "Critical"}:
        drivers.append(f"{row.get('activation_risk_level')} activation risk")
    if row.get("health_category") in {"At risk", "Critical"}:
        drivers.append(f"{row.get('health_category')} customer health")
    if clean_text(row.get("blocker")) and normalize_text(row.get("blocker")) not in {
        "none",
        "no blocker",
    }:
        drivers.append(clean_text(row.get("blocker")))
    if clean_text(row.get("owner_coverage_status")) not in {"", "Covered"}:
        drivers.append(clean_text(row.get("owner_coverage_status")))
    if normalize_text(row.get("usage_signal")) in {"low", "none", "declining"}:
        drivers.append(f"Usage signal: {clean_text(row.get('usage_signal'))}")
    if normalize_text(row.get("payment_status")) in {"overdue", "unpaid", "payment failed"}:
        drivers.append(f"Payment status: {clean_text(row.get('payment_status'))}")
    training_status = normalize_text(row.get("training_completed"))
    if training_status == "no":
        drivers.append("Training incomplete")
    elif training_status == "partial":
        drivers.append("Training partially complete")
    if normalize_text(row.get("renewal_risk_signal")) in {
        "risk",
        "churn risk",
        "executive concern",
        "budget concern",
    }:
        drivers.append(f"Renewal risk: {clean_text(row.get('renewal_risk_signal'))}")
    if not drivers:
        drivers.append("Healthy onboarding signals")
    return "; ".join(drivers[:5])


def score_interpretation(row: pd.Series) -> str:
    """Explain how a founder should read the scores."""
    return (
        f"Health {row.get('customer_health_score')} means {row.get('health_category')}. "
        f"Risk {row.get('onboarding_risk_score')} maps to {row.get('activation_risk_level')} activation risk. "
        f"Founder attention {row.get('founder_attention_score')} maps to {row.get('founder_attention_category')}."
    )


def build_score_explanations(scored_accounts: pd.DataFrame) -> pd.DataFrame:
    """Build account-level score explanations for founder trust."""
    explanations = scored_accounts.copy()
    explanations["score_driver_summary"] = explanations.apply(score_driver_summary, axis=1)
    explanations["score_interpretation"] = explanations.apply(score_interpretation, axis=1)
    return explanations[
        [
            "account_id",
            "customer_name",
            "contract_value",
            "customer_health_score",
            "health_category",
            "onboarding_risk_score",
            "activation_risk_level",
            "founder_attention_score",
            "founder_attention_category",
            "score_driver_summary",
            "score_interpretation",
            "recommended_next_action",
        ]
    ].sort_values(
        by=["founder_attention_score", "onboarding_risk_score", "contract_value"],
        ascending=[False, False, False],
    )


def build_process_improvements(sla_risks: pd.DataFrame) -> pd.DataFrame:
    """Summarize recurring process issues from detected risks."""
    rows: list[dict[str, Any]] = []
    if sla_risks.empty:
        return pd.DataFrame(
            columns=[
                "improvement_id",
                "process_issue",
                "count",
                "affected_accounts",
                "suggested_fix",
                "owner_role",
                "expected_impact",
            ]
        )

    grouped = sla_risks.groupby("risk_type", sort=False)
    for index, (risk_type, group) in enumerate(grouped, start=1):
        process_issue, suggested_fix, owner_role, expected_impact = PROCESS_FIXES.get(
            risk_type,
            (
                f"{risk_type} is recurring across onboarding.",
                "Review root cause and assign one accountable owner.",
                "BizOps",
                "Improves operating visibility.",
            ),
        )
        rows.append(
            {
                "improvement_id": f"OI-{index:03d}",
                "process_issue": process_issue,
                "count": int(len(group)),
                "affected_accounts": join_names(group["customer_name"].tolist()),
                "suggested_fix": suggested_fix,
                "owner_role": owner_role,
                "expected_impact": expected_impact,
            }
        )
    return pd.DataFrame(rows)


def markdown_table(df: pd.DataFrame, columns: list[str], limit: int = 10) -> str:
    """Render a compact Markdown table."""
    if df.empty:
        return "No rows found.\n"
    display = df[columns].head(limit).copy()
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join(["---"] * len(columns)) + " |"]
    for _, row in display.iterrows():
        values = [clean_text(row.get(column), "") for column in columns]
        lines.append("| " + " | ".join(value.replace("|", "/") for value in values) + " |")
    return "\n".join(lines) + "\n"


def build_founder_memo(
    scored_accounts: pd.DataFrame,
    scorecard: pd.DataFrame,
    founder_queue: pd.DataFrame,
    sla_risks: pd.DataFrame,
    activation_matrix: pd.DataFrame,
    process_improvements: pd.DataFrame,
    company_config: dict[str, Any],
) -> str:
    """Build the founder onboarding memo."""
    total_accounts = len(scored_accounts)
    activated = int((scored_accounts["activation_status"].str.lower() == "activated").sum())
    at_risk = int(scored_accounts["health_category"].isin(["At risk", "Critical"]).sum())
    founder_now = int(
        (scored_accounts["founder_attention_category"] == "Founder intervention now").sum()
    )
    high_value_threshold = float(company_config["high_value_threshold"])
    high_value_risk = scored_accounts[
        (scored_accounts["contract_value"] >= high_value_threshold)
        & (scored_accounts["onboarding_risk_score"] >= 55)
    ]
    owner_gaps = scored_accounts[scored_accounts["owner_coverage_status"] != "Covered"]

    lines = [
        "# Founder Onboarding Memo",
        "",
        "## Data note",
        "",
        company_config.get(
            "data_context_note",
            "Confirm the data source before making customer decisions.",
        ),
        "",
        "## Executive summary",
        "",
        f"{company_config['company_name']} has {total_accounts} onboarding accounts in this review. "
        f"{activated} are activated, {at_risk} are at risk or critical, and {founder_now} need founder intervention now.",
        "",
        "Read the founder attention queue first, then review SLA risks and process improvements.",
        "",
        "Scores are deterministic. They use `config/scoring_rules.yml`, visible account fields, and rule-based risk detection. Review `outputs/account_score_explanations.csv` when you want the reason behind a score.",
        "",
        "## Onboarding health snapshot",
        "",
        markdown_table(
            scorecard,
            [
                "customer_name",
                "current_stage",
                "customer_health_score",
                "health_category",
                "onboarding_risk_score",
                "founder_attention_category",
            ],
            limit=10,
        ),
        "## Customers needing founder attention this week",
        "",
        markdown_table(
            founder_queue,
            [
                "priority_rank",
                "customer_name",
                "contract_value",
                "risk_reason",
                "founder_action",
                "due_timing",
            ],
            limit=10,
        ),
        "## SLA and handoff risks",
        "",
        markdown_table(
            sla_risks,
            ["customer_name", "risk_type", "severity", "owner", "recommended_fix"],
            limit=12,
        ),
        "## Activation bottlenecks",
        "",
        markdown_table(
            activation_matrix[activation_matrix["activation_gap"] != "Activated"],
            ["customer_name", "current_stage", "activation_gap", "recommended_activation_move"],
            limit=12,
        ),
        "## Owner gaps",
        "",
        markdown_table(
            owner_gaps,
            ["customer_name", "current_stage", "owner_coverage_status", "recommended_next_action"],
            limit=12,
        ),
        "## High-value accounts at risk",
        "",
        markdown_table(
            high_value_risk,
            [
                "customer_name",
                "contract_value",
                "current_stage",
                "activation_risk_level",
                "recommended_next_action",
            ],
            limit=10,
        ),
        "## Process improvements to make this week",
        "",
        markdown_table(
            process_improvements,
            ["improvement_id", "process_issue", "count", "suggested_fix", "owner_role"],
            limit=10,
        ),
        "## Recommended next 7-day actions",
        "",
        "1. Review every account in the founder attention queue and confirm owner, customer step, and due date.",
        "2. Fix missing owners before discussing lower-priority workflow improvements.",
        "3. Reset missed activation dates with customer-facing milestones.",
        "4. Run unblock sessions for integration, data migration, payment, and training risks.",
        "5. Update the CRM or customer success tracker with current stage, next step, and activation evidence.",
        "",
    ]
    return "\n".join(lines)


def build_operating_review(
    scored_accounts: pd.DataFrame,
    founder_queue: pd.DataFrame,
    sla_risks: pd.DataFrame,
    process_improvements: pd.DataFrame,
    company_config: dict[str, Any],
) -> str:
    """Build the weekly onboarding operating review."""
    blocked_accounts = scored_accounts[
        scored_accounts["activation_risk_level"].isin(["High", "Critical"])
    ]
    owner_gaps = scored_accounts[scored_accounts["owner_coverage_status"] != "Covered"]
    lines = [
        "# Onboarding Operating Review",
        "",
        "## Data note",
        "",
        company_config.get(
            "data_context_note",
            "Confirm the data source before making customer decisions.",
        ),
        "",
        "## Weekly onboarding review agenda",
        "",
        "1. Review activation progress by stage.",
        "2. Discuss founder attention queue.",
        "3. Inspect SLA and handoff risks.",
        "4. Decide owner changes and escalation paths.",
        "5. Commit process improvements for the next 7 days.",
        "",
        "## Metrics to inspect",
        "",
        f"- Accounts reviewed: {len(scored_accounts)}",
        f"- Activated accounts: {int((scored_accounts['activation_status'].str.lower() == 'activated').sum())}",
        f"- Accounts with high or critical activation risk: {len(blocked_accounts)}",
        f"- Accounts with owner gaps: {len(owner_gaps)}",
        f"- Open SLA risks: {len(sla_risks)}",
        "",
        "## Accounts to discuss",
        "",
        markdown_table(
            founder_queue,
            ["priority_rank", "customer_name", "risk_reason", "owner", "due_timing"],
            limit=12,
        ),
        "## Decisions needed",
        "",
        "- Which high-risk accounts need founder outreach this week?",
        "- Which accounts need new owners before the next customer touchpoint?",
        "- Which activation deadlines need to be reset with the customer?",
        "- Which blockers require product, implementation, finance, or executive escalation?",
        "",
        "## Owners and due dates",
        "",
        markdown_table(
            founder_queue,
            ["customer_name", "owner", "founder_action", "due_timing"],
            limit=12,
        ),
        "## What to update in CRM or customer success tracker",
        "",
        "- Current onboarding stage",
        "- Activation status",
        "- Activation criteria and evidence",
        "- Named onboarding, customer success, and implementation owners",
        "- Next step, due date, and blocker owner",
        "- Latest customer touchpoint date",
        "- Payment, support, usage, and renewal risk notes",
        "",
        "## What to escalate to founder",
        "",
        markdown_table(
            founder_queue[founder_queue["due_timing"].isin(["Today", "This week"])],
            ["customer_name", "risk_reason", "founder_action", "escalation_note"],
            limit=10,
        ),
        "## Process commitments",
        "",
        markdown_table(
            process_improvements,
            ["improvement_id", "process_issue", "suggested_fix", "owner_role"],
            limit=10,
        ),
        "",
    ]
    return "\n".join(lines)


def generate_outputs(
    input_csv: str | Path,
    company_config: dict[str, Any],
    scoring_config: dict[str, Any],
    output_dir: str | Path,
) -> dict[str, Path]:
    """Run the full reporting pipeline and write all outputs."""
    from .ingest import load_accounts

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    accounts = load_accounts(input_csv)
    scored_accounts = build_scored_accounts(accounts, company_config, scoring_config)
    scorecard = build_health_scorecard(scored_accounts)
    founder_queue = build_founder_attention_queue(scored_accounts)
    sla_risks = detect_sla_risks(scored_accounts, company_config)
    activation_matrix = build_activation_matrix(scored_accounts)
    score_explanations = build_score_explanations(scored_accounts)
    process_improvements = build_process_improvements(sla_risks)

    files = {
        "scorecard": output_path / "onboarding_health_scorecard.csv",
        "founder_queue": output_path / "founder_attention_queue.csv",
        "sla_risks": output_path / "onboarding_sla_risks.csv",
        "activation_matrix": output_path / "customer_activation_matrix.csv",
        "score_explanations": output_path / "account_score_explanations.csv",
        "process_improvements": output_path / "onboarding_process_improvements.csv",
        "founder_memo": output_path / "founder_onboarding_memo.md",
        "operating_review": output_path / "onboarding_operating_review.md",
    }

    scorecard.to_csv(files["scorecard"], index=False)
    founder_queue.to_csv(files["founder_queue"], index=False)
    sla_risks.to_csv(files["sla_risks"], index=False)
    activation_matrix.to_csv(files["activation_matrix"], index=False)
    score_explanations.to_csv(files["score_explanations"], index=False)
    process_improvements.to_csv(files["process_improvements"], index=False)
    files["founder_memo"].write_text(
        build_founder_memo(
            scored_accounts,
            scorecard,
            founder_queue,
            sla_risks,
            activation_matrix,
            process_improvements,
            company_config,
        ),
        encoding="utf-8",
    )
    files["operating_review"].write_text(
        build_operating_review(
            scored_accounts,
            founder_queue,
            sla_risks,
            process_improvements,
            company_config,
        ),
        encoding="utf-8",
    )
    return files

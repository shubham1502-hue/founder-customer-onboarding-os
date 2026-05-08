"""Command line interface."""

from __future__ import annotations

import argparse
from pathlib import Path

from .config import load_company_config, load_scoring_config
from .reporting import generate_outputs


DEFAULT_INPUT = Path("data/sample_onboarding_accounts.csv")
DEFAULT_COMPANY_CONFIG = Path("config/company_profile.yml")
DEFAULT_SCORING_CONFIG = Path("config/scoring_rules.yml")
DEFAULT_OUTPUT_DIR = Path("outputs")


def run_pipeline(args: argparse.Namespace) -> int:
    """Run the onboarding OS pipeline."""
    company_config = load_company_config(args.company_config)
    scoring_config = load_scoring_config(args.scoring_config)
    files = generate_outputs(args.input, company_config, scoring_config, args.output_dir)
    print("Generated onboarding control tower outputs:")
    for path in files.values():
        print(f"- {path}")
    print("Open outputs/founder_onboarding_memo.md first.")
    return 0


def build_parser() -> argparse.ArgumentParser:
    """Build CLI parser."""
    parser = argparse.ArgumentParser(
        prog="founder-customer-onboarding-os",
        description="Generate founder-ready onboarding health, risk, and intervention outputs.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    run_parser = subparsers.add_parser("run", help="Run the onboarding control tower.")
    run_parser.add_argument("--input", default=DEFAULT_INPUT, type=Path)
    run_parser.add_argument("--company-config", default=DEFAULT_COMPANY_CONFIG, type=Path)
    run_parser.add_argument("--scoring-config", default=DEFAULT_SCORING_CONFIG, type=Path)
    run_parser.add_argument("--output-dir", default=DEFAULT_OUTPUT_DIR, type=Path)
    run_parser.set_defaults(func=run_pipeline)

    demo_parser = subparsers.add_parser("demo", help="Run demo with bundled sample data.")
    demo_parser.set_defaults(
        input=DEFAULT_INPUT,
        company_config=DEFAULT_COMPANY_CONFIG,
        scoring_config=DEFAULT_SCORING_CONFIG,
        output_dir=DEFAULT_OUTPUT_DIR,
        func=run_pipeline,
    )
    return parser


def main() -> int:
    """CLI entrypoint."""
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())


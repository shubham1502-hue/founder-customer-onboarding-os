# Contributing

Thanks for improving Founder Customer Onboarding OS.

## Local setup

```bash
make install
make test
make demo
```

## Contribution guidelines

- Keep the base workflow offline and deterministic.
- Do not add paid API dependencies to the core workflow.
- Do not commit private customer data, secrets, API keys, credentials, support transcripts, contracts, or personal data.
- Use synthetic or anonymized sample data only.
- Keep scoring rules transparent and editable in `config/scoring_rules.yml`.
- Keep founder-facing documentation practical and concise.
- Do not add emojis.
- Do not use em dash characters.

## Pull request checklist

- Tests pass with `make test`.
- Demo outputs regenerate with `make demo`.
- README and docs are updated if behavior changes.
- New sample data is clearly synthetic.
- Generated junk files are not committed.


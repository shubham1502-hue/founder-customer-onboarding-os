# Founder Use Case

## Scenario

A founder reviews 20 onboarding accounts every Monday. The sales team knows what closed. Customer success knows some accounts are moving. Implementation knows which integrations are stuck. Finance knows one customer has not paid. No single view tells the founder which customers are likely to fail activation.

Founder Customer Onboarding OS creates that view from one CSV and two YAML files.

## How the founder uses it

1. The operator exports the current onboarding tracker to `data/sample_onboarding_accounts.csv`.
2. The founder or operator updates `config/company_profile.yml` with activation definition, owner roles, and review thresholds.
3. The operator runs `make run`.
4. The founder opens `outputs/founder_onboarding_memo.md`.
5. The founder reviews `outputs/founder_attention_queue.csv`.
6. The team assigns owners, due dates, and customer-facing next steps.

## What the founder learns

- Which accounts need founder intervention now.
- Which accounts have missed activation dates.
- Which customers have stale touchpoints.
- Which accounts have missing owner coverage.
- Which high-value customers are blocked before activation.
- Which activation bottlenecks repeat across accounts.
- Which process improvements should happen this week.

## Example decisions

- Founder calls the executive sponsor at a high-value blocked account.
- Implementation lead creates a technical unblock plan for integration risk.
- Customer success owner schedules training for accounts stuck before activation.
- Finance owner resolves payment blockers before rollout expands.
- BizOps changes the closed-won handoff checklist to prevent delayed onboarding starts.

## Practical result

The founder leaves the review with a ranked account queue, owner-backed actions, and a short list of process fixes. The team stops treating closed-won as done and starts managing activation as an operating system.


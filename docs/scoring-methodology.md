# Scoring Methodology

Founder Customer Onboarding OS uses deterministic rule-based scoring. It does not use an LLM, paid API, or hidden model.

## What the scores mean

| Score | Range | Meaning |
| --- | --- | --- |
| Customer health score | 0 to 100 | Higher is better. It measures whether the account looks likely to reach or sustain activation. |
| Onboarding risk score | 0 to 100 | Higher is worse. It measures operational risk in the onboarding journey. |
| Founder attention score | 0 to 100 | Higher means the founder or leadership team should review the account sooner. |

## Health categories

| Category | Score range |
| --- | --- |
| Healthy | 80 to 100 |
| Watch | 60 to 79 |
| At risk | 40 to 59 |
| Critical | Below 40 |

## Founder attention categories

| Category | Score range |
| --- | --- |
| Founder intervention now | 85 to 100 |
| Leadership review this week | 65 to 84 |
| Owner follow-up | 40 to 64 |
| Monitor | 20 to 39 |
| No action needed | Below 20 |

## Inputs used

The scorer uses only fields that are visible in the CSV and YAML config:

- Activation status
- Current onboarding stage
- Days in onboarding
- Days until target activation
- Customer sentiment
- Owner coverage
- Blocker severity
- Support ticket load
- Usage signal
- Payment status
- Integration requirement
- Data migration requirement
- Training completion
- Renewal risk signal
- Contract value
- High-value threshold
- Founder intervention threshold

## Where weights live

Weights live in `config/scoring_rules.yml`.

The default weights intentionally over-index on activation progress, blocker severity, deadline pressure, customer sentiment, owner clarity, usage signal, renewal risk, and founder attention need. That makes the tool useful for early-stage teams where customer context can disappear after close-won.

## How customer health is calculated

Customer health is a weighted positive score. It rewards:

- Clear activation progress
- Enough time before the activation deadline
- Positive customer sentiment
- Complete owner coverage
- Low blocker severity
- Low support ticket load
- Healthy usage
- Clean payment status
- Lower integration and migration complexity
- Completed training
- Low renewal risk

## How onboarding risk is calculated

Onboarding risk is a weighted risk score. It increases when:

- Onboarding is aging past the target activation window
- Activation deadline is close or missed
- Sentiment is concerned, negative, ghosting, or escalated
- Owner coverage is missing or partial
- Blockers exist
- Support tickets are rising
- Usage is low, none, or declining
- Payment is overdue, unpaid, or failed
- Integration or data migration is stuck
- Training is incomplete
- Renewal risk is visible

## How founder attention is calculated

Founder attention combines risk and leverage. It increases when:

- The account is high value
- Activation risk is high or critical
- Customer health is at risk or critical
- Sentiment is negative or executive escalated
- Renewal risk is churn risk or executive concern
- Owner coverage is missing
- Deadline pressure is high
- Blockers are severe

The output is intentionally action-oriented. The founder attention queue includes:

- `risk_reason`
- `founder_action`
- `owner`
- `due_timing`
- `expected_leverage`
- `escalation_note`

## How to audit a score

Open `outputs/account_score_explanations.csv`.

For each account, it shows:

- Health score and category
- Onboarding risk score and activation risk level
- Founder attention score and category
- Score driver summary
- Score interpretation
- Recommended next action

Then open `config/scoring_rules.yml` to adjust weights if the default model does not match your onboarding motion.

## What this is not

This is not a generic customer success dashboard. It is a founder operating system for making sure closed-won customers become activated customers.


# Onboarding Tracker Template

Use this template when building your customer onboarding CSV.

## Required fields

| Field | Example value | Notes |
| --- | --- | --- |
| account_id | ACC-101 | Stable account identifier |
| customer_name | Acme Ledger AI | Customer name |
| segment | SMB | Your customer segment |
| industry | Fintech | Customer industry |
| contract_value | 24000 | Numeric value |
| plan_type | Growth | Plan or package |
| close_date | 2026-04-29 | Use YYYY-MM-DD |
| onboarding_start_date | 2026-04-30 | Use YYYY-MM-DD |
| target_activation_date | 2026-05-28 | Use YYYY-MM-DD |
| current_stage | Technical integration | Must map to your config stages |
| onboarding_owner | Maya Rao | Can be blank, but blank owners create risk |
| sales_owner | Arjun Mehta | Deal context owner |
| customer_success_owner | Neha Kapoor | Adoption owner |
| implementation_owner | Dev Iyer | Technical or delivery owner |
| key_stakeholder_role | Head of Finance | Customer sponsor or main user role |
| product_use_case | Automated reconciliation | Main use case |
| activation_criteria | Three workflows live | Evidence of activation |
| activation_status | In progress | Activated, in progress, at risk, blocked, or not started |
| days_since_close | 9 | Numeric value |
| last_customer_touchpoint_date | 2026-05-07 | Use YYYY-MM-DD |
| next_step | Confirm first value report | Owner-backed next action |
| blocker | Integration stuck | Use None if no blocker |
| customer_sentiment | Positive | Champion, positive, neutral, concerned, negative, ghosting |
| support_tickets_open | 1 | Numeric value |
| usage_signal | Healthy | Healthy, growing, moderate, low, none, declining |
| integration_required | Yes | Yes or No |
| data_migration_required | No | Yes or No |
| training_completed | Partial | Yes, No, or Partial |
| payment_status | Paid | Paid, invoiced current, overdue, unpaid |
| renewal_risk_signal | None | None, watch, risk, churn risk, expansion potential |
| notes | Synthetic example | Optional context |

## Minimum viable tracker

If your tracker is messy, start with these fields first:

- Customer name
- Contract value
- Close date
- Onboarding start date
- Target activation date
- Current stage
- Owners
- Activation status
- Last customer touchpoint
- Next step
- Blocker
- Usage signal
- Training completion
- Payment status

## Data safety

Use synthetic data in public repos. Keep private customer data in a private fork or local machine only.


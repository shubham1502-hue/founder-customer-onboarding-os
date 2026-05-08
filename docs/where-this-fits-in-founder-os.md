# Where This Fits in Founder OS

Founder Customer Onboarding OS is the post-sale onboarding and activation layer.

It starts after a deal is closed or after a customer signs up. It should not replace sales intelligence, GTM research, weekly revenue diagnosis, or the company-wide weekly operating review.

## Portfolio architecture

- AI leverage decisions: `founder-ai-workflow-roi-os`
- Pre-call GTM: `ai-gtm-command-center`
- Post-call sales intelligence: `founder-led-sales-call-os`
- Weekly revenue diagnosis: `founder-os-revenue-engine`
- Post-sale onboarding: `founder-customer-onboarding-os`
- Weekly operating review: `founder-weekly-operating-review-agent`
- Investor narrative: `board-pack-investor-update-agent`
- Umbrella: `founder-os`

## What this repo owns

- Customer onboarding journey
- Activation progress
- Handoff risk
- SLA risk
- Missing owner detection
- Customer health scoring
- Founder intervention priorities
- Weekly onboarding memo
- Onboarding operating review

## What this repo does not own

- Pre-call account research
- Sales call summaries
- Objection handling
- Pipeline leakage diagnosis
- Company-wide weekly operating review
- Board pack narrative
- CRM architecture

## Why the boundary matters

Closed-won is not activated. This repo exists because many early-stage teams lose customer context after the deal closes. The founder needs a weekly operating view of which customers are stuck, which accounts need intervention, and which onboarding workflows are creating risk.


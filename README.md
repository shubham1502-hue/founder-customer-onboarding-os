# Founder Customer Onboarding OS

Turn closed-won customers into activated customers with onboarding health, SLA risk, founder attention queues, and weekly operating reviews.

This helps founders prevent closed-won customers from getting stuck after the sale. Replace one CSV, edit one YAML file, run one command, and open one memo that tells you:

- Which customers are stuck after closing
- Which accounts need founder attention this week
- Which handoffs, owners, blockers, payments, trainings, integrations, and migrations are creating activation risk
- What action each owner should take next

The base workflow is deterministic, offline-first, and does not require paid APIs or an LLM.

Start here:

```bash
make install
make run
open outputs/founder_onboarding_memo.md
```

## The founder problem

Founders often know which deals closed, but not which customers are stuck after the sale. Onboarding risk hides inside handoffs, stale touchpoints, missing owners, unclear activation criteria, support tickets, integrations, training, and customer silence.

This repo turns post-sale chaos into a founder-ready onboarding control tower.

## What this repo does

- Tracks onboarding health
- Scores customer health
- Flags activation risk
- Detects stale handoffs
- Finds missing owners
- Identifies SLA risks
- Creates a founder attention queue
- Finds process bottlenecks
- Generates a weekly onboarding memo
- Creates a weekly onboarding operating review

## What a founder gets in 10 minutes

- Customers needing founder attention
- Health scorecard
- SLA risk list
- Activation bottleneck view
- Owner gap view
- High-value accounts at risk
- Score explanations
- Process improvement list
- Founder onboarding memo

## Before and after

Before:

- Closed-won deals disappear into messy onboarding
- Customer success updates live in memory
- Founders hear about problems late
- Activation criteria are vague
- Handoffs are manual
- No weekly onboarding control tower

After:

- Onboarding health scorecard
- Founder attention queue
- SLA and handoff risk list
- Activation matrix
- Process improvement list
- Weekly onboarding memo
- Clear next actions and owners

## Who this is for

- Early-stage founders
- Founder's Office teams
- BizOps operators
- RevOps operators
- Customer Success operators
- B2B SaaS teams
- AI startup founders
- Founder-led services businesses
- Implementation-heavy startups

## Quick start

1. Fork repo
2. Clone repo
3. Install dependencies
4. Edit company config
5. Replace sample onboarding CSV
6. Run the system
7. Review outputs

```bash
make install
make run
```

| Step | File or command | What to do |
| --- | --- | --- |
| 1 | data/sample_onboarding_accounts.csv | Replace with your customer onboarding tracker |
| 2 | config/company_profile.yml | Edit activation definition, stages, owners, risk thresholds |
| 3 | make run | Generate scorecards, risks, queue, memo, and review |
| 4 | outputs/founder_onboarding_memo.md | Read this first |
| 5 | outputs/account_score_explanations.csv | Check why scores and recommendations were assigned |

You can also run:

```bash
python -m founder_customer_onboarding.cli run \
  --input data/sample_onboarding_accounts.csv \
  --company-config config/company_profile.yml \
  --scoring-config config/scoring_rules.yml \
  --output-dir outputs
```

Demo command:

```bash
python -m founder_customer_onboarding.cli demo
```

## How to fork and use this for your company

1. Click Fork.
2. Rename repo if needed.
3. Replace `data/sample_onboarding_accounts.csv`.
4. Edit `config/company_profile.yml`.
5. Edit `config/scoring_rules.yml` if needed.
6. Run `make run`.
7. Review `outputs/founder_onboarding_memo.md` first.
8. Review `outputs/founder_attention_queue.csv` second.
9. Connect outputs to Google Sheets, Notion, Airtable, HubSpot, Pipedrive, Attio, Salesforce, Linear, ClickUp, or your customer success tracker if relevant.

Non-technical path:

- Replace one CSV
- Edit one YAML file
- Run one command
- Read one memo

## Where this fits in the Founder OS

- Use [ai-gtm-command-center](https://github.com/shubham1502-hue/ai-gtm-command-center) before calls to research accounts and prepare outreach.
- Use [founder-led-sales-call-os](https://github.com/shubham1502-hue/founder-led-sales-call-os) after sales calls to extract objections and deal rescue actions.
- Use [founder-os-revenue-engine](https://github.com/shubham1502-hue/founder-os-revenue-engine) to diagnose funnel leakage.
- Use `founder-customer-onboarding-os` after close-won to track activation and onboarding risk.
- Use [founder-weekly-operating-review-agent](https://github.com/shubham1502-hue/founder-weekly-operating-review-agent) to roll onboarding risks into the weekly operating review.
- Use [board-pack-investor-update-agent](https://github.com/shubham1502-hue/board-pack-investor-update-agent) if onboarding, activation, or retention risk needs board or investor narrative.
- Use [founder-ai-workflow-roi-os](https://github.com/shubham1502-hue/founder-ai-workflow-roi-os) if onboarding workflows should be automated, hired for, outsourced, or left manual.
- Use [founder-os](https://github.com/shubham1502-hue/founder-os) as the umbrella operating system.

## Input format

The input is a CSV at `data/sample_onboarding_accounts.csv`. All sample rows are synthetic and fictionalized.

The bundled sample data and generated sample outputs are synthetic. They are designed to show the workflow, not to claim production usage by any real company.

Required columns:

- `account_id`: Stable account identifier
- `customer_name`: Customer or account name
- `segment`: Startup, SMB, mid-market, enterprise pilot, or your own segment
- `industry`: Customer industry
- `contract_value`: Contract value as a number
- `plan_type`: Plan or package sold
- `close_date`: Deal close date in `YYYY-MM-DD`
- `onboarding_start_date`: Onboarding start date in `YYYY-MM-DD`
- `target_activation_date`: Target activation date in `YYYY-MM-DD`
- `current_stage`: Current onboarding stage
- `onboarding_owner`: Person accountable for onboarding plan
- `sales_owner`: Person who closed the deal or owns deal context
- `customer_success_owner`: Person accountable for adoption and health
- `implementation_owner`: Person accountable for technical setup or delivery
- `key_stakeholder_role`: Main customer stakeholder role
- `product_use_case`: Primary customer use case
- `activation_criteria`: Evidence required to call the account activated
- `activation_status`: Activated, in progress, at risk, blocked, or not started
- `days_since_close`: Days since close at the time of review
- `last_customer_touchpoint_date`: Last customer touchpoint in `YYYY-MM-DD`
- `next_step`: Next owner-backed action
- `blocker`: Current blocker or `None`
- `customer_sentiment`: Champion, positive, neutral, concerned, negative, ghosting, stakeholder changed, or executive escalated
- `support_tickets_open`: Count of open support tickets
- `usage_signal`: Healthy, growing, moderate, pilot only, low, none, or declining
- `integration_required`: Yes or No
- `data_migration_required`: Yes or No
- `training_completed`: Yes, No, or Partial
- `payment_status`: Paid, invoiced current, invoice pending, overdue, unpaid, or payment failed
- `renewal_risk_signal`: None, watch, budget concern, risk, churn risk, executive concern, or expansion potential
- `notes`: Optional context

## Output files

Open `outputs/founder_onboarding_memo.md` first.

- `outputs/onboarding_health_scorecard.csv`: Account-level customer health, onboarding risk, activation risk, founder attention score, and recommended next action.
- `outputs/founder_attention_queue.csv`: Ranked list of accounts needing founder, leadership, or owner follow-up.
- `outputs/onboarding_sla_risks.csv`: Detected SLA, handoff, payment, owner, touchpoint, and blocker risks.
- `outputs/customer_activation_matrix.csv`: Activation gaps and recommended activation moves by account.
- `outputs/account_score_explanations.csv`: Account-level score drivers, score interpretation, and recommended next action.
- `outputs/onboarding_process_improvements.csv`: Recurring process issues with suggested fixes, owner roles, and expected impact.
- `outputs/founder_onboarding_memo.md`: Founder-ready weekly memo with summary, risks, bottlenecks, owner gaps, and next 7-day actions.
- `outputs/onboarding_operating_review.md`: Weekly operating review agenda, metrics, accounts to discuss, decisions, owners, and CRM updates.

## How to trust the scores

The scoring is deterministic and explainable. There are no hidden models.

- `customer_health_score` is a 0 to 100 positive score. Higher is better.
- `onboarding_risk_score` is a 0 to 100 risk score. Higher means more activation risk.
- `founder_attention_score` is a 0 to 100 priority score. Higher means the account deserves more senior review.
- Score weights live in `config/scoring_rules.yml`.
- Company thresholds live in `config/company_profile.yml`.
- Score explanations are written to `outputs/account_score_explanations.csv`.

Scores use visible account fields: activation status, days since close, activation deadline, customer sentiment, owner coverage, blockers, support tickets, usage signal, payment status, integration complexity, data migration complexity, training completion, renewal risk, and contract value.

The founder attention queue is not a black box. It combines risk, contract value, health, blocker severity, owner clarity, sentiment, renewal risk, and deadline pressure. The queue also includes `risk_reason`, `founder_action`, `owner`, `due_timing`, `expected_leverage`, and `escalation_note`.

See [docs/scoring-methodology.md](docs/scoring-methodology.md) for the full scoring explanation.

## Example founder workflow

- Monday: Review founder onboarding memo.
- Tuesday: Inspect founder attention queue.
- Wednesday: Unblock activation risks.
- Thursday: Update CRM or customer success tracker.
- Friday: Review process improvements and owner gaps.

## Customization guide

Customize `config/company_profile.yml` for:

- Activation definition
- Onboarding stages
- Risk thresholds
- Owner roles
- Escalation rules
- Review cadence
- Tools used by your team

Customize `config/scoring_rules.yml` for:

- Customer health weights
- Founder attention rules
- Onboarding risk weights
- Output thresholds

Customize `src/founder_customer_onboarding/reporting.py` if you want different output formats.

## Standalone or integrated

Standalone:
Use this repo by itself if you only need a post-sale onboarding control tower for activation risk, SLA issues, owner gaps, and founder attention accounts. Fork it, replace the sample input, run the workflow or copy the templates, and use the main output in your next founder review.

Integrated:
Use this repo with the Founder OS ecosystem if you want to connect it to adjacent operating workflows.

- Use after close-won.
- Feed onboarding risk into [founder-weekly-operating-review-agent](https://github.com/shubham1502-hue/founder-weekly-operating-review-agent).
- Feed activation or retention risks into [board-pack-investor-update-agent](https://github.com/shubham1502-hue/board-pack-investor-update-agent) when needed.
- Use [founder-ai-workflow-roi-os](https://github.com/shubham1502-hue/founder-ai-workflow-roi-os) if onboarding workflows become repetitive or ops-heavy.

## Lifecycle handoff

Before:

- [founder-led-sales-call-os](https://github.com/shubham1502-hue/founder-led-sales-call-os) for sales call context and deal risk.
- [founder-os-revenue-engine](https://github.com/shubham1502-hue/founder-os-revenue-engine) for close-won and funnel leakage context.
- [revops-infrastructure-playbook](https://github.com/shubham1502-hue/revops-infrastructure-playbook) for CRM handoffs and owner fields.

This repo produces:

- Onboarding health scorecard
- Founder attention queue
- SLA risk list
- Activation matrix
- Weekly onboarding memo

After:

- [founder-weekly-operating-review-agent](https://github.com/shubham1502-hue/founder-weekly-operating-review-agent) for weekly leadership review.
- [board-pack-investor-update-agent](https://github.com/shubham1502-hue/board-pack-investor-update-agent) when onboarding or activation risk needs investor narrative.
- [founder-ai-workflow-roi-os](https://github.com/shubham1502-hue/founder-ai-workflow-roi-os) when onboarding work should be automated, piloted, hired for, outsourced, or kept manual.

## Why this matters

This is not a customer success dashboard. It is a founder operating system for making sure closed-won customers become activated customers.

## Roadmap

- Google Sheets export
- Notion export
- Streamlit dashboard
- HubSpot integration
- Pipedrive integration
- Attio integration
- Salesforce integration
- Intercom or Zendesk support ticket import
- Slack escalation alerts
- Customer health trend tracking
- Renewal and expansion risk scoring

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT License. See [LICENSE](LICENSE).

## Built by

Built by Shubham Singh, a founder-facing operator focused on RevOps, GTM systems, startup metrics, AI workflows, and operating systems for early-stage teams.

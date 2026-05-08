# How to Fork and Use

This guide is written for non-technical founders and operators.

## 1. Fork the repo

Click Fork on GitHub. You can keep the repository name or rename it for your company.

## 2. Clone the repo

```bash
git clone https://github.com/YOUR-USERNAME/founder-customer-onboarding-os.git
cd founder-customer-onboarding-os
```

## 3. Install dependencies

```bash
make install
```

The base workflow uses Python, pandas, and PyYAML. It does not require paid APIs or an LLM.

## 4. Replace sample data

Open `data/sample_onboarding_accounts.csv`.

Replace the synthetic rows with your customer onboarding tracker. Keep the same column names. If your source tracker has more columns, you can keep them, but the required columns must remain.

Do not commit private customer data to a public repo.

## 5. Edit company config

Open `config/company_profile.yml`.

Update:

- Company name
- Target activation days
- Activation definition
- Onboarding stages
- High-value threshold
- Founder intervention threshold
- Owner roles
- Escalation rules
- Review cadence

## 6. Edit scoring rules if needed

Open `config/scoring_rules.yml`.

Most teams can start with the default weights. Adjust weights only if your onboarding model has a different risk profile. For example, implementation-heavy startups may increase integration and migration weights.

## 7. Run the repo

```bash
make run
```

## 8. Interpret outputs

Read these in order:

1. `outputs/founder_onboarding_memo.md`
2. `outputs/founder_attention_queue.csv`
3. `outputs/onboarding_sla_risks.csv`
4. `outputs/customer_activation_matrix.csv`
5. `outputs/onboarding_process_improvements.csv`

## 9. Use outputs in your operating rhythm

Bring the founder memo and attention queue to your weekly customer onboarding review. Assign owners and due dates. Update your CRM, customer success tracker, Notion workspace, Airtable base, HubSpot, Pipedrive, Attio, Salesforce, Linear, ClickUp, or Google Sheet after the meeting.


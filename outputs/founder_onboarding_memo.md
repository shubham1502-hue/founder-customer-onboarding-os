# Founder Onboarding Memo

## Data note

The bundled sample dataset and generated sample outputs are synthetic and fictionalized. Replace data/sample_onboarding_accounts.csv with your own private tracker before using this for company decisions.

## Executive summary

Demo Startup Customer Onboarding OS has 22 onboarding accounts in this review. 3 are activated, 11 are at risk or critical, and 8 need founder intervention now.

Read the founder attention queue first, then review SLA risks and process improvements.

Scores are deterministic. They use `config/scoring_rules.yml`, visible account fields, and rule-based risk detection. Review `outputs/account_score_explanations.csv` when you want the reason behind a score.

## Onboarding health snapshot

| customer_name | current_stage | customer_health_score | health_category | onboarding_risk_score | founder_attention_category |
| --- | --- | --- | --- | --- | --- |
| TerraWorks Energy | Kickoff complete | 41 | At risk | 62 | Founder intervention now |
| Riverline Logistics | Technical integration | 42 | At risk | 62 | Founder intervention now |
| Meridian Robotics | Technical integration | 44 | At risk | 60 | Founder intervention now |
| Prairie Foods Network | Activation review | 50 | At risk | 55 | Founder intervention now |
| Juniper BioTools | Activation review | 58 | At risk | 44 | Founder intervention now |
| Vertex Mining Analytics | Technical integration | 58 | At risk | 43 | Founder intervention now |
| DeltaOps Systems | Technical integration | 61 | Watch | 40 | Founder intervention now |
| Grove Robotics | Activation review | 70 | Watch | 32 | Founder intervention now |
| Northstar Legal Ops | Data migration | 48 | At risk | 54 | Owner follow-up |
| Kinetic Support Labs | Technical integration | 52 | At risk | 51 | Owner follow-up |

## Customers needing founder attention this week

| priority_rank | customer_name | contract_value | risk_reason | founder_action | due_timing |
| --- | --- | --- | --- | --- | --- |
| 1 | Meridian Robotics | 95000.0 | High-value account; Critical activation risk; At risk customer health; Integration blocked by security review | Founder sponsor call to reset trust and activation plan. | Today |
| 2 | TerraWorks Energy | 83000.0 | High-value account; Critical activation risk; At risk customer health; Partial owner gap | Assign owner coverage and review handoff quality. | Today |
| 3 | Riverline Logistics | 67000.0 | High-value account; Critical activation risk; At risk customer health; Payment failed and integration access withheld | Escalate technical unblock plan and confirm customer-side owner. | Today |
| 4 | Prairie Foods Network | 58000.0 | High-value account; Critical activation risk; At risk customer health; Customer questions ROI after delayed rollout | Founder sponsor call to reset trust and activation plan. | Today |
| 5 | Vertex Mining Analytics | 76000.0 | High-value account; Critical activation risk; At risk customer health; Product gap blocking activation | Review activation path and remove the highest leverage blocker. | Today |
| 6 | DeltaOps Systems | 72000.0 | High-value account; Critical activation risk; Integration stuck on customer API access; Risk | Escalate technical unblock plan and confirm customer-side owner. | Today |
| 7 | Grove Robotics | 64000.0 | High-value account; Critical activation risk; Stakeholder changed during activation; Risk | Review activation path and remove the highest leverage blocker. | Today |
| 8 | Juniper BioTools | 52000.0 | High-value account; Critical activation risk; At risk customer health; Unpaid invoice blocking rollout | Align finance and customer sponsor on payment path. | Today |
| 9 | Northstar Legal Ops | 9000.0 | Critical activation risk; At risk customer health; Data migration stuck with messy source files; Risk | Escalate technical unblock plan and confirm customer-side owner. | Next 3 business days |
| 10 | Quartz Education Group | 26000.0 | High activation risk; At risk customer health; Partial owner gap; Delayed handoff and stale touchpoint | Assign owner coverage and review handoff quality. | Next 3 business days |

## SLA and handoff risks

| customer_name | risk_type | severity | owner | recommended_fix |
| --- | --- | --- | --- | --- |
| Beacon Hiring Co | Delayed onboarding start | High | Riya Sen | Assign onboarding owner and schedule kickoff inside the handoff SLA. |
| Beacon Hiring Co | Unresolved blocker | Medium | Riya Sen | Convert blocker into a dated unblock plan with one accountable owner. |
| Beacon Hiring Co | Training incomplete | Medium | Riya Sen | Schedule training and confirm attendance from the customer owner. |
| Cloudforge Labs | Delayed onboarding start | High | Unassigned | Assign onboarding owner and schedule kickoff inside the handoff SLA. |
| Cloudforge Labs | Stale customer touchpoint | High | Unassigned | Create a customer touchpoint today and document the next action. |
| Cloudforge Labs | Missing owner | High | Unassigned | Assign onboarding, customer success, and implementation owners. |
| Cloudforge Labs | Unclear next step | Medium | Unassigned | Replace vague next step with a dated owner-backed action. |
| Cloudforge Labs | Unresolved blocker | Medium | Unassigned | Convert blocker into a dated unblock plan with one accountable owner. |
| Cloudforge Labs | Training incomplete | Medium | Unassigned | Schedule training and confirm attendance from the customer owner. |
| DeltaOps Systems | Unresolved blocker | High | Anika Menon | Convert blocker into a dated unblock plan with one accountable owner. |
| DeltaOps Systems | Integration stuck | High | Anika Menon | Create technical unblock plan with implementation and product owner. |
| Evergreen Clinic Group | Unresolved blocker | High | Isha Das | Convert blocker into a dated unblock plan with one accountable owner. |

## Activation bottlenecks

| customer_name | current_stage | activation_gap | recommended_activation_move |
| --- | --- | --- | --- |
| Beacon Hiring Co | Kickoff scheduled | Training not complete | Schedule training and confirm attendance. |
| Cloudforge Labs | Closed won | Training not complete | Schedule training and confirm attendance. |
| DeltaOps Systems | Technical integration | Integration not complete | Run integration unblock session with technical owner. |
| Evergreen Clinic Group | Data migration | Data migration not complete | Confirm source data owner and migration checklist. |
| Finley Finance Studio | Kickoff complete | Training not complete | Schedule training and confirm attendance. |
| Grove Robotics | Activation review | Customer engagement risk | Re-engage customer stakeholder and confirm priority. |
| Horizon Analytics | Training | Missing activation criteria | Define activation criteria with customer sponsor. |
| Ivory Desk Software | Training | Training not complete | Schedule training and confirm attendance. |
| Juniper BioTools | Activation review | Customer engagement risk | Re-engage customer stakeholder and confirm priority. |
| Kinetic Support Labs | Technical integration | Integration not complete | Run integration unblock session with technical owner. |
| Meridian Robotics | Technical integration | Integration not complete | Run integration unblock session with technical owner. |
| Northstar Legal Ops | Data migration | Data migration not complete | Confirm source data owner and migration checklist. |

## Owner gaps

| customer_name | current_stage | owner_coverage_status | recommended_next_action |
| --- | --- | --- | --- |
| Cloudforge Labs | Closed won | No owner assigned | Assign accountable owners before the next customer step. |
| Quartz Education Group | Kickoff scheduled | Partial owner gap | Assign accountable owners before the next customer step. |
| TerraWorks Energy | Kickoff complete | Partial owner gap | Assign accountable owners before the next customer step. |

## High-value accounts at risk

| customer_name | contract_value | current_stage | activation_risk_level | recommended_next_action |
| --- | --- | --- | --- | --- |
| Meridian Robotics | 95000.0 | Technical integration | Critical | Founder should contact the executive sponsor and reset the activation path. |
| Prairie Foods Network | 58000.0 | Activation review | Critical | Founder should contact the executive sponsor and reset the activation path. |
| Riverline Logistics | 67000.0 | Technical integration | Critical | Founder should contact the executive sponsor and reset the activation path. |
| TerraWorks Energy | 83000.0 | Kickoff complete | Critical | Assign accountable owners before the next customer step. |

## Process improvements to make this week

| improvement_id | process_issue | count | suggested_fix | owner_role |
| --- | --- | --- | --- | --- |
| OI-001 | Closed-won to onboarding handoff is missing SLA discipline. | 3 | Create a same-day closed-won handoff checklist and kickoff scheduling rule. | Head of CS |
| OI-002 | Blockers are recorded but not converted into unblock plans. | 19 | Turn every blocker into owner, due date, and escalation path. | Implementation Lead |
| OI-003 | Training completion is inconsistent. | 7 | Make training a tracked activation milestone with customer attendance. | Onboarding Lead |
| OI-004 | Customer communication is going stale during onboarding. | 9 | Add a weekly customer touchpoint SLA and stale-account review. | Customer Success Lead |
| OI-005 | Owner coverage is unclear across onboarding, CS, and implementation. | 3 | Require named owners before kickoff and during every stage change. | Founder or BizOps |
| OI-006 | Next steps are too vague to manage. | 1 | Require every account to have a dated next action with one owner. | Onboarding Lead |
| OI-007 | Technical integration blockers are slowing activation. | 5 | Create integration runbook with customer technical owner and internal owner. | Implementation Lead |
| OI-008 | Data migration ownership and source data readiness are weak. | 3 | Use a migration readiness checklist before kickoff. | Implementation Lead |
| OI-009 | Accounts are not converting onboarding activity into product usage. | 4 | Tie activation criteria to usage evidence and run adoption recovery. | Customer Success Lead |
| OI-010 | Activation dates are slipping without earlier intervention. | 9 | Review accounts 7 days before target activation and reset milestone plans. | Onboarding Lead |

## Recommended next 7-day actions

1. Review every account in the founder attention queue and confirm owner, customer step, and due date.
2. Fix missing owners before discussing lower-priority workflow improvements.
3. Reset missed activation dates with customer-facing milestones.
4. Run unblock sessions for integration, data migration, payment, and training risks.
5. Update the CRM or customer success tracker with current stage, next step, and activation evidence.

# KP EPI Data Quality Dashboard - Peshawar
**DHIS2 Portfolio Project for UNICEF Health Officer NO-1, Islamabad**
Author: Dr. Syed Rashid Mansoor, MBBS KMC 2025 | Health Systems QA (3.8 yrs)

## Objective
Build a DHIS2-based monitoring tool to track Penta-3 immunization coverage across BHUs in Peshawar District, flag facilities below UNICEF 80% target, and correlate data quality (completeness/timeliness) with performance — exactly as described in UNICEF Health Officer JD.

## Why This Matters for UNICEF
- UNICEF JD: "Support data collection, analysis, and monitoring through HMIS/DHIS2"
- My background: Led QA for 20+ staff, audited 5000+ clinical records, developed 4 SOPs, reduced errors 32%
- Translation: Same QA skills applied from US RCM (eClinicalWorks) to PK EPI data

## Dashboard Preview
| Facility | Penta3 Coverage | Data Completeness | Timeliness | Status | Action |
|----------|----------------|-------------------|------------|--------|--------|
| BHU Phandu | 78% | 85% | 3/4 | BELOW TARGET | Supportive Supervision |
| BHU Tehkal | 92% | 98% | 4/4 | MEETING TARGET | - |
| RHC Chamkani | 65% | 70% | 2/4 | BELOW - Critical | Urgent: Stock + Training |
| BHU Hayatabad | 88% | 95% | 4/4 | MEETING TARGET | - |
| THQ Mathra | 71% | 80% | 3/4 | BELOW TARGET | Supportive Supervision |
| BHU University | 95% | 100% | 4/4 | MEETING TARGET | Model Facility |

**Finding:** 3/6 facilities below 80% UNICEF target. Lowest (RHC Chamkani 65%) correlates with 70% completeness — suggests both supply and reporting issue.

## Features
- [x] DHIS2 API integration (`dhis2.py`) — connect to play.dhis2.org demo
- [x] Fallback mock data for Peshawar BHUs when offline
- [x] Automated flagging <80% coverage (UNICEF standard)
- [x] Priority score for field visit: `Priority = (80-Coverage) + 0.3*(100-Completeness)`
- [x] Export: `flagged_facilities_for_supervision.csv` for district action plan
- [x] Visuals: Coverage vs Target + Data Quality vs Performance scatter

## Tech Stack
Python, pandas, matplotlib, dhis2.py, HMIS concepts (orgUnit, dataElement, analytics)

## How to Run
```bash
pip install -r requirements.txt
python main.py
# Output: dashboard.png + flagged_facilities_for_supervision.csv
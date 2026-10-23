# The Algorithmic Mirror

A Streamlit dashboard for exploring potential hiring disparities in the included AI hiring dataset. It presents descriptive comparisons of hiring outcomes by gender, education and university tier, and employment-gap length.

## Features

- **The Prologue:** Introduces the hiring-audit scenario.
- **Act I — The Parity Paradox:** Compares hiring rates by gender and calculates each group's impact ratio relative to the group with the highest hiring rate. Ratios below 80% are flagged as potential adverse impact.
- **Act II — Credentials & Expectations:** Visualizes average expected salary and hiring rate by education level and university tier.
- **Act III — The Career Break Penalty:** Compares hiring rates across employment-gap groups.
- **Key Takeaways:** Presents suggested areas to investigate, including career-gap penalties, university-tier weighting, and selection outcomes.

The app also groups experience, employment gaps, and expected salaries into descriptive ranges, flags outliers in those fields, and marks candidates in the top quartile of technical skill.

## Requirements

- Python 3.10 or newer
- The included `AI_Hiring_Bias_Dataset.csv` file

## Setup and run

Open PowerShell in the project folder and run:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install streamlit pandas numpy plotly
python -m streamlit run app.py
```

Streamlit prints a local URL (usually `http://localhost:8501`) to open in your browser. If PowerShell does not allow activating the virtual environment, run the environment's Python directly:

```powershell
.\.venv\Scripts\python.exe -m pip install streamlit pandas numpy plotly
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Run the command from the project folder, or ensure the CSV remains next to `app.py`. The app resolves the dataset path relative to the script.

## Dataset

The dashboard reads `AI_Hiring_Bias_Dataset.csv`. The columns used by its analyses are:

| Column | Used for |
| --- | --- |
| `gender` | Grouping hiring outcomes for the 80% impact-ratio comparison |
| `hired` | Hiring outcome; expected to be `1` for hired and `0` otherwise |
| `education_level`, `university_tier` | Grouping expected salary and hiring outcomes |
| `expected_salary` | Salary averages and descriptive salary ranges |
| `employment_gap_months` | Career-gap groups and hiring-rate comparison |
| `years_experience` | Experience groups |
| `technical_skill_score` | Top-quartile performer flag |

The app calculates the gender impact ratio as a group's hiring rate divided by the highest observed group hiring rate. A ratio below 80% is shown as a potential adverse-impact flag; it is an audit signal, not by itself a legal determination or explanation of cause.

## Interpreting results

These charts show associations in the supplied dataset. They do not establish that a demographic characteristic or career gap caused a hiring outcome, nor do they validate the underlying screening model. Review data quality, group sizes, selection criteria, and applicable legal requirements before drawing conclusions. The narrative examples in the dashboard are written into the app and may need updating if you replace the dataset.

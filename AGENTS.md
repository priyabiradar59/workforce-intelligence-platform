# AI Agent Instructions — Workforce Intelligence Platform

## Project Overview
End-to-end People Analytics project: predictive employee attrition modeling with an interactive Streamlit dashboard. Built to demonstrate Python, SQL, ML, and data visualization skills for a Data Analyst / HR Analyst portfolio.

## Tech Stack
- **Language**: Python 3.11+
- **Data**: Pandas, NumPy, SQLAlchemy
- **Visualization**: Plotly, Seaborn, Matplotlib
- **Dashboard**: Streamlit
- **Database**: SQLite (local dev), SQL scripts in `sql/`
- **Notebooks**: Jupyter (EDA and experimentation)

## Project Structure
```
data/raw/          — Original datasets (CSV). Never modify raw data.
data/processed/    — Cleaned/transformed data ready for modeling
notebooks/         — Jupyter notebooks for EDA, feature engineering, modeling
src/               — Python modules (data processing, model training, utils)
sql/               — SQL scripts (schema creation, queries, analysis)
dashboard/         — Streamlit app files
tests/             — Unit tests for src/ modules
docs/              — Documentation and analysis reports
```

## Conventions
- Use snake_case for all Python files, functions, and variables
- Every notebook must have a numbered prefix: `01_eda.ipynb`, `02_feature_engineering.ipynb`
- SQL files use lowercase with underscores: `create_tables.sql`, `attrition_analysis.sql`
- Data pipeline: raw → cleaned → feature-engineered → model-ready
- All plots must have titles, axis labels, and legends
- Use f-strings for string formatting
- Type hints for all function signatures in `src/`

## Key Commands
```bash
# Install dependencies
pip install -r requirements.txt

# Run Streamlit dashboard
streamlit run dashboard/app.py

# Run tests
pytest tests/

# Run data pipeline
python src/pipeline.py
```

## Dataset
Using IBM HR Analytics Employee Attrition dataset (1,470 records, 35 features).
Download: https://www.kaggle.com/datasets/pavansubhasht/ibm-hr-analytics-attrition-dataset

## Development Workflow
1. EDA in notebooks → discover patterns
2. Build reusable functions in `src/`
3. SQL queries for database-style analysis
4. Build Streamlit dashboard for interactive visualization
5. Write tests for critical functions

## Dashboard Requirements
- KPI cards: attrition rate, avg tenure, satisfaction score
- Filters: department, job role, age group, overtime
- Charts: attrition by department, salary vs attrition, overtime impact
- Data explorer tab with download capability
- Must be deployable to Streamlit Cloud

## What Makes This Project Stand Out
- Interactive deployed dashboard (live URL for interviews)
- SQL + Python + Visualization in one project
- Advanced SQL queries (Window Functions, CTEs, CASE WHEN)
- Domain expertise from real HR analytics experience at Goldman Sachs
- Clean code structure with tests (shows software engineering maturity)

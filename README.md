# 📊 Workforce Intelligence Platform

### People Analytics Dashboard — Employee Attrition Analysis

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![SQL](https://img.shields.io/badge/SQL-SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](https://sqlite.org)
[![Pandas](https://img.shields.io/badge/Pandas-Data_Analysis-150458?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org)
[![Plotly](https://img.shields.io/badge/Plotly-Visualization-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)](https://plotly.com)

---

## 🎯 Problem Statement

Employee attrition costs companies **50-200% of an employee's annual salary**. This project analyzes 1,470 employee records across 35 HR metrics to uncover **why employees leave** and provides an interactive dashboard for data-driven retention strategies.

---

## 🔑 Key Findings

| Insight | Detail |
|---------|--------|
| **Overall Attrition Rate** | 16.1% (237 of 1,470 employees) |
| **#1 Driver** | Overtime — 3x higher attrition for OT workers |
| **Highest Risk Dept** | Sales — 20.6% attrition rate |
| **Income Gap** | Leavers earn $2,000+ less than stayers |
| **Critical Window** | First 2 years = highest attrition period |
| **Demographics** | Single employees leave 2x more than married |

---

## 🏗️ Architecture

```
Raw Data (CSV) → Data Cleaning → SQLite Database → Analysis & Visualization
                      ↓                                    ↓
              Processed CSVs                    Streamlit Dashboard
                      ↓                                    ↓
              Power BI / Tableau Exports         Interactive Charts & SQL
```

---

## 🖥️ Dashboard Preview

The interactive Streamlit dashboard includes:

| Tab | Features |
|-----|----------|
| 📈 **Overview & KPIs** | 6 KPI cards, department analysis, attrition distribution |
| 🗄️ **SQL Analysis** | 5 live SQL queries (Window Functions, CTEs, CASE WHEN) + custom query runner |
| 🐍 **Python Stats** | Descriptive stats, correlations, pivot tables, distributions |
| 📊 **Visual Deep Dive** | Heatmaps, box plots, overtime/satisfaction impact |
| 🔄 **Cross Analysis** | Dynamic chart builder, scatter plots with hover data |
| 📋 **Data Explorer** | Search, sort, filter, download CSV |

---

## 🛠️ Tech Stack

| Category | Tools |
|----------|-------|
| **Programming** | Python 3.11, SQL |
| **Data Processing** | Pandas, NumPy, SQLAlchemy |
| **Visualization** | Plotly, Seaborn, Matplotlib |
| **Dashboard** | Streamlit (responsive, mobile-friendly) |
| **Database** | SQLite |
| **BI Export** | Power BI (.xlsx), Tableau (.csv) |
| **Testing** | pytest (16 tests) |
| **Version Control** | Git, GitHub |

---

## 🚀 Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/Rohitmengji/workforce-intelligence-platform.git
cd workforce-intelligence-platform

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the data pipeline (creates database + processed files)
python src/pipeline.py

# 4. Start the dashboard
streamlit run dashboard/app.py
```

---

## 📁 Project Structure

```
├── dashboard/
│   └── app.py                    # Streamlit dashboard (responsive, 6 tabs)
├── notebooks/
│   └── 01_eda.ipynb              # Exploratory Data Analysis (fully executed)
├── src/
│   ├── data_loader.py            # Data ingestion & validation
│   ├── preprocessor.py           # Data cleaning & encoding
│   ├── database.py               # SQLite database creation
│   ├── pipeline.py               # End-to-end data pipeline
│   └── export_for_bi.py          # Power BI & Tableau export
├── sql/
│   ├── create_tables.sql         # Database schema with indexing
│   └── attrition_analysis.sql    # 8 advanced SQL queries
├── data/
│   ├── raw/                      # Original IBM HR dataset
│   ├── processed/                # Cleaned & encoded data
│   ├── exports/                  # Power BI (.xlsx) & Tableau (.csv)
│   └── hr_analytics.db           # SQLite database
├── tests/
│   ├── test_data_loader.py       # 10 data validation tests
│   └── test_preprocessor.py      # 6 preprocessing tests
├── .streamlit/config.toml        # Dashboard theme config
├── requirements.txt              # Python dependencies
└── AGENTS.md                     # AI agent instructions
```

---

## 📊 SQL Skills Demonstrated

The `sql/attrition_analysis.sql` file contains 8 advanced queries:

| # | Query | SQL Concepts |
|---|-------|-------------|
| 1 | Overall Attrition Rate | `COUNT`, `GROUP BY`, `ROUND` |
| 2 | Department Breakdown | `CASE WHEN`, multiple aggregations |
| 3 | Salary Ranking | `RANK() OVER`, `PARTITION BY` (Window Functions) |
| 4 | High-Risk Profile | `WITH` clause (CTE), `JOIN`, subqueries |
| 5 | Risk Bucketing | Nested `CASE WHEN`, conditional logic |
| 6 | Cumulative Analysis | `SUM() OVER` (Running Total) |
| 7 | Underpaid Employees | Correlated subquery |
| 8 | Dashboard KPI Query | Multiple `CASE WHEN` aggregations |

---

## 🐍 Python Skills Demonstrated

| Skill | Where Used |
|-------|-----------|
| **Pandas** (groupby, pivot_table, merge, apply) | All src/ modules |
| **Data Cleaning** (encoding, null handling, validation) | `src/preprocessor.py` |
| **Statistical Analysis** (describe, corr, distributions) | Dashboard Tab 3 |
| **Visualization** (Plotly, Seaborn, Matplotlib) | Notebook + Dashboard |
| **Database Integration** (SQLAlchemy, pd.read_sql) | `src/database.py` |
| **Modular Code** (functions, type hints, docstrings) | All src/ files |
| **Unit Testing** (pytest, assertions, test classes) | `tests/` |
| **Data Pipeline** (ETL: Extract, Transform, Load) | `src/pipeline.py` |

---

## 📈 Key Visualizations (from EDA Notebook)

1. **Attrition Distribution** — Pie + Bar chart showing 16.1% overall rate
2. **Department Comparison** — Sales has 20.6% attrition (highest)
3. **Income Analysis** — Violin plot: leavers earn significantly less
4. **Overtime Impact** — 3x higher attrition for OT employees
5. **Age & Tenure Patterns** — Young employees (18-25) at highest risk
6. **Correlation Heatmap** — Feature relationships with attrition
7. **Satisfaction Matrix** — Heatmap of job × environment satisfaction
8. **Marital Status** — Single employees: 2x attrition vs married

---

## 🏃 Commands Reference

| Command | Description |
|---------|-------------|
| `streamlit run dashboard/app.py` | Start interactive dashboard |
| `python src/pipeline.py` | Run full ETL pipeline |
| `python src/database.py` | Create/refresh SQLite database |
| `python src/export_for_bi.py` | Generate Power BI & Tableau files |
| `pytest tests/ -v` | Run all 16 unit tests |

---

## 📋 Dataset

**IBM HR Analytics Employee Attrition Dataset**
- **Source**: [Kaggle](https://www.kaggle.com/datasets/pavansubhasht/ibm-hr-analytics-attrition-dataset)
- **Records**: 1,470 employees
- **Features**: 35 (demographics, job details, satisfaction, compensation)
- **Target**: Attrition (Yes/No)

---

## 👩‍💻 Author

**Priyanka S Biradar**  
HR Analyst @ Goldman Sachs → Aspiring Data Analyst  
3.8 years experience | SQL • Python • Tableau • Power BI • Advanced Excel

[![GitHub](https://img.shields.io/badge/GitHub-priyabiradar59-181717?style=flat&logo=github)](https://github.com/priyabiradar59)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=flat&logo=linkedin)](https://linkedin.com/in/priyabiradar59)

---

## 📜 License

This project is licensed under the MIT License — free to use, modify, and distribute.

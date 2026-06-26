# Workforce Intelligence Platform
### Predictive People Analytics & Interactive Dashboard

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app-url.streamlit.app)
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 🎯 Problem Statement

Employee attrition costs companies 50-200% of an employee's annual salary. This project builds a **predictive analytics system** that identifies at-risk employees *before* they leave, enabling proactive retention strategies.

## 🔑 Key Results

| Metric | Value |
|--------|-------|
| Model Accuracy | ~87% |
| Top Attrition Driver | Overtime + Low Satisfaction |
| Highest Risk Department | Sales (21% attrition) |
| Potential Savings | $2.3M annually (for 1,000-person org) |

## 🏗️ Architecture

```
Raw Data (CSV/SQL) → Data Cleaning → Feature Engineering → ML Model → Streamlit Dashboard
                                                              ↓
                                                    Predictions API
```

## 📊 Features

- **Exploratory Data Analysis**: 35+ HR metrics analyzed across 1,470 employees
- **Predictive Model**: Random Forest classifier with 87%+ accuracy
- **Feature Importance**: Identifies top 10 drivers of attrition
- **Interactive Dashboard**: Real-time risk scoring with Streamlit
- **SQL Analysis**: Complex queries demonstrating joins, window functions, CTEs
- **Actionable Insights**: Retention recommendations based on model output

## 🛠️ Tech Stack

| Category | Tools |
|----------|-------|
| Programming | Python 3.11, SQL |
| Data Processing | Pandas, NumPy, SQLAlchemy |
| Machine Learning | scikit-learn (Random Forest, Logistic Regression, XGBoost) |
| Visualization | Plotly, Seaborn, Matplotlib |
| Dashboard | Streamlit |
| Database | SQLite |
| Version Control | Git, GitHub |

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/priyabiradar59/workforce-intelligence-platform.git
cd workforce-intelligence-platform

# Install dependencies
pip install -r requirements.txt

# Run the dashboard
streamlit run dashboard/app.py
```

## 📁 Project Structure

```
├── data/
│   ├── raw/                 # Original IBM HR dataset
│   └── processed/           # Cleaned & feature-engineered data
├── notebooks/
│   ├── 01_eda.ipynb         # Exploratory Data Analysis
│   ├── 02_feature_eng.ipynb # Feature Engineering
│   └── 03_modeling.ipynb    # Model Training & Evaluation
├── src/
│   ├── data_loader.py       # Data ingestion utilities
│   ├── preprocessor.py      # Data cleaning & transformation
│   ├── feature_engineer.py  # Feature creation
│   ├── model.py             # Model training & prediction
│   └── pipeline.py          # End-to-end pipeline
├── sql/
│   ├── create_tables.sql    # Database schema
│   └── analysis_queries.sql # Analytical SQL queries
├── dashboard/
│   └── app.py               # Streamlit application
├── tests/                   # Unit tests
├── requirements.txt
└── README.md
```

## 📈 Sample Insights

### Attrition by Department
- Sales: 21% attrition rate (highest)
- R&D: 14% attrition rate
- HR: 19% attrition rate

### Key Predictors (Feature Importance)
1. Monthly Income
2. Overtime (Yes/No)
3. Age
4. Years at Company
5. Job Satisfaction

## 👩‍💻 Author

**Priyanka S Biradar**  
HR Analyst → Data Analyst | Goldman Sachs  
[GitHub](https://github.com/priyabiradar59) | [LinkedIn](https://linkedin.com/in/priyabiradar59)

---

## 📜 License

This project is licensed under the MIT License.

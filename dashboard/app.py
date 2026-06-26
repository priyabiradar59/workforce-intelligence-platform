# ============================================================================
# dashboard/app.py — Responsive Interactive HR Analytics Dashboard
# ============================================================================
# FEATURES:
#   - Fully responsive (works on mobile, tablet, desktop)
#   - KPI cards with dynamic metrics
#   - SQL-powered analysis (live queries against SQLite)
#   - Python statistical analysis (correlations, distributions)
#   - Interactive filters and cross-filtering
#   - Downloadable reports
#   - Professional styling
# ============================================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pathlib import Path
from sqlalchemy import create_engine

# ============================================================================
# PAGE CONFIG
# ============================================================================
st.set_page_config(
    page_title="Workforce Intelligence Platform",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"  # Collapsed by default for mobile
)

# ============================================================================
# RESPONSIVE CSS — Makes UI work on all screen sizes
# ============================================================================
st.markdown("""
<style>
    /* ===== RESPONSIVE DESIGN ===== */
    
    /* Mobile-first: base styles for small screens */
    .main .block-container {
        padding: 1rem 1rem;
        max-width: 100%;
    }
    
    /* KPI Card styling */
    .kpi-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 12px;
        padding: 1.2rem;
        text-align: center;
        color: white;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin-bottom: 0.8rem;
        transition: transform 0.2s;
    }
    .kpi-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.15);
    }
    .kpi-value {
        font-size: clamp(1.5rem, 4vw, 2.2rem);
        font-weight: 700;
        margin: 0;
    }
    .kpi-label {
        font-size: clamp(0.75rem, 2vw, 0.9rem);
        opacity: 0.9;
        margin: 0;
    }
    
    /* Different card colors */
    .kpi-red { background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%); }
    .kpi-green { background: linear-gradient(135deg, #2ecc71 0%, #27ae60 100%); }
    .kpi-blue { background: linear-gradient(135deg, #3498db 0%, #2980b9 100%); }
    .kpi-orange { background: linear-gradient(135deg, #f39c12 0%, #e67e22 100%); }
    .kpi-purple { background: linear-gradient(135deg, #9b59b6 0%, #8e44ad 100%); }
    .kpi-teal { background: linear-gradient(135deg, #1abc9c 0%, #16a085 100%); }
    
    /* Section headers */
    .section-header {
        font-size: clamp(1.2rem, 3vw, 1.6rem);
        font-weight: 700;
        color: #2c3e50;
        border-bottom: 3px solid #3498db;
        padding-bottom: 0.5rem;
        margin: 1.5rem 0 1rem 0;
    }
    
    /* Insight boxes */
    .insight-box {
        background: #f8f9fa;
        border-left: 4px solid #3498db;
        padding: 1rem;
        border-radius: 0 8px 8px 0;
        margin: 0.8rem 0;
        font-size: clamp(0.85rem, 2vw, 1rem);
    }
    .insight-box-warning {
        border-left-color: #e74c3c;
        background: #fdf2f2;
    }
    .insight-box-success {
        border-left-color: #2ecc71;
        background: #f0fdf4;
    }
    
    /* SQL code display */
    .sql-box {
        background: #1e1e1e;
        color: #d4d4d4;
        padding: 1rem;
        border-radius: 8px;
        font-family: 'Courier New', monospace;
        font-size: clamp(0.7rem, 1.5vw, 0.85rem);
        overflow-x: auto;
        white-space: pre-wrap;
        word-wrap: break-word;
    }
    
    /* Tablet: 768px+ */
    @media (min-width: 768px) {
        .main .block-container {
            padding: 2rem 2rem;
        }
    }
    
    /* Desktop: 1024px+ */
    @media (min-width: 1024px) {
        .main .block-container {
            padding: 2rem 3rem;
        }
    }
    
    /* Hide Streamlit branding for cleaner look */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Make dataframes scroll horizontally on mobile */
    .stDataFrame {
        overflow-x: auto;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        flex-wrap: wrap;
    }
    .stTabs [data-baseweb="tab"] {
        font-size: clamp(0.8rem, 2vw, 1rem);
        padding: 0.5rem 1rem;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# DATA LOADING
# ============================================================================

@st.cache_data
def load_data():
    """Load raw CSV data."""
    data_path = Path(__file__).parent.parent / "data" / "raw" / "hr_employee_attrition.csv"
    return pd.read_csv(data_path)

@st.cache_data
def run_sql_query(query):
    """Run a SQL query against the SQLite database."""
    db_path = Path(__file__).parent.parent / "data" / "hr_analytics.db"
    if not db_path.exists():
        return None
    engine = create_engine(f"sqlite:///{db_path}")
    return pd.read_sql(query, engine)

df = load_data()

# ============================================================================
# SIDEBAR — Responsive Filters
# ============================================================================

with st.sidebar:
    st.title("🎯 Filters")
    st.markdown("---")
    
    # Department
    departments = ['All'] + sorted(df['Department'].unique().tolist())
    selected_dept = st.selectbox("🏢 Department", departments)
    
    # Job Role
    if selected_dept != 'All':
        roles = ['All'] + sorted(df[df['Department'] == selected_dept]['JobRole'].unique().tolist())
    else:
        roles = ['All'] + sorted(df['JobRole'].unique().tolist())
    selected_role = st.selectbox("💼 Job Role", roles)
    
    # Age range
    age_range = st.slider("👤 Age Range", 18, 60, (18, 60))
    
    # Overtime
    overtime_filter = st.selectbox("⏰ Overtime", ['All', 'Yes', 'No'])
    
    # Marital Status
    marital_filter = st.selectbox("💍 Marital Status", ['All', 'Single', 'Married', 'Divorced'])
    
    # Gender
    gender_filter = st.selectbox("⚧ Gender", ['All', 'Male', 'Female'])
    
    # Income range
    income_range = st.slider(
        "💰 Monthly Income",
        int(df['MonthlyIncome'].min()),
        int(df['MonthlyIncome'].max()),
        (int(df['MonthlyIncome'].min()), int(df['MonthlyIncome'].max()))
    )
    
    st.markdown("---")
    st.markdown(f"**Active filters**: {sum([selected_dept!='All', selected_role!='All', overtime_filter!='All', marital_filter!='All', gender_filter!='All'])}")

# Apply all filters
filtered_df = df.copy()
if selected_dept != 'All':
    filtered_df = filtered_df[filtered_df['Department'] == selected_dept]
if selected_role != 'All':
    filtered_df = filtered_df[filtered_df['JobRole'] == selected_role]
if overtime_filter != 'All':
    filtered_df = filtered_df[filtered_df['OverTime'] == overtime_filter]
if marital_filter != 'All':
    filtered_df = filtered_df[filtered_df['MaritalStatus'] == marital_filter]
if gender_filter != 'All':
    filtered_df = filtered_df[filtered_df['Gender'] == gender_filter]
filtered_df = filtered_df[
    (filtered_df['Age'] >= age_range[0]) & (filtered_df['Age'] <= age_range[1]) &
    (filtered_df['MonthlyIncome'] >= income_range[0]) & (filtered_df['MonthlyIncome'] <= income_range[1])
]

# ============================================================================
# HEADER
# ============================================================================

st.markdown("""
<h1 style='text-align: center; font-size: clamp(1.5rem, 5vw, 2.5rem); color: #2c3e50;'>
    📊 Workforce Intelligence Platform
</h1>
<p style='text-align: center; color: #7f8c8d; font-size: clamp(0.9rem, 2.5vw, 1.1rem); margin-bottom: 1rem;'>
    People Analytics Dashboard — Employee Attrition Insights | Powered by Python & SQL
</p>
""", unsafe_allow_html=True)

# Show filter status
if len(filtered_df) < len(df):
    st.info(f"📋 Showing **{len(filtered_df):,}** of {len(df):,} employees (filters active)")

# ============================================================================
# KPI CARDS — Responsive Grid
# ============================================================================

total = len(filtered_df)
attrition_count = (filtered_df['Attrition'] == 'Yes').sum()
attrition_rate = attrition_count / total * 100 if total > 0 else 0
avg_income = filtered_df['MonthlyIncome'].mean() if total > 0 else 0
avg_satisfaction = filtered_df['JobSatisfaction'].mean() if total > 0 else 0
avg_tenure = filtered_df['YearsAtCompany'].mean() if total > 0 else 0
overtime_pct = (filtered_df['OverTime'] == 'Yes').sum() / total * 100 if total > 0 else 0

col1, col2, col3 = st.columns(3)
col4, col5, col6 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="kpi-card kpi-blue">
        <p class="kpi-value">{total:,}</p>
        <p class="kpi-label">👥 Total Employees</p>
    </div>""", unsafe_allow_html=True)

with col2:
    color_class = "kpi-red" if attrition_rate > 16 else "kpi-green"
    st.markdown(f"""
    <div class="kpi-card {color_class}">
        <p class="kpi-value">{attrition_rate:.1f}%</p>
        <p class="kpi-label">🚪 Attrition Rate</p>
    </div>""", unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="kpi-card kpi-green">
        <p class="kpi-value">${avg_income:,.0f}</p>
        <p class="kpi-label">💰 Avg Monthly Income</p>
    </div>""", unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="kpi-card kpi-orange">
        <p class="kpi-value">{avg_satisfaction:.2f}/4</p>
        <p class="kpi-label">😊 Avg Job Satisfaction</p>
    </div>""", unsafe_allow_html=True)

with col5:
    st.markdown(f"""
    <div class="kpi-card kpi-purple">
        <p class="kpi-value">{avg_tenure:.1f} yrs</p>
        <p class="kpi-label">⏰ Avg Tenure</p>
    </div>""", unsafe_allow_html=True)

with col6:
    ot_class = "kpi-red" if overtime_pct > 30 else "kpi-teal"
    st.markdown(f"""
    <div class="kpi-card {ot_class}">
        <p class="kpi-value">{overtime_pct:.1f}%</p>
        <p class="kpi-label">⏰ Overtime Rate</p>
    </div>""", unsafe_allow_html=True)

st.markdown("---")

# ============================================================================
# TABS — All Analysis Sections
# ============================================================================

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📈 Overview",
    "🗄️ SQL Analysis",
    "🐍 Python Stats",
    "📊 Visual Deep Dive",
    "🔄 Cross Analysis",
    "📋 Data Explorer"
])

# ============================================================================
# TAB 1: OVERVIEW — Department & Role Analysis
# ============================================================================
with tab1:
    st.markdown('<div class="section-header">Department & Role Overview</div>', unsafe_allow_html=True)
    
    col_left, col_right = st.columns(2)
    
    with col_left:
        dept_rate = filtered_df.groupby('Department')['Attrition'].apply(
            lambda x: (x == 'Yes').sum() / len(x) * 100
        ).reset_index()
        dept_rate.columns = ['Department', 'Attrition_Rate']
        
        fig = px.bar(
            dept_rate, x='Department', y='Attrition_Rate',
            title='<b>Attrition Rate by Department</b>',
            color='Attrition_Rate', color_continuous_scale='RdYlGn_r',
            text=dept_rate['Attrition_Rate'].round(1).astype(str) + '%'
        )
        fig.add_hline(y=16.1, line_dash="dash", line_color="red",
                     annotation_text="Avg 16.1%")
        fig.update_layout(height=400, margin=dict(l=20, r=20, t=50, b=20))
        fig.update_traces(textposition='outside')
        st.plotly_chart(fig, width="stretch")
    
    with col_right:
        role_data = filtered_df.groupby('JobRole')['Attrition'].apply(
            lambda x: (x == 'Yes').sum() / len(x) * 100
        ).reset_index()
        role_data.columns = ['JobRole', 'Attrition_Rate']
        role_data = role_data.sort_values('Attrition_Rate', ascending=True)
        
        fig = px.bar(
            role_data, x='Attrition_Rate', y='JobRole',
            title='<b>Attrition Rate by Job Role</b>',
            orientation='h', color='Attrition_Rate',
            color_continuous_scale='RdYlGn_r'
        )
        fig.update_layout(height=400, margin=dict(l=20, r=20, t=50, b=20))
        st.plotly_chart(fig, width="stretch")
    
    # Insight box
    highest_dept = dept_rate.loc[dept_rate['Attrition_Rate'].idxmax()]
    st.markdown(f"""
    <div class="insight-box insight-box-warning">
        <b>🔍 Key Insight:</b> {highest_dept['Department']} department has the highest attrition 
        at <b>{highest_dept['Attrition_Rate']:.1f}%</b>. This exceeds the company average by 
        {highest_dept['Attrition_Rate'] - 16.1:.1f} percentage points.
    </div>""", unsafe_allow_html=True)

# ============================================================================
# TAB 2: SQL ANALYSIS — Live Queries with Results
# ============================================================================
with tab2:
    st.markdown('<div class="section-header">SQL-Powered Analysis (Live Queries)</div>', unsafe_allow_html=True)
    st.markdown("These queries run **live** against our SQLite database — demonstrating real SQL skills.")
    
    # --- Query 1: Department Summary with Window Functions ---
    st.markdown("#### 1️⃣ Department Summary (GROUP BY + Aggregations)")
    
    sql_query1 = """
SELECT 
    Department,
    COUNT(*) AS total_employees,
    SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) AS left_count,
    ROUND(SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) AS attrition_rate,
    ROUND(AVG(MonthlyIncome), 0) AS avg_income,
    ROUND(AVG(YearsAtCompany), 1) AS avg_tenure,
    ROUND(AVG(JobSatisfaction), 2) AS avg_satisfaction
FROM employees
GROUP BY Department
ORDER BY attrition_rate DESC"""
    
    with st.expander("📝 View SQL Query", expanded=False):
        st.code(sql_query1, language="sql")
    
    result1 = run_sql_query(sql_query1)
    if result1 is not None:
        st.dataframe(result1, width="stretch")
    
    st.markdown("---")
    
    # --- Query 2: Window Function — Salary Ranking ---
    st.markdown("#### 2️⃣ Salary Ranking within Department (RANK + PARTITION BY)")
    
    sql_query2 = """
SELECT 
    EmployeeNumber,
    Department,
    JobRole,
    MonthlyIncome,
    RANK() OVER (PARTITION BY Department ORDER BY MonthlyIncome DESC) AS salary_rank,
    ROUND(MonthlyIncome - AVG(MonthlyIncome) OVER (PARTITION BY Department), 0) AS diff_from_dept_avg
FROM employees
WHERE Attrition = 'Yes'
ORDER BY Department, salary_rank
LIMIT 15"""
    
    with st.expander("📝 View SQL Query", expanded=False):
        st.code(sql_query2, language="sql")
    
    result2 = run_sql_query(sql_query2)
    if result2 is not None:
        st.dataframe(result2, width="stretch")
    
    st.markdown("""
    <div class="insight-box">
        <b>💡 SQL Concept:</b> <code>RANK() OVER (PARTITION BY Department ORDER BY MonthlyIncome DESC)</code> 
        ranks employees by salary <i>within each department</i> separately. Window Functions are an advanced SQL skill 
        highly valued in interviews.
    </div>""", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # --- Query 3: CTE — High Risk Employee Profile ---
    st.markdown("#### 3️⃣ High-Risk Profile Analysis (CTE + Subquery)")
    
    sql_query3 = """
WITH dept_averages AS (
    SELECT 
        Department,
        ROUND(AVG(MonthlyIncome), 0) AS dept_avg_income,
        ROUND(AVG(YearsAtCompany), 1) AS dept_avg_tenure
    FROM employees
    GROUP BY Department
),
leavers AS (
    SELECT 
        e.Department,
        e.JobRole,
        COUNT(*) AS left_count,
        ROUND(AVG(e.MonthlyIncome), 0) AS avg_leaver_income,
        ROUND(AVG(e.YearsAtCompany), 1) AS avg_leaver_tenure,
        ROUND(AVG(e.Age), 0) AS avg_leaver_age
    FROM employees e
    WHERE e.Attrition = 'Yes'
    GROUP BY e.Department, e.JobRole
    HAVING COUNT(*) >= 5
)
SELECT 
    l.Department,
    l.JobRole,
    l.left_count,
    l.avg_leaver_income,
    d.dept_avg_income,
    l.avg_leaver_income - d.dept_avg_income AS income_gap,
    l.avg_leaver_tenure,
    l.avg_leaver_age
FROM leavers l
JOIN dept_averages d ON l.Department = d.Department
ORDER BY l.left_count DESC"""
    
    with st.expander("📝 View SQL Query", expanded=False):
        st.code(sql_query3, language="sql")
    
    result3 = run_sql_query(sql_query3)
    if result3 is not None:
        st.dataframe(result3, width="stretch")
    
    st.markdown("""
    <div class="insight-box insight-box-warning">
        <b>🔍 Finding:</b> Employees who leave typically earn LESS than their department average 
        (negative income_gap), confirming that compensation is a key attrition driver.
    </div>""", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # --- Query 4: CASE WHEN Risk Buckets ---
    st.markdown("#### 4️⃣ Employee Risk Bucketing (CASE WHEN)")
    
    sql_query4 = """
SELECT 
    CASE 
        WHEN OverTime = 'Yes' AND MonthlyIncome < 4000 AND YearsAtCompany <= 2 
        THEN 'HIGH RISK'
        WHEN OverTime = 'Yes' OR (MonthlyIncome < 3000 AND JobSatisfaction <= 2)
        THEN 'MEDIUM RISK'
        ELSE 'LOW RISK'
    END AS risk_level,
    COUNT(*) AS employee_count,
    SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) AS actually_left,
    ROUND(SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) AS actual_attrition_rate
FROM employees
GROUP BY risk_level
ORDER BY actual_attrition_rate DESC"""
    
    with st.expander("📝 View SQL Query", expanded=False):
        st.code(sql_query4, language="sql")
    
    result4 = run_sql_query(sql_query4)
    if result4 is not None:
        st.dataframe(result4, width="stretch")
        
        # Visualize risk buckets
        fig = px.bar(
            result4, x='risk_level', y='actual_attrition_rate',
            title='<b>Actual Attrition Rate by Risk Bucket</b>',
            color='risk_level',
            color_discrete_map={'HIGH RISK': '#e74c3c', 'MEDIUM RISK': '#f39c12', 'LOW RISK': '#2ecc71'},
            text='actual_attrition_rate'
        )
        fig.update_traces(texttemplate='%{text}%', textposition='outside')
        fig.update_layout(height=350, margin=dict(l=20, r=20, t=50, b=20))
        st.plotly_chart(fig, width="stretch")
    
    st.markdown("---")
    
    # --- Query 5: Cumulative Analysis ---
    st.markdown("#### 5️⃣ Cumulative Attrition by Tenure (Running Total)")
    
    sql_query5 = """
SELECT 
    YearsAtCompany,
    COUNT(*) AS total_at_tenure,
    SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) AS left_at_tenure,
    SUM(SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END)) 
        OVER (ORDER BY YearsAtCompany) AS cumulative_attrition,
    ROUND(SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) AS attrition_rate_at_tenure
FROM employees
GROUP BY YearsAtCompany
ORDER BY YearsAtCompany"""
    
    with st.expander("📝 View SQL Query", expanded=False):
        st.code(sql_query5, language="sql")
    
    result5 = run_sql_query(sql_query5)
    if result5 is not None:
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(
            go.Bar(x=result5['YearsAtCompany'], y=result5['left_at_tenure'],
                   name='Left at Tenure', marker_color='#e74c3c', opacity=0.7),
            secondary_y=False
        )
        fig.add_trace(
            go.Scatter(x=result5['YearsAtCompany'], y=result5['cumulative_attrition'],
                      name='Cumulative Attrition', line=dict(color='#2c3e50', width=3)),
            secondary_y=True
        )
        fig.update_layout(title='<b>When Do Employees Leave? (Tenure Analysis)</b>',
                         height=400, margin=dict(l=20, r=20, t=50, b=20))
        fig.update_xaxes(title_text="Years at Company")
        fig.update_yaxes(title_text="Employees Left", secondary_y=False)
        fig.update_yaxes(title_text="Cumulative Total", secondary_y=True)
        st.plotly_chart(fig, width="stretch")
    
    # --- Custom SQL Query ---
    st.markdown("---")
    st.markdown("#### 🔧 Run Your Own SQL Query")
    custom_query = st.text_area(
        "Enter a SQL query (table: `employees`)",
        value="SELECT Department, Gender, COUNT(*) AS count, ROUND(AVG(MonthlyIncome),0) AS avg_income\nFROM employees\nGROUP BY Department, Gender\nORDER BY avg_income DESC",
        height=100
    )
    if st.button("▶️ Run Query"):
        try:
            custom_result = run_sql_query(custom_query)
            if custom_result is not None:
                st.dataframe(custom_result, width="stretch")
                st.success(f"✅ {len(custom_result)} rows returned")
        except Exception as e:
            st.error(f"❌ Query error: {str(e)}")

# ============================================================================
# TAB 3: PYTHON STATISTICAL ANALYSIS
# ============================================================================
with tab3:
    st.markdown('<div class="section-header">Python Statistical Analysis</div>', unsafe_allow_html=True)
    st.markdown("Advanced analytics using Pandas, NumPy — demonstrating Python data skills.")
    
    # --- Descriptive Statistics ---
    st.markdown("#### 1️⃣ Descriptive Statistics (pandas .describe())")
    
    numeric_cols = ['Age', 'MonthlyIncome', 'YearsAtCompany', 'TotalWorkingYears',
                    'DistanceFromHome', 'PercentSalaryHike', 'YearsSinceLastPromotion']
    stats = filtered_df[numeric_cols].describe().round(2)
    st.dataframe(stats, width="stretch")
    
    st.markdown("---")
    
    # --- Comparison: Stayed vs Left ---
    st.markdown("#### 2️⃣ Stayed vs Left — Statistical Comparison")
    
    stayed = filtered_df[filtered_df['Attrition'] == 'No']
    left = filtered_df[filtered_df['Attrition'] == 'Yes']
    
    comparison_data = []
    for col in ['Age', 'MonthlyIncome', 'YearsAtCompany', 'TotalWorkingYears',
                'DistanceFromHome', 'JobSatisfaction', 'EnvironmentSatisfaction']:
        comparison_data.append({
            'Metric': col,
            'Stayed (Avg)': round(stayed[col].mean(), 1) if len(stayed) > 0 else 0,
            'Left (Avg)': round(left[col].mean(), 1) if len(left) > 0 else 0,
            'Difference': round(stayed[col].mean() - left[col].mean(), 1) if len(stayed) > 0 and len(left) > 0 else 0,
            'Insight': '⬆️ Higher for stayers' if stayed[col].mean() > left[col].mean() else '⬇️ Lower for stayers'
        })
    
    comparison_df = pd.DataFrame(comparison_data)
    st.dataframe(comparison_df, width="stretch", hide_index=True)
    
    st.markdown("""
    <div class="insight-box insight-box-success">
        <b>💡 Python Technique:</b> Used <code>groupby + .mean()</code> to compare averages between 
        two groups. This is the foundation of A/B testing and cohort analysis in data analytics.
    </div>""", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # --- Correlation Analysis ---
    st.markdown("#### 3️⃣ Correlation with Attrition (pandas .corr())")
    
    # Create numeric attrition column
    corr_df = filtered_df.copy()
    corr_df['Attrition_Num'] = (corr_df['Attrition'] == 'Yes').astype(int)
    corr_df['OverTime_Num'] = (corr_df['OverTime'] == 'Yes').astype(int)
    
    numeric_for_corr = ['Attrition_Num', 'Age', 'MonthlyIncome', 'YearsAtCompany',
                        'TotalWorkingYears', 'OverTime_Num', 'JobSatisfaction',
                        'EnvironmentSatisfaction', 'DistanceFromHome', 'NumCompaniesWorked',
                        'YearsSinceLastPromotion', 'WorkLifeBalance', 'StockOptionLevel']
    
    available_cols = [c for c in numeric_for_corr if c in corr_df.columns]
    correlations = corr_df[available_cols].corr()['Attrition_Num'].drop('Attrition_Num').sort_values()
    
    fig = px.bar(
        x=correlations.values, y=correlations.index,
        orientation='h',
        title='<b>Feature Correlation with Attrition</b>',
        color=correlations.values,
        color_continuous_scale='RdBu_r',
        labels={'x': 'Correlation Coefficient', 'y': 'Feature'}
    )
    fig.add_vline(x=0, line_dash="solid", line_color="black")
    fig.update_layout(height=450, margin=dict(l=20, r=20, t=50, b=20))
    st.plotly_chart(fig, width="stretch")
    
    st.markdown("""
    <div class="insight-box">
        <b>📖 Reading Correlations:</b><br>
        • <b>Positive</b> (red bars → right): Higher value = MORE likely to leave<br>
        • <b>Negative</b> (blue bars → left): Higher value = LESS likely to leave<br>
        • Overtime has the strongest POSITIVE correlation (drives attrition)
    </div>""", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # --- Pivot Table ---
    st.markdown("#### 4️⃣ Pivot Table Analysis (pandas .pivot_table())")
    
    pivot_col = st.selectbox("Pivot by:", ['Department', 'JobRole', 'MaritalStatus', 'OverTime', 'Gender'])
    
    pivot = pd.pivot_table(
        filtered_df,
        values=['MonthlyIncome', 'YearsAtCompany', 'JobSatisfaction', 'Age'],
        index=pivot_col,
        aggfunc={'MonthlyIncome': 'mean', 'YearsAtCompany': 'mean',
                 'JobSatisfaction': 'mean', 'Age': ['mean', 'count']}
    ).round(1)
    
    st.dataframe(pivot, width="stretch")
    
    st.markdown("---")
    
    # --- Distribution Analysis ---
    st.markdown("#### 5️⃣ Distribution Analysis (Histograms & Box Plots)")
    
    dist_col = st.selectbox("Analyze distribution of:", 
                           ['MonthlyIncome', 'Age', 'YearsAtCompany', 'DistanceFromHome',
                            'TotalWorkingYears', 'PercentSalaryHike'])
    
    col_l, col_r = st.columns(2)
    with col_l:
        fig = px.histogram(
            filtered_df, x=dist_col, color='Attrition',
            title=f'<b>{dist_col} Distribution</b>',
            barmode='overlay', opacity=0.7,
            color_discrete_map={'Yes': '#e74c3c', 'No': '#2ecc71'}
        )
        fig.update_layout(height=350, margin=dict(l=20, r=20, t=50, b=20))
        st.plotly_chart(fig, width="stretch")
    
    with col_r:
        fig = px.box(
            filtered_df, x='Attrition', y=dist_col,
            title=f'<b>{dist_col}: Stayed vs Left</b>',
            color='Attrition',
            color_discrete_map={'Yes': '#e74c3c', 'No': '#2ecc71'}
        )
        fig.update_layout(height=350, margin=dict(l=20, r=20, t=50, b=20))
        st.plotly_chart(fig, width="stretch")
    
    # Quick stats for selected column
    col_a, col_b, col_c, col_d = st.columns(4)
    col_a.metric("Mean", f"{filtered_df[dist_col].mean():.1f}")
    col_b.metric("Median", f"{filtered_df[dist_col].median():.1f}")
    col_c.metric("Std Dev", f"{filtered_df[dist_col].std():.1f}")
    col_d.metric("Skewness", f"{filtered_df[dist_col].skew():.2f}")

# ============================================================================
# TAB 4: VISUAL DEEP DIVE
# ============================================================================
with tab4:
    st.markdown('<div class="section-header">Visual Deep Dive</div>', unsafe_allow_html=True)
    
    # Overtime Impact
    col_l, col_r = st.columns(2)
    
    with col_l:
        ot_data = filtered_df.groupby('OverTime')['Attrition'].apply(
            lambda x: (x == 'Yes').sum() / len(x) * 100
        ).reset_index()
        ot_data.columns = ['OverTime', 'Attrition_Rate']
        
        fig = px.bar(
            ot_data, x='OverTime', y='Attrition_Rate',
            title='<b>Overtime Impact</b>',
            color='OverTime',
            color_discrete_map={'Yes': '#e74c3c', 'No': '#2ecc71'},
            text=ot_data['Attrition_Rate'].round(1).astype(str) + '%'
        )
        fig.update_traces(textposition='outside')
        fig.update_layout(height=380, margin=dict(l=20, r=20, t=50, b=20))
        st.plotly_chart(fig, width="stretch")
    
    with col_r:
        # Marital Status
        marital_data = filtered_df.groupby('MaritalStatus')['Attrition'].apply(
            lambda x: (x == 'Yes').sum() / len(x) * 100
        ).reset_index()
        marital_data.columns = ['MaritalStatus', 'Attrition_Rate']
        
        fig = px.bar(
            marital_data, x='MaritalStatus', y='Attrition_Rate',
            title='<b>Marital Status Impact</b>',
            color='Attrition_Rate', color_continuous_scale='RdYlGn_r',
            text=marital_data['Attrition_Rate'].round(1).astype(str) + '%'
        )
        fig.update_traces(textposition='outside')
        fig.update_layout(height=380, margin=dict(l=20, r=20, t=50, b=20))
        st.plotly_chart(fig, width="stretch")
    
    # Satisfaction heatmap
    st.markdown("#### Satisfaction Heatmap — Job Satisfaction vs Environment Satisfaction")
    
    heatmap_data = filtered_df.groupby(['JobSatisfaction', 'EnvironmentSatisfaction']).apply(
        lambda x: (x['Attrition'] == 'Yes').sum() / len(x) * 100
    ).reset_index()
    heatmap_data.columns = ['JobSatisfaction', 'EnvironmentSatisfaction', 'Attrition_Rate']
    
    heatmap_pivot = heatmap_data.pivot(
        index='JobSatisfaction', columns='EnvironmentSatisfaction', values='Attrition_Rate'
    )
    
    fig = px.imshow(
        heatmap_pivot,
        title='<b>Attrition Rate (%) by Satisfaction Levels</b>',
        labels=dict(x="Environment Satisfaction", y="Job Satisfaction", color="Attrition %"),
        color_continuous_scale='RdYlGn_r',
        text_auto='.1f',
        aspect='auto'
    )
    fig.update_layout(height=400, margin=dict(l=20, r=20, t=50, b=20))
    st.plotly_chart(fig, width="stretch")
    
    st.markdown("""
    <div class="insight-box insight-box-warning">
        <b>🔍 Insight:</b> Employees with LOW job satisfaction (1) AND LOW environment satisfaction (1) 
        have dramatically higher attrition. Both factors compound each other.
    </div>""", unsafe_allow_html=True)
    
    # Income by Job Level
    st.markdown("#### Income Distribution by Job Level")
    fig = px.box(
        filtered_df, x='JobLevel', y='MonthlyIncome', color='Attrition',
        title='<b>Monthly Income by Job Level (Stayed vs Left)</b>',
        color_discrete_map={'Yes': '#e74c3c', 'No': '#2ecc71'}
    )
    fig.update_layout(height=400, margin=dict(l=20, r=20, t=50, b=20))
    st.plotly_chart(fig, width="stretch")

# ============================================================================
# TAB 5: CROSS ANALYSIS
# ============================================================================
with tab5:
    st.markdown('<div class="section-header">Cross-Dimensional Analysis</div>', unsafe_allow_html=True)
    st.markdown("Analyze attrition across multiple dimensions simultaneously.")
    
    # Dynamic chart builder
    col_l, col_r = st.columns(2)
    with col_l:
        x_axis = st.selectbox("X-Axis (Category):", 
                             ['Department', 'JobRole', 'MaritalStatus', 'OverTime',
                              'Gender', 'BusinessTravel', 'EducationField'])
    with col_r:
        y_axis = st.selectbox("Y-Axis (Metric):", 
                             ['Attrition Rate (%)', 'Avg Monthly Income', 'Avg Age',
                              'Avg Tenure', 'Avg Satisfaction', 'Employee Count'])
    
    # Calculate selected metric
    if y_axis == 'Attrition Rate (%)':
        chart_data = filtered_df.groupby(x_axis)['Attrition'].apply(
            lambda x: (x == 'Yes').sum() / len(x) * 100
        ).reset_index()
        chart_data.columns = [x_axis, 'Value']
    elif y_axis == 'Avg Monthly Income':
        chart_data = filtered_df.groupby(x_axis)['MonthlyIncome'].mean().reset_index()
        chart_data.columns = [x_axis, 'Value']
    elif y_axis == 'Avg Age':
        chart_data = filtered_df.groupby(x_axis)['Age'].mean().reset_index()
        chart_data.columns = [x_axis, 'Value']
    elif y_axis == 'Avg Tenure':
        chart_data = filtered_df.groupby(x_axis)['YearsAtCompany'].mean().reset_index()
        chart_data.columns = [x_axis, 'Value']
    elif y_axis == 'Avg Satisfaction':
        chart_data = filtered_df.groupby(x_axis)['JobSatisfaction'].mean().reset_index()
        chart_data.columns = [x_axis, 'Value']
    else:
        chart_data = filtered_df.groupby(x_axis).size().reset_index()
        chart_data.columns = [x_axis, 'Value']
    
    chart_data['Value'] = chart_data['Value'].round(1)
    
    fig = px.bar(
        chart_data.sort_values('Value', ascending=False),
        x=x_axis, y='Value',
        title=f'<b>{y_axis} by {x_axis}</b>',
        color='Value', color_continuous_scale='Viridis',
        text='Value'
    )
    fig.update_traces(textposition='outside')
    fig.update_layout(height=450, margin=dict(l=20, r=20, t=50, b=20))
    st.plotly_chart(fig, width="stretch")
    
    # Scatter plot
    st.markdown("#### Scatter Plot — Explore Relationships")
    col_l, col_r = st.columns(2)
    with col_l:
        scatter_x = st.selectbox("X:", ['YearsAtCompany', 'Age', 'MonthlyIncome',
                                        'TotalWorkingYears', 'DistanceFromHome'])
    with col_r:
        scatter_y = st.selectbox("Y:", ['MonthlyIncome', 'Age', 'YearsAtCompany',
                                        'TotalWorkingYears', 'PercentSalaryHike'])
    
    fig = px.scatter(
        filtered_df, x=scatter_x, y=scatter_y,
        color='Attrition', size='JobLevel',
        title=f'<b>{scatter_y} vs {scatter_x}</b>',
        color_discrete_map={'Yes': '#e74c3c', 'No': '#2ecc71'},
        opacity=0.6, hover_data=['Department', 'JobRole']
    )
    fig.update_layout(height=450, margin=dict(l=20, r=20, t=50, b=20))
    st.plotly_chart(fig, width="stretch")

# ============================================================================
# TAB 6: DATA EXPLORER
# ============================================================================
with tab6:
    st.markdown('<div class="section-header">Data Explorer & Download</div>', unsafe_allow_html=True)
    
    st.markdown(f"**Dataset**: {len(filtered_df):,} rows × {filtered_df.shape[1]} columns (filtered)")
    
    # Search/filter within data
    search_term = st.text_input("🔍 Search in data (filters across all text columns):")
    
    display_df = filtered_df.copy()
    if search_term:
        mask = display_df.apply(lambda row: row.astype(str).str.contains(search_term, case=False).any(), axis=1)
        display_df = display_df[mask]
        st.markdown(f"Found **{len(display_df)}** matching rows")
    
    # Column selector
    selected_cols = st.multiselect(
        "Select columns:",
        display_df.columns.tolist(),
        default=['Age', 'Department', 'JobRole', 'MonthlyIncome',
                 'YearsAtCompany', 'OverTime', 'JobSatisfaction', 'MaritalStatus', 'Attrition']
    )
    
    if selected_cols:
        # Sorting
        sort_col = st.selectbox("Sort by:", selected_cols)
        sort_order = st.radio("Order:", ['Descending', 'Ascending'], horizontal=True)
        
        display_df = display_df[selected_cols].sort_values(
            sort_col, ascending=(sort_order == 'Ascending')
        )
        st.dataframe(display_df, width="stretch", height=500)
    
    # Download options
    st.markdown("---")
    col_dl1, col_dl2 = st.columns(2)
    with col_dl1:
        csv = filtered_df.to_csv(index=False)
        st.download_button("📥 Download Full Filtered Data (CSV)", csv, "hr_data_filtered.csv", "text/csv")
    with col_dl2:
        if selected_cols:
            csv_selected = display_df.to_csv(index=False)
            st.download_button("📥 Download Selected Columns (CSV)", csv_selected, "hr_data_selected.csv", "text/csv")

# ============================================================================
# FOOTER
# ============================================================================
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #7f8c8d; padding: 1rem;'>
    <p style='font-size: clamp(0.8rem, 2vw, 1rem);'>
        Built by <b>Priyanka S Biradar</b> | HR Analyst @ Goldman Sachs → Data Analyst<br>
        <a href='https://github.com/priyabiradar59' target='_blank'>GitHub</a> | 
        <a href='https://linkedin.com/in/priyabiradar59' target='_blank'>LinkedIn</a>
    </p>
    <p style='font-size: 0.8rem;'>Powered by Python • Pandas • SQL • Plotly • Streamlit</p>
</div>
""", unsafe_allow_html=True)

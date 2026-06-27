# ============================================================================
# INTERVIEW TALKING POINTS — Workforce Intelligence Platform
# ============================================================================
# Use these to confidently explain your project in Data Analyst interviews.
# Structure: STAR method (Situation → Task → Action → Result)
# ============================================================================


# ═══════════════════════════════════════════════════════════════════════════════
# 1. PROJECT OVERVIEW (30-second elevator pitch)
# ═══════════════════════════════════════════════════════════════════════════════

"""
"I built a People Analytics platform that analyzes 1,470 employee records 
to identify WHY employees leave. It combines Python, SQL, and an interactive 
Streamlit dashboard. The key finding was that overtime is the #1 attrition 
driver — employees working OT are 3x more likely to leave. The project 
includes advanced SQL queries with Window Functions and CTEs, a responsive 
dashboard, and data exports ready for Power BI and Tableau."
"""


# ═══════════════════════════════════════════════════════════════════════════════
# 2. TECHNICAL QUESTIONS & ANSWERS
# ═══════════════════════════════════════════════════════════════════════════════

TECHNICAL_QA = {
    
    # --- SQL QUESTIONS ---
    
    "Explain a Window Function you used": """
    I used RANK() OVER (PARTITION BY Department ORDER BY MonthlyIncome DESC)
    to rank employees by salary WITHIN each department separately.
    
    Unlike GROUP BY which collapses rows, Window Functions keep all rows 
    but add a calculated column. This helped me identify that employees who 
    left were often in the lower salary ranks of their department.
    
    I also used LAG() to compare each job level's average income to the 
    previous level, showing that the biggest salary jump happens at Level 3→4.
    """,
    
    "What is a CTE and why did you use it?": """
    CTE = Common Table Expression. It's like a temporary named result set.
    
    I used it to break a complex query into readable steps:
    1. First CTE calculated department averages
    2. Second CTE filtered employees who left  
    3. Final query JOINed them to compare leaver income vs dept average
    
    Why CTE over subquery? Readability. When queries get complex (3+ steps), 
    CTEs make them maintainable. I could also reference the same CTE multiple 
    times without recalculating.
    """,
    
    "How did you handle the CASE WHEN logic?": """
    I used nested CASE WHEN to create risk buckets:
    - HIGH RISK: Overtime=Yes AND Income<4000 AND Tenure<=2
    - MEDIUM RISK: Overtime=Yes OR (Low income AND low satisfaction)
    - LOW RISK: Everything else
    
    The validation? HIGH RISK bucket had 35%+ actual attrition rate vs 
    10% for LOW RISK — proving the logic works on real data.
    """,
    
    # --- PYTHON QUESTIONS ---
    
    "How did you clean the data?": """
    Three main steps:
    1. Removed 3 constant columns (same value for all 1,470 rows — zero information)
    2. Encoded the target variable (Attrition: Yes→1, No→0)
    3. One-hot encoded categorical features with drop_first=True to avoid multicollinearity
    
    I validated with unit tests — 16 tests checking data types, null values, 
    and expected shapes. This catches issues if the source data changes.
    """,
    
    "What Python libraries did you use and why?": """
    - Pandas: Data manipulation (groupby, pivot_table, merge, apply)
    - NumPy: Numerical operations
    - Plotly: Interactive charts (hover, zoom — better than static matplotlib for dashboards)
    - Seaborn: Statistical plots (heatmaps, violin plots for EDA notebook)
    - SQLAlchemy: Database connection (Python ↔ SQLite)
    - Streamlit: Web dashboard framework (Python → web app with zero JS)
    - pytest: Unit testing for data validation
    """,
    
    "Explain your data pipeline": """
    One command runs everything: python src/pipeline.py
    
    Flow: Raw CSV → Validate (null checks, shape checks) → Clean (remove constants, 
    encode target) → Save processed CSVs → Load into SQLite database → Verify
    
    Why pipeline? In production, data refreshes daily. A pipeline ensures 
    consistency and catches issues early. Mine uses modular functions I can 
    test independently.
    """,
    
    # --- DASHBOARD QUESTIONS ---
    
    "Why Streamlit over Tableau/Power BI?": """
    I used ALL THREE — they serve different purposes:
    
    - Streamlit: Custom Python logic, live SQL queries, responsive web app, 
      free deployment, shareable URL for interviews
    - Power BI: Star schema data model with DAX measures, enterprise-ready
    - Tableau: Pre-calculated fields for quick drag-and-drop visualization
    
    Streamlit showed I can BUILD dashboards with code.
    Power BI/Tableau showed I can work with standard BI tools.
    """,
    
    "How did you make it responsive?": """
    CSS media queries + clamp() for fluid typography:
    - Mobile (<768px): Single column, collapsed sidebar
    - Tablet (768-1024px): Two columns, compact padding
    - Desktop (>1024px): Full width, expanded layout
    
    KPI cards use gradient backgrounds with hover animations.
    Charts use Plotly which is naturally responsive (auto-resizes).
    """,
    
    # --- DATA MODELING QUESTIONS ---
    
    "Explain your Power BI data model": """
    I designed a Star Schema:
    - FACT TABLE (center): fact_employees — 1,470 rows with all metrics
    - DIMENSION TABLES: dim_department, dim_job_role, dim_demographics, 
      dim_satisfaction, dim_compensation
    
    Why star schema? Performance. Power BI queries facts through dimensions 
    using one-hop relationships. Also enables proper DAX measures like 
    CALCULATE with filter context.
    
    I pre-built 11 DAX measures (Attrition Rate, Risk Score, Retention Rate) 
    so the Power BI dashboard works immediately after import.
    """,
    
    # --- INSIGHTS QUESTIONS ---
    
    "What were your key findings?": """
    Top 5 attrition drivers (ranked by impact):
    1. OVERTIME — 3x higher attrition (30% vs 10%)
    2. LOW INCOME — Leavers earn $2,000+ less than stayers
    3. SHORT TENURE — 60% of attrition happens in first 2 years
    4. SINGLE STATUS — 2x more likely to leave vs married
    5. SALES DEPARTMENT — 20.6% attrition (highest)
    
    The most actionable: Overtime. A company can DIRECTLY control this 
    through workload monitoring and hiring more staff.
    """,
    
    "What recommendations would you give HR?": """
    1. Implement overtime alerts — flag employees exceeding 45hrs/week
    2. Compensation review — employees below department median + OT = flight risk
    3. First-year engagement program — most attrition happens in year 1-2
    4. Stay interviews for single employees under 30 (highest risk demographic)
    5. Sales department deep-dive — root cause analysis on their 20.6% rate
    """,
}


# ═══════════════════════════════════════════════════════════════════════════════
# 3. BEHAVIORAL QUESTIONS (STAR FORMAT)
# ═══════════════════════════════════════════════════════════════════════════════

BEHAVIORAL_ANSWERS = {
    
    "Tell me about a data project you built end-to-end": """
    SITUATION: I wanted to demonstrate full-stack data analyst skills — 
    Python, SQL, visualization, and business insights — in one project.
    
    TASK: Build a People Analytics platform that goes beyond basic EDA 
    to provide actionable retention strategies.
    
    ACTION: 
    - Designed a modular Python codebase with unit tests (16 passing)
    - Wrote 15+ advanced SQL queries (Window Functions, CTEs, CASE WHEN)
    - Built a responsive 6-tab Streamlit dashboard
    - Created a Power BI star schema data model with DAX measures
    - Deployed live on Streamlit Cloud with a shareable URL
    
    RESULT: Identified overtime as the #1 driver (3x attrition), 
    with specific recommendations that could save ~$2.3M annually 
    for a 1,000-person organization.
    """,
    
    "How do you approach a new dataset?": """
    My process:
    1. UNDERSTAND: Read documentation, check schema, understand business context
    2. VALIDATE: Check nulls, data types, distributions, outliers
    3. EXPLORE (EDA): Summary stats, correlations, group comparisons
    4. VISUALIZE: Charts that tell the story (not just pretty pictures)
    5. COMMUNICATE: Key findings in plain English with specific recommendations
    
    In this project, I followed this exact flow — starting with df.info() 
    and ending with a dashboard that any HR leader could use.
    """,
    
    "Describe a time you found a surprising insight in data": """
    SITUATION: I expected income to be the #1 attrition driver.
    
    FINDING: Overtime had a STRONGER correlation than income!
    - Overtime employees: 30% attrition
    - Non-overtime: 10% attrition
    - That's a 3x multiplier — bigger than the income effect.
    
    WHY IT MATTERS: Income is hard to change (budget constraints). 
    But overtime is directly controllable through workload management, 
    hiring, and policy changes. This makes it more actionable.
    """,
}


# ═══════════════════════════════════════════════════════════════════════════════
# 4. QUESTIONS TO ASK THE INTERVIEWER
# ═══════════════════════════════════════════════════════════════════════════════

QUESTIONS_TO_ASK = [
    "What BI tools does your team currently use? (Tableau, Power BI, Looker?)",
    "How is data structured — do you have a data warehouse or work with raw sources?",
    "What's the balance between ad-hoc analysis vs scheduled reporting?",
    "Are there specific KPIs the team tracks regularly?",
    "What does a typical week look like for this role?",
]


# ═══════════════════════════════════════════════════════════════════════════════
# 5. QUICK STATS TO MEMORIZE
# ═══════════════════════════════════════════════════════════════════════════════

QUICK_STATS = """
📊 PROJECT STATS (memorize these):
- Dataset: 1,470 employees × 35 features (IBM HR Analytics)
- Overall attrition rate: 16.1%
- Sales attrition: 20.6% (highest department)
- Overtime impact: 3x more likely to leave
- Income gap: Leavers earn $2,148 less on average
- Critical window: 60% of attrition in first 2 years
- Single employees: 25% attrition vs 12% for married
- SQL queries written: 15+ (including Window Functions, CTEs)
- Unit tests: 16 passing
- Dashboard tabs: 6 (Overview, SQL, Python Stats, Deep Dive, Cross Analysis, Explorer)
- Power BI model: Star schema with 5 dimension tables + 11 DAX measures
"""

if __name__ == "__main__":
    print(QUICK_STATS)
    print("\n📝 TECHNICAL Q&A TOPICS:")
    for q in TECHNICAL_QA:
        print(f"   • {q}")
    print("\n🎭 BEHAVIORAL QUESTIONS:")
    for q in BEHAVIORAL_ANSWERS:
        print(f"   • {q}")

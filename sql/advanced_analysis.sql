-- ============================================================================
-- advanced_analysis.sql — Advanced SQL Queries for Data Analyst Interviews
-- ============================================================================
-- These queries demonstrate skills beyond basics:
--   • Self-JOINs, NTILE, LAG/LEAD
--   • Percentile calculations
--   • Cohort analysis
--   • Year-over-year comparisons
--   • Complex CASE WHEN with multiple conditions
-- ============================================================================


-- ============================================================================
-- QUERY 1: NTILE — Divide employees into salary quartiles
-- CONCEPT: NTILE(4) splits data into 4 equal groups (quartiles)
-- INTERVIEW: "Segment employees by income percentile"
-- ============================================================================
SELECT 
    NTILE(4) OVER (ORDER BY MonthlyIncome) AS income_quartile,
    MIN(MonthlyIncome) AS min_income,
    MAX(MonthlyIncome) AS max_income,
    ROUND(AVG(MonthlyIncome), 0) AS avg_income,
    COUNT(*) AS employee_count,
    SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) AS left_count,
    ROUND(SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) AS attrition_rate
FROM employees
GROUP BY income_quartile
ORDER BY income_quartile;


-- ============================================================================
-- QUERY 2: LAG — Compare each employee's income to the next lower level
-- CONCEPT: LAG() accesses previous row's value
-- INTERVIEW: "How does income change across job levels?"
-- ============================================================================
WITH level_stats AS (
    SELECT 
        JobLevel,
        ROUND(AVG(MonthlyIncome), 0) AS avg_income,
        COUNT(*) AS headcount,
        ROUND(SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) AS attrition_rate
    FROM employees
    GROUP BY JobLevel
)
SELECT 
    JobLevel,
    avg_income,
    LAG(avg_income) OVER (ORDER BY JobLevel) AS prev_level_income,
    avg_income - LAG(avg_income) OVER (ORDER BY JobLevel) AS income_jump,
    ROUND((avg_income - LAG(avg_income) OVER (ORDER BY JobLevel)) * 100.0 
          / LAG(avg_income) OVER (ORDER BY JobLevel), 1) AS pct_increase,
    headcount,
    attrition_rate
FROM level_stats
ORDER BY JobLevel;


-- ============================================================================
-- QUERY 3: Cohort Analysis — Retention by tenure cohort
-- CONCEPT: GROUP BY tenure cohort + cumulative percentage
-- INTERVIEW: "What's the retention curve for new hires?"
-- ============================================================================
WITH tenure_cohorts AS (
    SELECT 
        CASE 
            WHEN YearsAtCompany = 0 THEN '0 (New Hire)'
            WHEN YearsAtCompany = 1 THEN '1 Year'
            WHEN YearsAtCompany BETWEEN 2 AND 3 THEN '2-3 Years'
            WHEN YearsAtCompany BETWEEN 4 AND 6 THEN '4-6 Years'
            WHEN YearsAtCompany BETWEEN 7 AND 10 THEN '7-10 Years'
            ELSE '10+ Years'
        END AS tenure_cohort,
        CASE 
            WHEN YearsAtCompany = 0 THEN 1
            WHEN YearsAtCompany = 1 THEN 2
            WHEN YearsAtCompany BETWEEN 2 AND 3 THEN 3
            WHEN YearsAtCompany BETWEEN 4 AND 6 THEN 4
            WHEN YearsAtCompany BETWEEN 7 AND 10 THEN 5
            ELSE 6
        END AS sort_order,
        Attrition
    FROM employees
)
SELECT 
    tenure_cohort,
    COUNT(*) AS total_in_cohort,
    SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) AS left_count,
    ROUND(SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) AS attrition_rate,
    ROUND(100 - SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) AS retention_rate
FROM tenure_cohorts
GROUP BY tenure_cohort, sort_order
ORDER BY sort_order;


-- ============================================================================
-- QUERY 4: Multi-factor risk scoring with DENSE_RANK
-- CONCEPT: Combining multiple risk factors + ranking
-- INTERVIEW: "Build a prioritized list of at-risk employees"
-- ============================================================================
WITH risk_scored AS (
    SELECT 
        EmployeeNumber,
        Department,
        JobRole,
        MonthlyIncome,
        YearsAtCompany,
        OverTime,
        JobSatisfaction,
        -- Calculate composite risk score
        (CASE WHEN OverTime = 'Yes' THEN 25 ELSE 0 END) +
        (CASE WHEN MonthlyIncome < 4000 THEN 20 ELSE 0 END) +
        (CASE WHEN JobSatisfaction <= 2 THEN 15 ELSE 0 END) +
        (CASE WHEN YearsAtCompany <= 2 THEN 15 ELSE 0 END) +
        (CASE WHEN EnvironmentSatisfaction <= 2 THEN 10 ELSE 0 END) +
        (CASE WHEN WorkLifeBalance <= 2 THEN 10 ELSE 0 END) +
        (CASE WHEN MaritalStatus = 'Single' THEN 5 ELSE 0 END) AS risk_score,
        Attrition
    FROM employees
    WHERE Attrition = 'No'  -- Only current employees
)
SELECT 
    EmployeeNumber,
    Department,
    JobRole,
    MonthlyIncome,
    YearsAtCompany,
    risk_score,
    DENSE_RANK() OVER (ORDER BY risk_score DESC) AS risk_rank,
    CASE 
        WHEN risk_score >= 50 THEN '🔴 Critical'
        WHEN risk_score >= 35 THEN '🟠 High'
        WHEN risk_score >= 20 THEN '🟡 Medium'
        ELSE '🟢 Low'
    END AS risk_category
FROM risk_scored
ORDER BY risk_score DESC
LIMIT 20;


-- ============================================================================
-- QUERY 5: Department comparison with PERCENT_RANK
-- CONCEPT: PERCENT_RANK shows where each dept stands relative to others
-- INTERVIEW: "How does each department compare on multiple metrics?"
-- ============================================================================
WITH dept_metrics AS (
    SELECT 
        Department,
        ROUND(AVG(MonthlyIncome), 0) AS avg_income,
        ROUND(AVG(JobSatisfaction), 2) AS avg_satisfaction,
        ROUND(AVG(YearsAtCompany), 1) AS avg_tenure,
        ROUND(SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) AS attrition_rate,
        ROUND(SUM(CASE WHEN OverTime = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) AS overtime_pct
    FROM employees
    GROUP BY Department
)
SELECT 
    Department,
    avg_income,
    avg_satisfaction,
    avg_tenure,
    attrition_rate,
    overtime_pct,
    -- Health score: lower attrition + higher satisfaction = healthier
    ROUND((100 - attrition_rate) * 0.4 + avg_satisfaction * 25 * 0.3 + 
          (100 - overtime_pct) * 0.3, 1) AS dept_health_score
FROM dept_metrics
ORDER BY dept_health_score DESC;


-- ============================================================================
-- QUERY 6: Promotion gap analysis
-- CONCEPT: Finding employees overdue for promotion
-- INTERVIEW: "Identify employees who may leave due to stagnation"
-- ============================================================================
SELECT 
    Department,
    JobRole,
    COUNT(*) AS overdue_count,
    ROUND(AVG(YearsSinceLastPromotion), 1) AS avg_years_since_promo,
    ROUND(AVG(MonthlyIncome), 0) AS avg_income,
    ROUND(AVG(JobSatisfaction), 2) AS avg_satisfaction,
    SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) AS left_count,
    ROUND(SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) AS attrition_rate
FROM employees
WHERE YearsSinceLastPromotion >= 5
  AND YearsAtCompany >= 5
  AND JobLevel < 4
GROUP BY Department, JobRole
HAVING COUNT(*) >= 3
ORDER BY attrition_rate DESC;


-- ============================================================================
-- QUERY 7: Gender pay equity analysis
-- CONCEPT: Comparing pay across demographics within same role
-- INTERVIEW: "Is there a gender pay gap within job roles?"
-- ============================================================================
SELECT 
    JobRole,
    Gender,
    COUNT(*) AS headcount,
    ROUND(AVG(MonthlyIncome), 0) AS avg_income,
    ROUND(AVG(MonthlyIncome) - AVG(AVG(MonthlyIncome)) OVER (PARTITION BY JobRole), 0) AS gap_from_role_avg,
    ROUND(SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) AS attrition_rate
FROM employees
GROUP BY JobRole, Gender
ORDER BY JobRole, Gender;

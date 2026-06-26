-- ============================================================================
-- attrition_analysis.sql — SQL Queries for HR Attrition Analysis
-- ============================================================================
-- PURPOSE: Demonstrate SQL skills for data analyst interviews
-- SKILLS SHOWN: Aggregations, JOINs, Window Functions, CTEs, CASE WHEN
-- 
-- Each query is labeled with the SQL CONCEPT it demonstrates
-- ============================================================================


-- ============================================================================
-- QUERY 1: Basic Aggregation — Overall Attrition Rate
-- CONCEPT: COUNT, GROUP BY, percentage calculation
-- INTERVIEW: "What's the overall attrition rate?"
-- ============================================================================
SELECT 
    Attrition,
    COUNT(*) AS employee_count,                           -- Count employees in each group
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 1) AS percentage  -- % of total
FROM employees
GROUP BY Attrition;


-- ============================================================================
-- QUERY 2: GROUP BY — Attrition by Department
-- CONCEPT: GROUP BY with multiple aggregations
-- INTERVIEW: "Which department has the highest attrition?"
-- ============================================================================
SELECT 
    Department,
    COUNT(*) AS total_employees,
    SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) AS employees_left,
    -- CASE WHEN: SQL's version of IF-THEN-ELSE
    -- Counts only rows where Attrition = 'Yes'
    ROUND(
        SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 
        1
    ) AS attrition_rate_pct
FROM employees
GROUP BY Department
ORDER BY attrition_rate_pct DESC;  -- Highest attrition first


-- ============================================================================
-- QUERY 3: Window Functions — Salary Ranking within Department
-- CONCEPT: RANK(), PARTITION BY, Window Functions
-- INTERVIEW: "Rank employees by salary within each department"
-- ============================================================================
SELECT 
    EmployeeNumber,
    Department,
    JobRole,
    MonthlyIncome,
    -- RANK() assigns a ranking number within each department
    -- PARTITION BY = "restart ranking for each department"
    -- ORDER BY MonthlyIncome DESC = highest salary gets rank 1
    RANK() OVER (PARTITION BY Department ORDER BY MonthlyIncome DESC) AS salary_rank,
    -- DENSE_RANK doesn't skip numbers for ties
    DENSE_RANK() OVER (PARTITION BY Department ORDER BY MonthlyIncome DESC) AS dense_salary_rank
FROM employees
WHERE Attrition = 'Yes'   -- Only look at people who left
ORDER BY Department, salary_rank
LIMIT 20;


-- ============================================================================
-- QUERY 4: CTE (Common Table Expression) — High-Risk Employee Profile
-- CONCEPT: WITH clause, subqueries, complex filtering
-- INTERVIEW: "Build a profile of high-risk employees"
-- ============================================================================
WITH attrition_stats AS (
    -- CTE = a temporary named result set (like a mini-table)
    -- WHY CTE? Makes complex queries readable by breaking them into steps
    SELECT 
        Department,
        JobRole,
        AVG(MonthlyIncome) AS avg_income,
        AVG(Age) AS avg_age,
        AVG(YearsAtCompany) AS avg_tenure,
        COUNT(*) AS left_count
    FROM employees
    WHERE Attrition = 'Yes'
    GROUP BY Department, JobRole
)
SELECT 
    Department,
    JobRole,
    ROUND(avg_income, 0) AS avg_income_of_leavers,
    ROUND(avg_age, 0) AS avg_age_of_leavers,
    ROUND(avg_tenure, 1) AS avg_tenure_of_leavers,
    left_count,
    -- Compare to overall average income
    ROUND(avg_income - (SELECT AVG(MonthlyIncome) FROM employees), 0) AS income_vs_company_avg
FROM attrition_stats
ORDER BY left_count DESC
LIMIT 10;


-- ============================================================================
-- QUERY 5: CASE WHEN — Categorize Employees into Risk Buckets
-- CONCEPT: CASE WHEN (conditional logic), multiple conditions
-- INTERVIEW: "Create a risk scoring system for employees"
-- ============================================================================
SELECT 
    EmployeeNumber,
    Department,
    JobRole,
    MonthlyIncome,
    OverTime,
    YearsAtCompany,
    JobSatisfaction,
    -- Create a risk score based on known attrition factors
    CASE 
        -- High Risk: multiple bad indicators
        WHEN OverTime = 'Yes' 
             AND MonthlyIncome < 4000 
             AND YearsAtCompany <= 2 
             AND JobSatisfaction <= 2
        THEN 'HIGH RISK'
        -- Medium Risk: some concerning indicators
        WHEN (OverTime = 'Yes' AND MonthlyIncome < 5000)
             OR (YearsAtCompany <= 1 AND JobSatisfaction <= 2)
        THEN 'MEDIUM RISK'
        -- Low Risk: stable indicators
        ELSE 'LOW RISK'
    END AS attrition_risk_level
FROM employees
WHERE Attrition = 'No'  -- Only current employees (predict who might leave)
ORDER BY 
    CASE 
        WHEN OverTime = 'Yes' AND MonthlyIncome < 4000 THEN 1
        WHEN OverTime = 'Yes' THEN 2
        ELSE 3
    END
LIMIT 20;


-- ============================================================================
-- QUERY 6: Window Functions — Running Average & Cumulative Count
-- CONCEPT: AVG() OVER, SUM() OVER with ORDER BY
-- INTERVIEW: "Show cumulative attrition trend by tenure"
-- ============================================================================
SELECT 
    YearsAtCompany,
    COUNT(*) AS employees_at_this_tenure,
    SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) AS left_at_this_tenure,
    -- Running total of employees who left (cumulative)
    SUM(SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END)) 
        OVER (ORDER BY YearsAtCompany) AS cumulative_attrition,
    -- Running average income of those who left
    ROUND(AVG(CASE WHEN Attrition = 'Yes' THEN MonthlyIncome END), 0) AS avg_income_of_leavers
FROM employees
GROUP BY YearsAtCompany
ORDER BY YearsAtCompany;


-- ============================================================================
-- QUERY 7: Subquery — Employees Below Department Average Salary
-- CONCEPT: Correlated subquery, comparison with group average
-- INTERVIEW: "Find underpaid employees who might be at risk"
-- ============================================================================
SELECT 
    e.EmployeeNumber,
    e.Department,
    e.JobRole,
    e.MonthlyIncome,
    -- Get the department average using a subquery
    (SELECT ROUND(AVG(MonthlyIncome), 0) 
     FROM employees 
     WHERE Department = e.Department) AS dept_avg_income,
    -- How far below average they are
    ROUND(e.MonthlyIncome - (
        SELECT AVG(MonthlyIncome) 
        FROM employees 
        WHERE Department = e.Department
    ), 0) AS diff_from_dept_avg
FROM employees e
WHERE e.Attrition = 'No'  -- Current employees only
  AND e.MonthlyIncome < (
      SELECT AVG(MonthlyIncome) 
      FROM employees 
      WHERE Department = e.Department
  )
ORDER BY diff_from_dept_avg ASC  -- Most underpaid first
LIMIT 15;


-- ============================================================================
-- QUERY 8: Summary Dashboard Query — KPIs for Streamlit
-- CONCEPT: Multiple aggregations in one query, ROUND
-- INTERVIEW: "Write a query that powers a dashboard's KPI cards"
-- ============================================================================
SELECT 
    -- Overall KPIs
    COUNT(*) AS total_employees,
    SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) AS total_attrition,
    ROUND(SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) AS attrition_rate,
    ROUND(AVG(MonthlyIncome), 0) AS avg_monthly_income,
    ROUND(AVG(Age), 0) AS avg_age,
    ROUND(AVG(YearsAtCompany), 1) AS avg_tenure,
    ROUND(AVG(JobSatisfaction), 2) AS avg_job_satisfaction,
    -- Breakdown
    SUM(CASE WHEN OverTime = 'Yes' THEN 1 ELSE 0 END) AS overtime_count,
    ROUND(AVG(CASE WHEN Attrition = 'Yes' THEN MonthlyIncome END), 0) AS avg_income_leavers,
    ROUND(AVG(CASE WHEN Attrition = 'No' THEN MonthlyIncome END), 0) AS avg_income_stayers
FROM employees;

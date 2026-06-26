-- ============================================================================
-- create_tables.sql — Database Schema for HR Analytics
-- ============================================================================
-- WHAT: Creates a SQLite database table to store employee data
-- WHY:  Demonstrates SQL skills (schema design, data types, constraints)
-- HOW:  Run this script to set up the database structure
-- WHEN: Once, at project setup (before loading data)
--
-- TABLE DESIGN DECISIONS:
--   - INTEGER for IDs and counts (whole numbers)
--   - TEXT for categorical data (department names, etc.)
--   - REAL for decimal numbers (salary rates)
--   - PRIMARY KEY on EmployeeNumber (unique identifier)
-- ============================================================================

-- Drop table if it exists (for re-running the script safely)
DROP TABLE IF EXISTS employees;

-- Create the main employees table
-- Each column stores one attribute about an employee
CREATE TABLE employees (
    -- IDENTIFIERS
    EmployeeNumber INTEGER PRIMARY KEY,    -- Unique ID for each employee
    
    -- DEMOGRAPHICS
    Age INTEGER NOT NULL,                  -- Employee age in years
    Gender TEXT NOT NULL,                   -- Male or Female
    MaritalStatus TEXT NOT NULL,            -- Single, Married, or Divorced
    DistanceFromHome INTEGER,              -- Distance from home (in units)
    
    -- JOB DETAILS
    Department TEXT NOT NULL,              -- Sales, R&D, or HR
    JobRole TEXT NOT NULL,                 -- Specific job title
    JobLevel INTEGER,                      -- 1-5 (Junior to Executive)
    BusinessTravel TEXT,                    -- Non-Travel, Travel_Rarely, Travel_Frequently
    
    -- COMPENSATION
    MonthlyIncome REAL NOT NULL,           -- Monthly salary in dollars
    DailyRate REAL,                        -- Daily rate
    HourlyRate REAL,                       -- Hourly rate
    MonthlyRate REAL,                      -- Monthly rate
    PercentSalaryHike INTEGER,             -- Last salary increase (%)
    StockOptionLevel INTEGER,              -- 0-3 (stock options granted)
    
    -- EXPERIENCE
    TotalWorkingYears INTEGER,             -- Total career experience
    YearsAtCompany INTEGER,               -- Years at current company
    YearsInCurrentRole INTEGER,            -- Years in current role
    YearsSinceLastPromotion INTEGER,       -- Years since last promotion
    YearsWithCurrManager INTEGER,          -- Years with current manager
    NumCompaniesWorked INTEGER,            -- Number of previous employers
    TrainingTimesLastYear INTEGER,          -- Training sessions attended
    
    -- SATISFACTION & PERFORMANCE
    JobSatisfaction INTEGER,               -- 1-4 (Low to Very High)
    EnvironmentSatisfaction INTEGER,        -- 1-4 (Low to Very High)
    RelationshipSatisfaction INTEGER,       -- 1-4 (Low to Very High)
    WorkLifeBalance INTEGER,               -- 1-4 (Bad to Best)
    JobInvolvement INTEGER,                -- 1-4 (Low to Very High)
    PerformanceRating INTEGER,             -- 3-4 (Excellent or Outstanding)
    
    -- WORK CONDITIONS
    OverTime TEXT,                          -- Yes or No
    
    -- EDUCATION
    Education INTEGER,                     -- 1-5 (Below College to Doctor)
    EducationField TEXT,                   -- Field of study
    
    -- TARGET VARIABLE (what we want to predict!)
    Attrition TEXT NOT NULL                -- Yes or No (did they leave?)
);

-- Create an index on Department for faster queries
-- WHY: We'll frequently filter/group by department
CREATE INDEX idx_department ON employees(Department);

-- Create an index on Attrition for faster filtering
CREATE INDEX idx_attrition ON employees(Attrition);

-- Verify table was created
SELECT 'Table created successfully!' AS status;

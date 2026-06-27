# ============================================================================
# src/powerbi_export.py — Power BI Star Schema Data Model
# ============================================================================
# PURPOSE: Create a professional Power BI-ready data model using STAR SCHEMA.
#
# WHAT IS STAR SCHEMA:
#   The industry-standard way to organize data for BI tools.
#   - FACT TABLE (center): Measurable events (employee records with metrics)
#   - DIMENSION TABLES (points of star): Descriptive attributes
#
#   Why? Power BI performs 10x faster with star schema vs flat tables.
#   Interviewers LOVE seeing this — it shows you understand data modeling.
#
# TABLES CREATED:
#   1. fact_employees      — Main fact table (metrics, foreign keys)
#   2. dim_department      — Department details
#   3. dim_job_role        — Job role hierarchy
#   4. dim_demographics    — Age groups, gender, marital status
#   5. dim_satisfaction    — Satisfaction level lookups
#   6. dim_compensation    — Income bands and stock options
#   7. measures_reference  — Pre-built DAX formulas for Power BI
#
# HOW TO USE IN POWER BI:
#   1. Get Data → Excel → Select hr_powerbi_model.xlsx
#   2. Load ALL sheets
#   3. Go to Model view → Create relationships (instructions in sheet)
#   4. Use DAX measures from measures_reference sheet
# ============================================================================

import pandas as pd
import numpy as np
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
from data_loader import load_raw_data

EXPORT_DIR = Path(__file__).parent.parent / "data" / "exports"
EXPORT_DIR.mkdir(parents=True, exist_ok=True)


def create_star_schema():
    """
    Build a star schema data model for Power BI.
    
    STAR SCHEMA STRUCTURE:
    
                    dim_department
                         |
    dim_demographics -- fact_employees -- dim_job_role
                         |
                    dim_satisfaction
                         |
                    dim_compensation
    """
    print("⭐ Building Power BI Star Schema...")
    df = load_raw_data()
    
    # =========================================================================
    # DIMENSION TABLE 1: dim_department
    # =========================================================================
    dim_department = pd.DataFrame({
        'DepartmentID': range(1, df['Department'].nunique() + 1),
        'Department': sorted(df['Department'].unique()),
    })
    # Add department-level aggregates
    dept_stats = df.groupby('Department').agg(
        Total_Headcount=('EmployeeNumber', 'count'),
        Dept_Avg_Income=('MonthlyIncome', 'mean'),
        Dept_Avg_Age=('Age', 'mean'),
        Dept_Attrition_Rate=('Attrition', lambda x: (x == 'Yes').sum() / len(x) * 100)
    ).round(1).reset_index()
    dim_department = dim_department.merge(dept_stats, on='Department')
    
    print(f"   ✅ dim_department: {len(dim_department)} rows")
    
    # =========================================================================
    # DIMENSION TABLE 2: dim_job_role
    # =========================================================================
    job_roles = df[['Department', 'JobRole', 'JobLevel']].drop_duplicates()
    dim_job_role = pd.DataFrame({
        'JobRoleID': range(1, len(df['JobRole'].unique()) + 1),
        'JobRole': sorted(df['JobRole'].unique()),
    })
    # Add role-level stats
    role_stats = df.groupby('JobRole').agg(
        Role_Headcount=('EmployeeNumber', 'count'),
        Role_Avg_Income=('MonthlyIncome', 'mean'),
        Role_Avg_Level=('JobLevel', 'mean'),
        Role_Attrition_Rate=('Attrition', lambda x: (x == 'Yes').sum() / len(x) * 100)
    ).round(1).reset_index()
    dim_job_role = dim_job_role.merge(role_stats, on='JobRole')
    
    print(f"   ✅ dim_job_role: {len(dim_job_role)} rows")
    
    # =========================================================================
    # DIMENSION TABLE 3: dim_demographics
    # =========================================================================
    dim_demographics = pd.DataFrame({
        'AgeGroupID': [1, 2, 3, 4, 5],
        'AgeGroup': ['18-25', '26-35', '36-45', '46-55', '56-65'],
        'AgeGroup_Min': [18, 26, 36, 46, 56],
        'AgeGroup_Max': [25, 35, 45, 55, 65],
        'Career_Stage': ['Early Career', 'Growth Phase', 'Mid Career', 'Senior', 'Pre-Retirement']
    })
    
    print(f"   ✅ dim_demographics: {len(dim_demographics)} rows")
    
    # =========================================================================
    # DIMENSION TABLE 4: dim_satisfaction
    # =========================================================================
    dim_satisfaction = pd.DataFrame({
        'SatisfactionID': [1, 2, 3, 4],
        'Level': ['Low', 'Medium', 'High', 'Very High'],
        'Score': [1, 2, 3, 4],
        'Description': [
            'Dissatisfied — high attrition risk',
            'Somewhat satisfied — monitor closely',
            'Satisfied — stable retention',
            'Very satisfied — likely to stay'
        ]
    })
    
    print(f"   ✅ dim_satisfaction: {len(dim_satisfaction)} rows")
    
    # =========================================================================
    # DIMENSION TABLE 5: dim_compensation
    # =========================================================================
    dim_compensation = pd.DataFrame({
        'IncomeBandID': [1, 2, 3, 4],
        'IncomeBand': ['Low (<$3K)', 'Medium ($3K-$6K)', 'High ($6K-$10K)', 'Very High (>$10K)'],
        'Min_Income': [0, 3000, 6000, 10000],
        'Max_Income': [2999, 5999, 9999, 99999],
        'Risk_Level': ['High Risk', 'Medium Risk', 'Low Risk', 'Very Low Risk']
    })
    
    print(f"   ✅ dim_compensation: {len(dim_compensation)} rows")
    
    # =========================================================================
    # FACT TABLE: fact_employees (the main table with foreign keys)
    # =========================================================================
    fact = df.copy()
    
    # Add foreign keys to link to dimension tables
    dept_map = dict(zip(dim_department['Department'], dim_department['DepartmentID']))
    role_map = dict(zip(dim_job_role['JobRole'], dim_job_role['JobRoleID']))
    
    fact['DepartmentID'] = fact['Department'].map(dept_map)
    fact['JobRoleID'] = fact['JobRole'].map(role_map)
    
    # Add calculated columns (saves DAX formulas in Power BI)
    fact['Attrition_Flag'] = (fact['Attrition'] == 'Yes').astype(int)
    fact['OverTime_Flag'] = (fact['OverTime'] == 'Yes').astype(int)
    
    fact['AgeGroup'] = pd.cut(
        fact['Age'], bins=[17, 25, 35, 45, 55, 65],
        labels=['18-25', '26-35', '36-45', '46-55', '56-65']
    )
    fact['AgeGroupID'] = pd.cut(
        fact['Age'], bins=[17, 25, 35, 45, 55, 65],
        labels=[1, 2, 3, 4, 5]
    ).astype(int)
    
    fact['IncomeBand'] = pd.cut(
        fact['MonthlyIncome'], bins=[0, 3000, 6000, 10000, 99999],
        labels=['Low (<$3K)', 'Medium ($3K-$6K)', 'High ($6K-$10K)', 'Very High (>$10K)']
    )
    fact['IncomeBandID'] = pd.cut(
        fact['MonthlyIncome'], bins=[0, 3000, 6000, 10000, 99999],
        labels=[1, 2, 3, 4]
    ).astype(int)
    
    fact['Tenure_Bucket'] = pd.cut(
        fact['YearsAtCompany'], bins=[-1, 1, 3, 5, 10, 40],
        labels=['<1 yr', '1-3 yrs', '3-5 yrs', '5-10 yrs', '10+ yrs']
    )
    
    # Satisfaction index (avg of all satisfaction scores)
    fact['Satisfaction_Index'] = (
        fact['JobSatisfaction'] + fact['EnvironmentSatisfaction'] +
        fact['RelationshipSatisfaction'] + fact['WorkLifeBalance']
    ) / 4
    
    # Risk score (simple rule-based)
    fact['Risk_Score'] = 0
    fact.loc[fact['OverTime'] == 'Yes', 'Risk_Score'] += 25
    fact.loc[fact['MonthlyIncome'] < 4000, 'Risk_Score'] += 20
    fact.loc[fact['JobSatisfaction'] <= 2, 'Risk_Score'] += 15
    fact.loc[fact['YearsAtCompany'] <= 2, 'Risk_Score'] += 15
    fact.loc[fact['MaritalStatus'] == 'Single', 'Risk_Score'] += 10
    fact.loc[fact['EnvironmentSatisfaction'] <= 2, 'Risk_Score'] += 10
    fact.loc[fact['WorkLifeBalance'] <= 2, 'Risk_Score'] += 5
    
    fact['Risk_Category'] = pd.cut(
        fact['Risk_Score'], bins=[-1, 20, 40, 100],
        labels=['Low Risk', 'Medium Risk', 'High Risk']
    )
    
    print(f"   ✅ fact_employees: {len(fact)} rows × {fact.shape[1]} columns")
    
    # =========================================================================
    # DAX MEASURES REFERENCE
    # =========================================================================
    measures = pd.DataFrame({
        'Measure_Name': [
            'Total Employees',
            'Attrition Count',
            'Attrition Rate %',
            'Avg Monthly Income',
            'Avg Tenure',
            'Avg Satisfaction',
            'Overtime Rate %',
            'High Risk Count',
            'Attrition Rate YoY Change',
            'Income vs Dept Avg',
            'Retention Rate %'
        ],
        'DAX_Formula': [
            'Total Employees = COUNTROWS(fact_employees)',
            'Attrition Count = SUM(fact_employees[Attrition_Flag])',
            'Attrition Rate % = DIVIDE([Attrition Count], [Total Employees], 0) * 100',
            'Avg Monthly Income = AVERAGE(fact_employees[MonthlyIncome])',
            'Avg Tenure = AVERAGE(fact_employees[YearsAtCompany])',
            'Avg Satisfaction = AVERAGE(fact_employees[Satisfaction_Index])',
            'Overtime Rate % = DIVIDE(SUM(fact_employees[OverTime_Flag]), [Total Employees], 0) * 100',
            'High Risk Count = CALCULATE([Total Employees], fact_employees[Risk_Category] = "High Risk")',
            'Attrition YoY = [Attrition Rate %] - CALCULATE([Attrition Rate %], PREVIOUSYEAR(dim_date[Date]))',
            'Income vs Dept = AVERAGE(fact_employees[MonthlyIncome]) - AVERAGE(dim_department[Dept_Avg_Income])',
            'Retention Rate % = 100 - [Attrition Rate %]'
        ],
        'Description': [
            'Count of all employees in current filter context',
            'Number of employees who left (Attrition = Yes)',
            'Percentage of employees who left',
            'Average monthly salary across filtered employees',
            'Average years at company',
            'Combined satisfaction score (1-4 scale)',
            'Percentage working overtime',
            'Employees in high-risk category',
            'Year-over-year change in attrition rate',
            'Difference between employee income and department average',
            'Percentage of employees retained (100 - attrition rate)'
        ],
        'Use_In': [
            'KPI Card',
            'KPI Card',
            'KPI Card, Bar Chart',
            'KPI Card, Table',
            'KPI Card',
            'Gauge Chart',
            'KPI Card',
            'KPI Card, Alert',
            'Line Chart',
            'Column Chart',
            'KPI Card'
        ]
    })
    
    print(f"   ✅ measures_reference: {len(measures)} DAX formulas")
    
    # =========================================================================
    # RELATIONSHIP GUIDE
    # =========================================================================
    relationships = pd.DataFrame({
        'From_Table': ['fact_employees', 'fact_employees', 'fact_employees', 'fact_employees', 'fact_employees'],
        'From_Column': ['DepartmentID', 'JobRoleID', 'AgeGroupID', 'JobSatisfaction', 'IncomeBandID'],
        'To_Table': ['dim_department', 'dim_job_role', 'dim_demographics', 'dim_satisfaction', 'dim_compensation'],
        'To_Column': ['DepartmentID', 'JobRoleID', 'AgeGroupID', 'SatisfactionID', 'IncomeBandID'],
        'Cardinality': ['Many-to-One', 'Many-to-One', 'Many-to-One', 'Many-to-One', 'Many-to-One'],
        'Cross_Filter': ['Both', 'Both', 'Both', 'Both', 'Both']
    })
    
    # =========================================================================
    # SAVE TO EXCEL (Multi-sheet)
    # =========================================================================
    excel_path = EXPORT_DIR / "hr_powerbi_model.xlsx"
    
    with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
        fact.to_excel(writer, sheet_name='fact_employees', index=False)
        dim_department.to_excel(writer, sheet_name='dim_department', index=False)
        dim_job_role.to_excel(writer, sheet_name='dim_job_role', index=False)
        dim_demographics.to_excel(writer, sheet_name='dim_demographics', index=False)
        dim_satisfaction.to_excel(writer, sheet_name='dim_satisfaction', index=False)
        dim_compensation.to_excel(writer, sheet_name='dim_compensation', index=False)
        measures.to_excel(writer, sheet_name='dax_measures', index=False)
        relationships.to_excel(writer, sheet_name='relationships_guide', index=False)
    
    print(f"\n   💾 Saved: {excel_path}")
    print(f"      8 sheets: fact_employees + 5 dimensions + DAX measures + relationships guide")
    
    return excel_path


def create_powerbi_csv_files():
    """
    Also export as separate CSVs (alternative import method for Power BI).
    Some users prefer CSV imports over Excel.
    """
    print("\n📁 Creating separate CSV files for Power BI...")
    
    powerbi_dir = EXPORT_DIR / "powerbi_csvs"
    powerbi_dir.mkdir(exist_ok=True)
    
    df = load_raw_data()
    
    # Fact table
    fact = df.copy()
    fact['Attrition_Flag'] = (fact['Attrition'] == 'Yes').astype(int)
    fact['OverTime_Flag'] = (fact['OverTime'] == 'Yes').astype(int)
    fact['AgeGroup'] = pd.cut(fact['Age'], bins=[17,25,35,45,55,65],
                              labels=['18-25','26-35','36-45','46-55','56-65'])
    fact['IncomeBand'] = pd.cut(fact['MonthlyIncome'], bins=[0,3000,6000,10000,99999],
                               labels=['Low','Medium','High','Very High'])
    fact['Satisfaction_Index'] = (fact['JobSatisfaction'] + fact['EnvironmentSatisfaction'] +
                                  fact['RelationshipSatisfaction'] + fact['WorkLifeBalance']) / 4
    
    fact.to_csv(powerbi_dir / "fact_employees.csv", index=False)
    
    # Dimension CSVs
    dept = df.groupby('Department').agg(
        Headcount=('EmployeeNumber','count'),
        Avg_Income=('MonthlyIncome','mean'),
        Attrition_Rate=('Attrition', lambda x: (x=='Yes').sum()/len(x)*100)
    ).round(1).reset_index()
    dept.to_csv(powerbi_dir / "dim_department.csv", index=False)
    
    roles = df.groupby('JobRole').agg(
        Headcount=('EmployeeNumber','count'),
        Avg_Income=('MonthlyIncome','mean'),
        Avg_Level=('JobLevel','mean'),
        Attrition_Rate=('Attrition', lambda x: (x=='Yes').sum()/len(x)*100)
    ).round(1).reset_index()
    roles.to_csv(powerbi_dir / "dim_job_role.csv", index=False)
    
    print(f"   ✅ CSVs saved to: {powerbi_dir}/")
    print(f"      fact_employees.csv, dim_department.csv, dim_job_role.csv")


if __name__ == "__main__":
    print("🚀 POWER BI DATA MODEL GENERATOR")
    print("=" * 60)
    
    create_star_schema()
    create_powerbi_csv_files()
    
    print("\n" + "=" * 60)
    print("🎉 POWER BI MODEL COMPLETE!")
    print("=" * 60)
    print("""
    📂 Files created:
       • data/exports/hr_powerbi_model.xlsx (Star Schema — 8 sheets)
       • data/exports/powerbi_csvs/         (Individual CSV files)
    
    📊 HOW TO USE IN POWER BI:
       1. Open Power BI Desktop
       2. Get Data → Excel → Select hr_powerbi_model.xlsx
       3. Select ALL sheets → Load
       4. Go to Model View → Create relationships:
          - fact_employees[DepartmentID] → dim_department[DepartmentID]
          - fact_employees[JobRoleID] → dim_job_role[JobRoleID]
          - fact_employees[AgeGroupID] → dim_demographics[AgeGroupID]
       5. Use DAX measures from 'dax_measures' sheet
       6. Build your dashboard!
    
    💡 SUGGESTED POWER BI VISUALS:
       • KPI Cards: Attrition Rate, Avg Income, Headcount
       • Stacked Bar: Attrition by Department
       • Donut Chart: Risk Category distribution
       • Matrix: Department × Job Role × Attrition Rate
       • Slicer: Department, Age Group, Income Band
       • Line Chart: Tenure vs Attrition
    """)

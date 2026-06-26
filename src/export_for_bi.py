# ============================================================================
# src/export_for_bi.py — Export Data for Power BI & Tableau
# ============================================================================
# PURPOSE: Generate analysis-ready files in formats optimized for BI tools.
#
# EXPORTS CREATED:
#   1. Excel (.xlsx) with multiple sheets — for Power BI
#   2. CSV with pre-calculated metrics — for Tableau
#   3. Summary pivot tables — for quick dashboard creation
#
# WHY:
#   - Shows you can work across tools (Python → Power BI → Tableau)
#   - Pre-calculated fields save time in BI tool modeling
#   - Multiple sheets in Excel = ready-made data model
#
# HOW TO USE IN POWER BI:
#   Get Data → Excel → Select the .xlsx file → Load all sheets
#
# HOW TO USE IN TABLEAU:
#   Connect → Text File → Select the CSV → Start visualizing
# ============================================================================

import pandas as pd
import numpy as np
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
from data_loader import load_raw_data

# Output directory
EXPORT_DIR = Path(__file__).parent.parent / "data" / "exports"
EXPORT_DIR.mkdir(parents=True, exist_ok=True)


def create_excel_export():
    """
    Create a multi-sheet Excel file optimized for Power BI.
    
    SHEETS:
        1. Raw Data — Full employee dataset
        2. Department Summary — Aggregated KPIs per department
        3. Role Analysis — Attrition metrics per job role
        4. Monthly Trends — Tenure-based attrition patterns
        5. Risk Segments — Pre-built employee risk categories
    """
    print("📊 Creating Power BI Excel export...")
    
    df = load_raw_data()
    
    # --- Sheet 1: Full dataset with calculated columns ---
    df_enhanced = df.copy()
    # Add useful calculated fields for BI tools
    df_enhanced['Attrition_Flag'] = (df['Attrition'] == 'Yes').astype(int)
    df_enhanced['Income_Band'] = pd.cut(
        df['MonthlyIncome'],
        bins=[0, 3000, 6000, 10000, 20000],
        labels=['Low (<3K)', 'Medium (3K-6K)', 'High (6K-10K)', 'Very High (>10K)']
    )
    df_enhanced['Age_Group'] = pd.cut(
        df['Age'],
        bins=[17, 25, 35, 45, 55, 65],
        labels=['18-25', '26-35', '36-45', '46-55', '56-65']
    )
    df_enhanced['Tenure_Group'] = pd.cut(
        df['YearsAtCompany'],
        bins=[-1, 2, 5, 10, 40],
        labels=['0-2 yrs', '3-5 yrs', '6-10 yrs', '10+ yrs']
    )
    
    # --- Sheet 2: Department Summary ---
    dept_summary = df.groupby('Department').agg(
        Total_Employees=('EmployeeNumber', 'count'),
        Attrition_Count=('Attrition', lambda x: (x == 'Yes').sum()),
        Attrition_Rate=('Attrition', lambda x: (x == 'Yes').sum() / len(x) * 100),
        Avg_Income=('MonthlyIncome', 'mean'),
        Avg_Age=('Age', 'mean'),
        Avg_Tenure=('YearsAtCompany', 'mean'),
        Avg_Satisfaction=('JobSatisfaction', 'mean'),
        Overtime_Pct=('OverTime', lambda x: (x == 'Yes').sum() / len(x) * 100)
    ).round(1).reset_index()
    
    # --- Sheet 3: Role Analysis ---
    role_summary = df.groupby(['Department', 'JobRole']).agg(
        Total_Employees=('EmployeeNumber', 'count'),
        Attrition_Count=('Attrition', lambda x: (x == 'Yes').sum()),
        Attrition_Rate=('Attrition', lambda x: (x == 'Yes').sum() / len(x) * 100),
        Avg_Income=('MonthlyIncome', 'mean'),
        Min_Income=('MonthlyIncome', 'min'),
        Max_Income=('MonthlyIncome', 'max'),
        Avg_Tenure=('YearsAtCompany', 'mean')
    ).round(1).reset_index()
    
    # --- Sheet 4: Tenure Analysis ---
    tenure_analysis = df.groupby('YearsAtCompany').agg(
        Total_Employees=('EmployeeNumber', 'count'),
        Attrition_Count=('Attrition', lambda x: (x == 'Yes').sum()),
        Attrition_Rate=('Attrition', lambda x: (x == 'Yes').sum() / len(x) * 100),
        Avg_Income=('MonthlyIncome', 'mean')
    ).round(1).reset_index()
    
    # --- Sheet 5: Risk Segments ---
    df_risk = df.copy()
    df_risk['Risk_Level'] = 'Low Risk'
    df_risk.loc[
        (df_risk['OverTime'] == 'Yes') & (df_risk['MonthlyIncome'] < 4000) & 
        (df_risk['YearsAtCompany'] <= 2),
        'Risk_Level'
    ] = 'High Risk'
    df_risk.loc[
        ((df_risk['OverTime'] == 'Yes') | 
         ((df_risk['MonthlyIncome'] < 3000) & (df_risk['JobSatisfaction'] <= 2))) &
        (df_risk['Risk_Level'] != 'High Risk'),
        'Risk_Level'
    ] = 'Medium Risk'
    
    risk_summary = df_risk.groupby('Risk_Level').agg(
        Employee_Count=('EmployeeNumber', 'count'),
        Actual_Attrition=('Attrition', lambda x: (x == 'Yes').sum()),
        Actual_Attrition_Rate=('Attrition', lambda x: (x == 'Yes').sum() / len(x) * 100),
        Avg_Income=('MonthlyIncome', 'mean'),
        Avg_Satisfaction=('JobSatisfaction', 'mean')
    ).round(1).reset_index()
    
    # --- Write to Excel ---
    excel_path = EXPORT_DIR / "hr_analytics_powerbi.xlsx"
    with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
        df_enhanced.to_excel(writer, sheet_name='Employee_Data', index=False)
        dept_summary.to_excel(writer, sheet_name='Department_Summary', index=False)
        role_summary.to_excel(writer, sheet_name='Role_Analysis', index=False)
        tenure_analysis.to_excel(writer, sheet_name='Tenure_Analysis', index=False)
        risk_summary.to_excel(writer, sheet_name='Risk_Segments', index=False)
    
    print(f"   ✅ Excel saved: {excel_path}")
    print(f"      Sheets: Employee_Data, Department_Summary, Role_Analysis, Tenure_Analysis, Risk_Segments")
    return excel_path


def create_tableau_export():
    """
    Create CSV files optimized for Tableau.
    
    WHY SEPARATE FROM EXCEL:
        - Tableau works best with flat CSVs
        - Pre-calculated fields reduce Tableau prep time
        - Includes ALL fields Tableau needs for common chart types
    """
    print("\n📈 Creating Tableau CSV export...")
    
    df = load_raw_data()
    
    # Create an enriched flat file with all calculated fields
    tableau_df = df.copy()
    
    # Add calculated measures (saves time in Tableau)
    tableau_df['Attrition_Flag'] = (df['Attrition'] == 'Yes').astype(int)
    tableau_df['Income_Band'] = pd.cut(
        df['MonthlyIncome'],
        bins=[0, 3000, 6000, 10000, 20000],
        labels=['Low', 'Medium', 'High', 'Very High']
    )
    tableau_df['Age_Group'] = pd.cut(
        df['Age'],
        bins=[17, 25, 35, 45, 55, 65],
        labels=['18-25', '26-35', '36-45', '46-55', '56-65']
    )
    tableau_df['Tenure_Bucket'] = pd.cut(
        df['YearsAtCompany'],
        bins=[-1, 1, 3, 5, 10, 40],
        labels=['<1 yr', '1-3 yrs', '3-5 yrs', '5-10 yrs', '10+ yrs']
    )
    tableau_df['Satisfaction_Level'] = pd.cut(
        df['JobSatisfaction'],
        bins=[0, 1, 2, 3, 4],
        labels=['Low', 'Medium', 'High', 'Very High']
    )
    
    # Income per year of experience (useful for scatter plots)
    tableau_df['Income_Per_Year_Exp'] = (
        df['MonthlyIncome'] / (df['TotalWorkingYears'].replace(0, 1))
    ).round(0)
    
    # Save
    csv_path = EXPORT_DIR / "hr_analytics_tableau.csv"
    tableau_df.to_csv(csv_path, index=False)
    
    print(f"   ✅ CSV saved: {csv_path}")
    print(f"      Columns: {tableau_df.shape[1]} (including calculated fields)")
    print(f"      Rows: {tableau_df.shape[0]}")
    return csv_path


def create_summary_report():
    """
    Create a summary CSV with pre-aggregated KPIs for quick dashboarding.
    """
    print("\n📋 Creating summary report...")
    
    df = load_raw_data()
    
    # Overall KPIs
    kpis = pd.DataFrame([{
        'Metric': 'Total Employees',
        'Value': len(df),
        'Category': 'Overview'
    }, {
        'Metric': 'Attrition Rate (%)',
        'Value': round((df['Attrition'] == 'Yes').sum() / len(df) * 100, 1),
        'Category': 'Overview'
    }, {
        'Metric': 'Avg Monthly Income',
        'Value': round(df['MonthlyIncome'].mean(), 0),
        'Category': 'Compensation'
    }, {
        'Metric': 'Avg Age',
        'Value': round(df['Age'].mean(), 0),
        'Category': 'Demographics'
    }, {
        'Metric': 'Avg Tenure (Years)',
        'Value': round(df['YearsAtCompany'].mean(), 1),
        'Category': 'Retention'
    }, {
        'Metric': 'Avg Job Satisfaction',
        'Value': round(df['JobSatisfaction'].mean(), 2),
        'Category': 'Engagement'
    }, {
        'Metric': 'Overtime Rate (%)',
        'Value': round((df['OverTime'] == 'Yes').sum() / len(df) * 100, 1),
        'Category': 'Workload'
    }, {
        'Metric': 'Highest Attrition Dept',
        'Value': 'Sales (20.6%)',
        'Category': 'Risk'
    }, {
        'Metric': 'Highest Risk Factor',
        'Value': 'Overtime (3x impact)',
        'Category': 'Risk'
    }])
    
    kpi_path = EXPORT_DIR / "kpi_summary.csv"
    kpis.to_csv(kpi_path, index=False)
    print(f"   ✅ KPI Summary: {kpi_path}")
    
    return kpi_path


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("🚀 EXPORTING DATA FOR BI TOOLS")
    print("=" * 60)
    
    create_excel_export()
    create_tableau_export()
    create_summary_report()
    
    print("\n" + "=" * 60)
    print("🎉 ALL EXPORTS COMPLETE!")
    print("=" * 60)
    print(f"""
    📁 Export files created in: data/exports/
    
    FOR POWER BI:
       → Open: data/exports/hr_analytics_powerbi.xlsx
       → Get Data → Excel → Select file → Load all sheets
       → Create relationships between sheets on 'Department'
    
    FOR TABLEAU:
       → Connect → Text File → hr_analytics_tableau.csv
       → All calculated fields are pre-built (Age_Group, Income_Band, etc.)
       → Drag and drop to create visualizations immediately
    
    FOR QUICK REFERENCE:
       → data/exports/kpi_summary.csv (key metrics at a glance)
    """)

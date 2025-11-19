# FinRisk-Analytics-Customer-Loan-Risk-and-Opportunity

Project Overview
This project analyzes transactional and demographic data from FinFuture Bank to build a data-driven loan risk model and identify high-potential customer segments for the marketing team. The primary goal is to reduce loan defaults and increase the conversion rate of personal loan campaigns.

# Business Problems
   - Rising loan default rates (up 1.2% QoQ).
   - Inefficient marketing spend with low conversion rates.

# Project Steps
**1. Data Sourcing & Understanding**
  - Two core tables used:
      - account_holders: demographics, financial health, CIBIL, product usage, loan history.
      - transactions: inflows, outflows, spending behavior, payment habits.

**2. SQL Feature Engineering**
  - An SQL pipeline aggregates transactions per customer: This produces a single consolidated Account_Features table containing.
    - Total inflow & outflow
    - Net cash flow
    - Burn rate (outflow ÷ inflow)
    - Credit card and UPI usage
    - Withdrawal behavior
    - Total transactions

**3. Python Cleaning & Enrichment**
  - Performed in Pandas:
    - Missing value handling (e.g., CIBIL median imputation)
    - Creating new features:
    - Customer tenure
    - Total wealth (balance + FDs)
    - Outflow-to-balance ratio
    - Age groups
  - Splitting into two datasets:
    - Customers with loan history (for risk analysis)
    - Customers with no loan (for prospect analysis)

**4. Exploratory Data Analysis (EDA)**
  - Key insights visualized using boxplots, KDE plots, and scatterplots:
  - CIBIL distribution across outcomes
  - Net cash flow patterns
  - Total wealth vs. burn rate clusters

**5. Dashboard & Visual Flow**
  - Power BI Dashboard includes:
      - Key Performance Indicators (KPIs)
      - CIBIL Score Distribution (Box Plot)
      - Loan Defaulters by Age Group (Bar Chart)
      - Average Wealth Distribution (Bar Chart)
      - Interactive Flowcharts (example placeholders):
      - Credit Card Distribution (Pie Chart):
  <img width="1835" height="1059" alt="image" src="https://github.com/user-attachments/assets/e223623b-e024-4d18-a782-cdea1b31b020" />


**Data Flow: Raw Data → SQL Aggregation → Python Cleaning → EDA → Insights**

**Risk Decision Flow: Applicant → Score Check → Behavioral Metrics → Risk Flag**

**Marketing Funnel Flow: Prospect Identification → Segmentation → Campaign → Conversion Tracking**

# Key Findings & Recommendation.
   - Risk Insight: A "Red Flag" profile (CIBIL < 700 & Net Cash Flow < $500) was identified. Customers in this group have a 4x higher default rate.
       - Recommendation: Implement an automated alert in the underwriting system for manual review.
   - Marketing Insight: A "High-Potential" segment non-loan customers was identified (CIBIL > 750, Tenure > 3 years, Total Wealth > $20k).
       - Recommendation: Launch a targeted, "pre-approved" loan campaign for this segment.
# Results & Feedbacks
  - Identified clear behavioral risk indicators that traditional CIBIL-only checks miss.
  - Built a profile of customers most likely to repay and take larger loans.
  - Delivered practical recommendations for underwriting, marketing, and cross-selling teams.

# Tech Stack
  - Data Aggregation: SQL (MSSQL)
  - Data Analysis & Cleaning: Python (Pandas, NumPy)
  - Data Visualization: PowerBi, Matplotlib, Seaborn
  - PPT presentation: Gamma

# Project Structure
  - Data_creation.py : Contains the python script for generating the data.
  - account_holders.csv/transactions.csv : Contains the data in csv format.
  - sql_aggregation.sql : Contains the query to compute data from both tables into one for simpler analysis
  - FinRisk_analysis.ipynb : Contains the python script of the analytical process.
  - Risk_analysis.sql : The key SQL query used for solving business questions.
  - Risk_analysis.pbix : Contains the PowerBi Dashboard.
  - risk_analysis_summary.pdf : A PDF summary of the business findings.
  - risk_analysis_presentaion.pptx : A PPT presentation of the project.

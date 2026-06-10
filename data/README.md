# Data Layer Infrastructure

## Schema Specification
The execution scripts in `src/` expect a raw source file named `raw_investment_data.csv` placed in this directory containing the following initial layout:

| Column Name | Expected Format | Context |
| :--- | :--- | :--- |
| `Transaction_ID` | String / Numeric | Unique identifier alphanumeric tag |
| `Join_Date` | String (Variable notation) | Registration date requiring standard ISO conversion |
| `Raw_Amount` | String (Currency alphanumeric) | Financial figures requiring numeric cleaning |
| `Growth_Rate` | String (Percentage notation) | Compounding rate indicator |

## Mock Data Generation Script
For testing purposes, run `src/data_cleaning.py` to auto-generate a sample dataset if `raw_investment_data.csv` is absent.

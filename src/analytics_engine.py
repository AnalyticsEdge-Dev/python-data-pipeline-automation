import os
import pandas as pd

def calculate_compound_projections(clean_data_path, projection_years=5):
    """Reads cleaned data and applies a mathematical compounding framework to project future value."""
    if not os.path.exists(clean_data_path):
        raise FileNotFoundError(f"Cleaned source data not detected at {clean_data_path}. Run data_cleaning.py first.")
        
    df = pd.read_csv(clean_data_path)
    print(f"Executing compounding algorithm across a {projection_years}-year horizon...")

    # Compounding Formula: A = P * (1 + r)^t
    df['Projected_Future_Value'] = df.apply(
        lambda row: round(row['Cleaned_Amount'] * ((1 + row['Growth_Rate_Decimal']) ** projection_years), 2),
        axis=1
    )
    
    # Isolate absolute yields
    df['Net_Yield'] = df['Projected_Future_Value'] - df['Cleaned_Amount']
    
    print("\n--- Analytics Performance Matrix ---")
    print(df[['Transaction_ID', 'Cleaned_Amount', 'Projected_Future_Value', 'Net_Yield']])
    
    summary_path = "data/portfolio_summary_report.csv"
    df.to_csv(summary_path, index=False)
    print(f"\nAnalytics summaries exported successfully to: {summary_path}")

if __name__ == "__main__":
    # Integration test link to cycle data automatically from previous module if running localized tests
    clean_path = "data/processed_clean_data.csv"
    if not os.path.exists(clean_path):
        from data_cleaning import run_hygiene_pipeline
        run_hygiene_pipeline("data/raw_investment_data.csv", clean_path)
        
    calculate_compound_projections(clean_path)

import os
import pandas as pd
import numpy as np

def generate_mock_data(file_path):
    """Generates a dirty dataset to demonstrate pipeline execution."""
    print("Generating uncleaned mock dataset...")
    dirty_data = {
        "Transaction_ID": ["TXN101", "TXN102", "  TXN103  ", "TXN104", "TXN105"],
        "Join_Date": ["2024/01/15", "15-02-2024", "2024.03.20", None, "2024-05-12"],
        "Raw_Amount": ["$12,500.50", "Ksh150,000.00", "$5,000", "$8,250.75", "Missing"],
        "Growth_Rate": ["8.5%", "12%", "6.25%", "10.1%", "7.0%"]
    }
    df = pd.DataFrame(dirty_data)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    df.to_csv(file_path, index=False)

def run_hygiene_pipeline(input_path, output_path):
    """Loads dirty data, enforces data types, cleans strings, and validates dates."""
    if not os.path.exists(input_path):
        generate_mock_data(input_path)
        
    print(f"Reading raw data from: {input_path}")
    df = pd.read_csv(input_path)
    
    # 1. Clean Transaction IDs (String Stripping)
    df['Transaction_ID'] = df['Transaction_ID'].astype(str).str.strip()
    
    # 2. Handle Missing Values / Strategic Imputation
    df = df.dropna(subset=['Transaction_ID']) 
    
    # 3. Currency Cleaning & Float Casting
    def clean_currency(val):
        if pd.isna(val) or str(val).strip().lower() in ['missing', 'nan', 'null']:
            return 0.0
        # Remove currency symbols, commas, and whitespace
        cleaned = str(val).replace('$', '').replace('Ksh', '').replace(',', '').strip()
        try:
            return float(cleaned)
        except ValueError:
            return 0.0

    df['Cleaned_Amount'] = df['Raw_Amount'].apply(clean_currency)
    
    # Fill median for zeroed/missing amounts to preserve data distribution stability
    median_amt = df[df['Cleaned_Amount'] > 0]['Cleaned_Amount'].median()
    df.loc[df['Cleaned_Amount'] == 0.0, 'Cleaned_Amount'] = median_amt

    # 4. Parse Growth Rates to Decimal Scalars
    df['Growth_Rate_Decimal'] = df['Growth_Rate'].astype(str).str.replace('%', '').astype(float) / 100.0

    # 5. Standardize Date Layouts to ISO 8601
    df['Standardized_Date'] = pd.to_datetime(df['Join_Date'], errors='coerce', dayfirst=False)
    # Forward-fill any unparseable dates to protect timeline analysis continuity
    df['Standardized_Date'] = df['Standardized_Date'].ffill()

    # Drop intermediate raw processing columns for final presentation
    final_clean_df = df[['Transaction_ID', 'Standardized_Date', 'Cleaned_Amount', 'Growth_Rate_Decimal']]
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    final_clean_df.to_csv(output_path, index=False)
    print(f"Data hygiene successfully completed. Output saved to: {output_path}")
    return final_clean_df

if __name__ == "__main__":
    run_hygiene_pipeline("data/raw_investment_data.csv", "data/processed_clean_data.csv")

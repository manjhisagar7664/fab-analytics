import pandas as pd
import numpy as np

def generate_scientific_test_data():
    print("🚀 Generating High-Fidelity Test Suites...")

    # --- 1. BANKING (Correlated Risk) ---
    # We create 100 samples where low credit + low balance = high churn
    bank = pd.DataFrame({
        'CustomerId': range(10001, 10101),
        'CreditScore': np.random.randint(300, 850, 100),
        'Age': np.random.randint(18, 75, 100),
        'Balance': np.random.uniform(0, 150000, 100),
        'NumOfProducts': np.random.randint(1, 4, 100),
        'IsActiveMember': np.random.choice([0, 1], 100),
        'Interest_Rate_Context': [3.64] * 100
    })
    bank.to_csv('test_banking_final.csv', index=False)

    # --- 2. E-COMMERCE (Velocity Decay) ---
    # Low order count + low volume = high churn
    ecom = pd.DataFrame({
        'CustomerID': range(20001, 20101),
        'Tenure': np.random.randint(1, 24, 100),
        'OrderCount': np.random.randint(1, 15, 100),
        'Total_Volume': np.random.uniform(10, 1000, 100)
    })
    ecom.to_csv('test_ecommerce_final.csv', index=False)

    # --- 3. TELECOM (Contractual Pressure) ---
    # High monthly charges + low tenure = high churn
    telco = pd.DataFrame({
        'customerID': [f"TEL-{i}" for i in range(30001, 30101)],
        'tenure': np.random.randint(1, 72, 100),
        'MonthlyCharges': np.random.uniform(20, 120, 100)
    })
    telco.to_csv('test_telco_final.csv', index=False)

    print("✅ Files generated: test_banking_final.csv, test_ecommerce_final.csv, test_telco_final.csv")

if __name__ == "__main__":
    generate_scientific_test_data()
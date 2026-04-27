import os
import joblib
import pandas as pd
import numpy as np
import shap
from xgboost import XGBClassifier
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler

# --- CONFIG ---
DATA_DIR = 'data'
MODEL_DIR = 'models'
os.makedirs(MODEL_DIR, exist_ok=True)

def get_ensemble_pipeline():
    xgb = XGBClassifier(n_estimators=100, learning_rate=0.05, max_depth=6)
    rf = RandomForestClassifier(n_estimators=100, max_depth=12, n_jobs=-1)
    lr = LogisticRegression(max_iter=2000)
    return Pipeline([
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler()),
        ('classifier', VotingClassifier(estimators=[('xgb', xgb), ('rf', rf), ('lr', lr)], voting='soft'))
    ])

def save_elite_explainer(pipeline, X_sample, model_name):
    print(f"🔬 [STAGE: SHAP] Computing Elite Explainer for {model_name}...")
    preprocessing = Pipeline(steps=pipeline.steps[:-1])
    X_transformed = preprocessing.transform(X_sample)
    xgb_model = pipeline.named_steps['classifier'].estimators_[0] 
    explainer = shap.TreeExplainer(xgb_model)
    joblib.dump(explainer, os.path.join(MODEL_DIR, f'{model_name}_explainer.pkl'))
    joblib.dump(X_transformed, os.path.join(MODEL_DIR, f'{model_name}_base_data.pkl'))
    print(f"✅ {model_name.capitalize()} Explainer Locked.")

def train_banking():
    print("🏦 [TRAINING] Banking Sector...")
    macro_df = pd.read_excel(os.path.join(DATA_DIR, 'FEDFUNDS.xlsx'), sheet_name='Monthly')
    rate = macro_df.sort_values('observation_date').iloc[-1]['FEDFUNDS']
    df = pd.read_csv(os.path.join(DATA_DIR, 'Churn_Modelling.csv'))
    df['Interest_Rate_Context'] = rate
    features = ['CreditScore', 'Age', 'Balance', 'NumOfProducts', 'IsActiveMember', 'Interest_Rate_Context']
    pipe = get_ensemble_pipeline()
    pipe.fit(df[features], df['Exited'])
    joblib.dump(pipe, os.path.join(MODEL_DIR, 'banking_model.pkl'))
    save_elite_explainer(pipe, df[features].head(5000), 'banking')

def train_ecommerce():
    print("🛒 [TRAINING] E-Commerce Sector...")
    path = os.path.join(DATA_DIR, 'online_retail_II.xlsx')
    s1, s2 = pd.read_excel(path, sheet_name='Year 2009-2010'), pd.read_excel(path, sheet_name='Year 2010-2011')
    c1, c2 = set(s1['Customer ID'].dropna().unique()), set(s2['Customer ID'].dropna().unique())
    churned = list(c1 - c2)
    df = s1.groupby('Customer ID').agg({'Quantity': 'sum', 'Invoice': 'count'}).reset_index()
    df.columns = ['CustomerID', 'Total_Volume', 'OrderCount']; df['Churn'] = df['CustomerID'].apply(lambda x: 1 if x in churned else 0); df['Tenure'] = 12
    X = df[['Tenure', 'OrderCount']]
    pipe = get_ensemble_pipeline()
    pipe.fit(X, df['Churn'])
    joblib.dump(pipe, os.path.join(MODEL_DIR, 'ecommerce_model.pkl'))
    save_elite_explainer(pipe, X.head(5000), 'ecommerce')

def train_telco():
    print("📞 [TRAINING] Telecom Sector...")
    df = pd.read_csv(os.path.join(DATA_DIR, 'WA_Fn-UseC_-Telco-Customer-Churn.csv'))
    df['Churn'] = df['Churn'].map({'Yes': 1, 'No': 0})
    features = ['tenure', 'MonthlyCharges']
    pipe = get_ensemble_pipeline()
    pipe.fit(df[features], df['Churn'])
    joblib.dump(pipe, os.path.join(MODEL_DIR, 'telco_model.pkl'))
    save_elite_explainer(pipe, df[features].head(5000), 'telco')

if __name__ == "__main__":
    train_banking()
    train_ecommerce()
    train_telco()
    print("\n👑 TRIPLE-SECTOR ENSEMBLE COMPLETE. ALL MODELS EXPLAINABLE.")
import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
import shap
import numpy as np
from sklearn.pipeline import Pipeline

# --- PAGE CONFIG ---
st.set_page_config(layout="wide", page_title="Fab", page_icon="🛡️")

# --- IMPORT USER MANUAL FUNCTION ---
from manual import render_user_manual  # ✅ Must be imported before use

# --- SIDEBAR ---
with st.sidebar:
    st.title("🛡️ Fab")

    # Button to open manual
    show_manual = st.button("📖 Open User Manual")

    st.divider()
    uploaded_file = st.file_uploader("Upload Sector Data (CSV)", type="csv")

    if uploaded_file:
        mode = st.radio("Navigation", ["Global Overview", "Visual Insights", "Predictive Simulation"])

    st.info("**Engine Status:** Phase 4 (Complete)")

# --- MAIN CONTENT ---
if show_manual:
    render_user_manual()  # ✅ This now works correctly
    st.stop()  # Prevents dashboard from rendering below the manual

# --- TRANSLATION DICTIONARY ---
FEAT_MAP = {
    'OrderCount': 'Engagement', 'Tenure': 'Loyalty', 'tenure': 'Account Age', 
    'CreditScore': 'Credit Standing', 'MonthlyCharges': 'Billing Level', 
    'Balance': 'Account Balance', 'NumOfProducts': 'Service Count'
}


# --- DATA ROUTING ---
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    cols = df.columns
    sector, model_path, expl_path, feat_cols, id_col = None, None, None, None, None

    if 'CreditScore' in cols:
        sector, model_path, expl_path = "Banking", 'models/banking_model.pkl', 'models/banking_explainer.pkl'
        feat_cols, id_col = ['CreditScore', 'Age', 'Balance', 'NumOfProducts', 'IsActiveMember', 'Interest_Rate_Context'], 'CustomerId'
    elif 'OrderCount' in cols:
        sector, model_path, expl_path = "E-Commerce", 'models/ecommerce_model.pkl', 'models/ecommerce_explainer.pkl'
        feat_cols, id_col = ['Tenure', 'OrderCount'], 'CustomerID'
    elif 'tenure' in cols:
        sector, model_path, expl_path = "Telecom", 'models/telco_model.pkl', 'models/telco_explainer.pkl'
        feat_cols, id_col = ['tenure', 'MonthlyCharges'], 'customerID'

    # LOAD MODELS
    pipe = joblib.load(model_path)
    explainer = joblib.load(expl_path)
    
    # CALCULATE RISK
    probs = pipe.predict_proba(df[feat_cols])[:, 1]
    df['Risk_Score'] = (probs * 100).round(1)
    df['Status'] = df['Risk_Score'].apply(lambda x: "🟢 Stable" if x <= 40 else ("🟡 Warning" if x <= 70 else "🔴 Critical"))

    # SHAP ANALYSIS
    X_proc = Pipeline(steps=pipe.steps[:-1]).transform(df[feat_cols])
    shap_v = explainer(X_proc)
    
    reasons = []
    for i in range(len(df)):
        idx = np.argmax(shap_v.values[i])
        reasons.append(f"Optimize {FEAT_MAP.get(feat_cols[idx], feat_cols[idx])}")
    df['Strategic_Focus'] = reasons

    # --- VIEW: GLOBAL OVERVIEW ---
    if mode == "Global Overview":
        st.header(f"📈 {sector} Intelligence")
        c1, c2, c3 = st.columns(3)
        c1.metric("Total Base", len(df))
        c2.metric("Avg Risk", f"{df['Risk_Score'].mean():.1f}%")
        c3.metric("Critical Alerts", len(df[df['Risk_Score'] > 70]))
        st.dataframe(df[[id_col, 'Risk_Score', 'Status', 'Strategic_Focus']].sort_values('Risk_Score', ascending=False), use_container_width=True)

    # --- VIEW: VISUAL INSIGHTS ---
    elif mode == "Visual Insights":
        st.header("📊 Market Trends")
        col_a, col_b = st.columns(2)
        
        with col_a:
            st.subheader("Account Health Breakdown")
            fig1, ax1 = plt.subplots()
            counts = df['Status'].value_counts()
            ax1.pie(counts, labels=counts.index, autopct='%1.1f%%', colors=['#2ecc71', '#f1c40f', '#e74c3c'])
            fig1.patch.set_facecolor('none')
            st.pyplot(fig1)
            
        with col_b:
            st.subheader("Risk Progression Trend")
            # Create the specific clean line graph style you shared
            # We sort by the main feature to get a clean upwards/downwards line
            main_f = feat_cols[0]
            trend_data = df.groupby(main_f)['Risk_Score'].mean().reset_index()
            fig2, ax2 = plt.subplots()
            # Clean blue line with markers like the image
            sns.lineplot(data=trend_data, x=main_f, y='Risk_Score', marker='o', color='#3498db', linewidth=2.5)
            ax2.set_xlabel(FEAT_MAP.get(main_f, main_f))
            ax2.grid(True, alpha=0.2)
            fig2.patch.set_facecolor('none')
            st.pyplot(fig2)

    # --- VIEW: PREDICTIVE SIMULATION ---
    else:
        st.header("🔮 Simulation: Strategic Intervention")
        target_id = st.selectbox("Select Client ID", df[id_col].tolist())
        cust_row = df[df[id_col] == target_id].iloc[0]
        
        st.divider()
        L, R = st.columns([1, 1])
        
        with L:
            st.subheader("🛠️ Apply Retain Strategies")
            # Custom Strategic Sliders
            discount = st.slider("Apply Discount (%)", 0, 50, 0)
            combo = st.checkbox("Apply 'Combo Offer' (Add Service)")
            disputes = st.select_slider("Dispute Resolution Status", options=["Pending Tickets", "Reviewing", "Resolved"])
            
            # Prepare data for new prediction
            sim_data = cust_row[feat_cols].to_frame().T
            
            # Applying Business Logic to Data
            if 'MonthlyCharges' in sim_data.columns:
                sim_data['MonthlyCharges'] *= (1 - (discount/100))
            if combo and 'NumOfProducts' in sim_data.columns:
                sim_data['NumOfProducts'] += 1
            if disputes == "Resolved" and 'IsActiveMember' in sim_data.columns:
                sim_data['IsActiveMember'] = 1 # Simulating an active, happy user

            if st.button("Run Simulation", type="primary"):
                new_p = pipe.predict_proba(sim_df := sim_data[feat_cols])[:, 1][0]
                new_s = round(new_p * 100, 1)
                old_s = cust_row['Risk_Score']
                
                st.subheader("Simulation Results")
                st.metric("New Predicted Risk", f"{new_s}%", delta=f"{round(new_s - old_s, 1)}%", delta_color="inverse")
                
                if new_s < old_s:
                    st.success("✅ Positive Impact: This strategy is expected to stabilize the account.")
                else:
                    st.warning("⚠️ Neutral Impact: Additional intervention may be required.")

        with R:
            st.subheader("Current Profile")
            st.write(cust_row[feat_cols].to_frame(name="Value"))
            st.info(f"**AI Focus Area:** {cust_row['Strategic_Focus']}")

else:
    st.info("### 🛡️ Fab Ready\nUpload a data file to begin analysis.")

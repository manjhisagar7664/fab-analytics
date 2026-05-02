# manual.py
import streamlit as st

def render_user_manual():
    """Displays the FAB User Manual in the main content area."""
    st.title("📖 FAB User Manual")
    st.markdown("---")

    st.header("1. System Overview")
    st.write("""
    FAB is a multi-sector churn prediction and retention analytics tool. 
    It uses trained AI models to calculate risk scores, explain drivers of churn, 
    and simulate retention strategies across Banking, Telecom, and E-Commerce sectors.
    """)

    st.header("2. Uploading Data")
    st.write("""
    Upload a **CSV file** containing customer-level data. 
    The app automatically detects the sector based on column names.
    """)

    st.subheader("2.1 Banking Sector")
    st.markdown("""
    **Required Columns:**
    - `CreditScore`
    - `Age`
    - `Balance`
    - `NumOfProducts`
    - `IsActiveMember`
    - `Interest_Rate_Context`
    """)

    st.subheader("2.2 Telecom Sector")
    st.markdown("""
    **Required Columns:**
    - `tenure`
    - `MonthlyCharges`
    """)

    st.subheader("2.3 E-Commerce Sector")
    st.markdown("""
    **Required Columns:**
    - `Tenure`
    - `OrderCount`
    """)

    st.header("3. Dashboard Options")
    st.write("After uploading, choose a mode from the sidebar:")

    st.markdown("""
    - **Global Overview**  
      • Shows total customer base, average risk score, and number of critical alerts  
      • Displays a sortable table with Risk Score, Status, and Strategic Focus  

    - **Visual Insights**  
      • Pie chart of account health breakdown (Stable, Warning, Critical)  
      • Line chart showing risk progression trend by main feature  

    - **Predictive Simulation**  
      • Select a customer ID  
      • Apply retention strategies (discounts, combo offers, dispute resolution)  
      • Run simulation to see impact on risk score  
    """)

    st.header("4. Outputs")
    st.markdown("""
    - **Risk_Score:** Probability of churn (0–100%)  
    - **Status:** 🟢 Stable, 🟡 Warning, 🔴 Critical  
    - **Strategic_Focus:** Feature most influencing churn, derived from SHAP analysis  
    """)

    st.header("5. Simulation Controls")
    st.markdown("""
    - **Discount (%):** Reduce monthly charges  
    - **Combo Offer:** Add an extra product/service  
    - **Dispute Resolution:** Mark customer as satisfied (active member)  
    """)

    st.header("6. Exporting Results")
    st.write("Use Streamlit’s built-in download options to export tables as CSV.")

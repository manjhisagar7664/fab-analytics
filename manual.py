# manual.py
import streamlit as st

def render_user_manual():
    """Renders the FAB User Manual and Operation Instructions."""
    st.markdown("---")
    with st.expander("📖 FAB User Manual"):
        st.subheader("1. System Overview")
        st.caption("Analytical framework for multi-sector churn prediction using an Ensemble Engine.")

        st.subheader("2. Input Schemas")
        st.markdown("""
        - **Banking**: `CreditScore`, `Age`, `Balance`
        - **Telecom**: `tenure`, `MonthlyCharges`
        - **E-Commerce**: `Tenure`, `OrderCount`
        """)

        st.subheader("3. Operation Steps")
        st.markdown("""
        1. **Upload**: Use the UI to submit a CSV/Excel file.
        2. **Filter**: Tap the **'Eye'** icon to toggle visible metrics.
        3. **Export**: Use the **'Download'** button to save results as a CSV.
        """)

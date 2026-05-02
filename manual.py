import streamlit as st

def render_user_manual():
    """Renders the FAB User Manual and Operation Instructions."""
    st.sidebar.markdown("---")
    with st.sidebar.expander("📖 FAB User Manual"):
        st.subheader("1. System Overview")
        st.caption("Analytical framework for multi-sector churn prediction using an Ensemble Engine.")

        st.subheader("2. Input Schemas")
        st.markdown("""
        - **Banking**: `CreditScore`, `Age`, `Balance`[cite: 4]
        - **Telecom**: `tenure`, `MonthlyCharges`[cite: 4]
        - **E-Commerce**: `Tenure`, `OrderCount`[cite: 4]
        """)

        st.subheader("3. Operation Steps")
        st.markdown("""
        1. **Upload**: Use the UI to submit a CSV/Excel file[cite: 4].
        2. **Filter**: Tap the **'Eye'** icon to toggle visible metrics[cite: 4].
        3. **Export**: Use the **'Download'** button to save results as a CSV[cite: 4].
        """)

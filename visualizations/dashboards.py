import streamlit as st

def create_metrics_dashboard(col1_val, col2_val, col3_val):
    """Membuat dashboard metrics"""
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Metric 1", col1_val)
    with col2:
        st.metric("Metric 2", col2_val)
    with col3:
        st.metric("Metric 3", col3_val)

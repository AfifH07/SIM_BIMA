import pandas as pd
import streamlit as st

def load_csv(file):
    """Load CSV file"""
    try:
        df = pd.read_csv(file)
        return df
    except Exception as e:
        st.error(f"Error loading CSV: {e}")
        return None

def load_excel(file):
    """Load Excel file"""
    try:
        df = pd.read_excel(file)
        return df
    except Exception as e:
        st.error(f"Error loading Excel: {e}")
        return None

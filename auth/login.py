import streamlit as st

def login_page():
    """Halaman login"""
    st.title("Login")
    
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        # Implementasi autentikasi
        pass

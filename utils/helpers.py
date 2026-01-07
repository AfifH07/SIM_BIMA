import streamlit as st

def show_success(message):
    """Menampilkan pesan sukses"""
    st.success(message)

def show_error(message):
    """Menampilkan pesan error"""
    st.error(message)

def show_warning(message):
    """Menampilkan pesan warning"""
    st.warning(message)

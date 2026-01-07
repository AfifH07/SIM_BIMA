# File: pages/1_🏠_Beranda.py
import streamlit as st
import sys
from pathlib import Path

# Tambahkan root directory ke path untuk import
root_dir = Path(__file__).parent.parent
sys.path.append(str(root_dir))

from components.sidebar import render_top_navigation, hide_default_sidebar

# Set page config (HARUS di paling atas)
st.set_page_config(
    page_title="Beranda - SIM Akademik",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Panggil fungsi sidebar
hide_default_sidebar()
render_top_navigation()

# Set current page untuk highlight menu
st.session_state['current_page'] = '🏠 Beranda'

# ============================================
# KONTEN HALAMAN BERANDA
# ============================================

st.title("🏠 Beranda")
st.markdown("---")

# Your page content here...
st.write("Selamat datang di SIM Akademik")

# Contoh konten
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Mahasiswa", "1,234", "+12")

with col2:
    st.metric("Rata-rata IPK", "3.45", "+0.05")

with col3:
    st.metric("Tingkat Kelulusan", "92%", "+3%")
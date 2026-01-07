import streamlit as st
import pandas as pd
from pathlib import Path
import sys

# Path setup
if 'path_initialized' not in st.session_state:
    root_dir = Path(__file__).parent.parent
    if str(root_dir) not in sys.path:
        sys.path.insert(0, str(root_dir))
    st.session_state.path_initialized = True

# Imports
from components.header import render_page_header, add_page_style
from components.sidebar import render_custom_sidebar
from components.footer import render_minimal_footer

# Page setup
add_page_style()
render_custom_sidebar()

# Page header
render_page_header(
    title="Prediksi Kelulusan",
    icon="🎓",
    description="Sistem prediksi kelulusan berbasis machine learning"
)

# Main content
st.markdown("### 🤖 Model Prediksi")

if 'df_clean' in st.session_state and st.session_state['df_clean'] is not None:
    df = st.session_state['df_clean']
    
    st.info("ℹ️ **Fitur prediksi kelulusan akan segera hadir!**")
    
    # Placeholder untuk model info
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Model", "Random Forest")
    
    with col2:
        st.metric("Accuracy", "92%")
    
    with col3:
        st.metric("Features", "15")
    
    st.markdown("---")
    
    # Form input untuk prediksi individual
    st.markdown("### 📝 Prediksi Individual")
    
    with st.form("prediction_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            nama = st.text_input("Nama Siswa")
            nisn = st.text_input("NISN")
        
        with col2:
            nilai_rata = st.number_input("Rata-rata Nilai", min_value=0.0, max_value=100.0, value=75.0)
            kehadiran = st.slider("Kehadiran (%)", 0, 100, 90)
        
        submitted = st.form_submit_button("🎯 Prediksi", type="primary")
        
        if submitted:
            # Placeholder untuk hasil prediksi
            st.success("✅ Hasil Prediksi:")
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Status", "LULUS", delta="Confidence: 95%")
            with col2:
                st.metric("Probabilitas", "95%")

else:
    st.warning("⚠️ Belum ada data. Silakan upload data terlebih dahulu.")
    
    if st.button("📤 Ke Halaman Upload", type="primary"):
        st.switch_page("pages/5_📤_Upload_Data.py")

# Footer
render_minimal_footer()
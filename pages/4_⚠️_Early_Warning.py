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
    title="Early Warning System",
    icon="⚠️",
    description="Sistem deteksi dini siswa berisiko gagal"
)

# Main content
if 'df_clean' in st.session_state and st.session_state['df_clean'] is not None:
    df = st.session_state['df_clean']
    
    # Threshold settings
    st.markdown("### ⚙️ Pengaturan Threshold")
    
    col1, col2 = st.columns(2)
    with col1:
        threshold_nilai = st.slider("Threshold Nilai Berisiko", 0, 100, 60)
    with col2:
        threshold_kehadiran = st.slider("Threshold Kehadiran (%)", 0, 100, 75)
    
    st.markdown("---")
    
    # Find at-risk students
    if 'NILAI' in df.columns:
        at_risk = df[df['NILAI'] < threshold_nilai]
        
        # Metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            total_siswa = df['NISN'].nunique() if 'NISN' in df.columns else len(df)
            st.metric("Total Siswa", total_siswa)
        
        with col2:
            at_risk_count = len(at_risk)
            st.metric("Siswa Berisiko", at_risk_count, delta=f"{(at_risk_count/len(df)*100):.1f}%")
        
        with col3:
            safe_count = len(df) - at_risk_count
            st.metric("Siswa Aman", safe_count)
        
        st.markdown("---")
        
        # Display at-risk students
        if not at_risk.empty:
            st.error(f"🚨 Ditemukan {len(at_risk)} data dengan nilai di bawah {threshold_nilai}")
            
            # Show data
            display_columns = ['NAMA_SISWA', 'NISN', 'NILAI', 'MAPEL_ID'] if all(col in at_risk.columns for col in ['NAMA_SISWA', 'NISN', 'NILAI', 'MAPEL_ID']) else at_risk.columns[:4]
            
            st.dataframe(
                at_risk[display_columns].head(20),
                use_container_width=True
            )
            
            # Download button
            csv = at_risk.to_csv(index=False).encode('utf-8-sig')
            st.download_button(
                label="📥 Download Data Siswa Berisiko",
                data=csv,
                file_name=f"siswa_berisiko_{pd.Timestamp.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
        else:
            st.success("✅ Tidak ada siswa berisiko ditemukan!")
    
    else:
        st.warning("⚠️ Kolom 'NILAI' tidak ditemukan dalam data.")

else:
    st.warning("⚠️ Belum ada data. Silakan upload data terlebih dahulu.")
    
    if st.button("📤 Ke Halaman Upload", type="primary"):
        st.switch_page("pages/5_📤_Upload_Data.py")

# Footer
render_minimal_footer()
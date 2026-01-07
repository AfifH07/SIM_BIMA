import streamlit as st
import pandas as pd
from datetime import datetime
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
    title="Laporan",
    icon="📋",
    description="Generate dan export laporan akademik"
)

# Main content
if 'df_clean' in st.session_state and st.session_state['df_clean'] is not None:
    df = st.session_state['df_clean']
    
    st.markdown("### 📊 Generate Laporan")
    
    # Report configuration
    col1, col2 = st.columns(2)
    
    with col1:
        report_type = st.selectbox(
            "Jenis Laporan",
            [
                "Laporan Nilai Keseluruhan",
                "Laporan Per Siswa",
                "Laporan Per Mata Pelajaran",
                "Laporan Kelulusan",
                "Laporan Siswa Berisiko"
            ]
        )
    
    with col2:
        format_type = st.selectbox(
            "Format Export",
            ["CSV", "Excel", "PDF"]
        )
    
    # Date range
    st.markdown("#### 📅 Periode Laporan")
    col1, col2 = st.columns(2)
    
    with col1:
        start_date = st.date_input("Dari Tanggal", datetime.now())
    
    with col2:
        end_date = st.date_input("Sampai Tanggal", datetime.now())
    
    # Additional filters
    with st.expander("🔧 Filter Tambahan", expanded=False):
        if 'SEMESTER' in df.columns:
            semester = st.multiselect("Semester", df['SEMESTER'].unique())
        
        if 'MAPEL_ID' in df.columns:
            mapel = st.multiselect("Mata Pelajaran", df['MAPEL_ID'].unique())
    
    st.markdown("---")
    
    # Generate button
    if st.button("📥 Generate Laporan", type="primary", use_container_width=True):
        with st.spinner("Generating laporan..."):
            # Simulate processing
            import time
            time.sleep(1)
            
            st.success(f"✅ Laporan {report_type} berhasil dibuat!")
            
            # Preview
            st.markdown("### 👁 Preview Laporan")
            st.dataframe(df.head(10), use_container_width=True)
            
            # Download button
            if format_type == "CSV":
                csv = df.to_csv(index=False).encode('utf-8-sig')
                st.download_button(
                    label="📥 Download Laporan CSV",
                    data=csv,
                    file_name=f"laporan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            
            elif format_type == "Excel":
                try:
                    from io import BytesIO
                    buffer = BytesIO()
                    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                        df.to_excel(writer, index=False)
                    
                    st.download_button(
                        label="📥 Download Laporan Excel",
                        data=buffer.getvalue(),
                        file_name=f"laporan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True
                    )
                except:
                    st.error("❌ Excel export memerlukan library openpyxl")
            
            elif format_type == "PDF":
                st.info("ℹ️ PDF export akan segera hadir!")

else:
    st.warning("⚠️ Belum ada data. Silakan upload data terlebih dahulu.")
    
    if st.button("📤 Ke Halaman Upload", type="primary"):
        st.switch_page("pages/5_📤_Upload_Data.py")

# Footer
render_minimal_footer()
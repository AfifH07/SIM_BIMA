import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
import sys

# Path setup (one-time)
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
    title="Analisis Performa",
    icon="📊",
    description="Dashboard dan analisis performa akademik siswa"
)

# Main content
if 'df_clean' in st.session_state and st.session_state['df_clean'] is not None:
    df = st.session_state['df_clean']
    
    # Overview metrics
    st.markdown("### 📈 Overview Performa")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_siswa = df['NISN'].nunique() if 'NISN' in df.columns else len(df)
        st.metric("Total Siswa", f"{total_siswa:,}")
    
    with col2:
        if 'NILAI' in df.columns:
            avg_nilai = df['NILAI'].mean()
            st.metric("Rata-rata Nilai", f"{avg_nilai:.2f}")
        else:
            st.metric("Rata-rata Nilai", "-")
    
    with col3:
        if 'NILAI' in df.columns:
            nilai_tertinggi = df['NILAI'].max()
            st.metric("Nilai Tertinggi", f"{nilai_tertinggi:.2f}")
        else:
            st.metric("Nilai Tertinggi", "-")
    
    with col4:
        if 'NILAI' in df.columns:
            nilai_terendah = df['NILAI'].min()
            st.metric("Nilai Terendah", f"{nilai_terendah:.2f}")
        else:
            st.metric("Nilai Terendah", "-")
    
    st.markdown("---")
    
    # Tabs untuk berbagai analisis
    tab1, tab2, tab3 = st.tabs(["📊 Distribusi Nilai", "👥 Analisis Siswa", "📚 Analisis Mapel"])
    
    with tab1:
        if 'NILAI' in df.columns:
            st.markdown("#### Histogram Distribusi Nilai")
            fig = px.histogram(
                df,
                x='NILAI',
                nbins=30,
                title='Distribusi Nilai Keseluruhan',
                labels={'NILAI': 'Nilai', 'count': 'Jumlah'},
                color_discrete_sequence=['#3B82F6']
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Box plot
            st.markdown("#### Box Plot Nilai")
            fig = px.box(
                df,
                y='NILAI',
                title='Box Plot Distribusi Nilai'
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.markdown("#### 🔝 Top 10 Siswa")
        if 'NAMA_SISWA' in df.columns and 'NILAI' in df.columns:
            top_students = df.groupby('NAMA_SISWA')['NILAI'].mean().sort_values(ascending=False).head(10)
            
            fig = px.bar(
                x=top_students.index,
                y=top_students.values,
                labels={'x': 'Nama Siswa', 'y': 'Rata-rata Nilai'},
                title='Top 10 Siswa Berdasarkan Rata-rata Nilai'
            )
            fig.update_xaxis(tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)
            
            # Table
            st.dataframe(
                top_students.reset_index().rename(columns={'NAMA_SISWA': 'Nama', 'NILAI': 'Rata-rata'}),
                use_container_width=True
            )
    
    with tab3:
        if 'MAPEL_ID' in df.columns and 'NILAI' in df.columns:
            st.markdown("#### Performa per Mata Pelajaran")
            
            mapel_stats = df.groupby('MAPEL_ID')['NILAI'].agg(['mean', 'min', 'max', 'count']).round(2)
            mapel_stats.columns = ['Rata-rata', 'Minimum', 'Maksimum', 'Jumlah Data']
            
            st.dataframe(
                mapel_stats.sort_values('Rata-rata', ascending=False),
                use_container_width=True
            )
            
            # Bar chart
            fig = px.bar(
                x=mapel_stats.index,
                y=mapel_stats['Rata-rata'],
                labels={'x': 'Mata Pelajaran', 'y': 'Rata-rata Nilai'},
                title='Rata-rata Nilai per Mata Pelajaran'
            )
            fig.update_xaxis(tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)

else:
    st.warning("⚠️ Belum ada data. Silakan upload data terlebih dahulu di halaman **📤 Upload Data**.")
    
    if st.button("📤 Ke Halaman Upload", type="primary"):
        st.switch_page("pages/5_📤_Upload_Data.py")

# Footer
render_minimal_footer()
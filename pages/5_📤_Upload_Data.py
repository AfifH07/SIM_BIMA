"""
Upload Data Page - SIM Akademik
Halaman untuk upload dan processing data leger
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from pathlib import Path
import sys

# ============================================
# PATH SETUP (One-time at module level)
# ============================================
if 'path_initialized' not in st.session_state:
    root_dir = Path(__file__).parent.parent
    if str(root_dir) not in sys.path:
        sys.path.insert(0, str(root_dir))
    st.session_state.path_initialized = True

# ============================================
# IMPORTS
# ============================================
from components.header import render_page_header, add_page_style
from components.sidebar import render_custom_sidebar
from components.footer import render_minimal_footer

# Import utilities
from utils.data_processor import load_and_process_excel
from utils.leger_cleaner import (
    create_student_summary, 
    create_subject_analysis, 
    save_clean_data
)

# ============================================
# PAGE SETUP
# ============================================
add_page_style()  # Add custom CSS
render_custom_sidebar()  # Render sidebar content

# ============================================
# HELPER FUNCTIONS
# ============================================

def display_upload_stats(df_clean):
    """Display quick statistics after upload"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "📊 Total Records",
            f"{len(df_clean):,}",
            help="Jumlah total data"
        )
    
    with col2:
        if 'NISN' in df_clean.columns:
            unique_students = df_clean['NISN'].nunique()
            st.metric(
                "👨‍🎓 Jumlah Siswa",
                f"{unique_students:,}",
                help="Siswa unik berdasarkan NISN"
            )
        else:
            st.metric("👨‍🎓 Jumlah Siswa", "N/A")
    
    with col3:
        if 'NILAI' in df_clean.columns:
            avg_score = df_clean['NILAI'].mean()
            st.metric(
                "📈 Rata-rata Nilai",
                f"{avg_score:.2f}",
                help="Rata-rata nilai keseluruhan"
            )
        else:
            st.metric("📈 Rata-rata Nilai", "N/A")
    
    with col4:
        if 'MAPEL_ID' in df_clean.columns:
            unique_subjects = df_clean['MAPEL_ID'].nunique()
            st.metric(
                "📚 Jumlah Mapel",
                f"{unique_subjects}",
                help="Mata pelajaran unik"
            )
        else:
            st.metric("📚 Jumlah Mapel", "N/A")


def display_grade_distribution(df):
    """Display grade distribution pie chart"""
    bins = [0, 60, 70, 80, 90, 100]
    labels = ['E (<60)', 'D (60-70)', 'C (70-80)', 'B (80-90)', 'A (90-100)']
    df['GRADE'] = pd.cut(df['NILAI'], bins=bins, labels=labels, include_lowest=True)
    
    grade_counts = df['GRADE'].value_counts().reset_index()
    grade_counts.columns = ['Grade', 'Count']
    
    fig = px.pie(
        grade_counts,
        values='Count',
        names='Grade',
        title='Distribusi Grade Nilai',
        color_discrete_sequence=px.colors.sequential.RdBu,
        hole=0.4
    )
    
    fig.update_traces(
        textposition='inside',
        textinfo='percent+label',
        hovertemplate='<b>%{label}</b><br>Jumlah: %{value}<br>Persentase: %{percent}<extra></extra>'
    )
    
    return fig


def display_student_ranking(df):
    """Display top students ranking"""
    summary = create_student_summary(df)
    
    if not summary.empty:
        # Add ranking column
        summary['RANKING'] = range(1, len(summary) + 1)
        summary = summary[['RANKING', 'NAMA_SISWA', 'RATA_RATA', 'JUMLAH_MAPEL']]
        
        # Display top 10 in table
        st.markdown("#### 🏆 Top 10 Siswa Terbaik")
        st.dataframe(
            summary.head(10).style.background_gradient(
                subset=['RATA_RATA'],
                cmap='RdYlGn',
                vmin=0,
                vmax=100
            ),
            use_container_width=True,
            hide_index=True
        )
        
        # Bar chart
        fig = px.bar(
            summary.head(10),
            x='NAMA_SISWA',
            y='RATA_RATA',
            color='RATA_RATA',
            title='Visualisasi Top 10 Siswa',
            labels={'NAMA_SISWA': 'Nama Siswa', 'RATA_RATA': 'Rata-rata Nilai'},
            color_continuous_scale='RdYlGn',
            text='RATA_RATA'
        )
        
        fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
        fig.update_layout(
            xaxis_tickangle=-45,
            showlegend=False,
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        return summary
    
    return pd.DataFrame()

# ============================================
# MAIN PAGE CONTENT
# ============================================

# Page header
render_page_header(
    title="Upload & Processing Data",
    icon="📤",
    description="Unggah dan proses data leger nilai rapor dengan mudah"
)

# Sidebar settings (will appear in the actual sidebar)
with st.sidebar:
    st.markdown("---")
    st.markdown("### ⚙️ Pengaturan Upload")
    
    file_type = st.selectbox(
        "📋 Jenis File",
        ["Data Leger", "Data Siswa", "Data Nilai", "Data Presensi"],
        help="Pilih jenis data yang akan diupload"
    )
    
    auto_save = st.checkbox("💾 Simpan otomatis", value=True)
    show_raw = st.checkbox("👁️ Tampilkan data mentah", value=False)
    
    st.markdown("---")
    st.info("""
    **📌 Format yang didukung:**
    - CSV (.csv)
    - Excel (.xlsx, .xls)
    
    **💡 Tips:**
    - Pastikan format data sesuai
    - Maksimal ukuran file: 200MB
    """)

# Main tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "📤 Upload Data", 
    "👁 Preview Data", 
    "📊 Analisis", 
    "💾 Riwayat Upload"
])

# ============================================
# TAB 1: UPLOAD DATA
# ============================================
with tab1:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📁 Upload File Data")
        
        uploaded_file = st.file_uploader(
            f"Pilih file {file_type}",
            type=['csv', 'xlsx', 'xls'],
            help="Drag and drop atau klik untuk memilih file",
            key="file_uploader"
        )
    
    with col2:
        st.markdown("### 📋 Template")
        st.markdown("""
        Belum punya template?
        
        Download template sesuai kebutuhan:
        """)
        
        # Template download buttons
        if st.button("📥 Template Leger", use_container_width=True):
            st.info("Template akan didownload...")
        
        if st.button("📥 Template Siswa", use_container_width=True):
            st.info("Template akan didownload...")
    
    if uploaded_file is not None:
        st.markdown("---")
        
        # File info
        file_size = uploaded_file.size / 1024  # KB
        st.info(f"📄 **File:** {uploaded_file.name} | 📊 **Ukuran:** {file_size:.2f} KB")
        
        # Process button
        if st.button("🚀 Proses Data", type="primary", use_container_width=True):
            # Processing with progress
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                # Step 1: Reading file
                status_text.text("📖 Membaca file...")
                progress_bar.progress(25)
                
                # Step 2: Processing
                status_text.text("⚙️ Memproses data...")
                progress_bar.progress(50)
                
                if file_type == "Data Leger":
                    df_clean, stats = load_and_process_excel(uploaded_file, 'leger')
                else:
                    df_clean, stats = load_and_process_excel(uploaded_file, 'general')
                
                progress_bar.progress(75)
                
                # Step 3: Saving
                if not df_clean.empty:
                    status_text.text("💾 Menyimpan data...")
                    
                    # Save to session state
                    st.session_state['df_clean'] = df_clean
                    st.session_state['file_name'] = uploaded_file.name
                    st.session_state['upload_time'] = datetime.now()
                    st.session_state['file_type'] = file_type
                    
                    # Add to upload history
                    if 'upload_history' not in st.session_state:
                        st.session_state['upload_history'] = []
                    
                    st.session_state['upload_history'].append({
                        'filename': uploaded_file.name,
                        'timestamp': datetime.now(),
                        'records': len(df_clean),
                        'type': file_type
                    })
                    
                    progress_bar.progress(100)
                    status_text.empty()
                    
                    # Success message
                    st.success("✅ Data berhasil diproses!")
                    st.balloons()
                    
                    # Display stats
                    st.markdown("### 📊 Ringkasan Data")
                    display_upload_stats(df_clean)
                    
                    # Auto save
                    if auto_save:
                        with st.spinner("💾 Menyimpan file..."):
                            save_results = save_clean_data(df_clean)
                            st.session_state['save_paths'] = save_results
                            st.success(f"✅ File tersimpan: `{save_results['csv_path']}`")
                    
                    # Download buttons
                    st.markdown("---")
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        csv = df_clean.to_csv(index=False).encode('utf-8-sig')
                        st.download_button(
                            label="📥 Download CSV",
                            data=csv,
                            file_name=f"cleaned_{uploaded_file.name.rsplit('.', 1)[0]}.csv",
                            mime="text/csv",
                            use_container_width=True
                        )
                    
                    with col2:
                        # Excel download (if openpyxl available)
                        try:
                            from io import BytesIO
                            buffer = BytesIO()
                            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                                df_clean.to_excel(writer, index=False)
                            
                            st.download_button(
                                label="📥 Download Excel",
                                data=buffer.getvalue(),
                                file_name=f"cleaned_{uploaded_file.name.rsplit('.', 1)[0]}.xlsx",
                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                use_container_width=True
                            )
                        except:
                            st.button("📥 Download Excel", disabled=True, use_container_width=True)
                    
                    with col3:
                        if st.button("🔄 Upload Lagi", use_container_width=True):
                            st.rerun()
                
                else:
                    st.error("❌ Data kosong atau format tidak sesuai!")
                    progress_bar.empty()
                    status_text.empty()
            
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                progress_bar.empty()
                status_text.empty()
    
    else:
        # Upload prompt dengan styling
        st.markdown("""
            <div style="
                border: 2px dashed #ccc;
                border-radius: 15px;
                padding: 60px;
                text-align: center;
                background: #f8f9fa;
                margin: 30px 0;
            ">
                <h3 style="color: #6c757d; margin: 0;">
                    📂 Belum ada file yang dipilih
                </h3>
                <p style="color: #6c757d; margin: 10px 0 0 0;">
                    Silakan upload file menggunakan uploader di atas
                </p>
            </div>
        """, unsafe_allow_html=True)

# ============================================
# TAB 2: PREVIEW DATA
# ============================================
with tab2:
    if 'df_clean' in st.session_state and st.session_state['df_clean'] is not None:
        st.markdown("### 👁 Preview Data Bersih")
        
        df_display = st.session_state['df_clean'].copy()
        
        # Filter controls
        col1, col2, col3 = st.columns(3)
        
        with col1:
            show_rows = st.slider(
                "Jumlah baris",
                min_value=10,
                max_value=min(100, len(df_display)),
                value=20,
                step=10
            )
        
        with col2:
            filter_type = st.selectbox(
                "Filter data",
                ["Semua Data", "Hanya Rerata", "Per Semester"]
            )
        
        with col3:
            if filter_type == "Per Semester" and 'SEMESTER' in df_display.columns:
                selected_semester = st.selectbox(
                    "Pilih Semester",
                    sorted(df_display['SEMESTER'].unique())
                )
        
        # Apply filters
        if filter_type == "Hanya Rerata" and 'IS_RERATA' in df_display.columns:
            df_display = df_display[df_display['IS_RERATA'] == True]
        elif filter_type == "Per Semester" and 'SEMESTER' in df_display.columns:
            df_display = df_display[df_display['SEMESTER'] == selected_semester]
        
        # Search functionality
        search_term = st.text_input("🔍 Cari data", placeholder="Ketik nama siswa, NISN, atau mata pelajaran...")
        if search_term:
            mask = df_display.astype(str).apply(
                lambda x: x.str.contains(search_term, case=False, na=False)
            ).any(axis=1)
            df_display = df_display[mask]
        
        # Display data
        st.dataframe(
            df_display.head(show_rows),
            use_container_width=True,
            height=400
        )
        
        # Data info
        st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            with st.expander("📋 Informasi Struktur Data", expanded=False):
                st.write(f"**Total Baris:** {len(df_display):,}")
                st.write(f"**Total Kolom:** {len(df_display.columns)}")
                st.write(f"**Ukuran Memory:** {df_display.memory_usage(deep=True).sum() / 1024:.2f} KB")
                
                st.markdown("**Daftar Kolom:**")
                for col in df_display.columns:
                    st.write(f"- `{col}`: {df_display[col].dtype}")
        
        with col2:
            if 'NILAI' in df_display.columns:
                with st.expander("📊 Statistik Nilai", expanded=False):
                    stats_df = df_display['NILAI'].describe().to_frame()
                    stats_df.columns = ['Nilai']
                    st.dataframe(stats_df, use_container_width=True)
    
    else:
        st.info("ℹ️ Belum ada data. Silakan upload file terlebih dahulu di tab **Upload Data**.")

# ============================================
# TAB 3: ANALISIS
# ============================================
with tab3:
    if 'df_clean' in st.session_state and st.session_state['df_clean'] is not None:
        df = st.session_state['df_clean']
        
        # Student Ranking
        if all(col in df.columns for col in ['NAMA_SISWA', 'NILAI', 'IS_RERATA']):
            st.markdown("## 🏆 Ranking Siswa")
            display_student_ranking(df)
            st.markdown("---")
        
        # Subject Analysis
        if 'MAPEL_ID' in df.columns:
            st.markdown("## 📚 Analisis Mata Pelajaran")
            
            subject_stats = create_subject_analysis(df)
            
            if not subject_stats.empty:
                col1, col2 = st.columns([1, 1])
                
                with col1:
                    st.markdown("#### 📊 Statistik per Mapel")
                    st.dataframe(
                        subject_stats.style.background_gradient(
                            subset=['RATA_RATA'],
                            cmap='RdYlGn'
                        ),
                        use_container_width=True,
                        height=400
                    )
                
                with col2:
                    st.markdown("#### 📦 Distribusi Nilai per Mapel")
                    fig = px.box(
                        df[df['IS_RERATA'] == True] if 'IS_RERATA' in df.columns else df,
                        x='MAPEL_ID',
                        y='NILAI',
                        color='MAPEL_ID',
                        title=''
                    )
                    fig.update_layout(
                        xaxis_tickangle=-45,
                        showlegend=False,
                        height=400
                    )
                    st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("---")
        
        # Overall Distribution
        if 'NILAI' in df.columns:
            st.markdown("## 📈 Distribusi Nilai Keseluruhan")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 📊 Histogram Nilai")
                fig = px.histogram(
                    df,
                    x='NILAI',
                    nbins=20,
                    color_discrete_sequence=['#667eea'],
                    marginal='box'
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.markdown("#### 🎯 Distribusi Grade")
                fig = display_grade_distribution(df)
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
    
    else:
        st.info("ℹ️ Belum ada data untuk dianalisis. Upload file terlebih dahulu.")

# ============================================
# TAB 4: UPLOAD HISTORY
# ============================================
with tab4:
    st.markdown("### 📜 Riwayat Upload")
    
    if 'upload_history' in st.session_state and st.session_state['upload_history']:
        history_df = pd.DataFrame(st.session_state['upload_history'])
        history_df['timestamp'] = pd.to_datetime(history_df['timestamp'])
        history_df = history_df.sort_values('timestamp', ascending=False)
        
        for idx, row in history_df.iterrows():
            with st.container():
                col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
                
                with col1:
                    st.write(f"**📄 {row['filename']}**")
                
                with col2:
                    st.write(f"🕐 {row['timestamp'].strftime('%d/%m/%Y %H:%M')}")
                
                with col3:
                    st.write(f"📊 {row['records']:,} records")
                
                with col4:
                    st.write(f"📋 {row['type']}")
                
                st.markdown("---")
        
        # Clear history button
        if st.button("🗑️ Hapus Riwayat", type="secondary"):
            st.session_state['upload_history'] = []
            st.rerun()
    
    else:
        st.info("ℹ️ Belum ada riwayat upload.")

# Footer
render_minimal_footer()
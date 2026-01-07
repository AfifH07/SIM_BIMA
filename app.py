"""
SIM Akademik - Main Application
Entry point untuk Streamlit Multi-Page App dengan Custom Navigation

Jalankan dengan: streamlit run app.py
"""

import streamlit as st
from pathlib import Path
import sys

# ============================================
# PATH SETUP
# ============================================
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

# ============================================
# PAGE CONFIGURATION
# ============================================
st.set_page_config(
    page_title="SIM Akademik - Beranda",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'mailto:support@simakademik.edu',
        'Report a bug': 'https://github.com/fadenco/sim-akademik/issues',
        'About': "# SIM Akademik v1.0\nSistem Informasi Manajemen Akademik"
    }
)

# ============================================
# IMPORT COMPONENTS
# ============================================
from components.sidebar import render_custom_sidebar
from components.header import render_header, add_page_style
from components.footer import render_footer

# ============================================
# SESSION STATE INITIALIZATION
# ============================================
def init_session_state():
    """Initialize session state variables"""
    
    # App state
    if 'initialized' not in st.session_state:
        st.session_state.initialized = True
    
    # Data state
    if 'df_clean' not in st.session_state:
        st.session_state.df_clean = None
    
    if 'file_name' not in st.session_state:
        st.session_state.file_name = None
    
    if 'upload_time' not in st.session_state:
        st.session_state.upload_time = None
    
    # History
    if 'upload_history' not in st.session_state:
        st.session_state.upload_history = []
    
    # Settings
    if 'theme' not in st.session_state:
        st.session_state.theme = 'light'

# ============================================
# MAIN FUNCTION
# ============================================
def main():
    """Main application entry point"""
    
    # Initialize session state
    init_session_state()
    
    # Add page styling
    add_page_style()
    
    # Render custom header (tanpa page title karena ini home)
    render_header()
    
    # Render custom sidebar (melengkapi sidebar navigation bawaan)
    render_custom_sidebar()
    
    # ============================================
    # HOME PAGE CONTENT
    # ============================================
    st.title("🎓 SELAMAT DATANG DI SIM AKADEMIK")
    st.markdown("---")
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        render_about_section()
    
    with col2:
        render_stats_widget()
        render_recent_activity()
    
    # Quick action buttons
    st.markdown("---")
    render_quick_actions()
    
    # Footer
    render_footer()

# ============================================
# CONTENT SECTIONS
# ============================================

def render_about_section():
    """Render about section"""
    st.markdown("""
    ### 📚 Tentang Sistem
    
    **SIM Akademik** adalah Sistem Informasi Manajemen yang dirancang khusus untuk:
    
    ✅ **Manajemen Data Akademik** - Upload, cleaning, dan pengelolaan data nilai  
    ✅ **Analisis Performa** - Visualisasi dan analisis data siswa  
    ✅ **Prediksi Kelulusan** - Sistem prediksi berbasis machine learning  
    ✅ **Early Warning System** - Deteksi dini siswa berisiko  
    ✅ **Laporan Otomatis** - Generate laporan dalam berbagai format
    
    ### 🚀 Mulai Dengan
    
    1. **Upload Data** - Unggah file Excel data leger
    2. **Analisis** - Lihat dashboard dan statistik
    3. **Prediksi** - Gunakan model prediksi kelulusan
    4. **Laporan** - Export hasil analisis
    
    ---
    
    💡 **Tips:** Gunakan menu navigasi di sidebar untuk berpindah antar halaman.
    """)

def render_stats_widget():
    """Render statistics widget"""
    st.markdown("### 📊 Statistik Sistem")
    
    if st.session_state.df_clean is not None:
        df = st.session_state.df_clean
        
        # Calculate real statistics
        total_students = df['NISN'].nunique() if 'NISN' in df.columns else len(df)
        avg_score = df['NILAI'].mean() if 'NILAI' in df.columns else 0
        total_subjects = df['MAPEL_ID'].nunique() if 'MAPEL_ID' in df.columns else 0
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric(
                "Total Siswa",
                f"{total_students:,}",
                help="Jumlah siswa unik"
            )
            st.metric(
                "Rata-rata Nilai",
                f"{avg_score:.1f}",
                help="Rata-rata nilai keseluruhan"
            )
        
        with col2:
            # Calculate pass rate (assuming passing grade is 60)
            if 'NILAI' in df.columns:
                pass_count = len(df[df['NILAI'] >= 60])
                pass_rate = (pass_count / len(df)) * 100
                st.metric(
                    "Tingkat Kelulusan",
                    f"{pass_rate:.0f}%",
                    help="Persentase nilai >= 60"
                )
            else:
                st.metric("Tingkat Kelulusan", "-")
            
            # Calculate at-risk students
            if 'NILAI' in df.columns:
                at_risk = len(df[df['NILAI'] < 60])
                st.metric(
                    "Siswa Berisiko",
                    f"{at_risk}",
                    delta=f"-{at_risk}" if at_risk > 0 else "0",
                    delta_color="inverse",
                    help="Siswa dengan nilai < 60"
                )
            else:
                st.metric("Siswa Berisiko", "-")
    
    else:
        # Show placeholder when no data
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Siswa", "-")
            st.metric("Rata-rata Nilai", "-")
        with col2:
            st.metric("Tingkat Kelulusan", "-")
            st.metric("Siswa Berisiko", "-")

def render_recent_activity():
    """Render recent activity widget"""
    st.markdown("---")
    st.markdown("### ⚡ Aktivitas Terbaru")
    
    if st.session_state.df_clean is not None:
        df = st.session_state.df_clean
        upload_time = st.session_state.upload_time
        file_name = st.session_state.file_name
        
        # Format timestamp
        if hasattr(upload_time, 'strftime'):
            time_str = upload_time.strftime('%d/%m/%Y %H:%M')
        else:
            time_str = str(upload_time)
        
        # Count unique students
        students = df['NISN'].nunique() if 'NISN' in df.columns else 'N/A'
        
        st.success(f"""
        **📁 Data Aktif:** {file_name}
        - 📅 Upload: {time_str}
        - 📊 Records: {len(df):,}
        - 👥 Siswa: {students}
        """)
    else:
        st.info("""
        ℹ️ **Belum ada data yang diupload**
        
        Silakan upload data melalui halaman **📤 Upload Data** untuk mulai menggunakan sistem.
        """)

def render_quick_actions():
    """Render quick action buttons"""
    st.markdown("### 🚀 Akses Cepat")
    
    cols = st.columns(5)
    
    # Button configurations
    quick_buttons = [
        ("📤", "Upload Data", "pages/5_📤_Upload_Data.py"),
        ("📊", "Dashboard", "pages/2_📊_Analisis_Performa.py"),
        ("🎓", "Prediksi", "pages/3_🎓_Prediksi_Kelulusan.py"),
        ("⚠️", "Warning", "pages/4_⚠️_Early_Warning.py"),
        ("📋", "Laporan", "pages/6_📋_Laporan.py")
    ]
    
    for idx, (icon, label, page_path) in enumerate(quick_buttons):
        with cols[idx]:
            if st.button(
                f"{icon} {label}",
                use_container_width=True,
                key=f"quick_action_{idx}",
                help=f"Navigasi ke {label}"
            ):
                st.switch_page(page_path)

def render_footer():
    """Render footer"""
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 20px;">
        <p style="margin: 5px 0;">
            <strong>SIM Akademik v1.0</strong> - Sistem Informasi Manajemen Akademik
        </p>
        <p style="margin: 5px 0; font-size: 14px;">
            Dikembangkan dengan ❤️ oleh <strong>FADEN CO</strong>
        </p>
        <p style="margin: 5px 0; font-size: 12px; color: #999;">
            © 2024 All Rights Reserved | 
            <a href="mailto:support@simakademik.edu" style="color: #3B82F6;">Support</a> | 
            <a href="https://github.com/fadenco/sim-akademik" style="color: #3B82F6;">GitHub</a>
        </p>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# RUN APPLICATION
# ============================================
if __name__ == "__main__":
    main()
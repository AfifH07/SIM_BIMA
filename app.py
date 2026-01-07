"""
SIM Akademik - Main Application
Entry point untuk Streamlit Multi-Page App dengan desain yang disempurnakan
"""

import streamlit as st
from pathlib import Path
import sys
from datetime import datetime

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
# CUSTOM CSS STYLING
# ============================================
st.markdown("""
    <style>
        /* Main container */
        .block-container {
            padding-top: 1rem;
            padding-bottom: 2rem;
            max-width: 1400px;
        }
        
        /* Hide Streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        
        /* Sidebar styling */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #F8FAFC 0%, #F1F5F9 100%);
        }
        
        /* Sidebar navigation items */
        [data-testid="stSidebarNav"] {
            background-color: transparent;
            padding-top: 1rem;
        }
        
        [data-testid="stSidebarNav"] > ul {
            padding-top: 1rem;
        }
        
        [data-testid="stSidebarNav"] li {
            margin: 0.25rem 0;
        }
        
        [data-testid="stSidebarNav"] a {
            padding: 0.75rem 1rem;
            border-radius: 0.5rem;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        
        [data-testid="stSidebarNav"] a:hover {
            background-color: rgba(59, 130, 246, 0.1);
            transform: translateX(5px);
        }
        
        [data-testid="stSidebarNav"] a[aria-current="page"] {
            background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%);
            color: white !important;
            font-weight: 600;
            box-shadow: 0 2px 8px rgba(59, 130, 246, 0.3);
        }
        
        /* Button styling */
        .stButton > button {
            border-radius: 0.5rem;
            font-weight: 500;
            transition: all 0.3s ease;
            border: none;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        }
        
        /* Metric styling */
        [data-testid="stMetricValue"] {
            font-size: 1.8rem;
            font-weight: 700;
            color: #1E3A8A;
        }
        
        [data-testid="stMetricLabel"] {
            font-size: 0.9rem;
            font-weight: 500;
            color: #64748B;
        }
        
        /* Card styling */
        .info-card {
            background: white;
            border-radius: 1rem;
            padding: 1.5rem;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
            border: 1px solid #E2E8F0;
            transition: all 0.3s ease;
            margin-bottom: 1rem;
        }
        
        .info-card:hover {
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
            transform: translateY(-2px);
        }
        
        /* Stats card */
        .stats-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 1rem;
            padding: 1.5rem;
            text-align: center;
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
            margin-bottom: 1rem;
        }
        
        /* Feature item */
        .feature-item {
            display: flex;
            align-items: flex-start;
            gap: 0.75rem;
            padding: 0.75rem;
            margin: 0.5rem 0;
            border-radius: 0.5rem;
            transition: all 0.3s ease;
            background: white;
        }
        
        .feature-item:hover {
            background-color: #F8FAFC;
            transform: translateX(5px);
        }
        
        /* Quick action button custom */
        .quick-action-btn {
            display: inline-block;
            padding: 1rem 1.5rem;
            background: white;
            border: 2px solid #E2E8F0;
            border-radius: 0.75rem;
            text-align: center;
            transition: all 0.3s ease;
            cursor: pointer;
            margin: 0.5rem;
        }
        
        .quick-action-btn:hover {
            border-color: #3B82F6;
            transform: translateY(-3px);
            box-shadow: 0 6px 16px rgba(59, 130, 246, 0.2);
        }
        
        /* Alert boxes */
        .stAlert {
            border-radius: 0.75rem;
            border-left: 4px solid #3B82F6;
        }
        
        /* Divider */
        hr {
            margin: 2rem 0;
            border: none;
            border-top: 2px solid #E2E8F0;
        }
        
        /* Expander */
        .streamlit-expanderHeader {
            font-weight: 600;
            color: #1E3A8A;
            border-radius: 0.5rem;
        }
    </style>
""", unsafe_allow_html=True)

# ============================================
# SESSION STATE INITIALIZATION
# ============================================
def init_session_state():
    """Initialize session state variables"""
    if 'initialized' not in st.session_state:
        st.session_state.initialized = True
    
    if 'df_clean' not in st.session_state:
        st.session_state.df_clean = None
    
    if 'file_name' not in st.session_state:
        st.session_state.file_name = None
    
    if 'upload_time' not in st.session_state:
        st.session_state.upload_time = None
    
    if 'upload_history' not in st.session_state:
        st.session_state.upload_history = []
    
    if 'theme' not in st.session_state:
        st.session_state.theme = 'light'

# ============================================
# MAIN FUNCTION
# ============================================
def main():
    """Main application entry point"""
    
    # Initialize session state
    init_session_state()
    
    # ============================================
    # HEADER SECTION
    # ============================================
    st.markdown("""
        <div style="
            background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%);
            padding: 2rem;
            margin: -1rem -1rem 2rem -1rem;
            border-radius: 0 0 1rem 1rem;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        ">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
                <div style="display: flex; align-items: center; gap: 1rem;">
                    <div style="font-size: 3rem;">🎓</div>
                    <div>
                        <h1 style="color: white; margin: 0; font-size: 2rem; font-weight: 700;">
                            SIM AKADEMIK
                        </h1>
                        <p style="color: rgba(255, 255, 255, 0.9); margin: 0.5rem 0 0 0; font-size: 1rem;">
                            Sistem Informasi Manajemen Akademik
                        </p>
                    </div>
                </div>
                <div style="text-align: right; color: white;">
                    <div style="font-size: 0.875rem; opacity: 0.9;">Version 1.0</div>
                    <div style="font-size: 0.75rem; opacity: 0.7;">© 2024 FADEN CO</div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # ============================================
    # WELCOME SECTION
    # ============================================
    st.markdown("""
        <div style="text-align: center; margin: 2rem 0;">
            <h1 style="font-size: 2.5rem; color: #1E3A8A; margin: 0;">
                🎓 SELAMAT DATANG DI SIM AKADEMIK
            </h1>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ============================================
    # QUICK ACTION BUTTONS (Top)
    # ============================================
    st.markdown("""
        <h2 style="text-align: center; color: #1E3A8A; margin-bottom: 1rem;">
            🚀 Akses Cepat
        </h2>
    """, unsafe_allow_html=True)
    
    cols = st.columns(5)
    
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
                f"{icon}\n\n**{label}**",
                use_container_width=True,
                key=f"quick_action_{idx}",
                help=f"Navigasi ke {label}"
            ):
                st.switch_page(page_path)
    
    st.markdown("---")
    
    # ============================================
    # MAIN CONTENT AREA
    # ============================================
    col1, col2 = st.columns([2, 1])
    
    with col1:
        render_about_section()
    
    with col2:
        render_stats_widget()
        st.markdown("")
        render_recent_activity()
    
    # ============================================
    # FOOTER
    # ============================================
    st.markdown("---")
    render_footer()

# ============================================
# CONTENT SECTIONS
# ============================================

def render_about_section():
    """Render about section with system features"""
    
    st.markdown("""
        <div class="info-card">
            <h2 style="color: #1E3A8A; margin-top: 0;">
                📊 Tentang Sistem
            </h2>
            <p style="color: #64748B; font-size: 1rem; line-height: 1.6;">
                <strong>SIM Akademik</strong> adalah Sistem Informasi Manajemen yang dirancang khusus untuk 
                membantu pengelolaan dan analisis data akademik siswa secara efisien dan modern.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("")
    
    # Features section
    st.markdown("""
        <div class="info-card">
            <h3 style="color: #1E3A8A; margin-top: 0;">
                ✨ Fitur Utama
            </h3>
        </div>
    """, unsafe_allow_html=True)
    
    features = [
        ("✅", "Manajemen Data Akademik", "Upload, cleaning, dan pengelolaan data nilai"),
        ("✅", "Analisis Performa", "Visualisasi dan analisis data siswa"),
        ("✅", "Prediksi Kelulusan", "Sistem prediksi berbasis machine learning"),
        ("✅", "Early Warning System", "Deteksi dini siswa berisiko"),
        ("✅", "Laporan Otomatis", "Generate laporan dalam berbagai format")
    ]
    
    for icon, title, desc in features:
        st.markdown(f"""
            <div class="feature-item">
                <div style="font-size: 1.5rem;">{icon}</div>
                <div>
                    <strong style="color: #1E3A8A;">{title}</strong><br>
                    <span style="color: #64748B; font-size: 0.9rem;">{desc}</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("")
    
    # Quick start guide
    st.markdown("""
        <div class="info-card">
            <h3 style="color: #1E3A8A; margin-top: 0;">
                🚀 Mulai Dengan
            </h3>
            <ol style="color: #64748B; line-height: 2;">
                <li><strong>Upload Data</strong> - Unggah file Excel data leger</li>
                <li><strong>Analisis</strong> - Lihat dashboard dan statistik</li>
                <li><strong>Prediksi</strong> - Gunakan model prediksi kelulusan</li>
                <li><strong>Laporan</strong> - Export hasil analisis</li>
            </ol>
        </div>
    """, unsafe_allow_html=True)
    
    st.info("💡 **Tips:** Gunakan menu navigasi di sidebar untuk berpindah antar halaman.")

def render_stats_widget():
    """Render statistics widget"""
    
    st.markdown("""
        <div class="stats-card">
            <h3 style="margin: 0 0 1rem 0; color: white;">📊 Statistik Sistem</h3>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("")
    
    if st.session_state.df_clean is not None:
        df = st.session_state.df_clean
        
        # Calculate real statistics
        total_students = df['NISN'].nunique() if 'NISN' in df.columns else len(df)
        avg_score = df['NILAI'].mean() if 'NILAI' in df.columns else 0
        
        st.metric(
            "👥 Total Siswa",
            f"{total_students:,}",
            help="Jumlah siswa unik"
        )
        
        st.metric(
            "📈 Rata-rata Nilai",
            f"{avg_score:.1f}",
            help="Rata-rata nilai keseluruhan"
        )
        
        # Calculate pass rate
        if 'NILAI' in df.columns:
            pass_count = len(df[df['NILAI'] >= 60])
            pass_rate = (pass_count / len(df)) * 100
            st.metric(
                "🎯 Tingkat Kelulusan",
                f"{pass_rate:.0f}%",
                delta=f"{pass_rate - 70:.0f}%" if pass_rate >= 70 else f"{pass_rate - 70:.0f}%",
                delta_color="normal" if pass_rate >= 70 else "inverse",
                help="Persentase nilai >= 60"
            )
        
        # At-risk students
        if 'NILAI' in df.columns:
            at_risk = len(df[df['NILAI'] < 60])
            st.metric(
                "⚠️ Siswa Berisiko",
                f"{at_risk}",
                delta=f"-{at_risk}" if at_risk > 0 else "0",
                delta_color="inverse",
                help="Siswa dengan nilai < 60"
            )
    
    else:
        # Placeholder metrics
        st.metric("👥 Total Siswa", "-", help="Upload data untuk melihat statistik")
        st.metric("📈 Rata-rata Nilai", "-", help="Upload data untuk melihat statistik")
        st.metric("🎯 Tingkat Kelulusan", "-", help="Upload data untuk melihat statistik")
        st.metric("⚠️ Siswa Berisiko", "-", help="Upload data untuk melihat statistik")

def render_recent_activity():
    """Render recent activity widget"""
    
    st.markdown("""
        <div class="info-card">
            <h3 style="color: #1E3A8A; margin-top: 0;">
                ⚡ Aktivitas Terbaru
            </h3>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("")
    
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
**✅ Data Aktif**

📁 **File:** {file_name}  
📅 **Upload:** {time_str}  
📊 **Records:** {len(df):,}  
👥 **Siswa:** {students}
        """)
    else:
        st.info("""
**ℹ️ Belum ada data yang diupload**

Silakan upload data melalui halaman **📤 Upload Data** untuk mulai menggunakan sistem.
        """)
        
        if st.button("📤 Upload Data", type="primary", use_container_width=True, key="upload_from_activity"):
            st.switch_page("pages/5_📤_Upload_Data.py")

def render_footer():
    """Render footer yang BENAR tanpa menampilkan code"""
    
    current_year = datetime.now().year
    
    # Footer container
    st.markdown(f"""
        <div style="
            text-align: center;
            padding: 2rem;
            background: linear-gradient(135deg, #F9FAFB 0%, #F3F4F6 100%);
            border-radius: 1rem;
            margin-top: 2rem;
            border: 1px solid #E2E8F0;
        ">
            <div style="margin-bottom: 1rem;">
                <h3 style="color: #1E3A8A; margin: 0; font-size: 1.25rem; font-weight: 700;">
                    🎓 SIM Akademik
                </h3>
                <p style="color: #64748B; margin: 0.5rem 0; font-size: 0.875rem;">
                    Sistem Informasi Manajemen Akademik
                </p>
            </div>
            
            <div style="margin: 1rem 0;">
                <span style="color: #3B82F6; margin: 0 0.75rem; font-size: 0.875rem; font-weight: 500;">
                    📧 support@simakademik.edu
                </span>
                <span style="color: #CBD5E1;">|</span>
                <span style="color: #3B82F6; margin: 0 0.75rem; font-size: 0.875rem; font-weight: 500;">
                    📚 Dokumentasi
                </span>
                <span style="color: #CBD5E1;">|</span>
                <span style="color: #3B82F6; margin: 0 0.75rem; font-size: 0.875rem; font-weight: 500;">
                    🐛 Report Bug
                </span>
            </div>
            
            <div style="margin-top: 1rem; padding-top: 1rem; border-top: 2px solid #E2E8F0;">
                <p style="color: #94A3B8; margin: 0; font-size: 0.75rem;">
                    © {current_year} <strong>FADEN CO</strong> - All Rights Reserved
                </p>
                <p style="color: #94A3B8; margin: 0.25rem 0 0 0; font-size: 0.7rem;">
                    Version 1.0.0 | Made with ❤️ using Streamlit
                </p>
            </div>
        </div>
    """, unsafe_allow_html=True)

# ============================================
# SIDEBAR CONTENT
# ============================================
with st.sidebar:
    st.markdown("""
        <div style="text-align: center; padding: 1rem 0;">
            <div style="font-size: 3rem; margin-bottom: 0.5rem;">🎓</div>
            <h2 style="margin: 0; color: #1E3A8A; font-size: 1.25rem;">SIM Akademik</h2>
            <p style="margin: 0.25rem 0 0 0; color: #64748B; font-size: 0.875rem;">
                Sistem Informasi Manajemen
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Quick actions in sidebar
    st.markdown("### ⚡ Aksi Cepat")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔄 Refresh", use_container_width=True, help="Refresh halaman", key="sidebar_refresh"):
            st.rerun()
    
    with col2:
        if st.button("ℹ️ Info", use_container_width=True, help="Informasi sistem", key="sidebar_info"):
            st.info("SIM Akademik v1.0\n\nDeveloped by FADEN CO")

# ============================================
# RUN APPLICATION
# ============================================
if __name__ == "__main__":
    main()
"""
SIM Akademik - Modern Minimalist Design
Versi alternatif dengan desain yang lebih modern dan clean
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
    initial_sidebar_state="expanded"
)

# ============================================
# MODERN MINIMALIST CSS
# ============================================
st.markdown("""
    <style>
        /* Import Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        /* Global styles */
        * {
            font-family: 'Inter', sans-serif;
        }
        
        /* Main container */
        .block-container {
            padding-top: 2rem;
            padding-bottom: 3rem;
            max-width: 1600px;
        }
        
        /* Hide defaults */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* Sidebar */
        [data-testid="stSidebar"] {
            background: #FFFFFF;
            border-right: 1px solid #F1F5F9;
        }
        
        [data-testid="stSidebarNav"] a {
            padding: 1rem 1.25rem;
            border-radius: 0.75rem;
            margin: 0.25rem 0;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
            font-weight: 500;
        }
        
        [data-testid="stSidebarNav"] a:hover {
            background: #F8FAFC;
            transform: translateX(4px);
        }
        
        [data-testid="stSidebarNav"] a[aria-current="page"] {
            background: #3B82F6;
            color: white !important;
            font-weight: 600;
        }
        
        /* Buttons */
        .stButton > button {
            border-radius: 0.75rem;
            font-weight: 500;
            border: 1px solid #E5E7EB;
            transition: all 0.2s ease;
            height: 100px;
            padding: 1rem;
        }
        
        .stButton > button:hover {
            border-color: #3B82F6;
            background: #EFF6FF;
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(59, 130, 246, 0.15);
        }
        
        /* Metrics */
        [data-testid="stMetricValue"] {
            font-size: 2rem;
            font-weight: 700;
            color: #0F172A;
        }
        
        [data-testid="stMetricLabel"] {
            font-size: 0.875rem;
            font-weight: 500;
            color: #64748B;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        
        /* Cards */
        .modern-card {
            background: white;
            border-radius: 1rem;
            padding: 2rem;
            border: 1px solid #F1F5F9;
            transition: all 0.3s ease;
            margin-bottom: 1.5rem;
        }
        
        .modern-card:hover {
            border-color: #E5E7EB;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
        }
        
        /* Hero section */
        .hero-section {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 4rem 2rem;
            border-radius: 1.5rem;
            text-align: center;
            margin: -1rem -1rem 3rem -1rem;
            position: relative;
            overflow: hidden;
        }
        
        .hero-section::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.05'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
        }
        
        /* Stats grid */
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1.5rem;
            margin: 2rem 0;
        }
        
        .stat-item {
            background: white;
            padding: 1.5rem;
            border-radius: 1rem;
            border: 1px solid #F1F5F9;
            text-align: center;
        }
        
        /* Feature list */
        .feature-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1.5rem;
            margin: 2rem 0;
        }
        
        .feature-card {
            background: white;
            padding: 1.5rem;
            border-radius: 1rem;
            border: 1px solid #F1F5F9;
            transition: all 0.3s ease;
        }
        
        .feature-card:hover {
            border-color: #3B82F6;
            transform: translateY(-4px);
            box-shadow: 0 12px 24px rgba(59, 130, 246, 0.1);
        }
        
        /* Typography */
        h1, h2, h3, h4, h5, h6 {
            color: #0F172A;
            font-weight: 700;
        }
        
        /* Divider */
        hr {
            margin: 3rem 0;
            border: none;
            border-top: 1px solid #F1F5F9;
        }
    </style>
""", unsafe_allow_html=True)

# ============================================
# SESSION STATE
# ============================================
def init_session_state():
    if 'initialized' not in st.session_state:
        st.session_state.initialized = True
    if 'df_clean' not in st.session_state:
        st.session_state.df_clean = None
    if 'file_name' not in st.session_state:
        st.session_state.file_name = None
    if 'upload_time' not in st.session_state:
        st.session_state.upload_time = None

# ============================================
# MAIN FUNCTION
# ============================================
def main():
    init_session_state()
    
    # Hero Section
    st.markdown("""
        <div class="hero-section">
            <div style="position: relative; z-index: 1;">
                <div style="font-size: 4rem; margin-bottom: 1rem;">🎓</div>
                <h1 style="color: white; margin: 0; font-size: 3rem; font-weight: 800;">
                    SIM Akademik
                </h1>
                <p style="color: rgba(255, 255, 255, 0.95); font-size: 1.25rem; margin: 1rem 0 0 0; font-weight: 400;">
                    Sistem Informasi Manajemen Akademik Modern
                </p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Quick Actions
    st.markdown("<h2 style='text-align: center; margin-bottom: 2rem;'>⚡ Akses Cepat</h2>", unsafe_allow_html=True)
    
    cols = st.columns(5)
    actions = [
        ("📤", "Upload Data", "pages/5_📤_Upload_Data.py"),
        ("📊", "Dashboard", "pages/2_📊_Analisis_Performa.py"),
        ("🎓", "Prediksi", "pages/3_🎓_Prediksi_Kelulusan.py"),
        ("⚠️", "Warning", "pages/4_⚠️_Early_Warning.py"),
        ("📋", "Laporan", "pages/6_📋_Laporan.py")
    ]
    
    for idx, (icon, label, page) in enumerate(actions):
        with cols[idx]:
            if st.button(f"{icon}\n\n**{label}**", use_container_width=True, key=f"action_{idx}"):
                st.switch_page(page)
    
    st.markdown("---")
    
    # Main Content
    col1, col2 = st.columns([2, 1], gap="large")
    
    with col1:
        render_features()
    
    with col2:
        render_stats()
    
    st.markdown("---")
    
    # Footer
    render_footer()

def render_features():
    """Render features section"""
    st.markdown("""
        <div class="modern-card">
            <h2 style="margin-top: 0;">🌟 Fitur Unggulan</h2>
            <p style="color: #64748B; line-height: 1.6;">
                Platform lengkap untuk manajemen dan analisis data akademik dengan teknologi terkini.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    features = [
        ("📊", "Data Management", "Upload dan kelola data nilai dengan mudah"),
        ("📈", "Analytics", "Dashboard interaktif dan visualisasi data"),
        ("🤖", "AI Prediction", "Prediksi kelulusan berbasis machine learning"),
        ("⚠️", "Early Warning", "Deteksi dini siswa berisiko"),
        ("📋", "Smart Reports", "Generate laporan otomatis"),
        ("🔒", "Secure", "Data aman dan terenkripsi")
    ]
    
    st.markdown('<div class="feature-grid">', unsafe_allow_html=True)
    
    for icon, title, desc in features:
        st.markdown(f"""
            <div class="feature-card">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">{icon}</div>
                <h4 style="margin: 0.5rem 0; color: #0F172A;">{title}</h4>
                <p style="color: #64748B; font-size: 0.875rem; margin: 0;">{desc}</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_stats():
    """Render statistics"""
    st.markdown("""
        <div class="modern-card">
            <h3 style="margin-top: 0;">📊 Statistik</h3>
        </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.df_clean is not None:
        df = st.session_state.df_clean
        
        total_students = df['NISN'].nunique() if 'NISN' in df.columns else len(df)
        avg_score = df['NILAI'].mean() if 'NILAI' in df.columns else 0
        
        st.metric("Total Siswa", f"{total_students:,}")
        st.metric("Rata-rata", f"{avg_score:.1f}")
        
        if 'NILAI' in df.columns:
            pass_rate = (len(df[df['NILAI'] >= 60]) / len(df)) * 100
            st.metric("Kelulusan", f"{pass_rate:.0f}%")
    else:
        st.info("Upload data untuk melihat statistik")

def render_footer():
    """Clean footer"""
    st.markdown(f"""
        <div style="
            text-align: center;
            padding: 2rem;
            background: #F8FAFC;
            border-radius: 1rem;
            border: 1px solid #F1F5F9;
        ">
            <p style="color: #64748B; margin: 0; font-size: 0.875rem;">
                © {datetime.now().year} <strong style="color: #0F172A;">SIM Akademik</strong> by FADEN CO
            </p>
            <p style="color: #94A3B8; margin: 0.5rem 0 0 0; font-size: 0.75rem;">
                Version 1.0.0 | Made with ❤️
            </p>
        </div>
    """, unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("""
        <div style="text-align: center; padding: 2rem 0;">
            <div style="font-size: 3rem;">🎓</div>
            <h2 style="margin: 0.5rem 0 0 0; color: #0F172A;">SIM Akademik</h2>
            <p style="color: #64748B; font-size: 0.875rem; margin: 0.5rem 0 0 0;">
                v1.0.0
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄", use_container_width=True, help="Refresh"):
            st.rerun()
    with col2:
        if st.button("ℹ️", use_container_width=True, help="Info"):
            st.info("SIM Akademik v1.0")

if __name__ == "__main__":
    main()
"""
Header Component untuk SIM Akademik
Menyediakan header yang konsisten di seluruh aplikasi
"""

import streamlit as st

def render_header(page_title=None, show_logo=True):
    """
    Render header aplikasi dengan branding
    
    Args:
        page_title (str, optional): Judul halaman spesifik. Jika None, hanya tampilkan logo
        show_logo (bool): Tampilkan logo dan branding. Default True
    
    Usage:
        # Di home page (app.py)
        render_header()
        
        # Di page lain
        render_header("Upload Data")
    """
    
    if show_logo:
        # Main header dengan gradient background
        st.markdown("""
            <div style="
                background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%);
                padding: 20px 30px;
                margin: -1rem -1rem 2rem -1rem;
                border-radius: 0 0 15px 15px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            ">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div style="display: flex; align-items: center; gap: 15px;">
                        <div style="font-size: 40px;">🎓</div>
                        <div>
                            <h1 style="color: white; margin: 0; font-size: 28px; font-weight: 700; letter-spacing: 1px;">
                                SIM AKADEMIK
                            </h1>
                            <p style="color: rgba(255, 255, 255, 0.9); margin: 5px 0 0 0; font-size: 14px; font-weight: 500;">
                                Sistem Informasi Manajemen Akademik
                            </p>
                        </div>
                    </div>
                    <div style="text-align: right; color: white;">
                        <div style="font-size: 12px; opacity: 0.9; margin-bottom: 3px;">Version 1.0</div>
                        <div style="font-size: 11px; opacity: 0.7;">© 2024 FADEN CO</div>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    # Page-specific title (jika ada)
    if page_title:
        st.markdown(f"""
            <div style="margin: 20px 0;">
                <h2 style="color: #1E3A8A; margin: 0; font-size: 24px;">
                    {page_title}
                </h2>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("---")


def render_page_header(title, icon="", description=None, show_breadcrumb=True):
    """
    Render header untuk halaman spesifik dengan breadcrumb
    
    Args:
        title (str): Judul halaman
        icon (str): Emoji icon untuk halaman
        description (str, optional): Deskripsi singkat halaman
        show_breadcrumb (bool): Tampilkan breadcrumb navigation
    
    Usage:
        render_page_header(
            title="Upload Data",
            icon="📤",
            description="Unggah dan proses data leger nilai",
            show_breadcrumb=True
        )
    """
    
    # Breadcrumb (opsional)
    if show_breadcrumb:
        st.markdown("""
            <div style="margin-bottom: 15px; font-size: 14px; color: #666;">
                <a href="/" style="color: #3B82F6; text-decoration: none;">🏠 Beranda</a>
                <span style="margin: 0 8px; color: #ccc;">›</span>
                <span style="color: #333;">{}</span>
            </div>
        """.format(title), unsafe_allow_html=True)
    
    # Page header dengan gradient
    desc_html = f"""
        <p style="color: rgba(255,255,255,0.9); margin: 10px 0 0 0; font-size: 15px;">
            {description}
        </p>
    """ if description else ""
    
    st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 30px;
            border-radius: 15px;
            margin-bottom: 30px;
            text-align: center;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        ">
            <h1 style="color: white; margin: 0; font-size: 32px;">
                {icon} {title}
            </h1>
            {desc_html}
        </div>
    """, unsafe_allow_html=True)


def add_page_style():
    """
    Tambahkan custom CSS untuk styling halaman
    Call this di awal setiap page untuk styling konsisten
    """
    st.markdown("""
        <style>
            /* Reduce top padding */
            .block-container {
                padding-top: 1rem;
                padding-bottom: 2rem;
            }
            
            /* Streamlit header spacing */
            header[data-testid="stHeader"] {
                background-color: transparent;
            }
            
            /* Custom scrollbar */
            ::-webkit-scrollbar {
                width: 10px;
                height: 10px;
            }
            
            ::-webkit-scrollbar-track {
                background: #f1f1f1;
                border-radius: 5px;
            }
            
            ::-webkit-scrollbar-thumb {
                background: #888;
                border-radius: 5px;
            }
            
            ::-webkit-scrollbar-thumb:hover {
                background: #555;
            }
            
            /* Metric styling */
            [data-testid="stMetricValue"] {
                font-size: 28px;
                font-weight: 600;
            }
            
            /* Button styling improvements */
            .stButton > button {
                transition: all 0.3s ease;
            }
            
            .stButton > button:hover {
                transform: translateY(-2px);
                box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            }
            
            /* Info box styling */
            .stAlert {
                border-radius: 10px;
                border-left: 4px solid #3B82F6;
            }
            
            /* DataFrame styling */
            .dataframe {
                border-radius: 8px;
                overflow: hidden;
            }
        </style>
    """, unsafe_allow_html=True)
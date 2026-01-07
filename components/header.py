"""
Header Component untuk SIM Akademik
Menyediakan header yang konsisten di seluruh aplikasi
"""

import streamlit as st

def render_page_header(title, icon="", description=None):
    """
    Render header untuk halaman spesifik
    
    Args:
        title (str): Judul halaman
        icon (str): Emoji icon untuk halaman
        description (str, optional): Deskripsi singkat halaman
    
    Usage:
        render_page_header(
            title="Upload Data",
            icon="📤",
            description="Unggah dan proses data leger nilai"
        )
    """
    
    desc_html = f"""
        <p style="color: rgba(255,255,255,0.95); margin: 0.75rem 0 0 0; font-size: 1.125rem; font-weight: 400;">
            {description}
        </p>
    """ if description else ""
    
    st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 2rem;
            border-radius: 1rem;
            margin-bottom: 2rem;
            text-align: center;
            box-shadow: 0 4px 16px rgba(102, 126, 234, 0.3);
        ">
            <h1 style="color: white; margin: 0; font-size: 2.5rem; font-weight: 700;">
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
            /* Main container */
            .block-container {
                padding-top: 1rem;
                padding-bottom: 2rem;
                max-width: 1200px;
            }
            
            /* Sidebar */
            [data-testid="stSidebar"] {
                background: linear-gradient(180deg, #F8FAFC 0%, #F1F5F9 100%);
            }
            
            /* Sidebar navigation */
            [data-testid="stSidebarNav"] {
                background-color: transparent;
                padding-top: 1rem;
            }
            
            [data-testid="stSidebarNav"] a {
                padding: 0.75rem 1rem;
                border-radius: 0.5rem;
                transition: all 0.3s ease;
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
            
            /* Metric styling */
            [data-testid="stMetricValue"] {
                font-size: 1.75rem;
                font-weight: 700;
                color: #1E3A8A;
            }
            
            [data-testid="stMetricLabel"] {
                font-size: 0.9rem;
                font-weight: 500;
                color: #64748B;
            }
            
            /* Button styling */
            .stButton > button {
                border-radius: 0.5rem;
                transition: all 0.3s ease;
                font-weight: 500;
            }
            
            .stButton > button:hover {
                transform: translateY(-2px);
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
            }
            
            /* DataFrame styling */
            .dataframe {
                border-radius: 0.5rem;
                overflow: hidden;
            }
            
            /* Alert styling */
            .stAlert {
                border-radius: 0.75rem;
                border-left-width: 4px;
            }
            
            /* Tab styling */
            .stTabs [data-baseweb="tab-list"] {
                gap: 0.5rem;
            }
            
            .stTabs [data-baseweb="tab"] {
                border-radius: 0.5rem 0.5rem 0 0;
                padding: 0.75rem 1.5rem;
                font-weight: 500;
            }
            
            /* Expander styling */
            .streamlit-expanderHeader {
                font-weight: 600;
                color: #1E3A8A;
                border-radius: 0.5rem;
            }
            
            /* Custom scrollbar */
            ::-webkit-scrollbar {
                width: 10px;
                height: 10px;
            }
            
            ::-webkit-scrollbar-track {
                background: #F1F5F9;
                border-radius: 5px;
            }
            
            ::-webkit-scrollbar-thumb {
                background: #94A3B8;
                border-radius: 5px;
            }
            
            ::-webkit-scrollbar-thumb:hover {
                background: #64748B;
            }
            
            /* Divider */
            hr {
                margin: 2rem 0;
                border: none;
                border-top: 2px solid #E2E8F0;
            }
        </style>
    """, unsafe_allow_html=True)
"""
Footer Component untuk SIM Akademik
"""

import streamlit as st
from datetime import datetime

def render_minimal_footer():
    """Render footer minimal (untuk page dengan banyak konten)"""
    st.markdown("---")
    st.markdown(f"""
    <div style="
        text-align: center;
        padding: 1.5rem;
        background: linear-gradient(135deg, #F9FAFB 0%, #F3F4F6 100%);
        border-radius: 0.75rem;
        margin-top: 2rem;
    ">
        <p style="color: #64748B; margin: 0; font-size: 0.875rem;">
            © {datetime.now().year} <strong style="color: #1E3A8A;">SIM Akademik</strong> by FADEN CO
        </p>
        <p style="color: #94A3B8; margin: 0.25rem 0 0 0; font-size: 0.75rem;">
            Version 1.0.0 | Made with ❤️ using Streamlit
        </p>
    </div>
    """, unsafe_allow_html=True)


def render_footer():
    """Render footer lengkap"""
    st.markdown("---")
    
    st.markdown(f"""
    <div style="
        text-align: center;
        padding: 2rem;
        background: linear-gradient(135deg, #F9FAFB 0%, #F3F4F6 100%);
        border-radius: 1rem;
        margin-top: 2rem;
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
            <a href="mailto:support@simakademik.edu" style="
                color: #3B82F6;
                text-decoration: none;
                margin: 0 0.75rem;
                font-size: 0.875rem;
                font-weight: 500;
            ">
                📧 Support
            </a>
            <span style="color: #CBD5E1;">|</span>
            <a href="https://github.com/fadenco/sim-akademik" style="
                color: #3B82F6;
                text-decoration: none;
                margin: 0 0.75rem;
                font-size: 0.875rem;
                font-weight: 500;
            ">
                📚 Dokumentasi
            </a>
            <span style="color: #CBD5E1;">|</span>
            <a href="https://github.com/fadenco/sim-akademik/issues" style="
                color: #3B82F6;
                text-decoration: none;
                margin: 0 0.75rem;
                font-size: 0.875rem;
                font-weight: 500;
            ">
                🐛 Report Bug
            </a>
        </div>
        
        <div style="margin-top: 1rem; padding-top: 1rem; border-top: 2px solid #E2E8F0;">
            <p style="color: #94A3B8; margin: 0; font-size: 0.75rem;">
                © {datetime.now().year} <strong>FADEN CO</strong> - All Rights Reserved
            </p>
            <p style="color: #94A3B8; margin: 0.25rem 0 0 0; font-size: 0.7rem;">
                Version 1.0.0 | Made with ❤️ using Streamlit
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
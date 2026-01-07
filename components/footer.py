"""
Footer Component untuk SIM Akademik
"""

import streamlit as st
from datetime import datetime

def render_footer(show_stats=False):
    """
    Render footer aplikasi
    
    Args:
        show_stats (bool): Tampilkan statistik session. Default False
    
    Usage:
        render_footer()
        render_footer(show_stats=True)
    """
    
    st.markdown("---")
    
    if show_stats:
        render_footer_stats()
        st.markdown("---")
    
    # Main footer
    current_year = datetime.now().year
    
    st.markdown(f"""
    <div style="
        text-align: center;
        padding: 25px 20px;
        background: linear-gradient(135deg, #F9FAFB 0%, #F3F4F6 100%);
        border-radius: 10px;
        margin-top: 30px;
    ">
        <div style="margin-bottom: 15px;">
            <h4 style="color: #1E3A8A; margin: 0; font-size: 18px;">
                🎓 SIM Akademik
            </h4>
            <p style="color: #666; margin: 5px 0; font-size: 14px;">
                Sistem Informasi Manajemen Akademik
            </p>
        </div>
        
        <div style="margin: 15px 0;">
            <a href="mailto:support@simakademik.edu" style="
                color: #3B82F6;
                text-decoration: none;
                margin: 0 10px;
                font-size: 13px;
            ">
                📧 Support
            </a>
            <span style="color: #ccc;">|</span>
            <a href="https://github.com/fadenco/sim-akademik" style="
                color: #3B82F6;
                text-decoration: none;
                margin: 0 10px;
                font-size: 13px;
            ">
                📚 Dokumentasi
            </a>
            <span style="color: #ccc;">|</span>
            <a href="https://github.com/fadenco/sim-akademik/issues" style="
                color: #3B82F6;
                text-decoration: none;
                margin: 0 10px;
                font-size: 13px;
            ">
                🐛 Report Bug
            </a>
        </div>
        
        <div style="margin-top: 15px; padding-top: 15px; border-top: 1px solid #E5E7EB;">
            <p style="color: #999; margin: 0; font-size: 12px;">
                © {current_year} <strong>FADEN CO</strong> - All Rights Reserved
            </p>
            <p style="color: #999; margin: 5px 0 0 0; font-size: 11px;">
                Version 1.0.0 | Made with ❤️ using Streamlit
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_footer_stats():
    """Render statistik di footer"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_records = len(st.session_state.get('df_clean', []))
        st.metric("📊 Total Records", f"{total_records:,}" if total_records > 0 else "-")
    
    with col2:
        history_count = len(st.session_state.get('upload_history', []))
        st.metric("📂 Upload History", history_count)
    
    with col3:
        # Session duration (example)
        st.metric("⏱️ Session", "Active")
    
    with col4:
        # Data status
        status = "✅ Ready" if st.session_state.get('df_clean') is not None else "⚠️ No Data"
        st.metric("🔄 Status", status)


def render_minimal_footer():
    """Render footer minimal (untuk page dengan banyak konten)"""
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #999; padding: 15px; font-size: 12px;">
        © 2024 <strong>SIM Akademik</strong> by FADEN CO
    </div>
    """, unsafe_allow_html=True)


def render_footer_with_back_to_top():
    """Render footer dengan tombol back to top"""
    render_footer()
    
    # Back to top button
    st.markdown("""
        <div style="text-align: center; margin-top: 20px;">
            <a href="#" style="
                display: inline-block;
                padding: 10px 20px;
                background: linear-gradient(135deg, #3B82F6 0%, #1E3A8A 100%);
                color: white;
                text-decoration: none;
                border-radius: 25px;
                font-size: 14px;
                font-weight: 500;
                transition: all 0.3s ease;
            " onmouseover="this.style.transform='translateY(-3px)'; this.style.boxShadow='0 6px 12px rgba(0,0,0,0.2)'"
               onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='none'">
                ⬆️ Back to Top
            </a>
        </div>
    """, unsafe_allow_html=True)
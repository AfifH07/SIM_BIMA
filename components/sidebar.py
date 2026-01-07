"""
Sidebar Component untuk SIM Akademik (Hybrid Approach)
Melengkapi (bukan mengganti) sidebar navigation bawaan Streamlit
"""

import streamlit as st
from datetime import datetime

def render_custom_sidebar():
    """
    Render custom sidebar content yang MELENGKAPI sidebar navigation bawaan
    TIDAK menghilangkan navigation links bawaan Streamlit
    
    Usage:
        # Di app.py atau di setiap page
        render_custom_sidebar()
    """
    
    # Styling untuk sidebar (TANPA menyembunyikan navigation)
    enhance_sidebar_style()
    
    with st.sidebar:
        # Logo dan branding di sidebar
        render_sidebar_branding()
        
        st.markdown("---")
        
        # Data status widget
        render_data_status_widget()
        
        st.markdown("---")
        
        # Quick actions
        render_sidebar_quick_actions()
        
        st.markdown("---")
        
        # System info
        render_system_info()


def render_sidebar_branding():
    """Render branding di sidebar"""
    st.markdown("""
        <div style="text-align: center; padding: 15px 0;">
            <div style="font-size: 48px; margin-bottom: 10px;">🎓</div>
            <h3 style="margin: 0; color: #1E3A8A; font-size: 18px;">SIM Akademik</h3>
            <p style="margin: 5px 0 0 0; color: #666; font-size: 12px;">
                Sistem Informasi Manajemen
            </p>
        </div>
    """, unsafe_allow_html=True)


def render_data_status_widget():
    """Widget untuk menampilkan status data yang aktif"""
    st.markdown("### 📊 Status Data")
    
    if st.session_state.get('df_clean') is not None:
        df = st.session_state['df_clean']
        file_name = st.session_state.get('file_name', 'Unknown')
        upload_time = st.session_state.get('upload_time')
        
        # Format timestamp
        if hasattr(upload_time, 'strftime'):
            time_str = upload_time.strftime('%d/%m/%Y %H:%M')
        else:
            time_str = str(upload_time) if upload_time else 'N/A'
        
        # Calculate stats
        total_records = len(df)
        unique_students = df['NISN'].nunique() if 'NISN' in df.columns else 'N/A'
        
        # Display in success box
        st.success(f"""
        **✅ Data Aktif**
        
        📁 **File:** {file_name}  
        📅 **Upload:** {time_str}  
        📊 **Records:** {total_records:,}  
        👥 **Siswa:** {unique_students}
        """)
        
        # Progress/metrics
        if 'NILAI' in df.columns:
            avg_score = df['NILAI'].mean()
            st.metric(
                label="📈 Rata-rata Nilai",
                value=f"{avg_score:.1f}",
                delta=f"{avg_score - 75:.1f}" if avg_score > 75 else None
            )
    
    else:
        st.info("""
        **ℹ️ Belum Ada Data**
        
        Silakan upload data melalui menu **📤 Upload Data** untuk memulai.
        """)


def render_sidebar_quick_actions():
    """Quick action buttons di sidebar"""
    st.markdown("### ⚡ Aksi Cepat")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔄 Refresh", use_container_width=True, help="Refresh halaman"):
            st.rerun()
    
    with col2:
        if st.button("🧹 Clear", use_container_width=True, help="Hapus semua data"):
            # Confirm dialog
            clear_data_with_confirmation()
    
    # Export button (jika ada data)
    if st.session_state.get('df_clean') is not None:
        st.markdown("---")
        if st.button("📥 Export Data", use_container_width=True, type="primary"):
            export_current_data()


def clear_data_with_confirmation():
    """Clear data dengan konfirmasi"""
    # Set flag untuk konfirmasi
    if 'confirm_clear' not in st.session_state:
        st.session_state.confirm_clear = False
    
    if not st.session_state.confirm_clear:
        st.session_state.confirm_clear = True
        st.warning("⚠️ Klik sekali lagi untuk konfirmasi hapus data")
    else:
        # Clear all data except initialization flag
        keys_to_keep = ['initialized']
        keys_to_delete = [k for k in st.session_state.keys() if k not in keys_to_keep]
        
        for key in keys_to_delete:
            del st.session_state[key]
        
        st.success("✅ Data berhasil dihapus!")
        st.rerun()


def export_current_data():
    """Export data yang sedang aktif"""
    if st.session_state.get('df_clean') is not None:
        df = st.session_state['df_clean']
        
        # Convert to CSV
        csv = df.to_csv(index=False).encode('utf-8-sig')
        
        # Trigger download
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name=f"data_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True
        )


def render_system_info():
    """System information di sidebar"""
    st.markdown("### ℹ️ Info Sistem")
    
    # Upload history count
    history_count = len(st.session_state.get('upload_history', []))
    
    with st.expander("📊 Statistik", expanded=False):
        st.markdown(f"""
        - **Upload History:** {history_count}
        - **Session Active:** ✅
        - **Version:** 1.0
        """)
    
    with st.expander("⚙️ Pengaturan", expanded=False):
        # Theme toggle (example)
        theme = st.selectbox(
            "Theme",
            ["Light", "Dark"],
            key="theme_selector"
        )
        
        # Auto-save toggle
        auto_save = st.checkbox(
            "Auto-save data",
            value=True,
            key="auto_save_setting"
        )
    
    with st.expander("📚 Bantuan", expanded=False):
        st.markdown("""
        **Navigasi:**
        - Gunakan menu di atas untuk berpindah halaman
        - Klik tombol untuk akses cepat
        
        **Tips:**
        - Upload data terlebih dahulu
        - Gunakan filter untuk analisis
        - Export hasil ke CSV/Excel
        
        **Support:**
        - 📧 support@simakademik.edu
        - 🔗 [Dokumentasi](https://docs.simakademik.edu)
        """)


def enhance_sidebar_style():
    """
    Enhance sidebar styling TANPA menghilangkan navigation
    Hanya memperbaiki tampilan, TIDAK hide navigation links
    """
    st.markdown("""
        <style>
            /* Sidebar background gradient */
            [data-testid="stSidebar"] {
                background: linear-gradient(180deg, #F9FAFB 0%, #F3F4F6 100%);
            }
            
            /* Sidebar navigation styling (TIDAK DIHILANGKAN!) */
            section[data-testid="stSidebarNav"] {
                padding-top: 2rem;
                padding-bottom: 1rem;
            }
            
            /* Style untuk navigation links */
            section[data-testid="stSidebarNav"] a {
                padding: 12px 16px;
                border-radius: 8px;
                margin: 4px 0;
                transition: all 0.3s ease;
            }
            
            section[data-testid="stSidebarNav"] a:hover {
                background-color: rgba(59, 130, 246, 0.1);
                transform: translateX(5px);
            }
            
            /* Active link styling */
            section[data-testid="stSidebarNav"] a[aria-current="page"] {
                background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%);
                color: white;
                font-weight: 600;
            }
            
            /* Sidebar divider */
            .sidebar .sidebar-content hr {
                margin: 1rem 0;
                border: none;
                border-top: 2px solid #E5E7EB;
            }
            
            /* Custom button styling in sidebar */
            .sidebar .stButton > button {
                border-radius: 8px;
                transition: all 0.3s ease;
                font-weight: 500;
            }
            
            .sidebar .stButton > button:hover {
                transform: translateY(-2px);
                box-shadow: 0 4px 8px rgba(0,0,0,0.15);
            }
            
            /* Metric in sidebar */
            .sidebar [data-testid="stMetricValue"] {
                font-size: 24px;
            }
            
            /* Expander in sidebar */
            .sidebar .streamlit-expanderHeader {
                font-weight: 600;
                color: #1E3A8A;
            }
        </style>
    """, unsafe_allow_html=True)


def get_current_page_name():
    """
    Detect current page dari query params atau session state
    Returns: string nama page
    """
    try:
        # Try to get from Streamlit's internal page info
        import streamlit.runtime.scriptrunner as sr
        ctx = sr.get_script_run_ctx()
        if ctx:
            page = ctx.page_script_hash
            return page
    except:
        pass
    
    # Fallback: return default
    return "home"
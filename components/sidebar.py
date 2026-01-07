"""
Sidebar Component untuk SIM Akademik
Komponen sidebar yang melengkapi navigation bawaan Streamlit
"""

import streamlit as st
from datetime import datetime

def render_custom_sidebar():
    """
    Render custom sidebar content yang MELENGKAPI sidebar navigation bawaan
    
    Usage:
        render_custom_sidebar()
    """
    
    with st.sidebar:
        # Branding
        st.markdown("""
            <div style="text-align: center; padding: 1rem 0; margin-bottom: 1rem;">
                <div style="font-size: 3.5rem; margin-bottom: 0.5rem;">🎓</div>
                <h2 style="margin: 0; color: #1E3A8A; font-size: 1.25rem; font-weight: 700;">
                    SIM Akademik
                </h2>
                <p style="margin: 0.25rem 0 0 0; color: #64748B; font-size: 0.875rem;">
                    Sistem Informasi Manajemen
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Data status widget
        render_data_status_widget()
        
        st.markdown("---")
        
        # Quick actions
        render_sidebar_quick_actions()
        
        st.markdown("---")
        
        # System info
        render_system_info()


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

📁 **File:** {file_name[:20]}...  
📅 **Upload:** {time_str}  
📊 **Records:** {total_records:,}  
👥 **Siswa:** {unique_students}
        """)
        
        # Metrics
        if 'NILAI' in df.columns:
            avg_score = df['NILAI'].mean()
            st.metric(
                label="📈 Rata-rata Nilai",
                value=f"{avg_score:.1f}",
                delta=f"{avg_score - 75:.1f}" if avg_score != 75 else "0"
            )
    
    else:
        st.info("""
**ℹ️ Belum Ada Data**

Silakan upload data melalui menu **📤 Upload Data**.
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
            clear_data_with_confirmation()
    
    # Export button (jika ada data)
    if st.session_state.get('df_clean') is not None:
        if st.button("📥 Export Data", use_container_width=True, type="primary"):
            export_current_data()


def clear_data_with_confirmation():
    """Clear data dengan konfirmasi"""
    if 'confirm_clear' not in st.session_state:
        st.session_state.confirm_clear = False
    
    if not st.session_state.confirm_clear:
        st.session_state.confirm_clear = True
        st.warning("⚠️ Klik sekali lagi untuk konfirmasi")
    else:
        # Clear all data except initialization flag
        keys_to_keep = ['initialized', 'path_initialized']
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
    
    with st.expander("📊 Statistik", expanded=False):
        history_count = len(st.session_state.get('upload_history', []))
        st.markdown(f"""
- **Upload History:** {history_count}
- **Session:** ✅ Active
- **Version:** 1.0.0
        """)
    
    with st.expander("📚 Bantuan", expanded=False):
        st.markdown("""
**Navigasi:**
- Gunakan menu untuk berpindah halaman
- Klik tombol untuk akses cepat

**Tips:**
- Upload data terlebih dahulu
- Gunakan filter untuk analisis
- Export hasil ke CSV/Excel

**Support:**
- 📧 support@simakademik.edu
- 🔗 [Dokumentasi](https://docs.simakademik.edu)
        """)
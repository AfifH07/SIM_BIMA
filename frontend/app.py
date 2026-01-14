"""
SIM SMA BIMA - Main Streamlit Dashboard
Dashboard utama untuk Sistem Informasi Manajemen SMA.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import requests

# Page config
st.set_page_config(
    page_title="SIM SMA BIMA",
    page_icon="🏫",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 5px;
    }
    h1 {
        color: #1f77b4;
    }
    </style>
""", unsafe_allow_html=True)

# API Configuration
API_BASE_URL = "http://localhost:8000/api"

# Session State untuk authentication
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_data' not in st.session_state:
    st.session_state.user_data = None
if 'token' not in st.session_state:
    st.session_state.token = None


def get_headers():
    """Get headers dengan token autentikasi."""
    if st.session_state.token:
        return {
            'Authorization': f'Token {st.session_state.token}',
            'Content-Type': 'application/json'
        }
    return {'Content-Type': 'application/json'}


def login_page():
    """Halaman login."""
    st.title("🏫 SIM SMA BIMA")
    st.subheader("Sistem Informasi Manajemen Sekolah")

    with st.form("login_form"):
        st.write("### Login")
        email = st.text_input("Email", placeholder="user@example.com")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")

        if submit:
            if email and password:
                try:
                    # Call login API
                    response = requests.post(
                        f"{API_BASE_URL}/auth/login/",
                        json={"email": email, "password": password}
                    )

                    if response.status_code == 200:
                        data = response.json()
                        st.session_state.authenticated = True
                        st.session_state.user_data = data
                        st.session_state.token = data.get('token')
                        st.success("✅ Login berhasil!")
                        st.rerun()
                    else:
                        st.error("❌ Email atau password salah")

                except Exception as e:
                    st.error(f"❌ Error koneksi ke server: {str(e)}")
                    st.info("💡 Pastikan backend Django sudah running di http://localhost:8000")
            else:
                st.warning("⚠️ Mohon isi email dan password")


def sidebar_navigation():
    """Sidebar untuk navigasi."""
    with st.sidebar:
        st.title("🏫 SIM SMA BIMA")

        if st.session_state.user_data:
            st.write(f"**User:** {st.session_state.user_data.get('full_name', 'Unknown')}")
            st.write(f"**Role:** {st.session_state.user_data.get('role_display', 'Unknown')}")
            st.divider()

        st.header("Menu")
        menu = st.radio(
            "Navigasi",
            ["Dashboard", "Data Siswa", "Data Guru", "Keuangan", "Prediksi PTN"],
            label_visibility="collapsed"
        )

        st.divider()

        if st.button("🚪 Logout"):
            st.session_state.authenticated = False
            st.session_state.user_data = None
            st.session_state.token = None
            st.rerun()

        return menu


def load_sample_data():
    """Load sample data untuk demo (jika API belum tersedia)."""
    # Sample data siswa
    students_data = pd.DataFrame({
        'Bulan': ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun'],
        'Jumlah': [320, 325, 330, 328, 335, 340]
    })

    # Sample data keuangan
    finance_data = pd.DataFrame({
        'Bulan': ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun'],
        'Pemasukan': [50000000, 52000000, 51000000, 53000000, 54000000, 55000000],
        'Pengeluaran': [35000000, 38000000, 36000000, 39000000, 40000000, 41000000]
    })

    return students_data, finance_data


def dashboard_page():
    """Halaman dashboard utama."""
    st.title("📊 Dashboard SIM SMA BIMA")
    st.write(f"Selamat datang, **{st.session_state.user_data.get('full_name', 'User')}**!")

    # Metrics Row
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="👨‍🎓 Total Siswa",
            value="340",
            delta="5 dari bulan lalu"
        )

    with col2:
        st.metric(
            label="👨‍🏫 Total Guru",
            value="45",
            delta="2 dari bulan lalu"
        )

    with col3:
        st.metric(
            label="💰 Pemasukan (Bulan Ini)",
            value="Rp 55.000.000",
            delta="Rp 1.000.000"
        )

    with col4:
        st.metric(
            label="📚 Jumlah Kelas",
            value="12",
            delta="0"
        )

    st.divider()

    # Charts Row
    col1, col2 = st.columns(2)

    students_data, finance_data = load_sample_data()

    with col1:
        st.subheader("📈 Tren Jumlah Siswa")

        fig = px.line(
            students_data,
            x='Bulan',
            y='Jumlah',
            markers=True,
            title="Jumlah Siswa per Bulan"
        )
        fig.update_layout(
            xaxis_title="Bulan",
            yaxis_title="Jumlah Siswa",
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("💰 Statistik Keuangan")

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=finance_data['Bulan'],
            y=finance_data['Pemasukan'],
            name='Pemasukan',
            marker_color='lightgreen'
        ))
        fig.add_trace(go.Bar(
            x=finance_data['Bulan'],
            y=finance_data['Pengeluaran'],
            name='Pengeluaran',
            marker_color='lightcoral'
        ))

        fig.update_layout(
            title="Pemasukan vs Pengeluaran",
            xaxis_title="Bulan",
            yaxis_title="Rupiah",
            barmode='group'
        )
        st.plotly_chart(fig, use_container_width=True)

    # Additional Info
    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.info("📅 **Agenda Hari Ini**\n\n"
                "- 08:00 - Upacara Bendera\n"
                "- 10:00 - Rapat Guru\n"
                "- 14:00 - Ekstrakurikuler")

    with col2:
        st.warning("⚠️ **Perhatian**\n\n"
                   "- 5 siswa belum membayar SPP\n"
                   "- 2 guru izin\n"
                   "- Jadwal ujian: 2 minggu lagi")

    with col3:
        st.success("✅ **Status Sistem**\n\n"
                   "- Database: Online\n"
                   "- API: Running\n"
                   "- Backup: Up to date")


def students_page():
    """Halaman data siswa."""
    st.title("👨‍🎓 Data Siswa")

    # Sample data
    students_df = pd.DataFrame({
        'NIS': ['2023001', '2023002', '2023003', '2023004', '2023005'],
        'Nama': ['Ahmad Rizki', 'Siti Nurhaliza', 'Budi Santoso', 'Dewi Lestari', 'Andi Wijaya'],
        'Kelas': ['XII IPA 1', 'XII IPA 1', 'XII IPS 1', 'XI IPA 2', 'XI IPS 1'],
        'Jenis Kelamin': ['L', 'P', 'L', 'P', 'L'],
        'Status': ['Aktif', 'Aktif', 'Aktif', 'Aktif', 'Aktif']
    })

    # Filters
    col1, col2, col3 = st.columns(3)

    with col1:
        search = st.text_input("🔍 Cari siswa", placeholder="Nama atau NIS")

    with col2:
        kelas_filter = st.selectbox("Kelas", ["Semua", "XII IPA 1", "XII IPS 1", "XI IPA 2", "XI IPS 1"])

    with col3:
        status_filter = st.selectbox("Status", ["Semua", "Aktif", "Lulus", "Keluar"])

    # Display data
    st.dataframe(students_df, use_container_width=True, hide_index=True)

    # Add student button
    if st.button("➕ Tambah Siswa Baru"):
        st.info("Fitur tambah siswa akan membuka form input")


def teachers_page():
    """Halaman data guru."""
    st.title("👨‍🏫 Data Guru")

    teachers_df = pd.DataFrame({
        'NIP': ['198501012010011001', '198702022011012002', '199003032012011003'],
        'Nama': ['Dr. Hadi Wijaya', 'Siti Aminah, M.Pd', 'Bambang Suryanto, S.Si'],
        'Mata Pelajaran': ['Matematika', 'Bahasa Indonesia', 'Fisika'],
        'Status': ['PNS', 'PNS', 'Honorer']
    })

    st.dataframe(teachers_df, use_container_width=True, hide_index=True)


def finance_page():
    """Halaman keuangan."""
    st.title("💰 Manajemen Keuangan")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Total Pemasukan (2024)", "Rp 320.000.000", "+5%")

    with col2:
        st.metric("Total Pengeluaran (2024)", "Rp 230.000.000", "+3%")

    st.divider()

    # Transaction history
    st.subheader("Riwayat Transaksi")

    transactions = pd.DataFrame({
        'Tanggal': ['2024-06-15', '2024-06-14', '2024-06-13'],
        'Keterangan': ['Pembayaran SPP - Ahmad Rizki', 'Pembelian ATK', 'Gaji Guru'],
        'Tipe': ['Pemasukan', 'Pengeluaran', 'Pengeluaran'],
        'Jumlah': ['Rp 500.000', 'Rp 2.500.000', 'Rp 35.000.000']
    })

    st.dataframe(transactions, use_container_width=True, hide_index=True)


def prediction_page():
    """Halaman prediksi PTN."""
    st.title("🎓 Prediksi Kelulusan PTN")

    st.write("Fitur prediksi menggunakan Machine Learning untuk memprediksi peluang kelulusan PTN.")

    with st.form("prediction_form"):
        col1, col2 = st.columns(2)

        with col1:
            nama = st.text_input("Nama Siswa")
            nilai_rata = st.number_input("Nilai Rata-rata", min_value=0.0, max_value=100.0, value=80.0)
            nilai_un = st.number_input("Nilai UN", min_value=0.0, max_value=100.0, value=85.0)

        with col2:
            prestasi = st.number_input("Jumlah Prestasi", min_value=0, value=2)
            ekstrakurikuler = st.number_input("Keaktifan Ekstrakurikuler (1-10)", min_value=1, max_value=10, value=7)
            ekonomi = st.selectbox("Kondisi Ekonomi", ["Kurang", "Cukup", "Baik"])

        predict = st.form_submit_button("🔮 Prediksi")

        if predict:
            # Simulasi prediksi (untuk demo)
            probability = min(95, (nilai_rata + nilai_un) / 2 + prestasi * 2 + ekstrakurikuler)

            st.success(f"### Hasil Prediksi untuk {nama}")
            st.metric("Peluang Lulus PTN", f"{probability:.1f}%")

            if probability >= 80:
                st.success("✅ Peluang tinggi untuk lulus PTN!")
            elif probability >= 60:
                st.warning("⚠️ Peluang cukup, perlu persiapan lebih baik")
            else:
                st.error("❌ Peluang rendah, butuh peningkatan signifikan")


# Main App Logic
def main():
    """Main app logic."""
    if not st.session_state.authenticated:
        login_page()
    else:
        menu = sidebar_navigation()

        if menu == "Dashboard":
            dashboard_page()
        elif menu == "Data Siswa":
            students_page()
        elif menu == "Data Guru":
            teachers_page()
        elif menu == "Keuangan":
            finance_page()
        elif menu == "Prediksi PTN":
            prediction_page()


if __name__ == "__main__":
    main()

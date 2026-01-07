# 🎓 SIM Akademik - Sistem Informasi Manajemen Akademik

<div align="center">

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.31.0-red.svg)
![License](https://img.shields.io/badge/license-MIT-yellow.svg)

Aplikasi berbasis Streamlit untuk manajemen dan analisis data akademik siswa dengan fitur machine learning.

[Demo](#demo) • [Fitur](#fitur) • [Instalasi](#instalasi) • [Penggunaan](#penggunaan) • [Dokumentasi](#dokumentasi)

</div>

---

## 📋 Daftar Isi

- [Tentang Proyek](#tentang-proyek)
- [Fitur Utama](#fitur-utama)
- [Teknologi](#teknologi)
- [Instalasi](#instalasi)
- [Penggunaan](#penggunaan)
- [Struktur Proyek](#struktur-proyek)
- [Kontribusi](#kontribusi)
- [Lisensi](#lisensi)

---

## 🎯 Tentang Proyek

**SIM Akademik** adalah Sistem Informasi Manajemen yang dirancang khusus untuk membantu institusi pendidikan dalam:

- 📊 **Manajemen Data** - Upload, cleaning, dan pengelolaan data nilai secara efisien
- 📈 **Analisis Performa** - Visualisasi dan analisis data siswa dengan dashboard interaktif
- 🎓 **Prediksi Kelulusan** - Sistem prediksi berbasis machine learning
- ⚠️ **Early Warning** - Deteksi dini siswa berisiko gagal
- 📋 **Laporan Otomatis** - Generate laporan dalam berbagai format

---

## ✨ Fitur Utama

### 1. 📤 Upload & Processing Data
- Upload file Excel/CSV data leger nilai
- Automatic data cleaning dan normalisasi
- Validasi data otomatis
- Support multiple file formats

### 2. 📊 Analisis Performa
- Dashboard interaktif dengan visualisasi data
- Statistik performa siswa dan mata pelajaran
- Ranking siswa otomatis
- Grafik distribusi nilai

### 3. 🎓 Prediksi Kelulusan
- Model machine learning untuk prediksi kelulusan
- Analisis faktor-faktor yang mempengaruhi kelulusan
- Confidence score untuk setiap prediksi

### 4. ⚠️ Early Warning System
- Deteksi otomatis siswa berisiko
- Threshold nilai yang dapat dikustomisasi
- Export daftar siswa berisiko

### 5. 📋 Laporan & Export
- Generate laporan dalam format CSV/Excel
- Multiple report templates
- Customizable report filters

---

## 🛠 Teknologi

Proyek ini dibangun menggunakan:

- **Frontend & Backend**: [Streamlit](https://streamlit.io/) 1.31.0
- **Data Processing**: [Pandas](https://pandas.pydata.org/) 2.2.0, [NumPy](https://numpy.org/) 1.26.3
- **Visualization**: [Plotly](https://plotly.com/) 5.18.0, [Matplotlib](https://matplotlib.org/) 3.8.2, [Seaborn](https://seaborn.pydata.org/) 0.13.1
- **Machine Learning**: [Scikit-learn](https://scikit-learn.org/) 1.4.0
- **File Processing**: [OpenPyXL](https://openpyxl.readthedocs.io/) 3.1.2

---

## 📥 Instalasi

### Prerequisites

Pastikan Anda sudah menginstall:
- Python 3.8 atau lebih tinggi
- pip (Python package manager)

### Langkah Instalasi

1. **Clone repository**
   ```bash
   git clone https://github.com/fadenco/sim-akademik.git
   cd sim-akademik
   ```

2. **Buat virtual environment (opsional tapi direkomendasikan)**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Verifikasi instalasi**
   ```bash
   streamlit --version
   ```

---

## 🚀 Penggunaan

### Menjalankan Aplikasi

```bash
streamlit run app.py
```

Aplikasi akan terbuka di browser Anda pada `http://localhost:8501`

### Quick Start Guide

1. **Upload Data**
   - Klik menu "📤 Upload Data" di sidebar
   - Pilih file Excel/CSV data leger nilai
   - Klik tombol "🚀 Proses Data"

2. **Analisis Data**
   - Buka "📊 Analisis Performa" untuk melihat dashboard
   - Explore berbagai visualisasi dan statistik

3. **Prediksi Kelulusan**
   - Gunakan "🎓 Prediksi Kelulusan" untuk prediksi
   - Input data siswa atau gunakan batch prediction

4. **Early Warning**
   - Akses "⚠️ Early Warning" untuk deteksi siswa berisiko
   - Atur threshold sesuai kebutuhan
   - Download daftar siswa berisiko

5. **Generate Laporan**
   - Buka "📋 Laporan" untuk membuat laporan
   - Pilih jenis dan format laporan
   - Download hasil laporan

---

## 📁 Struktur Proyek

```
sim-akademik/
├── app.py                      # Entry point aplikasi
├── requirements.txt            # Python dependencies
├── .streamlit/
│   └── config.toml            # Konfigurasi Streamlit
├── components/                 # Komponen UI reusable
│   ├── __init__.py
│   ├── header.py              # Header component
│   ├── footer.py              # Footer component
│   └── sidebar.py             # Sidebar component
├── pages/                      # Halaman aplikasi
│   ├── 1_🏠_Beranda.py
│   ├── 2_📊_Analisis_Performa.py
│   ├── 3_🎓_Prediksi_Kelulusan.py
│   ├── 4_⚠️_Early_Warning.py
│   ├── 5_📤_Upload_Data.py
│   └── 6_📋_Laporan.py
├── utils/                      # Utility functions
│   ├── __init__.py
│   ├── leger_cleaner.py       # Data cleaning utilities
│   ├── data_processor.py      # Data processing
│   ├── data_loader.py         # Data loading
│   └── data_validator.py      # Data validation
├── analytics/                  # Analytics modules
│   ├── __init__.py
│   ├── student_analytics.py   # Student analytics
│   ├── subject_analytics.py   # Subject analytics
│   └── class_analytics.py     # Class analytics
├── models/                     # ML models
│   ├── __init__.py
│   ├── prediction_model.py    # Graduation prediction
│   └── clustering_model.py    # Student clustering
├── visualizations/             # Visualization utilities
│   ├── __init__.py
│   ├── plots.py               # Plot functions
│   ├── charts.py              # Chart functions
│   └── dashboards.py          # Dashboard components
├── config/                     # Configuration files
│   ├── __init__.py
│   ├── settings.py            # App settings
│   └── database_config.py     # Database config
├── data/                       # Data directory
│   ├── sample/                # Sample data
│   ├── raw/                   # Raw data (gitignored)
│   └── processed/             # Processed data (gitignored)
├── tests/                      # Unit tests
│   ├── __init__.py
│   ├── test_data_processor.py
│   ├── test_models.py
│   └── test_analytics.py
├── docs/                       # Documentation
│   ├── user_guide.md
│   ├── developer_guide.md
│   ├── api_documentation.md
│   └── architecture.md
└── logs/                       # Log files (gitignored)
```

---

## 📖 Dokumentasi

### Format Data

**Data Leger Nilai (Excel/CSV)**
```
Struktur:
- Kolom identitas siswa: NO, NAMA_SISWA, NISN, NIS
- Kolom nilai: SMT1, SMT2, SMT3, SMT4, SMT5, SMT6, RERATA
- Satu baris per siswa
- Nilai dalam range 0-100
```

### API Documentation

Untuk dokumentasi lengkap API dan fungsi-fungsi internal, lihat [API Documentation](docs/api_documentation.md)

### User Guide

Panduan lengkap penggunaan aplikasi tersedia di [User Guide](docs/user_guide.md)

---

## 🤝 Kontribusi

Kontribusi sangat diterima! Berikut cara berkontribusi:

1. Fork repository ini
2. Buat branch fitur baru (`git checkout -b feature/AmazingFeature`)
3. Commit perubahan (`git commit -m 'Add some AmazingFeature'`)
4. Push ke branch (`git push origin feature/AmazingFeature`)
5. Buat Pull Request

### Guidelines

- Ikuti style guide Python (PEP 8)
- Tambahkan docstring untuk fungsi baru
- Update dokumentasi jika diperlukan
- Tambahkan unit tests untuk fitur baru

---

## 🐛 Bug Reports & Feature Requests

Jika menemukan bug atau ingin request fitur baru:

1. Cek [Issues](https://github.com/fadenco/sim-akademik/issues) yang sudah ada
2. Buat issue baru dengan template yang sesuai
3. Berikan deskripsi yang jelas dan lengkap

---

## 📝 Lisensi

Project ini dilisensikan under MIT License - lihat file [LICENSE](LICENSE) untuk detail.

---

## 👥 Tim Pengembang

**FADEN CO**

- 📧 Email: support@simakademik.edu
- 🌐 Website: [https://simakademik.edu](https://simakademik.edu)
- 💬 GitHub: [@fadenco](https://github.com/fadenco)

---

## 🙏 Acknowledgments

- Terimakasih kepada [Streamlit](https://streamlit.io/) untuk framework yang luar biasa
- Komunitas open source Python
- Semua kontributor yang telah membantu proyek ini

---

<div align="center">

**⭐ Jika proyek ini bermanfaat, jangan lupa berikan star! ⭐**

Made with ❤️ by FADEN CO

</div>
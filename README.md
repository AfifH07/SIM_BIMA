# 🏫 SIM SMA BIMA

**Sistem Informasi Manajemen Sekolah Menengah Atas**

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-4.2+-green.svg)](https://www.djangoproject.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.29+-red.svg)](https://streamlit.io/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14+-blue.svg)](https://www.postgresql.org/)

---

## 📝 Deskripsi Proyek

SIM SMA BIMA adalah sistem informasi manajemen sekolah berbasis web yang dirancang untuk memudahkan pengelolaan data siswa, guru, keuangan, kegiatan ekstrakurikuler, serta fitur prediksi kelulusan PTN menggunakan machine learning.

### 🎯 Fitur Utama

- ✅ **Manajemen Siswa** - Data lengkap siswa, kehadiran, dan prestasi
- ✅ **Manajemen Guru** - Profil guru, jadwal mengajar, evaluasi kinerja
- ✅ **Manajemen Kelas** - Penjadwalan, pembagian kelas, ruang kelas
- ✅ **Manajemen Nilai** - Input nilai, analisis, peringkat siswa
- ✅ **Manajemen Keuangan** - SPP, transaksi, laporan keuangan
- ✅ **Ekstrakurikuler** - Pendaftaran, rekam kegiatan, prestasi
- ✅ **Prediksi PTN** - ML model untuk prediksi kelulusan PTN
- ✅ **Dashboard Interaktif** - Visualisasi data real-time

### 👥 Target Pengguna

- **Admin Sekolah** - Akses penuh ke semua fitur
- **Guru** - Manajemen nilai, kehadiran, dan kelas
- **Siswa** - Akses data akademik dan prediksi PTN
- **Orang Tua** - Monitor perkembangan anak

---

## 🏗️ Arsitektur Sistem

### Tech Stack

| Component    | Technology      | Version |
|--------------|-----------------|---------|
| Frontend     | Streamlit       | 1.29+   |
| Backend      | Django REST API | 4.2+    |
| Database     | PostgreSQL      | 14+     |
| ML Framework | scikit-learn    | 1.3+    |
| ML Framework | XGBoost         | 2.0+    |
| Visualization| Plotly          | 5.18+   |

### Arsitektur 3-Tier

```
┌─────────────────┐
│   Streamlit     │  ← Presentation Layer (Port 8501)
│   Frontend      │
└────────┬────────┘
         │ REST API
┌────────▼────────┐
│   Django        │  ← Application Layer (Port 8000)
│   Backend       │
└────────┬────────┘
         │ ORM
┌────────▼────────┐
│   PostgreSQL    │  ← Data Layer (Port 5432)
│   Database      │
└─────────────────┘
```

---

## 📂 Struktur Proyek

```
sim-sma-bima/
├── backend/                # Django REST API
│   ├── config/            # Konfigurasi Django
│   ├── apps/              # Django apps (students, teachers, dll)
│   ├── core/              # Utilities & middleware
│   └── manage.py
├── frontend/              # Streamlit UI
│   ├── pages/             # Multi-page app
│   ├── components/        # Reusable components
│   ├── services/          # API integration
│   └── app.py
├── ml/                    # Machine Learning
│   ├── data/              # Datasets
│   ├── models/            # Trained models
│   ├── notebooks/         # Jupyter notebooks
│   └── src/               # ML source code
├── tests/                 # Test suite
├── docs/                  # Documentation
├── scripts/               # Utility scripts
└── docker/                # Docker configuration
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- PostgreSQL 14+
- Git

### Installation

1. **Clone repository:**
   ```bash
   git clone https://github.com/your-username/sim-sma-bima.git
   cd sim-sma-bima
   ```

2. **Setup virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

3. **Install dependencies:**
   ```bash
   pip install -r backend/requirements.txt
   pip install -r frontend/requirements.txt
   pip install -r ml/requirements.txt
   ```

4. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env dengan konfigurasi Anda
   ```

5. **Setup database:**
   ```bash
   # Lihat DATABASE_SETUP.md untuk panduan lengkap
   createdb sim_sma_bima_dev
   ```

6. **Run migrations:**
   ```bash
   cd backend
   python manage.py migrate
   python manage.py createsuperuser
   ```

7. **Run servers:**
   ```bash
   # Terminal 1 - Backend
   cd backend
   python manage.py runserver

   # Terminal 2 - Frontend
   cd frontend
   streamlit run app.py
   ```

8. **Access application:**
   - Frontend: http://localhost:8501
   - Backend API: http://localhost:8000/api
   - Admin Panel: http://localhost:8000/admin

📖 **Panduan lengkap:** [SETUP_GUIDE.md](./SETUP_GUIDE.md)

---

## 📚 Dokumentasi

- [📐 System Architecture](docs/architecture/system_design.md)
- [🗄️ Database Schema & ERD](docs/architecture/database_schema.md)
- [🔌 API Endpoints](docs/api/endpoints.md)
- [💾 Database Setup](DATABASE_SETUP.md)
- [🛠️ Development Setup](SETUP_GUIDE.md)

---

## 🧪 Testing

```bash
cd backend

# Run all tests
pytest

# Run specific tests
pytest tests/backend/test_views.py

# Run with coverage
pytest --cov=apps --cov-report=html

# View coverage report
# Open htmlcov/index.html in browser
```

---

## 🔐 Security Features

- ✅ Token-based authentication
- ✅ Role-based access control (RBAC)
- ✅ CORS protection
- ✅ CSRF protection
- ✅ SQL injection prevention (ORM)
- ✅ XSS protection
- ✅ Password hashing (bcrypt)
- ✅ HTTPS support (production)

---

## 📊 Machine Learning Features

### Prediksi Kelulusan PTN

Model menggunakan fitur:
- Nilai rata-rata
- Nilai UN
- Jumlah prestasi
- Keaktifan ekstrakurikuler
- Kondisi ekonomi
- Kehadiran

**Algorithms:**
- Logistic Regression
- Random Forest
- XGBoost (primary)

**Akurasi Model:** ~85% (pada test set)

---

## 🤝 Contributing

Belum menerima kontribusi eksternal. Proyek ini dikembangkan oleh tim internal.

---

## 📄 License

Proprietary - All Rights Reserved

Copyright © 2024 SIM SMA BIMA Development Team

---

## 👨‍💻 Development Team

- **Project Lead:** [Name]
- **Backend Developer:** [Name]
- **Frontend Developer:** [Name]
- **ML Engineer:** [Name]
- **Database Admin:** [Name]

---

## 📞 Support

Untuk pertanyaan atau bantuan:
- Email: support@simsma.com
- Issue Tracker: [GitHub Issues](https://github.com/your-username/sim-sma-bima/issues)
- Documentation: [docs/](docs/)

---

## 🗓️ Changelog

### Version 1.0.0 (2024-01-14)
- ✨ Initial release
- ✅ Complete CRUD for students, teachers, classes
- ✅ Financial management system
- ✅ ML prediction for PTN admission
- ✅ Interactive dashboard
- ✅ Multi-role authentication

---

## 🎯 Roadmap

- [ ] Mobile application (React Native/Flutter)
- [ ] Real-time notifications
- [ ] Advanced analytics dashboard
- [ ] Export to Excel/PDF
- [ ] Integration with NISN database
- [ ] Parent mobile app
- [ ] SMS/WhatsApp notifications
- [ ] E-learning module

---

**Made with ❤️ by SIM SMA BIMA Team**

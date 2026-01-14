# 🚀 Setup Guide - SIM SMA BIMA

## Panduan Lengkap Instalasi dan Konfigurasi Proyek

Dokumen ini berisi langkah-langkah lengkap untuk mengatur environment pengembangan SIM SMA BIMA dari awal.

---

## 📋 Prerequisites

Sebelum memulai, pastikan sudah terinstall:

- ✅ **Python 3.10+** - [Download Python](https://www.python.org/downloads/)
- ✅ **PostgreSQL 14+** - [Download PostgreSQL](https://www.postgresql.org/download/)
- ✅ **Git** - [Download Git](https://git-scm.com/downloads/)
- ✅ **Code Editor** (VS Code recommended) - [Download VS Code](https://code.visualstudio.com/)

### Verifikasi Instalasi

```bash
# Check Python version
python --version
# Output: Python 3.10.x atau lebih tinggi

# Check PostgreSQL
psql --version
# Output: psql (PostgreSQL) 14.x

# Check Git
git --version
# Output: git version 2.x.x
```

---

## 📂 Step 1: Clone Repository

```bash
# Clone repository (jika sudah ada di Git)
git clone https://github.com/your-username/sim-sma-bima.git
cd sim-sma-bima

# Atau jika belum, inisialisasi Git repository
cd sim-sma-bima
git init
git add .
git commit -m "Initial commit: project structure"
```

---

## 🐍 Step 2: Setup Python Virtual Environment

### Windows:

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Verify activation (prompt akan berubah)
# (venv) C:\path\to\sim-sma-bima>
```

### macOS/Linux:

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Verify activation
# (venv) user@computer:~/sim-sma-bima$
```

---

## 📦 Step 3: Install Dependencies

### Backend Dependencies (Django)

```bash
cd backend
pip install -r requirements.txt

# Verify installation
pip list | grep Django
# Output: Django  4.2.x
```

### Frontend Dependencies (Streamlit)

```bash
cd ../frontend
pip install -r requirements.txt

# Verify installation
pip list | grep streamlit
# Output: streamlit  1.29.x
```

### ML Dependencies

```bash
cd ../ml
pip install -r requirements.txt

# Verify installation
pip list | grep scikit-learn
# Output: scikit-learn  1.3.x
```

**IMPORTANT:** Install semua dependencies sekaligus (recommended):

```bash
# Dari root directory
pip install -r backend/requirements.txt
pip install -r frontend/requirements.txt
pip install -r ml/requirements.txt
```

---

## 🗄️ Step 4: Setup PostgreSQL Database

Baca panduan lengkap di [DATABASE_SETUP.md](./DATABASE_SETUP.md)

### Quick Setup:

```bash
# Login ke PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE sim_sma_bima_dev;

# Create user (optional)
CREATE USER sim_user WITH PASSWORD 'your_password';

# Grant privileges
GRANT ALL PRIVILEGES ON DATABASE sim_sma_bima_dev TO sim_user;

# Exit
\q
```

---

## ⚙️ Step 5: Environment Configuration

```bash
# Copy .env.example to .env
cp .env.example .env

# Edit .env file
# Windows: notepad .env
# macOS/Linux: nano .env
```

### Minimal Configuration (.env):

```env
# Database
DB_NAME=sim_sma_bima_dev
DB_USER=postgres
DB_PASSWORD=your_postgres_password
DB_HOST=localhost
DB_PORT=5432

# Django
SECRET_KEY=your-secret-key-here
DEBUG=True
DJANGO_SETTINGS_MODULE=config.settings.development

# API
API_BASE_URL=http://localhost:8000/api
```

### Generate SECRET_KEY:

```bash
cd backend
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copy output dan paste ke .env file.

---

## 🔧 Step 6: Django Initialization

Baca panduan lengkap di [DJANGO_INIT.md](./DJANGO_INIT.md)

### Quick Start:

```bash
cd backend

# Create migrations
python manage.py makemigrations

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
# Enter: email, full name, password

# Collect static files
python manage.py collectstatic --noinput

# Run development server
python manage.py runserver
```

**Verify:** Buka browser ke `http://localhost:8000/admin`

---

## 🎨 Step 7: Run Streamlit Frontend

```bash
# New terminal window
cd frontend

# Run Streamlit
streamlit run app.py
```

**Verify:** Buka browser ke `http://localhost:8501`

---

## 🧪 Step 8: Run Tests

```bash
cd backend

# Run all tests
pytest

# Run specific test file
pytest tests/backend/test_views.py

# Run with coverage
pytest --cov=apps --cov-report=html
```

---

## 📊 Step 9: Load Sample Data (Optional)

```bash
cd backend

# Run seed script
python manage.py shell < ../scripts/seed_data.py
```

---

## 🔍 Step 10: Verify Installation

### Checklist:

- [ ] Backend Django berjalan di `http://localhost:8000`
- [ ] Frontend Streamlit berjalan di `http://localhost:8501`
- [ ] Database PostgreSQL ter-configure dengan benar
- [ ] Admin panel dapat diakses (`/admin`)
- [ ] API endpoints berfungsi (`/api/students/`)
- [ ] Streamlit dapat connect ke API
- [ ] Tests berjalan tanpa error

### Test Connectivity:

```bash
# Test API endpoint
curl http://localhost:8000/api/students/
# Expected: JSON response atau 401 (jika perlu auth)

# Test Streamlit
# Open browser: http://localhost:8501
# Expected: Login page muncul
```

---

## 🚨 Troubleshooting

### Problem: ModuleNotFoundError

**Solution:**
```bash
# Pastikan virtual environment aktif
# Reinstall dependencies
pip install -r requirements.txt
```

### Problem: Database connection error

**Solution:**
```bash
# Check PostgreSQL service running
# Windows: services.msc → PostgreSQL service
# Linux: sudo systemctl status postgresql

# Verify .env database credentials
# Check DB_NAME, DB_USER, DB_PASSWORD
```

### Problem: Port already in use

**Solution:**
```bash
# Find and kill process
# Windows: netstat -ano | findstr :8000
#          taskkill /PID <pid> /F

# Linux/Mac: lsof -i :8000
#            kill <pid>

# Or use different port
python manage.py runserver 8001
```

### Problem: CORS error di Streamlit

**Solution:**
```python
# Check backend/config/settings/base.py
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8501",
    "http://127.0.0.1:8501",
]
```

---

## 📚 Next Steps

1. **Read Documentation:**
   - [System Architecture](docs/architecture/system_design.md)
   - [Database Schema](docs/architecture/database_schema.md)
   - [API Endpoints](docs/api/endpoints.md)

2. **Start Development:**
   - Create new models
   - Build API endpoints
   - Design Streamlit pages
   - Train ML models

3. **Setup Git Workflow:**
   - Create feature branches
   - Make commits
   - Push to remote

---

## 🛠️ Development Tools (Optional)

### Recommended VS Code Extensions:

- Python
- Pylance
- Django
- PostgreSQL
- GitLens
- Prettier
- ESLint

### Install via command:

```bash
code --install-extension ms-python.python
code --install-extension ms-python.vscode-pylance
code --install-extension batisteo.vscode-django
```

---

## 📞 Support

Jika mengalami masalah:

1. Check [Troubleshooting](#troubleshooting) section
2. Read relevant documentation
3. Check project issues on GitHub
4. Contact development team

---

## ✅ Quick Command Reference

```bash
# Activate venv
# Windows: venv\Scripts\activate
# Mac/Linux: source venv/bin/activate

# Run Django
cd backend && python manage.py runserver

# Run Streamlit
cd frontend && streamlit run app.py

# Run Tests
cd backend && pytest

# Make Migrations
cd backend && python manage.py makemigrations

# Migrate Database
cd backend && python manage.py migrate

# Create Superuser
cd backend && python manage.py createsuperuser
```

---

**Last Updated:** 2024-01-14
**Version:** 1.0
**Author:** SIM SMA BIMA Development Team

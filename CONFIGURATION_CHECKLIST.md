# ✅ Configuration Checklist - SIM SMA BIMA

## Panduan Lengkap Apa Saja Yang Perlu Disesuaikan

Dokumen ini berisi checklist lengkap untuk konfigurasi yang perlu disesuaikan dengan environment Anda.

---

## 1. 🗄️ Database Configuration

### ✓ Yang Perlu Disesuaikan:

#### 1.1 Create PostgreSQL Database

```bash
# Login ke PostgreSQL
psql -U postgres

# Buat database baru
CREATE DATABASE sim_sma_bima_dev;

# (Optional) Buat user khusus
CREATE USER sim_user WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE sim_sma_bima_dev TO sim_user;
```

#### 1.2 Update File .env

```env
# SESUAIKAN NILAI INI:
DB_NAME=sim_sma_bima_dev          # Nama database yang dibuat
DB_USER=postgres                   # Username PostgreSQL Anda
DB_PASSWORD=your_actual_password   # Password PostgreSQL Anda
DB_HOST=localhost                  # Host database (localhost untuk lokal)
DB_PORT=5432                       # Port PostgreSQL (default: 5432)
```

**📍 Lokasi File:** `sim-sma-bima/.env`

**⚠️ PENTING:**
- Jangan commit file `.env` ke Git (sudah ada di .gitignore)
- Gunakan password yang kuat untuk production
- Backup database secara berkala

---

## 2. 🔐 Django Security Configuration

### ✓ Yang Perlu Disesuaikan:

#### 2.1 Generate SECRET_KEY Baru

```bash
cd backend
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copy output dan paste ke .env:

```env
SECRET_KEY=your-generated-secret-key-here
```

#### 2.2 Update ALLOWED_HOSTS (Production)

Untuk production, tambahkan domain Anda:

```env
# Development
ALLOWED_HOSTS=localhost,127.0.0.1

# Production
ALLOWED_HOSTS=localhost,127.0.0.1,yourdomain.com,www.yourdomain.com
```

**📍 Lokasi File:** `sim-sma-bima/.env`

---

## 3. 🌐 CORS Configuration

### ✓ Yang Perlu Disesuaikan:

Jika Streamlit berjalan di port atau domain lain:

```env
# Default (local development)
CORS_ALLOWED_ORIGINS=http://localhost:8501,http://127.0.0.1:8501

# Custom port
CORS_ALLOWED_ORIGINS=http://localhost:8502,http://127.0.0.1:8502

# Production dengan domain
CORS_ALLOWED_ORIGINS=https://app.yourdomain.com,https://yourdomain.com
```

**📍 Lokasi File:**
- `sim-sma-bima/.env`
- `backend/config/settings/base.py` (fallback)

---

## 4. 📧 Email Configuration

### ✓ Yang Perlu Disesuaikan:

#### 4.1 Development (Console Email)

```env
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

Email akan terprint di console (tidak terkirim).

#### 4.2 Production (SMTP Email)

```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-specific-password
DEFAULT_FROM_EMAIL=noreply@yourdomain.com
```

**Untuk Gmail:**
1. Enable 2-Factor Authentication
2. Generate App Password: https://myaccount.google.com/apppasswords
3. Gunakan App Password (bukan password Gmail biasa)

**📍 Lokasi File:** `sim-sma-bima/.env`

---

## 5. 📂 Media & Static Files

### ✓ Yang Perlu Disesuaikan:

#### 5.1 Update Paths

```env
# Development (relative path)
MEDIA_ROOT=media
STATIC_ROOT=staticfiles

# Production (absolute path)
MEDIA_ROOT=/var/www/sim-sma-bima/media
STATIC_ROOT=/var/www/sim-sma-bima/staticfiles
```

#### 5.2 Create Directories

```bash
# Di root project
mkdir -p backend/media
mkdir -p backend/staticfiles
mkdir -p backend/media/students/photos
mkdir -p backend/media/teachers/photos
mkdir -p backend/media/users/photos
```

**📍 Lokasi File:** `sim-sma-bima/.env`

---

## 6. 🤖 Machine Learning Configuration

### ✓ Yang Perlu Disesuaikan:

```env
# Path ke directory models
ML_MODELS_DIR=ml/models/saved_models

# Versi model yang digunakan
ML_MODEL_VERSION=v1.0
```

#### Create ML Directories

```bash
mkdir -p ml/models/saved_models
mkdir -p ml/models/checkpoints
mkdir -p ml/data/raw
mkdir -p ml/data/processed
mkdir -p ml/data/features
```

**📍 Lokasi File:** `sim-sma-bima/.env`

---

## 7. 🔗 API Base URL

### ✓ Yang Perlu Disesuaikan:

Untuk koneksi Streamlit ke Django API:

```env
# Development
API_BASE_URL=http://localhost:8000/api

# Production
API_BASE_URL=https://api.yourdomain.com/api
```

**📍 Lokasi File:**
- `sim-sma-bima/.env`
- `frontend/config/settings.py` (bisa override di sini)

---

## 8. 🐳 Django Settings Module

### ✓ Yang Perlu Disesuaikan:

```env
# Development
DJANGO_SETTINGS_MODULE=config.settings.development

# Testing
DJANGO_SETTINGS_MODULE=config.settings.testing

# Production
DJANGO_SETTINGS_MODULE=config.settings.production
```

**📍 Lokasi File:** `sim-sma-bima/.env`

---

## 9. 📊 Streamlit Configuration

### ✓ Yang Perlu Disesuaikan (Optional):

Create file: `frontend/.streamlit/config.toml`

```toml
[server]
port = 8501
address = "localhost"
headless = true

[browser]
gatherUsageStats = false

[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "sans serif"
```

**📍 Lokasi File:** `frontend/.streamlit/config.toml` (buat baru)

---

## 10. 📝 Logging Configuration

### ✓ Yang Perlu Disesuaikan:

```env
# Log level: DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_LEVEL=INFO

# Log file path
LOG_FILE_PATH=logs/django.log
```

#### Create Logs Directory

```bash
mkdir -p logs
touch logs/.gitkeep
```

**📍 Lokasi File:** `sim-sma-bima/.env`

---

## 11. 🕐 Timezone & Language

### ✓ Yang Perlu Disesuaikan:

```env
# Timezone (sesuaikan dengan lokasi Anda)
TIME_ZONE=Asia/Jakarta

# Language code
LANGUAGE_CODE=id-ID
```

**Timezone Options:**
- Asia/Jakarta (WIB)
- Asia/Makassar (WITA)
- Asia/Jayapura (WIT)

**📍 Lokasi File:**
- `sim-sma-bima/.env`
- `backend/config/settings/base.py` (sudah di-set)

---

## 12. 🔒 Production Security Settings

### ✓ Yang Perlu Disesuaikan (Production Only):

Di file `backend/config/settings/production.py`:

```python
# HTTPS Settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# HSTS Settings
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
```

**📍 Lokasi File:** `backend/config/settings/production.py`

---

## 📋 Quick Setup Checklist

Setelah clone project, lakukan dalam urutan ini:

- [ ] **Step 1:** Install Python 3.10+
- [ ] **Step 2:** Install PostgreSQL 14+
- [ ] **Step 3:** Create virtual environment
- [ ] **Step 4:** Install dependencies
- [ ] **Step 5:** Create PostgreSQL database
- [ ] **Step 6:** Copy `.env.example` to `.env`
- [ ] **Step 7:** Update `.env` dengan konfigurasi Anda
- [ ] **Step 8:** Generate SECRET_KEY baru
- [ ] **Step 9:** Run migrations (`python manage.py migrate`)
- [ ] **Step 10:** Create superuser
- [ ] **Step 11:** Create media & static directories
- [ ] **Step 12:** Run Django server (`python manage.py runserver`)
- [ ] **Step 13:** Run Streamlit (`streamlit run app.py`)
- [ ] **Step 14:** Test login ke http://localhost:8501

---

## 🧪 Verification Commands

Setelah konfigurasi, verify dengan:

```bash
# Check database connection
cd backend
python manage.py dbshell
\conninfo
\q

# Check migrations
python manage.py showmigrations

# Check Django settings
python manage.py diffsettings

# Test Django server
python manage.py runserver
# Visit: http://localhost:8000/admin

# Test Streamlit
cd ../frontend
streamlit run app.py
# Visit: http://localhost:8501
```

---

## ❓ Troubleshooting

### Database Connection Error

```
django.db.utils.OperationalError: FATAL: password authentication failed
```

**Fix:**
1. Check `.env` file: DB_USER dan DB_PASSWORD benar
2. Test PostgreSQL login: `psql -U postgres -d sim_sma_bima_dev`
3. Reset password PostgreSQL jika perlu

### CORS Error di Streamlit

```
Access to fetch at 'http://localhost:8000/api/students/' has been blocked by CORS policy
```

**Fix:**
1. Check `CORS_ALLOWED_ORIGINS` di `.env`
2. Pastikan include protocol (`http://` atau `https://`)
3. Restart Django server setelah perubahan

### ImportError: No module named 'apps'

**Fix:**
```bash
# Pastikan virtual environment aktif
# Reinstall dependencies
pip install -r requirements.txt
```

---

## 📞 Need Help?

Jika masih ada masalah:

1. Check [SETUP_GUIDE.md](./SETUP_GUIDE.md)
2. Check [DATABASE_SETUP.md](./DATABASE_SETUP.md)
3. Check error log di `logs/django.log`
4. Contact development team

---

**Document Version:** 1.0
**Last Updated:** 2024-01-14
**Author:** SIM SMA BIMA Development Team

# 📥 Panduan Instalasi SIM Akademik

## Daftar Isi
1. [Persiapan](#persiapan)
2. [Instalasi di Windows](#instalasi-di-windows)
3. [Instalasi di macOS/Linux](#instalasi-di-macoslinux)
4. [Troubleshooting](#troubleshooting)
5. [Konfigurasi](#konfigurasi)

---

## Persiapan

### Requirement Sistem

**Minimum:**
- OS: Windows 10/11, macOS 10.14+, atau Linux (Ubuntu 18.04+)
- RAM: 4 GB
- Storage: 500 MB free space
- Python: 3.8 atau lebih tinggi

**Recommended:**
- RAM: 8 GB atau lebih
- Storage: 1 GB free space
- Python: 3.10+

### Check Python Version

Buka terminal/command prompt dan jalankan:

```bash
python --version
# atau
python3 --version
```

Jika Python belum terinstall, download dari [python.org](https://www.python.org/downloads/)

---

## Instalasi di Windows

### Step 1: Download Project

**Opsi A: Menggunakan Git**
```bash
# Install Git terlebih dahulu jika belum ada
# Download dari: https://git-scm.com/download/win

# Clone repository
git clone https://github.com/fadenco/sim-akademik.git
cd sim-akademik
```

**Opsi B: Download ZIP**
1. Download ZIP dari GitHub
2. Extract ke folder pilihan Anda
3. Buka Command Prompt di folder tersebut

### Step 2: Buat Virtual Environment

```bash
# Buat virtual environment
python -m venv venv

# Aktifkan virtual environment
venv\Scripts\activate

# Anda akan melihat (venv) di awal baris command
```

### Step 3: Install Dependencies

```bash
# Update pip terlebih dahulu
python -m pip install --upgrade pip

# Install semua dependencies
pip install -r requirements.txt
```

### Step 4: Verifikasi Instalasi

```bash
# Check Streamlit
streamlit --version

# Check pandas
python -c "import pandas; print(pandas.__version__)"

# Check plotly
python -c "import plotly; print(plotly.__version__)"
```

### Step 5: Jalankan Aplikasi

```bash
streamlit run app.py
```

Browser akan otomatis membuka aplikasi di `http://localhost:8501`

---

## Instalasi di macOS/Linux

### Step 1: Download Project

```bash
# Clone repository
git clone https://github.com/fadenco/sim-akademik.git
cd sim-akademik
```

### Step 2: Buat Virtual Environment

```bash
# Buat virtual environment
python3 -m venv venv

# Aktifkan virtual environment
source venv/bin/activate

# Anda akan melihat (venv) di awal baris command
```

### Step 3: Install Dependencies

```bash
# Update pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt
```

### Step 4: Verifikasi Instalasi

```bash
# Check semua packages
streamlit --version
python -c "import pandas; print(pandas.__version__)"
python -c "import plotly; print(plotly.__version__)"
```

### Step 5: Jalankan Aplikasi

```bash
streamlit run app.py
```

---

## Troubleshooting

### Error: "Python not found" atau "Command not found"

**Windows:**
1. Install Python dari python.org
2. Pastikan checkbox "Add Python to PATH" tercentang saat instalasi
3. Restart Command Prompt

**macOS/Linux:**
```bash
# Install Python 3
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install python3 python3-pip python3-venv

# macOS (menggunakan Homebrew)
brew install python3
```

### Error: "pip: command not found"

```bash
# Windows
python -m ensurepip --upgrade

# macOS/Linux
python3 -m ensurepip --upgrade
```

### Error: "Permission denied" (Linux/macOS)

```bash
# Gunakan pip tanpa sudo dengan virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Error: Package installation failed

```bash
# Clean pip cache
pip cache purge

# Install ulang dengan verbose
pip install -r requirements.txt -v

# Jika masih error, install satu per satu
pip install streamlit
pip install pandas
pip install plotly
# dst...
```

### Error: "ModuleNotFoundError" saat menjalankan aplikasi

```bash
# Pastikan virtual environment aktif
# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate

# Install ulang dependencies
pip install -r requirements.txt
```

### Error: Port 8501 sudah digunakan

```bash
# Gunakan port lain
streamlit run app.py --server.port 8502

# Atau kill process yang menggunakan port 8501
# Windows:
netstat -ano | findstr :8501
taskkill /PID <PID> /F

# macOS/Linux:
lsof -ti:8501 | xargs kill -9
```

### Aplikasi lambat atau hang

1. **Check memory usage** - Tutup aplikasi lain
2. **Clear browser cache** - Clear cache browser Anda
3. **Reduce data size** - Upload data dalam batch lebih kecil
4. **Restart aplikasi** - Ctrl+C di terminal, lalu jalankan ulang

---

## Konfigurasi

### Konfigurasi Streamlit

Edit file `.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#3B82F6"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F3F4F6"
textColor = "#1F2937"
font = "sans serif"

[server]
port = 8501
enableCORS = false
maxUploadSize = 200

[browser]
gatherUsageStats = false
```

### Konfigurasi Aplikasi

Edit file `config/settings.py`:

```python
# Pengaturan aplikasi
APP_NAME = "SIM Akademik"
APP_VERSION = "1.0.0"

# Pengaturan data
MAX_UPLOAD_SIZE_MB = 50
ALLOWED_FILE_TYPES = ['csv', 'xlsx', 'xls']

# Pengaturan visualisasi
CHART_HEIGHT = 400
CHART_WIDTH = 600
```

---

## Update Aplikasi

### Jika menggunakan Git:

```bash
# Pull latest changes
git pull origin main

# Install/update dependencies baru
pip install -r requirements.txt --upgrade
```

### Jika download manual:

1. Download ZIP versi terbaru
2. Backup data Anda (folder `data/`)
3. Replace semua file (kecuali `data/`)
4. Jalankan `pip install -r requirements.txt --upgrade`

---

## Uninstall

### Hapus Virtual Environment

```bash
# Windows
rmdir /s venv

# macOS/Linux
rm -rf venv
```

### Hapus Project Folder

Hapus folder `sim-akademik` secara manual

---

## Tips & Best Practices

1. **Selalu gunakan virtual environment** - Hindari conflict dengan package lain
2. **Update dependencies secara berkala** - `pip install -r requirements.txt --upgrade`
3. **Backup data** - Backup folder `data/` secara berkala
4. **Monitor resource** - Check CPU dan RAM usage
5. **Check logs** - Lihat terminal untuk error messages

---

## Dukungan

Jika masih mengalami masalah:

1. 📧 Email: support@simakademik.edu
2. 🐛 [Report Issue](https://github.com/fadenco/sim-akademik/issues)
3. 💬 [Discussions](https://github.com/fadenco/sim-akademik/discussions)

---

**Selamat menggunakan SIM Akademik! 🎓**

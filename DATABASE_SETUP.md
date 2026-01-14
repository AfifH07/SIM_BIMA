# 🗄️ Database Setup Guide - PostgreSQL

## 1. Install PostgreSQL

### Windows:
1. Download dari https://www.postgresql.org/download/windows/
2. Run installer
3. Set password untuk user `postgres`
4. Port default: 5432

### macOS (Homebrew):
```bash
brew install postgresql@14
brew services start postgresql@14
```

### Linux (Ubuntu/Debian):
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

---

## 2. Create Database

### Method 1: Using psql (Command Line)

```bash
# Login as postgres user
psql -U postgres

# Create database
CREATE DATABASE sim_sma_bima_dev;

# Create user (optional, for security)
CREATE USER sim_user WITH PASSWORD 'secure_password_here';

# Grant privileges
GRANT ALL PRIVILEGES ON DATABASE sim_sma_bima_dev TO sim_user;

# Connect to database
\c sim_sma_bima_dev

# List databases
\l

# Exit
\q
```

### Method 2: Using pgAdmin (GUI)

1. Open pgAdmin
2. Right-click "Databases" → "Create" → "Database"
3. Name: `sim_sma_bima_dev`
4. Owner: `postgres` (or `sim_user`)
5. Click "Save"

---

## 3. Configure Django Database Connection

Edit `.env` file:

```env
DB_ENGINE=django.db.backends.postgresql
DB_NAME=sim_sma_bima_dev
DB_USER=postgres
DB_PASSWORD=your_postgres_password
DB_HOST=localhost
DB_PORT=5432
```

---

## 4. Test Connection

```bash
cd backend

# Test connection using Django
python manage.py dbshell

# If successful, you'll see PostgreSQL prompt:
# sim_sma_bima_dev=#

# Exit with: \q
```

---

## 5. Run Migrations

```bash
# Create migration files
python manage.py makemigrations

# Apply migrations to database
python manage.py migrate

# Verify tables created
python manage.py dbshell
\dt  # List all tables
\q
```

---

## 6. Create Superuser

```bash
python manage.py createsuperuser

# Enter details:
# Email: admin@example.com
# Full name: Admin User
# Password: (enter secure password)
# Password (again): (confirm password)
```

---

## 7. Common PostgreSQL Commands

```sql
-- List all databases
\l

-- Connect to database
\c sim_sma_bima_dev

-- List all tables
\dt

-- Describe table structure
\d students

-- List all users
\du

-- Show current database
SELECT current_database();

-- Show all tables with row count
SELECT schemaname,relname,n_live_tup
FROM pg_stat_user_tables
ORDER BY n_live_tup DESC;
```

---

## 8. Backup & Restore

### Backup Database:

```bash
# Full backup
pg_dump -U postgres sim_sma_bima_dev > backup.sql

# Compressed backup
pg_dump -U postgres sim_sma_bima_dev | gzip > backup.sql.gz
```

### Restore Database:

```bash
# Drop existing database (CAUTION!)
psql -U postgres -c "DROP DATABASE sim_sma_bima_dev;"

# Create new database
psql -U postgres -c "CREATE DATABASE sim_sma_bima_dev;"

# Restore from backup
psql -U postgres sim_sma_bima_dev < backup.sql

# Or from compressed backup
gunzip -c backup.sql.gz | psql -U postgres sim_sma_bima_dev
```

---

## 9. Troubleshooting

### Can't connect to PostgreSQL:

```bash
# Check service status
# Windows: services.msc → PostgreSQL
# Linux: sudo systemctl status postgresql

# Start service
# Windows: Start from services.msc
# Linux: sudo systemctl start postgresql
```

### Password authentication failed:

1. Edit `pg_hba.conf`:
   - Windows: `C:\Program Files\PostgreSQL\14\data\pg_hba.conf`
   - Linux: `/etc/postgresql/14/main/pg_hba.conf`

2. Change method to `md5`:
```
# TYPE  DATABASE        USER            ADDRESS                 METHOD
local   all             postgres                                md5
host    all             all             127.0.0.1/32            md5
```

3. Restart PostgreSQL:
```bash
# Linux
sudo systemctl restart postgresql

# Windows
# Restart from services.msc
```

### Port 5432 already in use:

```bash
# Find process using port
# Windows: netstat -ano | findstr :5432
# Linux: sudo lsof -i :5432

# Kill process or change PostgreSQL port in postgresql.conf
```

---

**Last Updated:** 2024-01-14

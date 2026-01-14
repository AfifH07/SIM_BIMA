# Database Schema & ERD - SIM SMA BIMA

## 1. Database Overview

**Database Management System**: PostgreSQL 14+
**Normalization Level**: Third Normal Form (3NF)
**Character Encoding**: UTF-8
**Collation**: Indonesian (id_ID.UTF-8)

## 2. Entity Relationship Diagram (ERD)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         SIM SMA BIMA - DATABASE ERD                          │
└─────────────────────────────────────────────────────────────────────────────┘

┌──────────────────┐
│      users       │
├──────────────────┤
│ PK id           │◄─────────┐
│    email (UQ)   │          │
│    password     │          │
│    full_name    │          │ One
│    role         │          │
│    phone_number │          │
│    address      │          │
│    photo        │          │
│    is_active    │          │
│    date_joined  │          │
└──────────────────┘          │
                              │
         ┌────────────────────┼──────────────────────┐
         │                    │                      │
         │ One                │ One                  │ One
         │                    │                      │
┌────────▼────────┐  ┌────────▼────────┐  ┌────────▼────────┐
│    students     │  │    teachers     │  │  parent_profiles│
├─────────────────┤  ├─────────────────┤  ├─────────────────┤
│ PK id          │  │ PK id          │  │ PK id          │
│ FK user_id     │  │ FK user_id     │  │ FK user_id     │
│    nis (UQ)    │  │    nip (UQ)    │  │    relationship│
│    nisn        │  │    full_name   │  │    occupation  │
│    full_name   │  │    subject     │  └─────────────────┘
│    gender      │  │    qualification│          │
│    date_of_birth│ │    hire_date   │          │
│    place_of_birth│ │    status      │          │ Many
│    religion    │  │    photo       │          │
│    address     │  └─────────────────┘          │
│    city        │          │                    │
│    province    │          │ One                │
│    parent_name │          │                    │
│    parent_phone│          │                    │
│    admission_date│         │                   │
│ FK class_room_id│          │                   │
│    status      │          │                    │
│    photo       │          │                    │
└─────────────────┘          │                    │
         │                   │                    │
         │ Many              │                    │
         │                   │                    │
         │                   │                    │
┌────────▼────────┐          │         ┌──────────▼──────────┐
│parent_student   │          │         │   classrooms        │
├─────────────────┤          │         ├─────────────────────┤
│ PK id          │          │         │ PK id              │
│ FK parent_id   │──────────┘         │    name (UQ)       │
│ FK student_id  │                    │    grade_level     │
└─────────────────┘                    │    academic_year   │
                                       │ FK homeroom_teacher│
                                       │    capacity        │
         ┌─────────────────────────────┤    created_at      │
         │                             └─────────────────────┘
         │ Many                                │
         │                                     │ One
┌────────▼────────┐                            │
│     grades      │                            │
├─────────────────┤                            │
│ PK id          │                  ┌──────────▼──────────┐
│ FK student_id  │                  │   class_subjects    │
│ FK subject_id  │                  ├─────────────────────┤
│ FK teacher_id  │                  │ PK id              │
│    semester    │                  │ FK classroom_id    │
│    exam_type   │                  │ FK subject_id      │
│    value       │                  │ FK teacher_id      │
│    date        │                  │    schedule_day    │
│    notes       │                  │    schedule_time   │
└─────────────────┘                  └─────────────────────┘
         │                                     │
         │ Many                                │ Many
         │                                     │
         │              ┌──────────────────────┘
         │              │
         │      ┌───────▼────────┐
         └──────►    subjects    │
                ├────────────────┤
                │ PK id         │
                │    code (UQ)  │
                │    name       │
                │    category   │
                │    description│
                │    credits    │
                └────────────────┘

┌──────────────────┐
│   transactions   │
├──────────────────┤
│ PK id           │
│ FK student_id   │
│    type         │
│    category     │
│    amount       │
│    date         │
│    description  │
│    payment_method│
│    status       │
│    receipt_no   │
└──────────────────┘

┌────────────────────┐
│  extracurricular   │
├────────────────────┤
│ PK id             │
│    name           │
│    category       │
│    description    │
│ FK teacher_id     │
│    schedule_day   │
│    schedule_time  │
│    max_participants│
└────────────────────┘
         │
         │ Many-to-Many
         │
┌────────▼──────────────┐
│extracurricular_students│
├───────────────────────┤
│ PK id                │
│ FK extracurricular_id│
│ FK student_id        │
│    join_date         │
│    status            │
└───────────────────────┘

┌──────────────────┐
│   attendances    │
├──────────────────┤
│ PK id           │
│ FK student_id   │
│ FK subject_id   │
│    date         │
│    status       │
│    notes        │
└──────────────────┘

┌──────────────────┐
│ ptn_predictions  │
├──────────────────┤
│ PK id           │
│ FK student_id   │
│    probability  │
│    features     │ (JSONB)
│    model_version│
│    created_at   │
│    university   │
│    major        │
└──────────────────┘

Legend:
PK = Primary Key
FK = Foreign Key
UQ = Unique Constraint
```

## 3. Table Specifications

### 3.1 Users Table

Menyimpan data autentikasi dan informasi dasar user.

| Column         | Type         | Constraints                      | Description                    |
|----------------|--------------|----------------------------------|--------------------------------|
| id             | SERIAL       | PRIMARY KEY                      | Unique identifier              |
| email          | VARCHAR(255) | UNIQUE, NOT NULL                 | Email untuk login              |
| password       | VARCHAR(128) | NOT NULL                         | Hashed password                |
| full_name      | VARCHAR(255) | NOT NULL                         | Nama lengkap                   |
| role           | VARCHAR(10)  | NOT NULL, CHECK                  | ADMIN/TEACHER/STUDENT/PARENT   |
| phone_number   | VARCHAR(20)  | NULL                             | Nomor telepon                  |
| address        | TEXT         | NULL                             | Alamat lengkap                 |
| photo          | VARCHAR(255) | NULL                             | Path foto profil               |
| date_of_birth  | DATE         | NULL                             | Tanggal lahir                  |
| is_active      | BOOLEAN      | DEFAULT TRUE                     | Status aktif                   |
| is_verified    | BOOLEAN      | DEFAULT FALSE                    | Status verifikasi              |
| date_joined    | TIMESTAMP    | DEFAULT CURRENT_TIMESTAMP        | Tanggal bergabung              |
| last_login     | TIMESTAMP    | NULL                             | Login terakhir                 |

**Indexes:**
- `idx_users_email` ON email
- `idx_users_role` ON role

### 3.2 Students Table

Menyimpan data siswa lengkap.

| Column          | Type         | Constraints              | Description                |
|-----------------|--------------|--------------------------|----------------------------|
| id              | SERIAL       | PRIMARY KEY              | Unique identifier          |
| user_id         | INTEGER      | FOREIGN KEY, UNIQUE, NULL| Reference ke users         |
| nis             | VARCHAR(20)  | UNIQUE, NOT NULL         | Nomor Induk Siswa          |
| nisn            | VARCHAR(20)  | UNIQUE, NULL             | NISN                       |
| full_name       | VARCHAR(255) | NOT NULL                 | Nama lengkap               |
| nickname        | VARCHAR(100) | NULL                     | Nama panggilan             |
| gender          | CHAR(1)      | CHECK (M/F)              | Jenis kelamin              |
| date_of_birth   | DATE         | NOT NULL                 | Tanggal lahir              |
| place_of_birth  | VARCHAR(100) | NOT NULL                 | Tempat lahir               |
| religion        | VARCHAR(50)  | NOT NULL                 | Agama                      |
| blood_type      | VARCHAR(3)   | NULL                     | Golongan darah             |
| address         | TEXT         | NOT NULL                 | Alamat lengkap             |
| city            | VARCHAR(100) | NOT NULL                 | Kota                       |
| province        | VARCHAR(100) | NOT NULL                 | Provinsi                   |
| postal_code     | VARCHAR(10)  | NULL                     | Kode pos                   |
| phone_number    | VARCHAR(20)  | NULL                     | Nomor telepon              |
| email           | VARCHAR(255) | NULL                     | Email siswa                |
| parent_name     | VARCHAR(255) | NOT NULL                 | Nama orang tua             |
| parent_phone    | VARCHAR(20)  | NOT NULL                 | Telepon orang tua          |
| parent_email    | VARCHAR(255) | NULL                     | Email orang tua            |
| parent_occupation| VARCHAR(100)| NULL                     | Pekerjaan orang tua        |
| parent_address  | TEXT         | NULL                     | Alamat orang tua           |
| admission_date  | DATE         | NOT NULL                 | Tanggal masuk              |
| graduation_date | DATE         | NULL                     | Tanggal lulus              |
| status          | VARCHAR(10)  | DEFAULT 'ACTIVE'         | Status siswa               |
| class_room_id   | INTEGER      | FOREIGN KEY, NULL        | Reference ke classrooms    |
| photo           | VARCHAR(255) | NULL                     | Path foto                  |
| created_at      | TIMESTAMP    | DEFAULT CURRENT_TIMESTAMP| Tanggal dibuat             |
| updated_at      | TIMESTAMP    | AUTO UPDATE              | Tanggal diupdate           |

**Indexes:**
- `idx_students_nis` ON nis
- `idx_students_nisn` ON nisn
- `idx_students_status` ON status
- `idx_students_class_room` ON class_room_id

### 3.3 Teachers Table

| Column          | Type         | Constraints              | Description                |
|-----------------|--------------|--------------------------|----------------------------|
| id              | SERIAL       | PRIMARY KEY              | Unique identifier          |
| user_id         | INTEGER      | FOREIGN KEY, UNIQUE, NULL| Reference ke users         |
| nip             | VARCHAR(20)  | UNIQUE, NOT NULL         | Nomor Induk Pegawai        |
| full_name       | VARCHAR(255) | NOT NULL                 | Nama lengkap               |
| gender          | CHAR(1)      | CHECK (M/F)              | Jenis kelamin              |
| date_of_birth   | DATE         | NOT NULL                 | Tanggal lahir              |
| subject         | VARCHAR(100) | NOT NULL                 | Mata pelajaran             |
| qualification   | VARCHAR(100) | NOT NULL                 | Kualifikasi                |
| hire_date       | DATE         | NOT NULL                 | Tanggal bergabung          |
| status          | VARCHAR(10)  | DEFAULT 'ACTIVE'         | Status guru                |
| phone_number    | VARCHAR(20)  | NULL                     | Nomor telepon              |
| email           | VARCHAR(255) | NULL                     | Email                      |
| address         | TEXT         | NULL                     | Alamat                     |
| photo           | VARCHAR(255) | NULL                     | Path foto                  |
| created_at      | TIMESTAMP    | DEFAULT CURRENT_TIMESTAMP| Tanggal dibuat             |
| updated_at      | TIMESTAMP    | AUTO UPDATE              | Tanggal diupdate           |

**Indexes:**
- `idx_teachers_nip` ON nip
- `idx_teachers_status` ON status

### 3.4 ClassRooms Table

| Column              | Type         | Constraints              | Description                |
|---------------------|--------------|--------------------------|----------------------------|
| id                  | SERIAL       | PRIMARY KEY              | Unique identifier          |
| name                | VARCHAR(50)  | UNIQUE, NOT NULL         | Nama kelas (XII IPA 1)     |
| grade_level         | INTEGER      | NOT NULL                 | Tingkat kelas (10/11/12)   |
| academic_year       | VARCHAR(10)  | NOT NULL                 | Tahun ajaran (2023/2024)   |
| homeroom_teacher_id | INTEGER      | FOREIGN KEY, NULL        | Wali kelas                 |
| capacity            | INTEGER      | DEFAULT 36               | Kapasitas siswa            |
| room_number         | VARCHAR(20)  | NULL                     | Nomor ruangan              |
| created_at          | TIMESTAMP    | DEFAULT CURRENT_TIMESTAMP| Tanggal dibuat             |
| updated_at          | TIMESTAMP    | AUTO UPDATE              | Tanggal diupdate           |

**Indexes:**
- `idx_classrooms_name` ON name
- `idx_classrooms_grade_level` ON grade_level

### 3.5 Subjects Table

| Column       | Type         | Constraints              | Description                |
|--------------|--------------|--------------------------|----------------------------|
| id           | SERIAL       | PRIMARY KEY              | Unique identifier          |
| code         | VARCHAR(20)  | UNIQUE, NOT NULL         | Kode mata pelajaran        |
| name         | VARCHAR(100) | NOT NULL                 | Nama mata pelajaran        |
| category     | VARCHAR(50)  | NOT NULL                 | Kategori (UMUM/PEMINATAN)  |
| description  | TEXT         | NULL                     | Deskripsi                  |
| credits      | INTEGER      | DEFAULT 2                | SKS                        |
| created_at   | TIMESTAMP    | DEFAULT CURRENT_TIMESTAMP| Tanggal dibuat             |

### 3.6 Grades Table

| Column      | Type         | Constraints              | Description                |
|-------------|--------------|--------------------------|----------------------------|
| id          | SERIAL       | PRIMARY KEY              | Unique identifier          |
| student_id  | INTEGER      | FOREIGN KEY, NOT NULL    | Reference ke students      |
| subject_id  | INTEGER      | FOREIGN KEY, NOT NULL    | Reference ke subjects      |
| teacher_id  | INTEGER      | FOREIGN KEY, NOT NULL    | Reference ke teachers      |
| semester    | INTEGER      | CHECK (1/2)              | Semester                   |
| exam_type   | VARCHAR(20)  | NOT NULL                 | UH/UTS/UAS                 |
| value       | DECIMAL(5,2) | CHECK (0-100)            | Nilai                      |
| date        | DATE         | NOT NULL                 | Tanggal ujian              |
| notes       | TEXT         | NULL                     | Catatan                    |
| created_at  | TIMESTAMP    | DEFAULT CURRENT_TIMESTAMP| Tanggal dibuat             |

**Indexes:**
- `idx_grades_student` ON student_id
- `idx_grades_subject` ON subject_id
- `idx_grades_semester` ON semester

### 3.7 Transactions Table

| Column         | Type         | Constraints              | Description                |
|----------------|--------------|--------------------------|----------------------------|
| id             | SERIAL       | PRIMARY KEY              | Unique identifier          |
| student_id     | INTEGER      | FOREIGN KEY, NULL        | Reference ke students      |
| type           | VARCHAR(10)  | CHECK (INCOME/EXPENSE)   | Tipe transaksi             |
| category       | VARCHAR(50)  | NOT NULL                 | Kategori (SPP/UANG MAKAN)  |
| amount         | DECIMAL(12,2)| NOT NULL                 | Jumlah                     |
| date           | DATE         | NOT NULL                 | Tanggal transaksi          |
| description    | TEXT         | NULL                     | Keterangan                 |
| payment_method | VARCHAR(20)  | NOT NULL                 | Metode pembayaran          |
| status         | VARCHAR(20)  | DEFAULT 'PENDING'        | Status                     |
| receipt_no     | VARCHAR(50)  | UNIQUE, NULL             | Nomor bukti                |
| created_at     | TIMESTAMP    | DEFAULT CURRENT_TIMESTAMP| Tanggal dibuat             |

**Indexes:**
- `idx_transactions_student` ON student_id
- `idx_transactions_date` ON date
- `idx_transactions_type` ON type

### 3.8 PTN Predictions Table

| Column        | Type         | Constraints              | Description                |
|---------------|--------------|--------------------------|----------------------------|
| id            | SERIAL       | PRIMARY KEY              | Unique identifier          |
| student_id    | INTEGER      | FOREIGN KEY, NOT NULL    | Reference ke students      |
| probability   | DECIMAL(5,2) | CHECK (0-100)            | Probabilitas kelulusan     |
| features      | JSONB        | NOT NULL                 | Features yang digunakan    |
| model_version | VARCHAR(20)  | NOT NULL                 | Versi model                |
| university    | VARCHAR(255) | NULL                     | Target universitas         |
| major         | VARCHAR(255) | NULL                     | Target jurusan             |
| created_at    | TIMESTAMP    | DEFAULT CURRENT_TIMESTAMP| Tanggal prediksi           |

**Indexes:**
- `idx_predictions_student` ON student_id
- `idx_predictions_created` ON created_at

## 4. Normalization Analysis

### 4.1 First Normal Form (1NF)
✅ **Passed**
- Semua tabel memiliki primary key
- Tidak ada repeating groups
- Setiap kolom berisi atomic values

### 4.2 Second Normal Form (2NF)
✅ **Passed**
- Semua tabel sudah 1NF
- Tidak ada partial dependencies
- Non-key attributes tergantung penuh pada primary key

### 4.3 Third Normal Form (3NF)
✅ **Passed**
- Semua tabel sudah 2NF
- Tidak ada transitive dependencies
- Non-key attributes tidak tergantung pada non-key attributes lain

## 5. Relationships Summary

| Relationship                      | Type        | FK Location      |
|-----------------------------------|-------------|------------------|
| Users → Students                  | One-to-One  | students.user_id |
| Users → Teachers                  | One-to-One  | teachers.user_id |
| ClassRooms → Students             | One-to-Many | students.class_room_id |
| Teachers → ClassRooms (Homeroom)  | One-to-Many | classrooms.homeroom_teacher_id |
| Students → Grades                 | One-to-Many | grades.student_id |
| Subjects → Grades                 | One-to-Many | grades.subject_id |
| Teachers → Grades                 | One-to-Many | grades.teacher_id |
| Students → Transactions           | One-to-Many | transactions.student_id |
| Students → PTN Predictions        | One-to-Many | ptn_predictions.student_id |
| Extracurricular ↔ Students        | Many-to-Many| extracurricular_students |

## 6. Data Integrity Constraints

### 6.1 Cascading Rules

```sql
-- Delete User → Delete Student/Teacher
ON DELETE CASCADE

-- Delete ClassRoom → Set NULL pada Students
ON DELETE SET NULL

-- Delete Student → Delete Grades, Transactions, Predictions
ON DELETE CASCADE
```

### 6.2 Check Constraints

```sql
-- Gender must be 'M' or 'F'
CHECK (gender IN ('M', 'F'))

-- Grade value 0-100
CHECK (value >= 0 AND value <= 100)

-- Probability 0-100
CHECK (probability >= 0 AND probability <= 100)

-- Role validation
CHECK (role IN ('ADMIN', 'TEACHER', 'STUDENT', 'PARENT'))
```

---

**Document Version**: 1.0
**Last Updated**: 2024-01-14

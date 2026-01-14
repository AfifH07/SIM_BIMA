# API Endpoints Documentation - SIM SMA BIMA

## Base URL

```
Development: http://localhost:8000/api
Production: https://api.simsma.com/api
```

## Authentication

Semua endpoint (kecuali login/register) memerlukan authentication token.

**Header Format:**
```
Authorization: Token <your-token-here>
```

---

## 1. Authentication Endpoints

### 1.1 Login

**Endpoint:** `POST /api/auth/login/`

**Request Body:**
```json
{
  "email": "admin@example.com",
  "password": "password123"
}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "email": "admin@example.com",
  "full_name": "Admin User",
  "role": "ADMIN",
  "role_display": "Admin Sekolah",
  "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
  "is_verified": true
}
```

### 1.2 Logout

**Endpoint:** `POST /api/auth/logout/`

**Headers:**
```
Authorization: Token <token>
```

**Response (200 OK):**
```json
{
  "message": "Logout berhasil"
}
```

### 1.3 Change Password

**Endpoint:** `POST /api/auth/change-password/`

**Request Body:**
```json
{
  "old_password": "oldpass123",
  "new_password": "newpass456"
}
```

**Response (200 OK):**
```json
{
  "message": "Password berhasil diubah",
  "new_token": "new-token-here"
}
```

---

## 2. Students Endpoints

### 2.1 List Students

**Endpoint:** `GET /api/students/`

**Query Parameters:**
- `search` - Search by name, NIS, NISN (optional)
- `status` - Filter by status: ACTIVE, GRADUATED, DROPPED (optional)
- `class_id` - Filter by class ID (optional)
- `gender` - Filter by gender: M, F (optional)
- `page` - Page number (default: 1)
- `page_size` - Items per page (default: 20)

**Response (200 OK):**
```json
{
  "count": 100,
  "next": "http://localhost:8000/api/students/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "nis": "2023001",
      "full_name": "Ahmad Rizki",
      "gender": "M",
      "gender_display": "Laki-laki",
      "age": 17,
      "status": "ACTIVE",
      "status_display": "Aktif",
      "class_room": 1,
      "phone_number": "081234567890",
      "email": "ahmad@example.com"
    }
  ]
}
```

### 2.2 Get Student Detail

**Endpoint:** `GET /api/students/{id}/`

**Response (200 OK):**
```json
{
  "id": 1,
  "user": null,
  "nis": "2023001",
  "nisn": "0012345678",
  "full_name": "Ahmad Rizki",
  "nickname": "Rizki",
  "gender": "M",
  "gender_display": "Laki-laki",
  "date_of_birth": "2006-05-15",
  "place_of_birth": "Jakarta",
  "religion": "Islam",
  "blood_type": "A",
  "address": "Jl. Merdeka No. 123",
  "city": "Jakarta",
  "province": "DKI Jakarta",
  "postal_code": "12345",
  "phone_number": "081234567890",
  "email": "ahmad@example.com",
  "parent_name": "Budi Santoso",
  "parent_phone": "081987654321",
  "parent_email": "budi@example.com",
  "parent_occupation": "Wiraswasta",
  "parent_address": "Jl. Merdeka No. 123",
  "admission_date": "2023-07-01",
  "graduation_date": null,
  "status": "ACTIVE",
  "status_display": "Aktif",
  "class_room": 1,
  "photo": "/media/students/photos/rizki.jpg",
  "age": 17,
  "is_active": true,
  "full_address": "Jl. Merdeka No. 123, Jakarta, DKI Jakarta",
  "created_at": "2024-01-01T10:00:00Z",
  "updated_at": "2024-01-14T15:30:00Z"
}
```

### 2.3 Create Student

**Endpoint:** `POST /api/students/`

**Request Body:**
```json
{
  "nis": "2024001",
  "nisn": "0012345679",
  "full_name": "Siti Nurhaliza",
  "nickname": "Siti",
  "gender": "F",
  "date_of_birth": "2006-03-20",
  "place_of_birth": "Bandung",
  "religion": "Islam",
  "blood_type": "B",
  "address": "Jl. Sudirman No. 456",
  "city": "Bandung",
  "province": "Jawa Barat",
  "postal_code": "40123",
  "phone_number": "082123456789",
  "email": "siti@example.com",
  "parent_name": "Ahmad Wijaya",
  "parent_phone": "081234567890",
  "parent_email": "ahmad@example.com",
  "parent_occupation": "Pegawai Negeri",
  "admission_date": "2024-07-01"
}
```

**Response (201 CREATED):**
```json
{
  "id": 2,
  "nis": "2024001",
  "full_name": "Siti Nurhaliza",
  ...
}
```

### 2.4 Update Student

**Endpoint:** `PUT /api/students/{id}/` (Full update)
**Endpoint:** `PATCH /api/students/{id}/` (Partial update)

**Request Body (PATCH example):**
```json
{
  "phone_number": "082999888777",
  "email": "newemail@example.com"
}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "phone_number": "082999888777",
  "email": "newemail@example.com",
  ...
}
```

### 2.5 Delete Student

**Endpoint:** `DELETE /api/students/{id}/`

**Response (200 OK):**
```json
{
  "message": "Siswa berhasil dihapus."
}
```

### 2.6 Get Active Students

**Endpoint:** `GET /api/students/active/`

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "nis": "2023001",
    "full_name": "Ahmad Rizki",
    ...
  }
]
```

### 2.7 Get Students Statistics

**Endpoint:** `GET /api/students/statistics/`

**Response (200 OK):**
```json
{
  "total": 340,
  "active": 320,
  "graduated": 15,
  "dropped": 3,
  "suspended": 2,
  "male": 180,
  "female": 160
}
```

### 2.8 Graduate Student

**Endpoint:** `POST /api/students/{id}/graduate/`

**Response (200 OK):**
```json
{
  "id": 1,
  "status": "GRADUATED",
  "graduation_date": "2024-06-15",
  ...
}
```

---

## 3. Teachers Endpoints

### 3.1 List Teachers

**Endpoint:** `GET /api/teachers/`

**Query Parameters:**
- `search` - Search by name, NIP
- `status` - Filter by status
- `subject` - Filter by subject

**Response (200 OK):**
```json
{
  "count": 45,
  "results": [
    {
      "id": 1,
      "nip": "198501012010011001",
      "full_name": "Dr. Hadi Wijaya",
      "subject": "Matematika",
      "status": "ACTIVE"
    }
  ]
}
```

### 3.2 Create Teacher

**Endpoint:** `POST /api/teachers/`

**Request Body:**
```json
{
  "nip": "199003032015011002",
  "full_name": "Siti Aminah, M.Pd",
  "gender": "F",
  "date_of_birth": "1990-03-03",
  "subject": "Bahasa Indonesia",
  "qualification": "S2 Pendidikan Bahasa",
  "hire_date": "2015-01-15",
  "phone_number": "081234567890",
  "email": "siti@example.com"
}
```

---

## 4. Classes Endpoints

### 4.1 List Classes

**Endpoint:** `GET /api/classes/`

**Response (200 OK):**
```json
{
  "results": [
    {
      "id": 1,
      "name": "XII IPA 1",
      "grade_level": 12,
      "academic_year": "2023/2024",
      "homeroom_teacher": {
        "id": 1,
        "full_name": "Dr. Hadi Wijaya"
      },
      "student_count": 36
    }
  ]
}
```

### 4.2 Get Class Detail with Students

**Endpoint:** `GET /api/classes/{id}/`

**Response (200 OK):**
```json
{
  "id": 1,
  "name": "XII IPA 1",
  "students": [
    {
      "id": 1,
      "nis": "2023001",
      "full_name": "Ahmad Rizki"
    }
  ],
  "subjects": [
    {
      "id": 1,
      "name": "Matematika",
      "teacher": "Dr. Hadi Wijaya"
    }
  ]
}
```

---

## 5. Grades Endpoints

### 5.1 Get Student Grades

**Endpoint:** `GET /api/grades/?student_id={student_id}`

**Response (200 OK):**
```json
{
  "results": [
    {
      "id": 1,
      "student": "Ahmad Rizki",
      "subject": "Matematika",
      "teacher": "Dr. Hadi Wijaya",
      "semester": 1,
      "exam_type": "UTS",
      "value": 85.5,
      "date": "2024-01-15"
    }
  ]
}
```

### 5.2 Input Grade

**Endpoint:** `POST /api/grades/`

**Request Body:**
```json
{
  "student_id": 1,
  "subject_id": 1,
  "teacher_id": 1,
  "semester": 1,
  "exam_type": "UAS",
  "value": 90.0,
  "date": "2024-06-15",
  "notes": "Nilai bagus"
}
```

---

## 6. Finance Endpoints

### 6.1 List Transactions

**Endpoint:** `GET /api/finance/transactions/`

**Query Parameters:**
- `type` - INCOME or EXPENSE
- `student_id` - Filter by student
- `date_from` - Start date (YYYY-MM-DD)
- `date_to` - End date (YYYY-MM-DD)

**Response (200 OK):**
```json
{
  "results": [
    {
      "id": 1,
      "student": "Ahmad Rizki",
      "type": "INCOME",
      "category": "SPP",
      "amount": 500000,
      "date": "2024-01-05",
      "payment_method": "Transfer",
      "status": "PAID",
      "receipt_no": "RCP-2024-001"
    }
  ]
}
```

### 6.2 Create Transaction

**Endpoint:** `POST /api/finance/transactions/`

**Request Body:**
```json
{
  "student_id": 1,
  "type": "INCOME",
  "category": "SPP",
  "amount": 500000,
  "date": "2024-02-05",
  "description": "Pembayaran SPP Februari 2024",
  "payment_method": "Transfer"
}
```

### 6.3 Financial Report

**Endpoint:** `GET /api/finance/report/`

**Query Parameters:**
- `month` - Month (1-12)
- `year` - Year (YYYY)

**Response (200 OK):**
```json
{
  "period": "Januari 2024",
  "total_income": 55000000,
  "total_expense": 40000000,
  "balance": 15000000,
  "income_by_category": {
    "SPP": 50000000,
    "Uang Pendaftaran": 5000000
  },
  "expense_by_category": {
    "Gaji": 35000000,
    "ATK": 3000000,
    "Listrik": 2000000
  }
}
```

---

## 7. Predictions Endpoints

### 7.1 Create PTN Prediction

**Endpoint:** `POST /api/predictions/ptn/`

**Request Body:**
```json
{
  "student_id": 1,
  "features": {
    "nilai_rata": 85.5,
    "nilai_un": 88.0,
    "prestasi_count": 3,
    "ekstrakurikuler_score": 8,
    "ekonomi": "Baik"
  },
  "university": "Universitas Indonesia",
  "major": "Teknik Informatika"
}
```

**Response (201 CREATED):**
```json
{
  "id": 1,
  "student": "Ahmad Rizki",
  "probability": 87.5,
  "university": "Universitas Indonesia",
  "major": "Teknik Informatika",
  "model_version": "v1.0",
  "created_at": "2024-01-14T10:30:00Z",
  "recommendation": "Peluang tinggi. Pertahankan prestasi dan aktif di ekstrakurikuler."
}
```

### 7.2 Get Student Predictions

**Endpoint:** `GET /api/predictions/?student_id={student_id}`

**Response (200 OK):**
```json
{
  "results": [
    {
      "id": 1,
      "probability": 87.5,
      "university": "Universitas Indonesia",
      "major": "Teknik Informatika",
      "created_at": "2024-01-14T10:30:00Z"
    }
  ]
}
```

---

## Error Responses

### 400 Bad Request
```json
{
  "field_name": ["Error message here"]
}
```

### 401 Unauthorized
```json
{
  "detail": "Authentication credentials were not provided."
}
```

### 403 Forbidden
```json
{
  "detail": "You do not have permission to perform this action."
}
```

### 404 Not Found
```json
{
  "detail": "Not found."
}
```

### 500 Internal Server Error
```json
{
  "error": "Internal server error"
}
```

---

**Document Version**: 1.0
**Last Updated**: 2024-01-14

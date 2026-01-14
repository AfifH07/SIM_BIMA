# System Architecture - SIM SMA BIMA

## 1. Overview

SIM SMA BIMA adalah sistem informasi manajemen sekolah berbasis web yang menggunakan arsitektur 3-tier dengan komponen Machine Learning terintegrasi.

## 2. Architecture Pattern: 3-Tier Architecture

### 2.1 Presentation Layer (Frontend)
- **Technology**: Streamlit
- **Port**: 8501
- **Responsibility**:
  - User interface dan interaksi
  - Data visualization (charts, graphs)
  - Form input dan validasi client-side
  - Session management

### 2.2 Application Layer (Backend)
- **Technology**: Django REST Framework
- **Port**: 8000
- **Responsibility**:
  - Business logic processing
  - API endpoints (RESTful)
  - Authentication & Authorization
  - Data validation
  - Integration dengan ML model

### 2.3 Data Layer (Database)
- **Technology**: PostgreSQL
- **Port**: 5432
- **Responsibility**:
  - Data persistence
  - Data integrity
  - Transaction management
  - Query optimization

### 2.4 Machine Learning Layer
- **Technology**: scikit-learn, XGBoost
- **Responsibility**:
  - Model training
  - Prediction service
  - Feature engineering
  - Model evaluation

## 3. System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLIENT LAYER                             │
│                                                                  │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐       │
│  │  Admin   │  │   Guru   │  │  Siswa   │  │  Parent  │       │
│  │ Browser  │  │ Browser  │  │ Browser  │  │ Browser  │       │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘       │
│       │             │              │             │              │
└───────┼─────────────┼──────────────┼─────────────┼──────────────┘
        │             │              │             │
        └─────────────┴──────────────┴─────────────┘
                      │
                 HTTPS/HTTP
                      │
        ┌─────────────▼──────────────┐
        │   PRESENTATION LAYER       │
        │                            │
        │   ┌─────────────────┐     │
        │   │   Streamlit     │     │
        │   │   Frontend      │     │
        │   │   (Port 8501)   │     │
        │   └────────┬────────┘     │
        │            │               │
        └────────────┼───────────────┘
                     │
                REST API
                     │
        ┌────────────▼───────────────┐
        │   APPLICATION LAYER        │
        │                            │
        │  ┌──────────────────────┐ │
        │  │   Django Backend     │ │
        │  │   REST Framework     │ │
        │  │   (Port 8000)        │ │
        │  │                      │ │
        │  │  ┌───────────────┐  │ │
        │  │  │   API Layer   │  │ │
        │  │  └───────────────┘  │ │
        │  │  ┌───────────────┐  │ │
        │  │  │ Business Logic│  │ │
        │  │  └───────────────┘  │ │
        │  │  ┌───────────────┐  │ │
        │  │  │ Middleware    │  │ │
        │  │  │ - Auth        │  │ │
        │  │  │ - CORS        │  │ │
        │  │  │ - Logging     │  │ │
        │  │  └───────────────┘  │ │
        │  └──────────┬───────────┘ │
        │             │              │
        └─────────────┼──────────────┘
                      │
            ┌─────────┴─────────┐
            │                   │
    ORM (SQLAlchemy)      ML Inference
            │                   │
            │         ┌─────────▼─────────┐
            │         │  ML LAYER         │
            │         │                   │
            │         │ ┌──────────────┐ │
            │         │ │ Prediction   │ │
            │         │ │ Service      │ │
            │         │ └──────────────┘ │
            │         │ ┌──────────────┐ │
            │         │ │ Trained      │ │
            │         │ │ Models       │ │
            │         │ │ (.pkl/.joblib)│ │
            │         │ └──────────────┘ │
            │         └───────────────────┘
            │
    ┌───────▼────────────────────┐
    │     DATA LAYER             │
    │                            │
    │  ┌──────────────────────┐ │
    │  │   PostgreSQL DB      │ │
    │  │   (Port 5432)        │ │
    │  │                      │ │
    │  │  ┌────────────────┐ │ │
    │  │  │ Users          │ │ │
    │  │  │ Students       │ │ │
    │  │  │ Teachers       │ │ │
    │  │  │ Classes        │ │ │
    │  │  │ Grades         │ │ │
    │  │  │ Finance        │ │ │
    │  │  │ Extracurricular│ │ │
    │  │  │ Predictions    │ │ │
    │  │  └────────────────┘ │ │
    │  └──────────────────────┘ │
    └────────────────────────────┘
```

## 4. Technology Stack Summary

| Layer        | Technology           | Version  | Purpose                    |
|--------------|---------------------|----------|----------------------------|
| Frontend     | Streamlit           | 1.29+    | Web UI                     |
| Backend      | Django              | 4.2+     | REST API                   |
| Backend      | DRF                 | 3.14+    | API Framework              |
| Database     | PostgreSQL          | 14+      | Data Storage               |
| ML           | scikit-learn        | 1.3+     | ML Models                  |
| ML           | XGBoost             | 2.0+     | Advanced ML                |
| Visualization| Plotly              | 5.18+    | Charts                     |
| Testing      | pytest              | 7.4+     | Unit Testing               |

---

**Document Version**: 1.0
**Last Updated**: 2024-01-14

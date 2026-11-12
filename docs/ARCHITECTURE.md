# IntelliICU — Enterprise System Architecture Specification

## 1. System Overview

IntelliICU is an Enterprise AI Clinical Decision Support System (CDSS) engineered for Intensive Care Units (ICUs). The platform combines real-time physiological telemetry, predictive risk modeling, grounded Retrieval-Augmented Generation (RAG), and multi-provider Large Language Model reasoning.

```
+-------------------------------------------------------------------------+
|                              REACT FRONTEND                             |
|  - Vite, Tailwind CSS, Lucide, Recharts                                 |
|  - Live ICU Dashboard, Patient Profile, Telemetry, Hospital Assistant   |
|  - Real-time WebSocket Client & Server-Sent Events (SSE) Stream Reader  |
+--------------------+--------------------------------+--------------------+
                     | HTTP / REST                    | WebSockets / SSE
                     v                                v
+-------------------------------------------------------------------------+
|                           FASTAPI APPLICATION                           |
|  - Security & RBAC: JWT Bearer Tokens, Role-based Route Protection      |
|  - REST Endpoints: /api/v1/patients, /api/clinical-copilot, etc.        |
|  - Real-Time Hub: /ws/dashboard, /ws/patient/{id}                       |
+--------+-------------------+-------------------+-------------------+----+
         |                   |                   |                   |
         v                   v                   v                   v
+-----------------+ +-----------------+ +-----------------+ +-------------+
| POSTGRESQL 15   | | ML PREDICTOR    | | CHROMA VECTOR   | | MULTI-LLM   |
| SQLAlchemy 2.0  | | Scikit-Learn RF | | ChromaDB 0.4.x  | | ORCHESTRATOR|
| Longitudinal    | | 15 physiological| | 1,608 guideline | | Groq 120B   |
| vitals, alerts, | | indicators      | | chunks (SSC,    | | Gemini      |
| admissions, RBAC| | Risk Scoring    | | KDIGO, NICE)    | | (Zero Mock) |
+-----------------+ +-----------------+ +-----------------+ +-------------+
```

---

## 2. Architectural Tiers

### 2.1 Frontend Tier (`frontend/`)
- **Technology Stack:** React 19, Vite, Tailwind CSS, Axios, Lucide React, Recharts.
- **Routing & Guards:** React Router v7 with `AuthGuard` (JWT presence and expiration) and `PermissionGuard` (granular permission checks: `Dashboard`, `Patients`, `ClinicalAI`, `Alerts`, `Reports`, `Analytics`, `UserManagement`, `Settings`).
- **Telemetry Consumption:** `useWebSocket.js` connects with automatic reconnect and heartbeat to `/ws/dashboard?token=...`, streaming live vital drifts and alert changes.
- **AI Streaming:** `StreamingMarkdown.jsx` parses SSE chunks with CRLF/LF line normalization and guaranteed `finally` state cleanup.

### 2.2 Backend API Tier (`backend/app/`)
- **Framework:** FastAPI on Python 3.12 with Pydantic v2 schemas.
- **Dependency Injection:** Database sessions via `get_db()`, user identity via `get_current_user()`, and RBAC permission enforcement via `require_permission(perm)`.
- **Clinical Report Engine:** ReportLab generator producing downloadable PDF notes with temporal reconciliation of instantaneous vitals vs historical unresolved alarms.

### 2.3 Machine Learning & Explainability Tier (`backend/app/ai/`)
- **Model Artifact:** `backend/ml_models/intelliicu_final_model.pkl` (`RandomForestClassifier`, 809 MB).
- **Features (15 physiological metrics):** Heart rate, systolic BP, diastolic BP, respiratory rate, SpO2, temperature, WBC, lactate, platelets, creatinine, BUN, pH, PaO2, PaCO2, age.
- **Clinical Explainability:** Rule-based Physiological Rules Engine (`ExplainabilityEngine`) evaluating biomarker deviations (SIRS, SOFA, KDIGO criteria) with transparent `CLINICAL_RULES_ENGINE` labeling.

### 2.4 RAG & Vector Knowledge Tier (`backend/app/rag/`)
- **Vector Database:** ChromaDB 0.4.x (`backend/vector_db/chroma.sqlite3`).
- **Collection:** `intelliicu_knowledge_base` holding **1,608 clinical chunks**.
- **Embeddings:** `BAAI/bge-small-en-v1.5` running locally with `local_files_only=True` and `HF_HUB_OFFLINE=1`.
- **Knowledge Base Source Documents:**
  - Surviving Sepsis Campaign 2021 International Guidelines
  - KDIGO Clinical Practice Guideline for Acute Kidney Injury
  - NICE Guideline NG51 (Sepsis Recognition & Management)
  - AHA/ACC Guideline for Heart Failure Management
  - AACN Core Curriculum for High Acuity & Critical Care Nursing

### 2.5 Multi-Provider LLM Orchestrator (`backend/app/ai/orchestrator.py`)
- **Provider Chain:** Primary: Groq (`openai/gpt-oss-120b`) → Fallback: Google Gemini (`gemini-3.8-flash` / `gemini-2.5-flash`) → Controlled HTTP 503 (`LLMUnavailableError`).
- **Mock Safety:** `AI_ENABLE_MOCK_FALLBACK=false` strictly enforced in production.
- **Reasoning Budget:** Enforced `max_tokens >= 2048` to accommodate thinking tokens without truncating clinical JSON payloads.

---

## 3. Data Flow & Security Model

```
Clinician Request
       |
       v
+------------------+     JWT Validation & RBAC
| FastAPI Endpoint | ----------------------------> Reject 401 / 403
+--------+---------+
         |
         v
+-----------------------------------+
| PatientContextBuilder             | <---> PostgreSQL (Demographics, Telemetry, Labs)
+--------+--------------------------+
         |
         v
+-----------------------------------+
| Semantic Evidence Search          | <---> ChromaDB (Top-3 Guideline Chunks)
+--------+--------------------------+
         |
         v
+-----------------------------------+
| Multi-Provider Orchestrator       |
| 1. Try Groq (120B reasoning)     | ----> Success: JSON / SSE stream
| 2. On 429/500/timeout -> Gemini   | ----> Fallback Success: Normalized payload
| 3. On dual failure -> HTTP 503    | ----> Controlled Error (Zero Mock)
+-----------------------------------+
```

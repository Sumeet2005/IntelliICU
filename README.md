# IntelliICU — Enterprise AI Clinical Decision Support Platform (CDSS)

<p align="center">
  <strong>Intelligent Intensive Care Unit Telemetry, Real-Time Clinical Risk Scoring, Retrieval-Augmented Generation (RAG), and Resilient Multi-Provider LLM Orchestration</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12%20%7C%203.13-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/FastAPI-0.115+-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI" />
  <img src="https://img.shields.io/badge/React-18.3-61DAFB?style=for-the-badge&logo=react&logoColor=black" alt="React" />
  <img src="https://img.shields.io/badge/Vite-8.1-646CFF?style=for-the-badge&logo=vite&logoColor=white" alt="Vite" />
  <img src="https://img.shields.io/badge/PostgreSQL-16-4169E1?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL" />
  <img src="https://img.shields.io/badge/Scikit--Learn-Random%20Forest%20(200%20Trees)-F7931E?style=for-the-badge&logo=scikitlearn&logoColor=white" alt="Scikit-Learn" />
  <img src="https://img.shields.io/badge/ChromaDB-1%2C608%20Guideline%20Chunks-FF6F00?style=for-the-badge" alt="ChromaDB" />
  <img src="https://img.shields.io/badge/Groq%20%7C%20Gemini-Multi--Provider%20Failover-black?style=for-the-badge" alt="AI Orchestrator" />
  <img src="https://img.shields.io/badge/Docker-Production%20Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker" />
  <img src="https://img.shields.io/badge/Tests-30%2F30%20Passing-success?style=for-the-badge" alt="Tests" />
</p>

---

## Live Deployment & Quick Links

- **Live Application:** [https://intelliicu-frontend-production.up.railway.app](https://intelliicu-frontend-production.up.railway.app)
- **Repository:** [https://github.com/Sumeet2005/IntelliICU.git](https://github.com/Sumeet2005/IntelliICU.git)
- **Canonical Architecture Guide:** [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
- **Provider Configuration Guide:** [docs/PROVIDER_CONFIGURATION.md](docs/PROVIDER_CONFIGURATION.md)
- **Master Quality Gate & Acceptance Audit:** [docs/FINAL_QUALITY_GATE_AUDIT.md](docs/FINAL_QUALITY_GATE_AUDIT.md)

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Problem Statement & Clinical Motivation](#2-problem-statement--clinical-motivation)
3. [Project Objectives](#3-project-objectives)
4. [Key Features](#4-key-features)
5. [End-to-End System Architecture](#5-end-to-end-system-architecture)
6. [Complete Clinician Workflow](#6-complete-clinician-workflow)
7. [Machine Learning Prediction Pipeline](#7-machine-learning-prediction-pipeline)
8. [Retrieval-Augmented Generation (RAG) Architecture](#8-retrieval-augmented-generation-rag-architecture)
9. [Multi-Provider LLM Orchestration & Failover](#9-multi-provider-llm-orchestration--failover)
10. [LangChain Integration Architecture](#10-langchain-integration-architecture)
11. [Backend Architecture & API Design](#11-backend-architecture--api-design)
12. [Frontend Architecture & Clinical Dashboards](#12-frontend-architecture--clinical-dashboards)
13. [Database Architecture & Migrations](#13-database-architecture--migrations)
14. [Authentication & Role-Based Access Control (RBAC)](#14-authentication--role-based-access-control-rbac)
15. [Real-Time Telemetry & WebSockets](#15-real-time-telemetry--websockets)
16. [Server-Sent Events (SSE) Streaming Engine](#16-server-sent-events-sse-streaming-engine)
17. [Technology Stack Rationale](#17-technology-stack-rationale)
18. [Repository Directory Structure](#18-repository-directory-structure)
19. [REST API Specification](#19-rest-api-specification)
20. [Environment Configuration](#20-environment-configuration)
21. [Local Development & Installation](#21-local-development--installation)
22. [Docker Compose Deployment](#22-docker-compose-deployment)
23. [Automated Verification & Test Results](#23-automated-verification--test-results)
24. [How to Explain IntelliICU in a Technical Interview](#24-how-to-explain-intelliicu-in-a-technical-interview)
25. [Known Limitations](#25-known-limitations)
26. [Clinical Safety & Compliance Disclaimer](#26-clinical-safety--compliance-disclaimer)
27. [Future Roadmap](#27-future-roadmap)
28. [Author & Contact](#28-author--contact)

---

## 1. Project Overview

**IntelliICU** is an enterprise-grade AI Clinical Decision Support System (CDSS) built to demonstrate how machine learning, semantic retrieval-augmented generation (RAG), resilient LLM orchestration, and high-frequency real-time telemetry converge into a unified, reliable healthcare platform.

Operating in intensive care units requires clinicians to synthesize hundreds of continuous telemetry readings, sporadic lab panels, historical diagnoses, and institutional clinical protocols under severe cognitive load and strict time constraints. IntelliICU acts as an ambient clinical copilot: it continuously monitors physiological parameters, evaluates sepsis risk using an ensemble machine learning model, retrieves peer-reviewed guidelines using semantic vector search, and delivers structured, auditable clinical reasoning through resilient LLMs.

---

## 2. Problem Statement & Clinical Motivation

Intensive Care Units face several critical operational and diagnostic bottlenecks:

1. **Alarm Fatigue & Telemetry Overload:** Bedside monitors emit thousands of threshold-based audio alerts every 24 hours, over 85% of which are non-actionable, leading to desensitization and missed clinical deteriorations.
2. **Delayed Sepsis Recognition:** Sepsis mortality increases by approximately 7.6% for every hour antibiotics are delayed following the onset of septic hypotension. Early multivariate detection across subtle trends (e.g., slight tachycardia coupled with rising lactate and declining platelets) is vital.
3. **Clinical Guideline Disconnect:** Authoritative protocols (Surviving Sepsis Campaign, NICE guidelines, Brain Trauma Foundation) are extensive PDF documents that clinicians cannot readily consult during emergent resuscitations.
4. **AI Hallucination & Fragility:** General-purpose LLMs hallucinate medical dosages, lack access to real-time patient vitals, and fail catastrophically when an API provider experiences rate limits or downtime.

---

## 3. Project Objectives

- **Sub-Second Real-Time Telemetry:** Stream simulated bedside vitals (HR, SpO2, SBP, DBP, RR, Temp, GCS) via WebSockets to interactive dashboards without UI re-renders.
- **Explainable Clinical ML Risk Scoring:** Execute an ensemble Random Forest model across 13 canonical features with feature-level validation, lazy memory-mapped loading, and calibrated risk levels.
- **Grounded Semantic RAG:** Index authoritative clinical protocols into a persistent ChromaDB vector store (1,608 verified chunks) using `BAAI/bge-small-en-v1.5` embeddings, enforcing evidence-grounded AI recommendations with exact source citations.
- **Enterprise Multi-Provider LLM Resiliency:** Build a production `ProviderOrchestrator` featuring automated failover (Groq primary with `openai/gpt-oss-120b` → Google Gemini secondary with `gemini-3.8-flash`), token streaming via Server-Sent Events (SSE), and schema-enforced structured outputs.
- **Zero-Trust Security & RBAC:** Enforce cryptographically verified JWT tokens, bcrypt credential hashing, and role-based route guards across four distinct healthcare personas (Doctor, Nurse, Admin, Viewer).

---

## 4. Key Features

- **Interactive ICU Bedside Overview:** Real-time patient dashboard highlighting risk categories, active alerts, abnormal lab badges, and live telemetry trends.
- **Clinical Copilot:** Context-aware, guideline-grounded AI assistant capable of structured multi-turn clinical dialogue, differential diagnoses, and antibiotic management suggestions.
- **Hospital Assistant:** Institutional knowledge agent capable of answering protocol, triage, and operational queries using RAG.
- **Automated Clinical Progress & Discharge Notes:** Generates structured ICU clinical notes and exports downloadable, formatted PDF reports via ReportLab.
- **Telemetry Simulator:** Native background simulator emitting randomized, physiologically consistent ICU telemetry drifts to exercise real-time WebSocket feeds.
- **Diagnostic Studio & Model Evaluation:** Standalone reproducible evaluation suite assessing model performance on clinical tabular test sets without metric fabrication.

---

## 5. End-to-End System Architecture

IntelliICU adopts a decoupled, modern multi-tier micro-architecture:

```mermaid
flowchart TD
    subgraph ClientTier["Client Tier (Frontend - React 18 + Vite)"]
        UI["Clinician SPA (Tailwind CSS)"]
        WSClient["WebSocket Client (useWebSocket)"]
        SSEClient["SSE Stream Consumer (Fetch API)"]
        State["Auth & Clinical Context"]
    end

    subgraph GatewayTier["Gateway & Web Tier"]
        Nginx["Nginx Reverse Proxy (:80)"]
    end

    subgraph ServiceTier["Application Service Tier (FastAPI Backend)"]
        FastAPI["FastAPI REST / WS Engine (:8000)"]
        AuthModule["JWT & RBAC Security Engine"]
        SimModule["Telemetry Engine & Simulator"]
        Predictor["ML Predictor (LazyModelProxy)"]
        CopilotService["Clinical Copilot Service"]
        RAGService["KnowledgeService & Vector Engine"]
        Orchestrator["ProviderOrchestrator"]
    end

    subgraph ModelTier["AI & Machine Learning Assets"]
        RFModel["Random Forest Model (809 MB Memmap)"]
        ChromaStore["ChromaDB Vector Store (1,608 Chunks)"]
        PDFs["Clinical Guidelines (10 PDFs)"]
    end

    subgraph ExternalAITier["External LLM Providers"]
        Groq["Groq API (openai/gpt-oss-120b)"]
        Gemini["Google Gemini API (gemini-3.8-flash)"]
    end

    subgraph PersistenceTier["Data Tier"]
        Postgres[("PostgreSQL 16 Database")]
        Alembic["Alembic Migrations (c2d3e4f5a6b7)"]
    end

    UI --> Nginx
    Nginx --> FastAPI
    WSClient <-->|ws://.../ws/dashboard<br/>ws://.../ws/patient/:id| SimModule
    SSEClient <-->|text/event-stream| FastAPI

    FastAPI --> AuthModule
    FastAPI --> Predictor
    FastAPI --> CopilotService
    FastAPI --> Postgres

    Predictor --> RFModel
    CopilotService --> RAGService
    CopilotService --> Orchestrator
    RAGService --> ChromaStore
    RAGService -.-> PDFs

    Orchestrator -->|Primary| Groq
    Orchestrator -.->|Fallback on Fail| Gemini

    Postgres --- Alembic
```

---

## 6. Complete Clinician Workflow

```mermaid
sequenceDiagram
    autonumber
    actor Clinician as ICU Physician
    participant Web as React Web SPA
    participant API as FastAPI Backend
    participant Sim as Telemetry Simulator
    participant ML as Random Forest ML Engine
    participant RAG as KnowledgeService (ChromaDB)
    participant LLM as ProviderOrchestrator (Groq / Gemini)
    participant DB as PostgreSQL 16

    Clinician->>Web: Login with Credentials
    Web->>API: POST /api/auth/login
    API->>DB: Verify bcrypt password hash
    DB-->>API: User record (Role: Doctor)
    API-->>Web: JWT Bearer Token

    Web->>API: Establish WebSocket Connection (/ws/dashboard or /ws/patient/{id})
    loop Telemetry Drift Loop (Default 2.0s, Configurable)
        Sim->>API: Generate vital sign drift (HR, BP, SpO2)
        API->>DB: Persist vital sign reading
        API-->>Web: Broadcast vital tick via WebSocket
        Web->>Web: Update Recharts telemetry trends in real time
    end

    Clinician->>Web: Request Sepsis Risk Evaluation (Bed MICU-04)
    Web->>API: POST /api/v1/predictions/generate/{admission_id}
    API->>DB: Fetch latest vital signs & lab results
    API->>ML: Predictor.predict(vitals, labs)
    ML->>ML: Validate 13 features & run predict_proba
    ML-->>API: Risk: 86.4%, Level: HIGH, Model: v2.0-rf
    API->>DB: Save prediction record
    API-->>Web: Return risk score & clinical recommendation

    Clinician->>Web: Ask Copilot: "Recommend sepsis protocol and antibiotic dosing"
    Web->>API: POST /api/clinical-copilot/chat (stream=true)
    API->>DB: Build rich PatientContext (demographics, vitals, labs, alerts)
    API->>RAG: Semantic search top-3 guideline chunks (Surviving Sepsis)
    RAG-->>API: 3 verified clinical excerpts with citations
    API->>LLM: Stream prompt (Patient Context + Guidelines + Question)
    LLM-->>API: SSE tokens streamed in real time
    API-->>Web: text/event-stream chunks
    Web-->>Clinician: Render Markdown with live typing effect & exact citations
```

---

## 7. Machine Learning Prediction Pipeline

IntelliICU's risk scoring is powered by an ensemble machine learning model trained to identify sepsis and hemodynamic instability prior to clinical decompensation.

### Actual Model Architecture & Verification:
- **Algorithm:** `sklearn.ensemble._forest.RandomForestClassifier`
- **Ensemble Size:** 200 Decision Tree estimators
- **Input Dimensions:** Exactly 13 clinical numerical features
- **Serialization Format:** Joblib Memory-Mapped Array (`intelliicu_final_model.pkl`, 809.73 MB | SHA-256: `541ff082e7274cc1...`)
- **Model Loading:** Implemented using `LazyModelProxy` (`backend/app/ai/model_loader.py`). The 809MB weights are not deserialized during Uvicorn startup (allowing container launch in < 1 second); instead, the proxy lazily binds using `joblib.load(..., mmap_mode="r")` with thread locking upon the first inference call.
- **Classification Threshold:** Calibrated decision boundary at $0.20$ probability ($P \ge 0.20 \rightarrow \text{HIGH RISK}$).
- **Version Tag:** Tagged in prediction outputs and database records as `v2.0-rf`.

### 13 Canonical Clinical Features (Strict Ordering):
1. `heart_rate` (bpm)
2. `systolic_bp` (mmHg)
3. `diastolic_bp` (mmHg)
4. `respiratory_rate` (breaths/min)
5. `spo2` (%)
6. `temperature` (°C)
7. `wbc` ($10^9$/L)
8. `platelets` ($10^9$/L)
9. `creatinine` (mg/dL)
10. `bun` (Blood Urea Nitrogen, mg/dL)
11. `potassium` (mEq/L)
12. `chloride` (mEq/L)
13. `lactate` (mmol/L)

```mermaid
flowchart TD
    Vitals["Bedside Vital Signs (HR, BP, SpO2, RR, Temp)"]
    Labs["Laboratory Results (WBC, Plt, Cr, BUN, K, Cl, Lactate)"]
    
    Vitals --> FB["FeatureBuilder (backend/app/ai/feature_builder.py)"]
    Labs --> FB
    
    FB --> Val{"Validation Check:<br/>All 13 features present?<br/>Finite float check?<br/>No NaN / Inf?"}
    Val -- "Fail" --> Err["Raise ValueError (Missing / Non-finite)"]
    Val -- "Pass" --> Vector["Ordered Feature Vector (1x13 DataFrame)"]
    
    Vector --> Loader["LazyModelProxy (backend/app/ai/model_loader.py)"]
    Loader --> Mmap["Joblib mmap_mode='r'<br/>RandomForestClassifier (200 Trees)"]
    
    Mmap --> Prob["predict_proba() -> Class 1 Sepsis Probability"]
    
    Prob --> Thresh{"Probability >= 0.20?"}
    Thresh -- "Yes" --> High["Risk: HIGH<br/>Score: P * 100<br/>Action: Immediate ICU physician review.<br/>Consider sepsis protocol."]
    Thresh -- "No" --> Low["Risk: LOW<br/>Score: P * 100<br/>Action: Continue routine ICU monitoring."]
    
    High --> Out["Structured Prediction Response<br/>(Tagged model_version: v2.0-rf)"]
    Low --> Out
```

---

## 8. Retrieval-Augmented Generation (RAG) Architecture

IntelliICU implements a grounded clinical RAG system designed to prevent LLM hallucinations by conditioning generation strictly on peer-reviewed clinical guidelines.

### Vector Store & Knowledge Corpus:
- **Vector Database:** Persistent ChromaDB instance stored at `backend/vector_db/chroma.sqlite3` (20.7 MB).
- **Verified Corpus Chunks:** **1,608 verified guideline chunks** in collection `intelliicu_knowledge_base`.
- **Embedding Model:** `BAAI/bge-small-en-v1.5` (384-dimensional dense vectors) configured with `local_files_only=True` and `HF_HUB_OFFLINE=1` for guaranteed offline operation.
- **Authoritative Guidelines (10 PDFs in `backend/app/rag/knowledge_base/`):**
  1. *Surviving Sepsis Campaign International Guidelines* (Adult sepsis & septic shock)
  2. *NICE Sepsis Recognition, Diagnosis and Early Management*
  3. *Brain Trauma Foundation Guidelines* (Management of severe traumatic brain injury)
  4. *Post Cardiac Arrest Management Guidelines*
  5. *Pediatric Anaphylactic Shock Resuscitation Protocols*
  6. Plus 5 specialist critical care protocols covering acute kidney injury, ventilation strategies, and vasopressor titration.

### Document Ingestion Flowchart:

```mermaid
flowchart LR
    PDFs["Clinical Guideline PDFs (10 Documents)"] --> Loader["LangChain PyPDFLoader (loaders/pdf_loader.py)"]
    Loader --> Splitter["LangChain RecursiveCharacterTextSplitter (chunking/text_chunker.py)"]
    Splitter --> Chunks["Standardized Text Chunks (chunk_size=1000, overlap=150)"]
    Chunks --> Embedder["BAAI/bge-small-en-v1.5 Embedder (embedding_service.py)"]
    Embedder --> Vectors["384-Dimensional Dense Vectors + Metadata"]
    Vectors --> Chroma["ChromaDB Persistent Store (1,608 Chunks)"]
```

### RAG Retrieval & Clinical Grounding Flowchart:

```mermaid
flowchart TD
    UserQuery["Clinician Query: 'What is the recommended norepinephrine dosing?'"]
    UserQuery --> KS["KnowledgeService (backend/app/rag/knowledge_service.py)"]
    
    subgraph SearchStrategy["Hybrid Retrieval Engine"]
        KS --> Mode{"Semantic Embeddings Enabled?<br/>(ENABLE_SEMANTIC_EMBEDDINGS=true)"}
        Mode -- "True" --> Cosine["Encode Query via BGE-Small<br/>Execute ChromaDB Cosine Similarity Query"]
        Mode -- "False / Unavailable" --> Keyword["Keyword & TF Scoring Fallback"]
    end
    
    Cosine --> TopK["Filter Top-3 Evidence Chunks (Score >= 0.70)"]
    Keyword --> TopK
    
    TopK --> Formatter["Format Clinical Evidence Block:<br/>- Guideline Title<br/>- Source Organization<br/>- Protocol Section<br/>- Verbatim Excerpt"]
    
    Formatter --> Context["Combine with Live PatientContext:<br/>- Current Vitals & Laboratory Panels<br/>- Active Physician Alerts<br/>- Timeline Event History"]
    
    Context --> Prompt["Construct Strict Negative-Constraint Prompt:<br/>'Answer ONLY using supplied clinical context.<br/>If evidence is insufficient, state so explicitly.'"]
    
    Prompt --> LLM["ProviderOrchestrator"]
    LLM --> Answer["Grounded Answer + Exact Source Citations"]
```

---

## 9. Multi-Provider LLM Orchestration & Failover

To guarantee 99.99% availability during critical care inquiries, IntelliICU avoids single-provider dependencies through a dynamic `ProviderOrchestrator` (`backend/app/ai/orchestrator.py`).

### Active Provider Configuration:
- **Primary Provider:** **Groq API** running `openai/gpt-oss-120b` (Ultra-low latency inference, structured JSON output).
- **Secondary Fallback Provider:** **Google Gemini API** running `gemini-3.8-flash` (High-context medical reasoning, automatic failover).
- **Mock Fallback:** Configured via `AI_ENABLE_MOCK_FALLBACK=false` (Production mode rejects ungrounded mock responses, raising a controlled HTTP 503 if all upstream providers are unreachable).

```mermaid
flowchart TD
    Req["Clinical Copilot Request"] --> Orch["ProviderOrchestrator (backend/app/ai/orchestrator.py)"]
    
    Orch --> Primary["Execute Primary Provider: Groq (openai/gpt-oss-120b)"]
    
    Primary --> CheckPrimary{"Success within Timeout (30s)?"}
    CheckPrimary -- "HTTP 200 OK" --> OutPrimary["Stream / Return Structured JSON<br/>(provider: 'groq', fallback_used: false)"]
    
    CheckPrimary -- "RateLimit (429) / Timeout / 5xx" --> LogFail["Log Warning & Trigger Instant Failover"]
    
    LogFail --> Fallback["Execute Fallback Provider: Google Gemini (gemini-3.8-flash)"]
    
    Fallback --> CheckFallback{"Gemini Success within 30s?"}
    CheckFallback -- "HTTP 200 OK" --> OutFallback["Stream / Return Structured JSON<br/>(provider: 'gemini', fallback_used: true)"]
    
    CheckFallback -- "RateLimit / Network Error" --> CheckMock{"AI_ENABLE_MOCK_FALLBACK=true?"}
    CheckMock -- "True (Dev Mode)" --> OutMock["Return Deterministic Local Mock"]
    CheckMock -- "False (Production)" --> Err["Raise LLMUnavailableError<br/>Return HTTP 503: Clinical AI services unavailable."]
```

---

## 10. LangChain Integration Architecture

IntelliICU uses LangChain in a targeted, architectural manner:

### How LangChain is Used:
1. **Document Loading (`backend/app/rag/loaders/pdf_loader.py`):**
   - Utilizes `langchain_community.document_loaders.PyPDFLoader` to parse multi-page, complex layout clinical guideline PDFs into structured page streams.
2. **Text Chunking (`backend/app/rag/chunking/text_chunker.py`):**
   - Utilizes `langchain_text_splitters.RecursiveCharacterTextSplitter` configured with chunk boundaries (`\n\n`, `\n`, ` `, `""`), chunk size 1,000 characters, and overlap 150 characters to preserve medical protocol paragraph semantics.

### How LangChain is NOT Used:
- **No LangChain Agents or Chains:** LLM prompting, conversation memory, provider failover, and streaming are **not** managed through black-box LangChain chains or agent executors. These are handled natively by `ProviderOrchestrator` and `ClinicalCopilotService` to maintain deterministic latency, explicit error handling, and direct SSE streaming control.

---

## 11. Backend Architecture & API Design

The backend is built with **Python 3.12 / 3.13** and **FastAPI**, following a modular Domain-Driven Design (DDD) layered architecture:

```
backend/app/
├── ai/              # ML model loading, feature engineering, and LLM provider factory
├── api/             # REST API routes and WebSocket controllers
│   ├── v1/endpoints # Versioned REST endpoints (admissions, vitals, labs, predictions)
├── core/            # Config, security, JWT authentication, and structured logging
├── database/        # SQLAlchemy engine, session management, and seed data
├── models/          # Declarative SQLAlchemy ORM entities
├── rag/             # ChromaDB vector store, BGE embeddings, and guideline corpus
├── repositories/    # Encapsulated data-access layers
├── schemas/         # Pydantic v2 validation and response serialization models
├── services/        # Business logic (Clinical Copilot, Context Builder, Report Gen)
├── telemetry/       # Telemetry simulator and drift generator
└── websocket/       # Real-time WebSocket connection managers
```

### Layer Responsibilities:
- **Controller Layer (`app/api`):** Parses HTTP requests, validates JWT authorization tokens, and serializes Pydantic v2 schemas.
- **Service Layer (`app/services`):** Coordinates multi-step clinical workflows (e.g., patient context optimization, RAG retrieval, LLM prompt synthesis).
- **Data Access Layer (`app/repositories`):** Abstracts SQL operations using SQLAlchemy 2.0 query patterns, preventing leaky database abstractions.

---

## 12. Frontend Architecture & Clinical Dashboards

The frontend is a single-page application built with **React 18**, **Vite**, and **Tailwind CSS**, designed specifically for high-stress ICU environments:

- **State Management & Context:** Split across `AuthContext` (JWT session & user profile) and custom telemetry hooks.
- **Telemetry Streaming Hook (`useWebSocket`):** Maintains persistent WebSocket connections with automatic backoff reconnection, updating Recharts area charts without re-rendering the parent page.
- **Dynamic Code-Splitting:** All 12 pages are lazy-loaded via `React.lazy` and `Suspense`, achieving a clean initial bundle size and a **1.00s Vite production build**.
- **Clinical Copilot Panel:** Floating, collapsible chat drawer featuring live SSE streaming markdown formatting, copy-to-clipboard clinical notes, and expandable guideline citations.

---

## 13. Database Architecture & Migrations

IntelliICU utilizes **PostgreSQL 16** managed through **Alembic** migration tracking.

```mermaid
erDiagram
    USERS ||--o{ AUDIT_LOGS : performs
    PATIENTS ||--o{ ADMISSIONS : has
    PATIENTS ||--o{ ALERTS : triggers
    ADMISSIONS ||--o{ VITAL_SIGNS : records
    ADMISSIONS ||--o{ LAB_RESULTS : records
    ADMISSIONS ||--o{ PREDICTIONS : evaluates
    PATIENTS ||--o{ TIMELINE_EVENTS : logs

    PATIENTS {
        varchar id PK
        varchar hospital_patient_id UK
        varchar first_name
        varchar last_name
        date date_of_birth
        varchar gender
        varchar blood_group
        varchar status
    }

    ADMISSIONS {
        varchar id PK
        varchar patient_id FK
        varchar admission_number UK
        varchar diagnosis
        varchar doctor_name
        varchar ward
        varchar bed_number
        varchar status
    }

    VITAL_SIGNS {
        varchar id PK
        varchar admission_id FK
        float heart_rate
        float systolic_bp
        float diastolic_bp
        float respiratory_rate
        float spo2
        float temperature
        timestamp recorded_at
    }

    PREDICTIONS {
        varchar id PK
        varchar admission_id FK
        varchar prediction_type
        float risk_score
        varchar risk_level
        text recommendation
        varchar model_version
        timestamp created_at
    }
```

### Migration History:
- Managed under `backend/alembic/versions/` (11 versions).
- Current Schema State: **`c2d3e4f5a6b7 (head)`** (*add_missing_indexes_and_not_valid_fks*).
- Includes composite indexes on `(admission_id, recorded_at DESC)` and `(patient_id, created_at DESC)` to ensure sub-5ms lookup speeds during high-frequency telemetry simulation.

---

## 14. Authentication & Role-Based Access Control (RBAC)

Security in IntelliICU enforces defense-in-depth principles:

```mermaid
flowchart TD
    Client["Client HTTP / WS Request"] --> AuthGuard{"Valid JWT in 'Authorization: Bearer <token>'?"}
    
    AuthGuard -- "No / Expired" --> 401["Return HTTP 401 Unauthorized"]
    AuthGuard -- "Yes" --> Decode["Decode JWT Claims (username, role, exp)"]
    
    Decode --> CheckDB["UserRepository.get_by_username()"]
    CheckDB --> Active{"User exists & is_active=True?"}
    Active -- "No" --> 401
    Active -- "Yes" --> RBAC{"RBAC Check: User Role has Required Permission?"}
    
    subgraph Roles["Role Hierarchy"]
        Admin["Admin: Full Access (Users, Settings, ClinicalAI, Patients)"]
        Doctor["Doctor: Patients, Telemetry, ClinicalAI, Reports"]
        Nurse["Nurse: Patients, Telemetry, Alerts (No Settings)"]
        Viewer["Viewer: Read-Only Dashboard"]
    end
    
    RBAC -- "Permission Missing" --> 403["Return HTTP 403 Forbidden"]
    RBAC -- "Authorized" --> Exec["Execute Protected API Route / WS Stream"]
```

---

## 15. Real-Time Telemetry & WebSockets

To replicate an active ICU monitoring floor without requiring actual hospital monitors, IntelliICU includes a real-time WebSocket telemetry engine:

- **Broadcasting Endpoints:** `/ws/dashboard` (global ICU floor telemetry) and `/ws/patient/{patient_id}` (individual patient telemetry)
- **Simulation Engine (`backend/app/websocket/simulator.py`):** Runs an asynchronous background loop generating physiologically bounded vital sign drifts (e.g., respiratory rate drifts correlated with heart rate changes) every 2.0 seconds by default (configurable via `SIMULATOR_INTERVAL_SECONDS`).
- **Client Handling:** The frontend `useWebSocket` hook consumes incoming ticks and pushes them into circular ring buffers, rendering smooth real-time SVG waveform charts without frame stutter.

---

## 16. Server-Sent Events (SSE) Streaming Engine

For conversational interactions with Clinical Copilot, responses stream in real time using Server-Sent Events:

```mermaid
sequenceDiagram
    participant React as React Frontend (EventSource / Fetch)
    participant API as FastAPI (/api/clinical-copilot/chat)
    participant LLM as Groq / Gemini Streaming API

    React->>API: POST /api/clinical-copilot/chat?stream=true
    API->>API: Compile PatientContext & retrieve ChromaDB chunks
    API->>LLM: stream_chat(prompt)
    API-->>React: HTTP 200 OK (Content-Type: text/event-stream)
    
    loop Token Streaming
        LLM-->>API: Yield Token Chunk ("Patient ", "exhibits ", "hypotension")
        API-->>React: data: {"type": "token", "content": "Patient "}
        React->>React: Append to live Markdown display
    end

    API-->>React: data: {"type": "metadata", "retrieved_sources": [...]}
    API-->>React: data: [DONE]
```

---

## 17. Technology Stack Rationale

| Layer | Selected Technology | Why Chosen Over Alternatives |
| :--- | :--- | :--- |
| **Frontend** | React 18 + Vite | Sub-second HMR development, component modularity, clean virtual DOM diffing for high-frequency telemetry rendering over Angular/Vue. |
| **Styling** | Tailwind CSS v4 | Zero-runtime CSS utility classes, dark-mode ICU theme optimization, highly maintainable responsive layouts. |
| **Backend** | Python 3.12 + FastAPI | Native asynchronous event loop, automatic OpenAPI documentation, tight integration with scientific Python/ML libraries over Node.js/Go. |
| **Data Validation** | Pydantic v2 | C-based core serialization engine (`pydantic-core`) offering 5x faster request parsing than Pydantic v1. |
| **Database** | PostgreSQL 16 | ACID transactional integrity, relational consistency for multi-table clinical admissions, mature composite index performance over MongoDB. |
| **ORM & Migrations** | SQLAlchemy 2.0 + Alembic | Explicit SQL query generation, safe transactional schema migrations, strict type safety over raw database drivers. |
| **ML Engine** | Scikit-Learn Random Forest | Robust to non-linear interactions across physiological vitals, resistant to overfitting on clinical cohorts, native multi-tree voting over single decision trees. |
| **Vector Store** | ChromaDB (Persistent SQLite) | Embedded, zero-infrastructure vector database with metadata filtering and native cosine distance search over heavy external clusters. |
| **Embeddings** | BAAI/bge-small-en-v1.5 | State-of-the-art MTEB clinical retrieval performance in a compact 384-dimensional model capable of running completely offline. |
| **LLM Inference** | Groq (`gpt-oss-120b`) | Unrivaled LPU token generation speed (~300+ tokens/sec) providing instantaneous clinical answers over standard cloud inference APIs. |

---

## 18. Repository Directory Structure

```
D:\Projects\IntelliICU\
├── .github/workflows/ci.yml       # GitHub Actions CI workflow
├── .env.example                   # Master environment variable template
├── docker-compose.yml             # Multi-container production orchestration
├── pytest.ini                     # Pytest runner configuration
├── README.md                      # Primary project documentation
├── docs/                          # Canonical engineering documentation
│   ├── ARCHITECTURE.md            # Complete enterprise architecture blueprint
│   ├── CLEANUP_REPORT.md          # Consolidated audit and cleanup manifest
│   ├── FINAL_QUALITY_GATE_AUDIT.md# Final quality gate acceptance audit report
│   └── PROVIDER_CONFIGURATION.md  # Groq and Gemini configuration guide
├── backend/                       # FastAPI enterprise backend application
│   ├── alembic/                   # Database migration versions (11 scripts)
│   ├── app/
│   │   ├── ai/                    # ML model loader, feature builder, predictor, providers
│   │   │   ├── providers/         # Groq, Gemini, Ollama, and base provider classes
│   │   │   ├── evaluate_model.py  # Standalone ML evaluation script
│   │   │   ├── factory.py         # Provider factory resolving active LLM
│   │   │   ├── feature_builder.py # 13-feature canonical validator
│   │   │   ├── model_loader.py    # LazyModelProxy memory-mapping 809MB weights
│   │   │   ├── orchestrator.py    # Multi-provider failover and streaming orchestrator
│   │   │   └── predictor.py       # ML risk scoring and threshold engine
│   │   ├── api/                   # REST routers and WebSocket handlers
│   │   │   ├── v1/endpoints/      # Admissions, vitals, labs, predictions
│   │   │   ├── clinical_ai.py     # AI prediction and synthesis router
│   │   │   ├── clinical_copilot.py# Clinical Copilot chat, SSE streaming, and reports
│   │   │   └── hospital_assistant.py# Hospital Assistant RAG router
│   │   ├── core/                  # Config, logging, JWT authentication, RBAC dependencies
│   │   ├── database/              # SQLAlchemy engine, session factory, seed data
│   │   ├── models/                # SQLAlchemy ORM declarative models
│   │   ├── rag/                   # ChromaDB vector store, BGE embeddings, PDF loaders
│   │   │   ├── knowledge_base/    # 10 clinical guideline PDFs
│   │   │   ├── chunking/          # LangChain RecursiveCharacterTextSplitter wrapper
│   │   │   ├── loaders/           # LangChain PyPDFLoader wrapper
│   │   │   └── knowledge_service.py# In-memory and ChromaDB retrieval service
│   │   ├── repositories/          # Encapsulated data-access layers
│   │   ├── schemas/               # Pydantic v2 validation models
│   │   ├── services/              # Business logic (Copilot, Context Builder, Report Gen)
│   │   ├── telemetry/             # Real-time telemetry generator
│   │   └── websocket/             # WebSocket connection routes and simulator
│   ├── ml_models/
│   │   └── intelliicu_final_model.pkl # 809MB Random Forest model artifact (Joblib memmap)
│   ├── vector_db/
│   │   └── chroma.sqlite3         # ChromaDB persistent store (1,608 chunks)
│   ├── tests/                     # Automated test suites (30 passing tests)
│   ├── Dockerfile                 # Python 3.12 container specification
│   ├── requirements.txt           # Pinned backend dependencies
│   └── start.sh                   # Container entrypoint with auto-migrations
└── frontend/                      # React 18 + Vite + Tailwind CSS frontend
    ├── src/
    │   ├── assets/                # Backgrounds, styles, images
    │   ├── components/            # Modular UI widgets
    │   │   ├── clinicalCopilot/   # ChatBubble, ChatPanel
    │   │   ├── dashboardV2/       # KPISection, LiveAnalytics, PatientDrawer
    │   │   ├── hospitalAssistant/ # Hospital Assistant drawer
    │   │   └── telemetry/         # TrendChart, Waveform monitor
    │   ├── context/               # AuthContext and global state
    │   ├── hooks/                 # useWebSocket, useAuth
    │   ├── pages/                 # 12 clinical pages
    │   └── services/              # Axios API clients and WebSocket managers
    ├── Dockerfile                 # Multi-stage Node build + Nginx container
    ├── nginx.conf                 # Production SPA routing and proxy config
    ├── package.json               # Pinned frontend dependencies
    └── vite.config.js             # Vite bundler configuration
```

---

## 19. REST API Specification

| Method | Endpoint | Access Level | Description |
| :--- | :--- | :--- | :--- |
| `GET` | `/health` | Public | System health check (Database, AI Orchestrator, Telemetry). |
| `POST` | `/api/auth/login` | Public | Authenticates credentials, returning a signed JWT access token. |
| `GET` | `/api/v1/patients` | Doctor, Nurse, Admin | Fetches list of all active ICU patients with current bed numbers. |
| `GET` | `/api/v1/vital-signs/admission/{admission_id}` | Doctor, Nurse, Admin | Returns historical vital signs for a given admission. |
| `POST` | `/api/v1/predictions/generate/{admission_id}` | ClinicalAI Permission | Executes the Random Forest model across latest vitals and labs. |
| `POST` | `/api/clinical-copilot/chat` | ClinicalAI Permission | Clinical Copilot dialogue; supports `?stream=true` for SSE tokens. |
| `POST` | `/api/clinical-copilot/report` | Reports Permission | Generates structured ICU clinical notes (Progress, Discharge). |
| `GET` | `/api/clinical-copilot/report/{id}/pdf` | Reports Permission | Downloads generated clinical report as a formatted PDF. |
| `POST` | `/api/hospital-assistant/chat` | ClinicalAI Permission | Institutional RAG assistant for hospital protocols. |
| `GET` | `/api/ai/health?live=true` | Doctor, Admin | Validates live API connectivity with Groq and Gemini upstream APIs. |
| `WS` | `/ws/dashboard` | Authenticated | Live ICU dashboard telemetry updates across all beds. |
| `WS` | `/ws/patient/{patient_id}` | Authenticated | Live patient-specific vital signs stream (default 2.0s interval). |

---

## 20. Environment Configuration

Copy `.env.example` to create your local `.env`:

```bash
cp .env.example .env
```

### Essential Configuration Variables:
```env
# Application Environment
ENVIRONMENT=development
PORT=8000
SECRET_KEY=generate_a_secure_random_64_character_key_here
DEBUG=false

# Database Configuration (PostgreSQL)
DATABASE_URL=postgresql+psycopg://intelliicu:secure_password@localhost:5433/intelliicu_db

# Primary AI Provider (Groq)
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=openai/gpt-oss-120b
GROQ_TIMEOUT_SECONDS=30.0

# Secondary AI Provider (Google Gemini Fallback)
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-3.8-flash
GEMINI_TIMEOUT_SECONDS=30.0

# AI Configuration Flags
AI_PROVIDER=groq
AI_FALLBACK_PROVIDER=gemini
AI_ENABLE_MOCK_FALLBACK=false
CLINICAL_LLM_STREAMING=true

# RAG & Semantic Embeddings
ENABLE_SEMANTIC_EMBEDDINGS=true
HF_HUB_OFFLINE=1
```

*(Note: Never commit your actual `.env` file containing API keys to source control).*

---

## 21. Local Development & Installation

### Prerequisites:
- Python 3.12 or 3.13
- Node.js 20+ and npm
- PostgreSQL 16 (or run PostgreSQL via Docker)

### 1. Backend Setup:
```powershell
# Navigate to backend directory
cd backend

# Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate   # Windows
# source .venv/bin/activate # Linux / macOS

# Install pinned dependencies
pip install -r requirements.txt

# Run database migrations to head
alembic upgrade head

# Start FastAPI development server
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 2. Frontend Setup:
```powershell
# Navigate to frontend directory in a separate terminal
cd frontend

# Install pinned dependencies
npm install

# Start Vite development server
npm run dev
```

Open [http://localhost:5173](http://localhost:5173) in your browser.

---

## 22. Docker Compose Deployment

The simplest way to run the entire IntelliICU platform locally with all dependencies:

```powershell
# From project root
docker compose up --build -d
```

### Verified Port Mappings:
- **Frontend SPA (Nginx):** [http://localhost:80](http://localhost:80)
- **FastAPI Backend:** [http://localhost:8000](http://localhost:8000)
- **PostgreSQL Database:** `localhost:5433` (mapped from container `5432`)

### Checking Container Health:
```powershell
docker compose ps
```

---

## 23. Automated Verification & Test Results

IntelliICU includes comprehensive automated test coverage spanning unit, security, ML inference, and end-to-end integration tests:

### Executing the Test Suite:
```powershell
$env:PYTHONPATH="backend"
py -m pytest backend/tests/ -v
```

### Verified Test Results:
```text
============================= test session starts =============================
collected 30 items

backend/tests/test_end_to_end_integration.py::TestEndToEndIntegration::test_copilot_batch_rag_and_reasoning_engines PASSED
backend/tests/test_end_to_end_integration.py::TestEndToEndIntegration::test_copilot_returns_503_when_all_providers_unavailable PASSED
backend/tests/test_end_to_end_integration.py::TestEndToEndIntegration::test_copilot_system_message_refreshes_rag_evidence_on_cache_hit PASSED
backend/tests/test_end_to_end_integration.py::TestEndToEndIntegration::test_report_generation_and_pdf_download PASSED
backend/tests/test_groq_gemini_orchestration.py::TestGroqProvider::test_groq_auth_and_rate_limit_errors PASSED
backend/tests/test_groq_gemini_orchestration.py::TestGroqProvider::test_groq_malformed_response_raises PASSED
backend/tests/test_groq_gemini_orchestration.py::TestGroqProvider::test_groq_plain_text_mode_without_json_object PASSED
backend/tests/test_groq_gemini_orchestration.py::TestGroqProvider::test_groq_streaming_fragmented_and_empty_chunks PASSED
backend/tests/test_groq_gemini_orchestration.py::TestGroqProvider::test_groq_successful_structured_response PASSED
backend/tests/test_groq_gemini_orchestration.py::TestGroqProvider::test_init_with_and_without_credentials PASSED
backend/tests/test_groq_gemini_orchestration.py::TestGeminiProvider::test_gemini_successful_and_failure_handling PASSED
backend/tests/test_groq_gemini_orchestration.py::TestGeminiProvider::test_gemini_transient_503_retries_and_recovers PASSED
backend/tests/test_groq_gemini_orchestration.py::TestOrchestratorFailoverAndStreaming::test_both_fail_raises_controlled_error_without_mock PASSED
backend/tests/test_groq_gemini_orchestration.py::TestOrchestratorFailoverAndStreaming::test_explicit_mock_fallback_when_enabled PASSED
backend/tests/test_groq_gemini_orchestration.py::TestOrchestratorFailoverAndStreaming::test_groq_failure_falls_back_to_gemini PASSED
backend/tests/test_groq_gemini_orchestration.py::TestOrchestratorFailoverAndStreaming::test_groq_success_does_not_call_gemini PASSED
backend/tests/test_groq_gemini_orchestration.py::TestOrchestratorFailoverAndStreaming::test_streaming_pre_token_failover_and_mid_stream_error PASSED
backend/tests/test_groq_gemini_orchestration.py::TestAIConfigAndAPIIntegration::test_ai_config_and_health_endpoints PASSED
backend/tests/test_groq_gemini_orchestration.py::TestAIConfigAndAPIIntegration::test_env_precedence_over_stale_json PASSED
backend/tests/test_ml_and_rag.py::TestMLAndRAG::test_explainability_is_honestly_labelled_as_clinical_rules PASSED
backend/tests/test_ml_and_rag.py::TestMLAndRAG::test_feature_order_and_validation PASSED
backend/tests/test_ml_and_rag.py::TestMLAndRAG::test_hospital_assistant_uses_provider_factory_not_hardcoded_mock PASSED
backend/tests/test_security_and_rbac.py::TestSecurityAndRBAC::test_inactive_user_rejected PASSED
backend/tests/test_security_and_rbac.py::TestSecurityAndRBAC::test_unauthenticated_ai_timeline_telemetry_rejected PASSED
backend/tests/test_security_and_rbac.py::TestSecurityAndRBAC::test_unauthenticated_v1_endpoints_rejected PASSED
backend/tests/test_security_and_rbac.py::TestSecurityAndRBAC::test_unauthenticated_websocket_rejected PASSED
backend/tests/test_security_and_rbac.py::TestSecurityAndRBAC::test_viewer_forbidden_on_clinical_ai_and_settings PASSED
backend/tests/test_seeder_and_simulator.py::TestSeederAndSimulatorSafety::test_seeder_skipped_when_disabled PASSED
backend/tests/test_seeder_and_simulator.py::TestSeederAndSimulatorSafety::test_simulator_db_persistence_disabled_by_default PASSED
backend/tests/test_seeder_and_simulator.py::TestSeederAndSimulatorSafety::test_simulator_stop_flag PASSED

================= 30 passed, 36 warnings in 76.09s =================
```

---

## 24. How to Explain IntelliICU in a Technical Interview

Use these structured talking points when presenting IntelliICU to engineering hiring managers:

### 30-Second Elevator Pitch:
> "IntelliICU is an enterprise Clinical Decision Support Platform designed to mitigate cognitive overload in intensive care units. It streams high-frequency bedside telemetry via WebSockets, evaluates sepsis risk using an ensemble Random Forest model across 13 clinical features, grounds clinical reasoning in peer-reviewed protocols via a 1,608-chunk ChromaDB RAG vector store, and delivers real-time recommendations using a resilient, multi-provider LLM orchestrator that automatically fails over from Groq to Google Gemini."

### 2-Minute Technical Deep Dive:
> "From an engineering standpoint, IntelliICU addresses three critical challenges in production AI systems: latency, reliability, and hallucination prevention.
> 
> First, on latency: bedside telemetry updates continuously at configurable real-time intervals (default 2.0s). We avoid database polling bottlenecks by maintaining persistent WebSockets that push vital drifts directly to client ring-buffers without triggering React re-renders. For the ML pipeline, rather than incurring a 10-second container cold-start deserializing an 809MB model, we built a `LazyModelProxy` that memory-maps the Random Forest weights on the first inference call, allowing our FastAPI containers to start in under a second.
> 
> Second, on hallucination: general-purpose LLMs cannot be trusted with unstructured medical queries. We built an offline RAG engine with ChromaDB and BGE-small embeddings indexing 10 authoritative guideline PDFs into 1,608 chunks. When a clinician queries the Copilot, we construct an optimized patient context from PostgreSQL, retrieve the top-3 guideline chunks, and enforce strict negative constraints in the prompt, requiring exact source citations.
> 
> Third, on reliability: medical systems cannot drop requests due to an API outage. Our `ProviderOrchestrator` uses Groq's LPU as primary for 300+ token/second speed. If Groq hits rate limits or times out, it automatically fails over to Gemini Flash within the same request lifecycle and streams tokens back to the clinician via Server-Sent Events."

### Common Technical Questions & Answers:

<details>
<summary><strong>Q: Why did you use a Random Forest model instead of a Deep Neural Network or XGBoost?</strong></summary>

**A:** ICU tabular data typically exhibits complex, non-linear physiological interactions (e.g., tachycardia is benign unless paired with falling systolic BP and rising lactate). Random Forest models with 200 trees are exceptionally resilient to overfitting on correlated clinical features, require minimal scaling artifacts, and produce well-calibrated class probabilities. Additionally, tree ensembles allow straightforward post-hoc explainability and feature importance analysis, which are regulatory requirements in healthcare.
</details>

<details>
<summary><strong>Q: How do you handle LLM rate limits and API timeouts in a live hospital setting?</strong></summary>

**A:** We implemented the `ProviderOrchestrator` pattern with active-passive failover. Primary requests go to Groq (`openai/gpt-oss-120b`). If Groq returns an HTTP 429 (Rate Limit), 5xx server error, or exceeds our 30-second timeout, the orchestrator intercepts the exception, records a warning log, and instantly re-routes the prompt to Google Gemini (`gemini-3.8-flash`). In production mode (`AI_ENABLE_MOCK_FALLBACK=false`), if both providers fail, it returns an explicit HTTP 503 rather than hallucinating dangerous mock advice.
</details>

<details>
<summary><strong>Q: Why did you build custom RAG orchestration instead of using LangChain chains?</strong></summary>

**A:** While we utilize LangChain's battle-tested `PyPDFLoader` and `RecursiveCharacterTextSplitter` for document extraction and chunking, we deliberately avoided LangChain agent chains for the runtime query pipeline. In critical care systems, black-box agent abstractions add unpredictable latency, complex call stacks, and difficult debugging during mid-stream failures. Our native Python `KnowledgeService` and `ProviderOrchestrator` provide deterministic control over SSE token generation, exact memory budgeting, and explicit error recovery.
</details>

---

## 25. Known Limitations

- **Simulated Physiological Telemetry:** Because access to live hospital patient monitoring networks (Philips IntelliVue / GE Healthcare) is restricted by patient privacy regulations, telemetry drifts are synthesized via a background numerical simulator.
- **HL7 / FHIR Integration:** The current platform ingests vitals via REST and WebSockets; direct HL7 v2 MLLP feeds or FHIR R4 interfaces are planned for future releases.
- **Single Model Version:** Risk scoring is calibrated for adult ICU sepsis identification; pediatric and neurological risk stratification models are not yet deployed.

---

## 26. Clinical Safety & Compliance Disclaimer

> **IMPORTANT CLINICAL NOTICE:**  
> IntelliICU is a software engineering reference implementation and research prototype developed for educational, portfolio, and technical demonstration purposes only.
> 
> - **Not a Certified Medical Device:** IntelliICU has not been evaluated, cleared, or approved by the United States Food and Drug Administration (FDA), European Medicines Agency (EMA), or any other medical regulatory authority.
> - **No Real-World Clinical Use:** It is not intended for use in the diagnosis, cure, mitigation, treatment, or prevention of disease in humans or animals.
> - **Not a Clinician Replacement:** AI-generated predictions, risk levels, and copilot summaries must never supersede the independent clinical judgment of a licensed healthcare provider.
> - **Regulatory Compliance:** This deployment is not HIPAA or GDPR-certified and must not be used to store Protected Health Information (PHI).

---

## 27. Future Roadmap

- [ ] **HL7 / FHIR R4 Ingestion Pipeline:** Add native FHIR `Observation` and `Patient` resource listeners.
- [ ] **Multi-Modal Imaging Integration:** Ingest and visualize chest X-rays (DICOM format) with segmentation overlays.
- [ ] **Continuous Online ML Monitoring:** Track prediction drift and feature distribution shifts using Evidently AI.
- [ ] **Wearable Sensor Integration:** Extend WebSocket protocols to accept BLE telemetry streams from clinical wearables.

---

## 28. Author & Contact

**Developed by:** Sumeet  
**Project Link:** [https://github.com/Sumeet2005/IntelliICU.git](https://github.com/Sumeet2005/IntelliICU.git)  
**Live Application:** [https://intelliicu-frontend-production.up.railway.app](https://intelliicu-frontend-production.up.railway.app)

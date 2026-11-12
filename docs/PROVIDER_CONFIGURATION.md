# IntelliICU — Provider Configuration & Verification Guide

## 1. Environment Variables (`backend/.env` or Root `.env`)

```dotenv
# Primary & Fallback Orchestration
AI_PROVIDER=groq
AI_FALLBACK_PROVIDER=gemini
AI_ENABLE_MOCK_FALLBACK=false

# Groq (Primary)
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=openai/gpt-oss-120b
GROQ_TIMEOUT_SECONDS=30.0

# Google Gemini (Fallback)
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-3.8-flash
GEMINI_TIMEOUT_SECONDS=30.0

# Generation Defaults
CLINICAL_LLM_TEMPERATURE=0.2
CLINICAL_LLM_MAX_TOKENS=1024
CLINICAL_LLM_STREAMING=true
```

> **Security Note:** Never commit `.env` files or paste API keys into logs or source control.

---

## 2. Docker Execution

```powershell
# 1. Navigate to project root
cd D:\Projects\IntelliICU

# 2. Rebuild and start backend + frontend (preserves existing PostgreSQL volume)
docker compose up -d --build backend frontend

# 3. Verify container status
docker compose ps
```

---

## 3. How to Verify Provider Health, Groq Primary, and Gemini Fallback

1. **Check Provider Health (Non-Live vs Live):**
   - `GET http://localhost:8000/api/ai/health?live=false` (requires Bearer JWT) — shows `credentials_configured` for primary & fallback without making external API calls.
   - `GET http://localhost:8000/api/ai/health?live=true` (requires Bearer JWT) — performs live `models.list()` against Groq and Gemini and verifies `openai/gpt-oss-120b` and `gemini-3.8-flash` availability.
2. **Verify Groq Primary:**
   - Send `POST http://localhost:8000/api/clinical-copilot/chat` with a valid JWT. Inspect `provider_metadata` in the response: `provider: "groq"`, `fallback_used: false`, `simulated: false`.
3. **Verify Groq → Gemini Fallback:**
   - Temporarily set an invalid `GROQ_API_KEY` or `GROQ_MODEL=nonexistent-model` in `backend/.env` (with a valid `GEMINI_API_KEY`), restart `backend`, and call `/api/clinical-copilot/chat`.
   - `provider_metadata` will report `provider: "gemini"`, `fallback_used: true`, `primary_provider: "groq"`, and `primary_error` (sanitized).
4. **Verify Controlled Failure (No Silent Mock):**
   - With `AI_ENABLE_MOCK_FALLBACK=false` and both keys invalid/missing, `/api/clinical-copilot/chat` returns HTTP `503` (`LLMUnavailableError`) instead of fabricating a mock clinical response.

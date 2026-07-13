# IntelliICU Production Operations & Deployment Guide

This guide describes how to deploy, monitor, and maintain the IntelliICU enterprise clinical decision support platform in production environments.

## 1. Prerequisites
- **Docker**: Engine version 20.10+
- **Docker Compose**: Version 2.0+

## 2. Configuration Setup
Create a `.env` file in the `backend` directory based on the provided sample [backend/.env.example](file:///d:/Projects/IntelliICU/backend/.env.example):
```bash
cp backend/.env.example backend/.env
```
Ensure that you generate a strong secret key for `AUTH_SECRET_KEY` and set the PostgreSQL credentials accordingly.

## 3. Local Containerized Launch
To build and start all containers (PostgreSQL database, FastAPI backend, and Nginx frontend) in the background:
```bash
docker-compose up --build -d
```

During startup, the backend container automatically runs Alembic database schema migrations using [backend/start.sh](file:///d:/Projects/IntelliICU/backend/start.sh) prior to launching the Gunicorn process.

## 4. Monitoring & Health Checks
FastAPI exposes health monitoring signals to load balancers, orchestrators, and ping scripts:
- **Liveness probe**: `GET /health` (or `/live`)
- **Readiness probe**: `GET /ready`

These endpoints return status codes and connection health reports:
```json
{
  "status": "healthy",
  "database": "connected",
  "services": "online",
  "timestamp": "2026-07-13T19:10:00Z"
}
```

## 5. Logs & Audits
Structured JSON logs are generated and rotated automatically inside the container system to avoid local disc overflow. Gunicorn stdout/stderr flows can be retrieved using standard docker logs:
```bash
docker logs -f intelliicu-backend
```

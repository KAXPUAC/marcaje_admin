# Marcaje Admin - Agent Instructions

## Project Overview
FastAPI service for facial recognition-based attendance marking (marcaje) for Universidad Galileo. Uses AWS Rekognition for liveness detection + face search, Oracle 12c for persistence.

## Developer Commands
```bash
# Run dev server (auto-reload)
uv run fastapi dev

# Install/sync dependencies
uv sync
```

## Architecture
```
main.py                          # FastAPI app, DB pool init, router registration
api/v1/endpoints/liveness.py     # POST /create-session, POST /verify
services/rekognition_service.py  # AWS Rekognition face search by department collection
repositories/marcaje_repo.py     # Oracle 12c queries (EMPLEADO_BIOMETRIA, MARCAJES_ASISTENCIA)
core/database.py                 # Oracle connection pool (oracledb)
core/config.py                   # Pydantic Settings from .env
core/aws.py                      # boto3 Rekognition client singleton
```

## Key Conventions
- **Department collections**: AWS Rekognition collection naming = `depto_{departamento_id.lower()}`
- **Liveness threshold**: 85% confidence minimum (hardcoded in liveness.py:29)
- **Face match threshold**: 90% similarity (default in rekognition_service.py:12)
- **DB pool**: min=2, max=10 connections, initialized at startup
- **Env loading**: `.env` file at project root, loaded via `dotenv` with `override=True`

## Required Environment Variables (.env)
```
AWS_REGION, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_S3_BUCKET_NAME
ORACLE_USER, ORACLE_PASSWORD, ORACLE_DNS
```

## Data Flow (Verify Endpoint)
1. Client calls `/api/v1/liveness/create-session` → returns AWS session_id
2. Client runs AWS liveness check on device → gets session_id
3. Client calls `/api/v1/liveness/verify` with `{session_id, departamento_id, tipo_marcaje}`
4. Server fetches liveness result from AWS → validates status=SUCCEEDED + confidence≥85%
5. Server searches face in department's Rekognition collection (threshold 90%)
6. Server looks up `EMPLEADO_ID` from `EMPLEADO_BIOMETRIA` by `FACE_ID`
7. Server inserts into `MARCAJES_ASISTENCIA` (EMPLEADO_ID, TIPO_MARCAJE, SIMILITUD_PORCENTAJE)

## Notable Files (Empty/Placeholder)
- `api/v1/endpoints/marcaje.py` - empty
- `api/v1/endpoints/empleados.py` - empty
- `schemas/marcaje.py` - empty
- `repositories/empleado_repo.py` - empty
- `services/liveness_service.py` - empty
- `api/v1/router.py` - empty

## Missing/To Verify
- No test suite found
- No lint/typecheck config (ruff, mypy, pyright)
- No CI/CD workflows
- No Dockerfile or deployment config
- Oracle 12c must be accessible for dev (no local mock)
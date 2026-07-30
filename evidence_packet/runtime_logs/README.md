# Runtime Logs

This directory should contain runtime log output captured during a live demonstration of MITRA.

## Required Logs

1. **`backend_startup.txt`** — Terminal output showing the FastAPI backend starting successfully.
   - Source: copy content from `Screenshotss/backendterminal.png` or re-run `uvicorn app.main:app`

2. **`frontend_serve.txt`** — Terminal output showing the frontend being served.
   - Source: `Screenshotss/frontendterminal.png`

3. **`health_check.json`** — JSON response from `GET /health` confirming the backend is alive.
   - Capture with: `curl http://localhost:8000/health`

4. **`conversation_trace.json`** — A sample request/response from `POST /api/assistant`.
   - Source: `backend/MITRA_CONTROL_PLANE_LIVE_JSON.json` or `backend/FULL_SYSTEM_TRACE.json`

## Available Evidence

The backend directory already contains extensive runtime proof files:
- `backend/FULL_SYSTEM_TRACE.json`
- `backend/MITRA_CONTROL_PLANE_LIVE_JSON.json`
- `backend/TRACE_CONTINUITY_PROOF.md`
- `backend/reminder_execution_trace.json`

These can be copied here.

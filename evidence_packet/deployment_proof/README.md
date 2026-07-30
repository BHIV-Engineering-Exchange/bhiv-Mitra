# Deployment Proof

This directory contains proof that MITRA is deployed and accessible.

## Local Deployment

### Start Backend
```bash
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Backend will be available at: `http://localhost:8000`

API docs (Swagger UI): `http://localhost:8000/docs`

### Serve Frontend
```bash
# From the project root — any static server works:
npx serve .
# or
python -m http.server 5500
```

MITRA pages will be at:
- `http://localhost:5500/login.html`
- `http://localhost:5500/signup.html`
- `http://localhost:5500/pages/gurukul.html`
- `http://localhost:5500/pages/samruddhi.html`
- `http://localhost:5500/pages/setu.html`
- `http://localhost:5500/pages/uniguru.html`

---

## Verification Steps

1. Open `http://localhost:5500/login.html` → MITRA FAB should be visible in bottom-right
2. Click the FAB → companion window should expand with the greeting message
3. Type a message and press Enter → message appears in chat; backend responds
4. Navigate to `http://localhost:5500/pages/gurukul.html` → same conversation continues
5. Navigate to `http://localhost:5500/pages/samruddhi.html` → same conversation continues
6. Navigate to `http://localhost:5500/pages/setu.html` → same conversation continues

---

## Remote Deployment

See `backend/render.yaml` and `backend/DEPLOYMENT_CONFIG.md` for Render.com deployment configuration.

Backend is deployed at: *(update with actual URL from Raj's production runtime)*

---

## Evidence

- `Screenshotss/backendterminal.png` — backend running
- `Screenshotss/frontendterminal.png` — frontend being served
- `Screenshotss/swagger.png` — Swagger UI confirming API endpoints
- `Screenshotss/loginpage.png` — login page with MITRA visible

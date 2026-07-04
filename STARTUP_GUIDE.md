# MITRA - Complete Startup Guide

## Quick Start

### Prerequisites

1. Python 3.10+ installed
2. Node.js 16+ installed
3. MongoDB Atlas account (or local MongoDB)

---

## Backend Setup

### 1. Navigate to Backend Directory

```bash
cd backend
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

### 3. Activate Virtual Environment

**Windows:**
```bash
venv\Scripts\activate
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables

The `.env` file has been created with your MongoDB URI:

```
MONGODB_URI=mongodb+srv://blackholeinfiverse54_db_user:Gjpl998Z6hsQLjJF@artha.rzneis7.mongodb.net/?appName=Artha
DATABASE_NAME=mitra_production
```

**Important:** Update these values in `backend/.env`:

```env
# Required for production
API_KEY=your_secure_api_key_here
JWT_SECRET_KEY=your_secure_jwt_secret_here

# Optional: Add at least one LLM provider for AI responses
# GROQ_API_KEY=your_groq_key
# OPENAI_API_KEY=your_openai_key
```

### 6. Start Backend Server

```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### 7. Verify Backend is Running

Open browser and go to:
- API Documentation: http://localhost:8000/docs
- Health Check: http://localhost:8000/health
- Root Info: http://localhost:8000/

---

## Frontend Setup

### 1. Navigate to Frontend Directory

```bash
cd frontend/frontend
```

### 2. Install Dependencies

```bash
npm install
```

### 3. Configure Environment Variables

The `.env` file has been created with:

```
REACT_APP_API_URL=http://localhost:8000
REACT_APP_API_KEY=mitra_production_api_key_2026_secure_random_value
```

**Important:** Make sure the `REACT_APP_API_KEY` matches the `API_KEY` in `backend/.env`

### 4. Start Frontend Server

```bash
npm start
```

### 5. Verify Frontend is Running

Open browser and go to:
- Frontend: http://localhost:3000

---

## MongoDB Connection

Your MongoDB Atlas connection is configured:

```env
MONGODB_URI=mongodb+srv://blackholeinfiverse54_db_user:Gjpl998Z6hsQLjJF@artha.rzneis7.mongodb.net/?appName=Artha
DATABASE_NAME=mitra_production
```

### Verify MongoDB Connection

1. Start the backend server
2. Check the health endpoint: http://localhost:8000/health
3. Look for `"mongodb": "ok"` in the response

### MongoDB Collections

The following collections will be created automatically:

- `users` - User accounts
- `tasks` - Task records
- `audit_logs` - Bucket audit trail with trace IDs

---

## Testing the System

### 1. Test Backend API

**Signup:**
```bash
curl -X POST http://localhost:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -H "X-API-Key: mitra_production_api_key_2026_secure_random_value" \
  -d '{"name": "Test User", "email": "test@example.com", "password": "testpass123"}'
```

**Login:**
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -H "X-API-Key: mitra_production_api_key_2026_secure_random_value" \
  -d '{"email": "test@example.com", "password": "testpass123"}'
```

**Chat:**
```bash
curl -X POST http://localhost:8000/api/assistant \
  -H "Content-Type: application/json" \
  -H "X-API-Key: mitra_production_api_key_2026_secure_random_value" \
  -d '{
    "version": "3.0.0",
    "input": {"message": "Hello, what can you do?"},
    "context": {"platform": "web", "device": "desktop"}
  }'
```

**Mitra Evaluate:**
```bash
curl -X POST http://localhost:8000/api/mitra/evaluate \
  -H "Content-Type: application/json" \
  -H "X-API-Key: mitra_production_api_key_2026_secure_random_value" \
  -d '{
    "event": {"title": "Test", "content": "This is a test event"},
    "user_id": "test_user"
  }'
```

### 2. Test Frontend

1. Open http://localhost:3000
2. Sign up for a new account
3. Login with your credentials
4. Start chatting with the assistant

### 3. Run Tests

```bash
cd backend
python -m pytest tests/ -v
```

---

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API info and endpoints |
| `/health` | GET | Health check with MongoDB status |
| `/health/system` | GET | Deep system health |
| `/api/auth/signup` | POST | User signup |
| `/api/auth/login` | POST | User login |
| `/api/auth/me` | GET | Get current user |
| `/api/assistant` | POST | Main chat endpoint |
| `/api/mitra/evaluate` | POST | Policy evaluation |
| `/api/replay/{trace_id}` | POST | Replay trace |
| `/api/replay/{trace_id}/stages` | GET | Get trace stages |
| `/api/replay/compare` | POST | Compare traces |
| `/api/metrics` | GET | System metrics |
| `/api/metrics/system` | GET | Detailed metrics |
| `/api/metrics/enforcement` | GET | Enforcement stats |
| `/webhooks/whatsapp` | POST | WhatsApp webhook |
| `/webhooks/telegram` | POST | Telegram webhook |
| `/webhooks/email` | POST | Email webhook |
| `/webhooks/instagram` | POST | Instagram webhook |

---

## Environment Variables Reference

### Required

| Variable | Description | Your Value |
|----------|-------------|------------|
| `MONGODB_URI` | MongoDB connection string | `mongodb+srv://blackholeinfiverse54_db_user:Gjpl998Z6hsQLjJF@artha.rzneis7.mongodb.net/?appName=Artha` |
| `DATABASE_NAME` | MongoDB database name | `mitra_production` |
| `API_KEY` | API key for authentication | Set in `.env` |
| `JWT_SECRET_KEY` | JWT signing secret | Set in `.env` |

### Optional (for AI responses)

| Variable | Description |
|----------|-------------|
| `GROQ_API_KEY` | Groq API key (free tier available) |
| `OPENAI_API_KEY` | OpenAI API key |
| `GOOGLE_API_KEY` | Google Gemini API key |
| `MISTRAL_API_KEY` | Mistral API key |

### Optional (for integrations)

| Variable | Description |
|----------|-------------|
| `TWILIO_ACCOUNT_SID` | Twilio account SID |
| `TWILIO_AUTH_TOKEN` | Twilio auth token |
| `TELEGRAM_BOT_TOKEN` | Telegram bot token |
| `BREVO_API_KEY` | Brevo email API key |
| `SENDGRID_API_KEY` | SendGrid email API key |

---

## Troubleshooting

### Backend Won't Start

1. Check Python version: `python --version` (need 3.10+)
2. Check MongoDB connection: Verify `MONGODB_URI` in `.env`
3. Check port availability: Ensure port 8000 is not in use

### Frontend Won't Start

1. Check Node.js version: `node --version` (need 16+)
2. Clear npm cache: `npm cache clean --force`
3. Reinstall dependencies: `rm -rf node_modules && npm install`

### MongoDB Connection Issues

1. Verify IP whitelist in MongoDB Atlas
2. Check username/password in connection string
3. Verify network connectivity

### API Key Errors

1. Ensure `API_KEY` is set in `backend/.env`
2. Ensure `REACT_APP_API_KEY` in `frontend/frontend/.env` matches
3. Restart both servers after changing keys

---

## Production Deployment

### Backend (Render)

1. Push code to GitHub
2. Connect repository to Render
3. Set environment variables in Render dashboard
4. Deploy with:
   - Root Directory: `backend`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### Frontend (Vercel)

1. Push code to GitHub
2. Connect repository to Vercel
3. Set environment variables in Vercel dashboard
4. Deploy with:
   - Root Directory: `frontend/frontend`
   - Build Command: `npm run build`
   - Output Directory: `build`

---

## Support

For issues or questions:
1. Check the API documentation at http://localhost:8000/docs
2. Review the health status at http://localhost:8000/health
3. Check the metrics at http://localhost:8000/api/metrics

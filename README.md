<div align="center">
  <h1>Mitra AI Command Center</h1>
  <p><strong>A deterministic, safe, and powerful universal AI companion.</strong></p>
</div>

---

## 📖 Overview

The **Mitra AI Command Center** is a full-stack, multimodal AI assistant designed with a strict emphasis on deterministic safety and dynamic routing. It seamlessly connects a responsive React frontend to a high-performance FastAPI backend. 

Mitra is built with a sophisticated **Control Plane** and **Policy Enforcement Engine**. Every user request is intercepted, checked against safety artifacts, classified by intent, and routed to the appropriate execution agent (General Chat, Task, Email, etc.)—guaranteeing that the system fails closed on unsafe inputs and reliably delegates tasks.

---

## ✨ Features

- **Responsive Chat Interface**: Built with modern React and TypeScript for fluid interactions.
- **Backend API Integration**: Powered by FastAPI for high-speed, asynchronous request handling.
- **Advanced Prompt Routing**: Intelligently routes queries using `assistant_orchestrator.py` based on extracted intents and platform signals.
- **Intent Classification**: Custom NLU pipeline (`intentflow.py`) resolving intents, entities, dates, and urgencies.
- **Multi-Agent Workflows**: Dedicated execution paths for:
  - General Chat (Knowledge base/LLMs)
  - Tasks (EMS / Todo lists)
  - Communications (Email, WhatsApp, Telegram, Instagram)
  - Utilities (Calendar, Reminders)
- **Multi-language Support**: Automatically translates inputs and outputs using the `multilingual_service`.
- **Voice Support**: Integrated speech-to-text and text-to-speech (XTTS engine) for multimodal capability.
- **Authentication**: Secured via API Key validation.
- **Deterministic Enforcement**: Safety-first pipeline that validates request context against `BucketService` before LLM generation.
- **Offline Development Mode**: Can run entirely locally using an in-memory database fallback and the `Uniguru` local knowledge base mock engine.

---

## 🛠 Tech Stack

- **Frontend**: React, TypeScript, HTML/CSS
- **Backend**: Python 3.10+, FastAPI, Uvicorn
- **Database**: MongoDB (Production), Shared Class-level Memory Store (Development)
- **LLM Providers**: Modular integration supporting OpenAI, Groq, Google Gemini, and Mistral (with a local `Uniguru` fallback).
- **Other Libraries**: Pydantic, python-dotenv, Regex, Dateutil

---

## 📂 Project Structure

```text
MITRA-Universal-Companion/
│
├── backend/
│   ├── app/
│   │   ├── core/                  # Orchestrator, LLM Bridge, IntentFlow, Prompts
│   │   ├── external/enforcement/  # Policy Engine, Deterministic Trace logic
│   │   ├── services/              # BucketService, ControlPlaneService, Multilingual
│   │   └── main.py                # FastAPI Entrypoint
│   └── requirements.txt           # Backend dependencies
│
├── frontend/
│   └── frontend/
│       ├── src/                   # React components, services, ContextStore
│       └── package.json           # Frontend dependencies
│
└── README.md
```

---

## ⚙️ Installation

### Prerequisites
- Node.js (v16+)
- Python (3.10+)
- npm or yarn

### 1. Clone the repository
```bash
git clone <repository-url>
cd MITRA-Universal-Companion
```

### 2. Setup Backend
```bash
cd backend
python -m venv venv
# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Setup Frontend
```bash
cd ../frontend/frontend
npm install
```

---

## 🔐 Environment Variables

Create a `.env` file in the `backend/` directory.

| Variable | Description | Required |
|----------|-------------|----------|
| `API_KEY` | Authenticates frontend requests to the backend. | Yes |
| `OPENAI_API_KEY` | Optional: OpenAI provider key. | No |
| `GROQ_API_KEY` | Optional: Groq provider key. | No |
| `GOOGLE_API_KEY` | Optional: Google Gemini provider key. | No |
| `MISTRAL_API_KEY` | Optional: Mistral provider key. | No |
| `LLM_CACHE_MAX_SIZE` | LRU Cache max size (defaults to 500). | No |

---

## 🚀 Running the Project

### Running the Backend
From the `backend/` directory (with your virtual environment activated):
```bash
uvicorn app.main:app --reload
```
The backend API will run on `http://127.0.0.1:8000`.

### Running the Frontend
From the `frontend/frontend/` directory:
```bash
npm start
```
The React UI will run on `http://localhost:3000`.

---

## 📸 Screenshots

| Home Page | Chat Interface |
|-----------|----------------|
| *[Screenshot Placeholder]* | *[Screenshot Placeholder]* |

| AI Response | Task Creation Workflow |
|-------------|------------------------|
| *[Screenshot Placeholder]* | *[Screenshot Placeholder]* |

| API Integration / Swagger |
|---------------------------|
| *[Screenshot Placeholder]*|

---

## 📚 API Documentation

FastAPI automatically generates interactive Swagger/OpenAPI documentation for the backend. 
Once the backend is running, you can explore and test the endpoints directly by navigating to:
**[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)**

---

## 🧪 Testing

The system has been manually validated against the following testing suite to ensure intent isolation, local constraint parsing, and safety bypassing:

- **Identity Check**: `"Who are you?"` -> Successfully returns the standard identity fallback.
- **Constraints**: `"Explain AI in two lines."` -> Parses offline constraints and truncates to 2 lines.
- **Edge-case Safety**: `"What is the capital of India?"` -> General chat routing (prevents false-positive `api` triggers).
- **Skill Checks**: `"Write a Python function to add two numbers."` -> Safely handles Python knowledge requests.


---

## ⚠️ Known Issues

- **Constraint Rigidity in Offline Mode**: The local offline model (`Uniguru`) uses regex and dictionary lookup. It only parses explicitly coded constraints like `"2 lines"` or `"sentence"`. Dynamic capabilities heavily rely on integrating real LLM API keys.
- **Action Extraction Limitations**: `assistant_orchestrator.py` uses Regex to extract action parameters (like emails or dates). Highly complex or deeply nested grammatical instructions might fail to extract valid task parameters, falling back to an error prompt.

---

## 💡 Future Improvements

1. **LLM-Based Intent Classification**: Upgrade the heuristic Regex intent engine (`intentflow.py`) to use lightweight LLMs for dynamic entity and intent classification.
2. **Persistent Vector Database**: Replace the localized dictionary knowledge base with a RAG (Retrieval-Augmented Generation) pipeline backed by a Vector DB for robust, contextual offline data.
3. **Multi-threading State Lock**: Add `threading.Lock` to the development `BucketService` shared memory store to prevent race conditions during high-volume testing.
4. **Enhanced Production Persistence**: Ensure strict MongoDB connection retries in production rather than silently dropping to an in-memory store.

---

## 🤝 Contributing
Contributions are always welcome. Please ensure that the `MitraControlPlaneService` deterministic requirements are not violated before submitting any PRs. 

---

## 📄 License
*Specify License Here (e.g. MIT, Apache 2.0)*

---

## ✍️ Author
**Mitra Development Team**

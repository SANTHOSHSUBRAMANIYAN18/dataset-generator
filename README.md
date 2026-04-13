# AI Dataset Generator MVP

Minimal full-stack prototype with:

- `frontend`: React + Vite
- `backend`: Node.js + Express
- `ml-service`: FastAPI

## Run locally

### 1. Start the Python ML service

```bash
cd ml-service
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### 2. Start the Node backend

```bash
cd backend
npm install
npm run dev
```

### 3. Start the React frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs on `http://localhost:5173` and sends requests to the backend on `http://localhost:4000`.

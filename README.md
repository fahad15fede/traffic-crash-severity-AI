# 🚗 Traffic Crashes.AI

[![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)](https://react.dev/)
[![FastAPI](https://img.shields.io/badge/fastapi-109989?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![XGBoost](https://img.shields.io/badge/xgboost-2C8EAD?style=for-the-badge&logo=scikitlearn&logoColor=white)](https://xgboost.readthedocs.io/)
[![Supabase](https://img.shields.io/badge/Supabase-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white)](https://supabase.com/)
[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)

An advanced, full-stack machine learning web application that predicts **traffic accident injury severity** based on real-time environmental, roadway, and collision factors. Built with a production-ready **React + Vite** frontend, a scalable **FastAPI** backend (hosted on Hugging Face Spaces Docker), and **Supabase** for secure user authentication and PostgreSQL-backed state persistence.

---

## 🌟 Live Architecture

| Service | Role | URL / Technology |
|:---|:---|:---|
| **Frontend UI** | Premium Client Application | Hosted on Vercel |
| **Backend API** | FastAPI Predictor & Middleware | [Hugging Face Spaces](https://fede8rma-carcrashai.hf.space) |
| **Auth & DB** | PostgreSQL & Secure Sessions | [Supabase Database](https://tjyxnhzuvygcmthesuov.supabase.co) |

---

## 🎨 Premium UI & Styling System

The user interface has been redesigned to align with premium, high-fidelity design aesthetics, incorporating:
- **Outlined Floating-Label Selects**: Input boxes feature sharp, subtle borders. When a field is unselected, the label floats vertically in the center as a placeholder. When focused or when a value is selected, the label transitions smoothly up onto the top-left border line, maintaining 100% legibility and structural beauty.
- **Unified Custom Controls**: Stepper inputs ("Vehicles Involved"), range sliders ("Crash Hour"), and toggle switches ("Intersection involved?") are wrapped in matching custom outlined field cards, with static labels sitting cleanly on the borders.
- **Responsive Layout**: Designed with a dynamic 2-column grid layout for desktop viewports that seamlessly collapses into a single-column stacked layout (`gap: 20px`) on mobile devices, ensuring fluid responsiveness and visual consistency.

---

## ⚙️ Robust Predictions & Normalization Layer

The platform is designed to handle heterogenous model classes gracefully:
1. **Model 1 (Pulse - Random Forest)**: Returns string-based class predictions directly (`'NO_INJURY'`, `'MINOR'`, `'SEVERE'`).
2. **Model 2 (Nexus - XGBoost)**: Predicts numeric classes (`[0, 1, 2]`) which may occasionally be formatted as string-floats (e.g. `'1.0'`, `'2.0'`) depending on serialisation engines.

### Unified Resiliency Engine
- **Backend Level (`backend/main.py`)**: Features a robust `to_label` conversion routine that converts float-formatted string representations to integers safely before resolving labels:
  ```python
  def to_label(v):
      try:
          val_int = int(float(v))
          return LABEL_MAP.get(val_int, str(v))
      except (ValueError, TypeError):
          return str(v)
  ```
- **Frontend Normalization Layer (`App.jsx`)**: Standardizes all response keys on the client side using a lookup dictionary. This ensures that even if the deployed API changes versions, the frontend will map predictions and confidence statistics to standard uppercase keys (`NO_INJURY`, `MINOR`, `SEVERE`) seamlessly:
  ```javascript
  const FRONTEND_LABEL_MAP = {
    "0": "NO_INJURY",
    "1": "MINOR",
    "2": "SEVERE",
    "NO_INJURY": "NO_INJURY",
    "MINOR": "MINOR",
    "SEVERE": "SEVERE",
  };
  ```

---

## 📂 Project Structure

```
carCrashFata/
├── backend/
│   ├── main.py                   # FastAPI prediction server
│   ├── model_final_rf.pkl        # Model 1 — Random Forest (Pulse)
│   ├── model_final_xgboost1.pkl  # Model 2 — XGBoost (Nexus)
│   ├── requirements.txt          # Python virtual env dependencies
│   ├── requirements_hf.txt       # Hugging Face deployment dependencies
│   ├── Dockerfile                # Production Docker container definition
│   ├── test_batch.py             # Integration batch tests for both models
│   └── test_models.py            # Local pickle direct validation (100 cases)
├── frontend/
│   ├── src/
│   │   ├── App.jsx               # React main app (form, results, auth integration)
│   │   ├── App.css               # Outlined floating-label design system
│   │   ├── index.css             # Base reset and modern font import
│   │   ├── components/
│   │   │   └── AuthModal.jsx     # Supabase login & signup dialog
│   │   └── lib/
│   │       └── supabase.js       # Client wrapper for Supabase JS API
│   ├── .env                      # Local client credentials (git-ignored)
│   └── package.json              # React project definition
├── AUTH_DB_PLAN.md               # Backend auth integration design notes
└── README.md                     # Main project showcase document
```

---

## 🛠️ Features

- **Multi-Model Inference**: Switch seamlessly between the lightweight **Pulse** model (Random Forest, unlimited free usage) and the heavy-duty **Nexus** model (XGBoost, requires sign-in).
- **Explainable AI (XAI)**:
  - Extracts the top risk factor (e.g. adverse weather, curved road, high-impact crash types) dynamically based on user inputs.
  - Dynamically renders tailored, actionable safety tips matching the predicted injury severity and risk factors.
  - Live interactive bar charts of the top active risk weights.
- **Confidence Distribution**: Renders a standard-compliant, color-coded conic gradient pie chart illustrating the model's confidence across classes.
- **Token-Gated Authentication**:
  - Unauthenticated guests receive 3 free trial tokens for the high-end **Nexus** model.
  - Signing up via Supabase awards the user 10 permanent tokens, stored in a PostgreSQL `profiles` table.
- **Secure Architecture**: Session state is persistent and synced via the Supabase client.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- Node.js 16+

### 1. Run the FastAPI Backend
```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run server
uvicorn main:app --reload
```
The API server will launch at `http://127.0.0.1:8000`.

### 2. Run the React Frontend
```bash
cd frontend
npm install
npm run dev
```
The application will launch at `http://localhost:5173`.

---

## 📧 Database Schema (PostgreSQL)

Set up these tables in your Supabase SQL editor:

```sql
-- User profiles (automatically synced via PostgreSQL triggers on auth.users)
create table profiles (
  id              uuid primary key references auth.users(id) on delete cascade,
  email           text,
  model1_tokens   int not null default 10,
  created_at      timestamptz default now()
);

-- Prediction history
create table predictions (
  id          uuid primary key default gen_random_uuid(),
  user_id     uuid references profiles(id) on delete cascade,
  model_used  int not null,
  severity    text not null,
  confidence  jsonb,
  inputs      jsonb,
  created_at  timestamptz default now()
);
```

---

## 🧪 Testing Suite

### Direct Pickle Validation
Directly evaluates the `.pkl` files locally over 100 mock cases without running the API server:
```bash
cd backend
python test_models.py
```
Outputs classification reports, F1-scores, and ranks the models by prediction accuracy.

### Live API Batch Test
Tests the live FastAPI server across 40 labelled scenarios:
```bash
cd backend
python test_batch.py
```

---

## 🎨 UI Branding & Styling Reference

| Token Name | Hex Code | Purpose |
|:---|:---|:---|
| **Deep Space** | `#0d0d0d` | Core app canvas background |
| **Steel Blue** | `#34435E` | Sidebar card panels, high-contrast text |
| **Amber Gold** | `#FFC857` | Active borders, badges, premium headings |
| **Vivid Violet**| `#7C3AED` | Brand `.AI` accent, focused form outlines |
| **Safe Green** | `#22c55e` | `.no_injury` severity theme |
| **Warning Amber**| `#eab308` | `.minor` severity theme |
| **Danger Red** | `#ef4444` | `.severe` severity theme |
| **Warm Canvas**| `#f5f5f5` | Form background card |

---

## 📦 Deployment Instructions

### Frontend (Vercel)
1. Link your GitHub repository to Vercel.
2. Set the root directory to `frontend`.
3. Inject client environment variables:
   - `VITE_SUPABASE_URL`
   - `VITE_SUPABASE_ANON_KEY`
   - `VITE_API_URL` (Points to the FastAPI server)

### Backend (Hugging Face Spaces)
1. Create a Hugging Face Space using the **Docker SDK**.
2. Push all code under the `backend/` directory (including the `.pkl` models and `Dockerfile`).
3. Set your Space's environment variables / secrets:
   - `SUPABASE_URL`
   - `SUPABASE_SERVICE_KEY`
   - `SUPABASE_JWKS_URL`

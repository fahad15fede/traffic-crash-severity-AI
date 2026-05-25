# Traffic Crashes.AI

A full-stack ML web app that predicts traffic accident injury severity based on environmental, road, and crash conditions. Built with React + Vite on the frontend, FastAPI on the backend (hosted on Hugging Face Spaces), and Supabase for auth and database.

---

## Live

| Service | URL |
|---|---|
| Frontend | Vercel (your deployment URL) |
| Backend API | https://fede8rma-carcrashai.hf.space |
| Supabase | https://tjyxnhzuvygcmthesuov.supabase.co |

---

## Project Structure

```
carCrashFata/
├── backend/
│   ├── main.py                   # FastAPI app
│   ├── model_final_rf.pkl        # Model 1 — Random Forest
│   ├── model_final_xgboost1.pkl  # Model 2 — XGBoost
│   ├── requirements_hf.txt       # HF Space dependencies
│   ├── Dockerfile                # HF Space Docker config
│   ├── test_batch.py             # Live API batch test (both models)
│   └── test_models.py            # Direct pkl evaluation (100 cases)
├── frontend/
│   ├── src/
│   │   ├── App.jsx               # Main app + form + results
│   │   ├── App.css               # Styling
│   │   ├── components/
│   │   │   └── AuthModal.jsx     # Login / signup modal
│   │   └── lib/
│   │       └── supabase.js       # Supabase client
│   ├── .env                      # Vite env vars (not committed)
│   └── package.json
├── AUTH_DB_PLAN.md               # Auth + database implementation plan
└── README.md
```

---

## Features

- Predicts one of three severity classes: `NO_INJURY`, `MINOR`, `SEVERE`
- Per-class confidence percentages via `predict_proba`
- Two models selectable in the UI:
  - **Model 1 — Random Forest**: available to all users, no login required
  - **Model 2 — XGBoost**: requires sign in (unlimited predictions)
- Dynamic safety tips driven by the top risk factor detected in the inputs
- Live risk factor analysis with weighted bars
- Confidence pie chart (shown after prediction)
- Supabase auth — email/password signup and login
- User profiles with `model1_tokens` tracked in Postgres
- Prediction history stored in `predictions` table

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React 18, Vite |
| Backend | FastAPI, Uvicorn |
| ML Models | scikit-learn Random Forest, XGBoost |
| Auth + DB | Supabase (Postgres + Auth) |
| Hosting | Vercel (frontend), Hugging Face Spaces (backend) |
| Containerisation | Docker |

---

## Getting Started

### Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS/Linux

pip install fastapi uvicorn pandas scikit-learn imbalanced-learn xgboost joblib

uvicorn main:app --reload
```

API runs at `http://localhost:8000`

### Frontend

```bash
cd frontend
npm install
npm run dev
```

App runs at `http://localhost:5173`

---

## Environment Variables

### `frontend/.env`
```
VITE_SUPABASE_URL=https://your-project.supabase.co
VITE_SUPABASE_ANON_KEY=eyJ...
VITE_API_URL=https://fede8rma-carcrashai.hf.space
```

### `backend/.env`
```
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_KEY=sb_secret_...
SUPABASE_JWKS_URL=https://your-project.supabase.co/auth/v1/.well-known/jwks.json
```

---

## API

### `POST /predict`

**Request body:**
```json
{
  "weather_condition": "RAIN",
  "lighting_condition": "DARKNESS",
  "roadway_surface_cond": "WET",
  "road_defect": "NO DEFECTS",
  "traffic_control_device": "TRAFFIC SIGNAL",
  "trafficway_type": "NOT DIVIDED",
  "alignment": "STRAIGHT AND LEVEL",
  "intersection_related_i": "Y",
  "first_crash_type": "ANGLE",
  "prim_contributory_cause": "FAILING TO YIELD RIGHT-OF-WAY",
  "damage": "OVER $1,500",
  "num_units": 2,
  "crash_hour": 22,
  "crash_day_of_week": 6,
  "crash_month": 11,
  "model": 2
}
```

**Response:**
```json
{
  "predicted_severity": "MINOR",
  "confidence": {
    "MINOR": 61.3,
    "NO_INJURY": 28.4,
    "SEVERE": 10.3
  },
  "model_used": 2
}
```

---

## Input Fields

| Field | Type | Example values |
|---|---|---|
| `weather_condition` | string | `CLEAR`, `RAIN`, `SNOW`, `FOG/SMOKE/HAZE` |
| `lighting_condition` | string | `DAYLIGHT`, `DARKNESS`, `DUSK`, `DAWN` |
| `roadway_surface_cond` | string | `DRY`, `WET`, `SNOW OR SLUSH`, `ICE` |
| `road_defect` | string | `NO DEFECTS`, `RUT, HOLES`, `CONSTRUCTION` |
| `traffic_control_device` | string | `TRAFFIC SIGNAL`, `STOP SIGN/FLASHER`, `NO CONTROLS` |
| `trafficway_type` | string | `NOT DIVIDED`, `ONE-WAY`, `DIVIDED - W/MEDIAN BARRIER` |
| `alignment` | string | `STRAIGHT AND LEVEL`, `CURVE ON GRADE` |
| `intersection_related_i` | string | `Y` or `N` |
| `first_crash_type` | string | `REAR END`, `ANGLE`, `FIXED OBJECT`, `HEAD ON` |
| `prim_contributory_cause` | string | `FAILING TO YIELD RIGHT-OF-WAY`, `WEATHER` |
| `damage` | string | `OVER $1,500`, `$501 - $1,500`, `$500 OR LESS` |
| `num_units` | int | `1` – `10` |
| `crash_hour` | int | `0` – `23` |
| `crash_day_of_week` | int | `1` (Sun) – `7` (Sat) |
| `crash_month` | int | `1` – `12` |
| `model` | int | `1` (RF) or `2` (XGBoost) |

---

## Database Schema (Supabase)

```sql
-- User profiles (auto-linked to auth.users)
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

## Auth Flow

- **Model 1 (RF)** — available to all visitors, no login required
- **Model 2 (XGBoost)** — clicking it prompts login/signup if not authenticated
- After 5 Model 1 uses, a nudge appears suggesting sign-in for Model 2
- Signup creates a user in Supabase Auth and a profile row with 10 Model 1 tokens
- Sessions are persisted automatically by the Supabase JS client

---

## Testing

### Batch API test (requires backend running)
```bash
cd backend
venv\Scripts\python test_batch.py
```
Tests both models across 40 labelled cases, reports pass/fail and confidence per prediction.

### Direct model evaluation
```bash
cd backend
venv\Scripts\python test_models.py
```
Loads `model_final_rf.pkl` and `model_final_xgboost1.pkl` directly, runs 100 cases, prints accuracy, weighted F1, and classification report for each — ranked by F1.

---

## Deployment

### Frontend → Vercel
1. Push repo to GitHub
2. Import in Vercel, set root to `frontend`
3. Add env vars: `VITE_SUPABASE_URL`, `VITE_SUPABASE_ANON_KEY`, `VITE_API_URL`

### Backend → Hugging Face Spaces
1. Create a new Space (Docker SDK)
2. Push `backend/` contents including both `.pkl` files
3. Add secrets: `SUPABASE_URL`, `SUPABASE_SERVICE_KEY`, `SUPABASE_JWKS_URL`
4. Space builds from `Dockerfile` and exposes port `7860`

---

## UI Color Palette

| Color | Hex | Usage |
|---|---|---|
| Black | `#000000` | Topbar background |
| Navy | `#34435E` | Results panel, cards |
| Amber | `#FFC857` | Accents, button, headings |
| Violet | `#7C3AED` | `.AI` brand accent |
| Green | `#22c55e` | No injury severity |
| Yellow | `#eab308` | Minor severity |
| Red | `#ef4444` | Severe / danger |
| Off-white | `#f5f5f5` | Input panel background |

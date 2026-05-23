# Traffic Accident Severity Predictor

A full-stack ML web app that predicts the injury severity of a traffic accident based on environmental, road, and crash conditions. Built with a React frontend and a FastAPI backend serving a trained Random Forest model.

---

## Project Structure

```
carCrashFata/
├── backend/
│   ├── main.py               # FastAPI app — prediction endpoint
│   ├── model_rf_new.pkl      # Trained Random Forest model
│   ├── requirements.txt      # Python dependencies
│   ├── test_batch.py         # Live API batch test (10 cases via HTTP)
│   └── test_models.py        # Direct model evaluation (100 cases, F1 scoring)
└── frontend/
    ├── src/
    │   ├── App.jsx            # Main React component
    │   └── App.css            # Styling (custom palette)
    ├── index.html
    └── package.json
```

---

## Features

- Predicts one of three severity classes: `NO_INJURY`, `MINOR`, `SEVERE`
- Returns per-class confidence percentages via `predict_proba`
- Dynamic risk factor analysis based on form inputs (lighting, surface, weather, etc.)
- Severity-specific safety tips and messages
- Live confidence bar chart and pie chart
- Split-panel UI — light input panel / dark results panel

---

## Tech Stack

| Layer    | Technology                        |
|----------|-----------------------------------|
| Frontend | React 18, Vite                    |
| Backend  | FastAPI, Uvicorn                  |
| ML Model | scikit-learn Random Forest        |
| Data     | pandas                            |
| Styling  | Plain CSS (custom design system)  |

---

## Getting Started

### 1. Backend

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate

pip install fastapi uvicorn pandas scikit-learn imbalanced-learn

uvicorn main:app --reload
```

API runs at `http://localhost:8000`

---

### 2. Frontend

```bash
cd frontend
npm install
npm run dev
```

App runs at `http://localhost:5173`

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
  "crash_month": 11
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
  }
}
```

---

## Input Fields

| Field                   | Type    | Example values                                      |
|-------------------------|---------|-----------------------------------------------------|
| `weather_condition`     | string  | `CLEAR`, `RAIN`, `SNOW`, `FOG/SMOKE/HAZE`           |
| `lighting_condition`    | string  | `DAYLIGHT`, `DARKNESS`, `DUSK`, `DAWN`              |
| `roadway_surface_cond`  | string  | `DRY`, `WET`, `SNOW OR SLUSH`, `ICE`                |
| `road_defect`           | string  | `NO DEFECTS`, `RUT, HOLES`, `CONSTRUCTION`          |
| `traffic_control_device`| string  | `TRAFFIC SIGNAL`, `STOP SIGN/FLASHER`, `NO CONTROLS`|
| `trafficway_type`       | string  | `NOT DIVIDED`, `ONE-WAY`, `DIVIDED - W/MEDIAN BARRIER` |
| `alignment`             | string  | `STRAIGHT AND LEVEL`, `CURVE ON GRADE`              |
| `intersection_related_i`| string  | `Y` or `N`                                          |
| `first_crash_type`      | string  | `REAR END`, `ANGLE`, `FIXED OBJECT`, `HEAD ON`      |
| `prim_contributory_cause`| string | `FAILING TO YIELD RIGHT-OF-WAY`, `WEATHER`          |
| `damage`                | string  | `OVER $1,500`, `$501 - $1,500`, `$500 OR LESS`      |
| `num_units`             | int     | `1` – `10`                                          |
| `crash_hour`            | int     | `0` – `23`                                          |
| `crash_day_of_week`     | int     | `1` (Sun) – `7` (Sat)                               |
| `crash_month`           | int     | `1` – `12`                                          |

---

## Testing

### Batch API test (requires backend running)

```bash
cd backend
venv\Scripts\python test_batch.py
```

Runs 10 labelled test cases against the live API and reports pass/fail with confidence scores.

### Direct model evaluation

```bash
cd backend
venv\Scripts\python test_models.py
```

Loads all `.pkl` files in the backend folder, runs 100 test cases (40 NO_INJURY, 30 MINOR, 30 SEVERE) directly through each model, and prints accuracy, weighted F1, and a per-class classification report — ranked by F1.

---

## UI Color Palette

| Color     | Hex       | Usage                        |
|-----------|-----------|------------------------------|
| Black     | `#000000` | Topbar background            |
| Navy      | `#34435E` | Results panel, cards         |
| Amber     | `#FFC857` | Accents, button, headings    |
| Mint      | `#ABEBD2` | No-injury indicator          |
| Red       | `#CA3C25` | Severe / danger indicator    |
| Off-white | `#f5f5f5` | Input panel background       |

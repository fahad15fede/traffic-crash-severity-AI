import pickle, os
import pandas as pd
from sklearn.metrics import f1_score, classification_report

# ── 100 test cases ──────────────────────────────────────────────────────────
cases = [
  # NO_INJURY cases (1-40)
  {"w":"CLEAR","l":"DAYLIGHT","s":"DRY","d":"NO DEFECTS","t":"TRAFFIC SIGNAL","tw":"ONE-WAY","a":"STRAIGHT AND LEVEL","i":"N","h":11,"dow":2,"m":6,"y":"NO_INJURY"},
  {"w":"CLEAR","l":"DAYLIGHT","s":"DRY","d":"NO DEFECTS","t":"TRAFFIC SIGNAL","tw":"ONE-WAY","a":"STRAIGHT AND LEVEL","i":"N","h":15,"dow":3,"m":4,"y":"NO_INJURY"},
  {"w":"CLEAR","l":"DAYLIGHT","s":"DRY","d":"NO DEFECTS","t":"TRAFFIC SIGNAL","tw":"DIVIDED - W/MEDIAN BARRIER","a":"STRAIGHT AND LEVEL","i":"Y","h":13,"dow":4,"m":5,"y":"NO_INJURY"},
  {"w":"CLEAR","l":"DAYLIGHT","s":"DRY","d":"NO DEFECTS","t":"TRAFFIC SIGNAL","tw":"NOT DIVIDED","a":"STRAIGHT AND LEVEL","i":"N","h":9,"dow":2,"m":3,"y":"NO_INJURY"},
  {"w":"CLEAR","l":"DAYLIGHT","s":"DRY","d":"NO DEFECTS","t":"STOP SIGN/FLASHER","tw":"ONE-WAY","a":"STRAIGHT AND LEVEL","i":"N","h":10,"dow":3,"m":7,"y":"NO_INJURY"},
  {"w":"CLEAR","l":"DAYLIGHT","s":"DRY","d":"NO DEFECTS","t":"TRAFFIC SIGNAL","tw":"NOT DIVIDED","a":"STRAIGHT ON GRADE","i":"N","h":14,"dow":4,"m":8,"y":"NO_INJURY"},
  {"w":"CLEAR","l":"DAYLIGHT","s":"DRY","d":"NO DEFECTS","t":"YIELD","tw":"ONE-WAY","a":"STRAIGHT AND LEVEL","i":"N","h":16,"dow":5,"m":6,"y":"NO_INJURY"},
  {"w":"CLEAR","l":"DAYLIGHT","s":"DRY","d":"NO DEFECTS","t":"TRAFFIC SIGNAL","tw":"DIVIDED - W/MEDIAN BARRIER","a":"STRAIGHT AND LEVEL","i":"N","h":8,"dow":1,"m":5,"y":"NO_INJURY"},
  {"w":"CLEAR","l":"DAYLIGHT","s":"DRY","d":"NO DEFECTS","t":"TRAFFIC SIGNAL","tw":"ONE-WAY","a":"STRAIGHT AND LEVEL","i":"Y","h":12,"dow":3,"m":9,"y":"NO_INJURY"},
  {"w":"CLEAR","l":"DAYLIGHT","s":"DRY","d":"NO DEFECTS","t":"STOP SIGN/FLASHER","tw":"NOT DIVIDED","a":"STRAIGHT AND LEVEL","i":"N","h":17,"dow":2,"m":4,"y":"NO_INJURY"},
  {"w":"CLEAR","l":"DAYLIGHT","s":"DRY","d":"NO DEFECTS","t":"TRAFFIC SIGNAL","tw":"ONE-WAY","a":"STRAIGHT AND LEVEL","i":"N","h":7,"dow":4,"m":6,"y":"NO_INJURY"},
  {"w":"CLEAR","l":"DAYLIGHT","s":"DRY","d":"NO DEFECTS","t":"TRAFFIC SIGNAL","tw":"DIVIDED - W/MEDIAN BARRIER","a":"STRAIGHT ON GRADE","i":"N","h":11,"dow":5,"m":7,"y":"NO_INJURY"},
  {"w":"CLEAR","l":"DAYLIGHT","s":"DRY","d":"NO DEFECTS","t":"TRAFFIC SIGNAL","tw":"NOT DIVIDED","a":"STRAIGHT AND LEVEL","i":"Y","h":10,"dow":1,"m":8,"y":"NO_INJURY"},
  {"w":"CLEAR","l":"DAYLIGHT","s":"DRY","d":"NO DEFECTS","t":"YIELD","tw":"ONE-WAY","a":"STRAIGHT AND LEVEL","i":"N","h":13,"dow":2,"m":5,"y":"NO_INJURY"},
  {"w":"CLEAR","l":"DAYLIGHT","s":"DRY","d":"NO DEFECTS","t":"TRAFFIC SIGNAL","tw":"ONE-WAY","a":"STRAIGHT AND LEVEL","i":"N","h":15,"dow":6,"m":3,"y":"NO_INJURY"},
  {"w":"CLEAR","l":"DAYLIGHT","s":"DRY","d":"NO DEFECTS","t":"TRAFFIC SIGNAL","tw":"NOT DIVIDED","a":"STRAIGHT AND LEVEL","i":"N","h":9,"dow":3,"m":6,"y":"NO_INJURY"},
  {"w":"CLEAR","l":"DAYLIGHT","s":"DRY","d":"NO DEFECTS","t":"STOP SIGN/FLASHER","tw":"DIVIDED - W/MEDIAN BARRIER","a":"STRAIGHT AND LEVEL","i":"N","h":14,"dow":4,"m":4,"y":"NO_INJURY"},
  {"w":"CLEAR","l":"DAYLIGHT","s":"DRY","d":"NO DEFECTS","t":"TRAFFIC SIGNAL","tw":"ONE-WAY","a":"STRAIGHT ON GRADE","i":"N","h":16,"dow":2,"m":7,"y":"NO_INJURY"},
  {"w":"CLEAR","l":"DAYLIGHT","s":"DRY","d":"NO DEFECTS","t":"TRAFFIC SIGNAL","tw":"NOT DIVIDED","a":"STRAIGHT AND LEVEL","i":"Y","h":11,"dow":5,"m":5,"y":"NO_INJURY"},
  {"w":"CLEAR","l":"DAYLIGHT","s":"DRY","d":"NO DEFECTS","t":"TRAFFIC SIGNAL","tw":"ONE-WAY","a":"STRAIGHT AND LEVEL","i":"N","h":8,"dow":3,"m":9,"y":"NO_INJURY"},
  {"w":"CLEAR","l":"DAYLIGHT","s":"DRY","d":"NO DEFECTS","t":"TRAFFIC SIGNAL","tw":"DIVIDED - W/MEDIAN BARRIER","a":"STRAIGHT AND LEVEL","i":"N","h":10,"dow":1,"m":6,"y":"NO_INJURY"},
  {"w":"CLEAR","l":"DAYLIGHT","s":"DRY","d":"NO DEFECTS","t":"YIELD","tw":"NOT DIVIDED","a":"STRAIGHT AND LEVEL","i":"N","h":12,"dow":4,"m":8,"y":"NO_INJURY"},
  {"w":"CLEAR","l":"DAYLIGHT","s":"DRY","d":"NO DEFECTS","t":"TRAFFIC SIGNAL","tw":"ONE-WAY","a":"STRAIGHT AND LEVEL","i":"Y","h":14,"dow":2,"m":4,"y":"NO_INJURY"},
  {"w":"CLEAR","l":"DAYLIGHT","s":"DRY","d":"NO DEFECTS","t":"STOP SIGN/FLASHER","tw":"ONE-WAY","a":"STRAIGHT ON GRADE","i":"N","h":9,"dow":5,"m":7,"y":"NO_INJURY"},
  {"w":"CLEAR","l":"DAYLIGHT","s":"DRY","d":"NO DEFECTS","t":"TRAFFIC SIGNAL","tw":"NOT DIVIDED","a":"STRAIGHT AND LEVEL","i":"N","h":15,"dow":3,"m":5,"y":"NO_INJURY"},
  {"w":"CLEAR","l":"DAYLIGHT","s":"DRY","d":"NO DEFECTS","t":"TRAFFIC SIGNAL","tw":"DIVIDED - W/MEDIAN BARRIER","a":"STRAIGHT AND LEVEL","i":"N","h":11,"dow":6,"m":3,"y":"NO_INJURY"},
  {"w":"CLEAR","l":"DAYLIGHT","s":"DRY","d":"NO DEFECTS","t":"TRAFFIC SIGNAL","tw":"ONE-WAY","a":"STRAIGHT AND LEVEL","i":"N","h":13,"dow":4,"m":6,"y":"NO_INJURY"},
  {"w":"CLEAR","l":"DAYLIGHT","s":"DRY","d":"NO DEFECTS","t":"YIELD","tw":"ONE-WAY","a":"STRAIGHT AND LEVEL","i":"Y","h":10,"dow":2,"m":9,"y":"NO_INJURY"},
  {"w":"CLEAR","l":"DAYLIGHT","s":"DRY","d":"NO DEFECTS","t":"TRAFFIC SIGNAL","tw":"NOT DIVIDED","a":"STRAIGHT ON GRADE","i":"N","h":16,"dow":1,"m":4,"y":"NO_INJURY"},
  {"w":"CLEAR","l":"DAYLIGHT","s":"DRY","d":"NO DEFECTS","t":"TRAFFIC SIGNAL","tw":"ONE-WAY","a":"STRAIGHT AND LEVEL","i":"N","h":8,"dow":5,"m":7,"y":"NO_INJURY"},
  {"w":"CLEAR","l":"DAYLIGHT","s":"DRY","d":"NO DEFECTS","t":"STOP SIGN/FLASHER","tw":"DIVIDED - W/MEDIAN BARRIER","a":"STRAIGHT AND LEVEL","i":"N","h":12,"dow":3,"m":5,"y":"NO_INJURY"},
  {"w":"CLEAR","l":"DAYLIGHT","s":"DRY","d":"NO DEFECTS","t":"TRAFFIC SIGNAL","tw":"ONE-WAY","a":"STRAIGHT AND LEVEL","i":"Y","h":14,"dow":4,"m":6,"y":"NO_INJURY"},
  {"w":"CLEAR","l":"DAYLIGHT","s":"DRY","d":"NO DEFECTS","t":"TRAFFIC SIGNAL","tw":"NOT DIVIDED","a":"STRAIGHT AND LEVEL","i":"N","h":9,"dow":2,"m":8,"y":"NO_INJURY"},
  {"w":"CLEAR","l":"DAYLIGHT","s":"DRY","d":"NO DEFECTS","t":"YIELD","tw":"ONE-WAY","a":"STRAIGHT AND LEVEL","i":"N","h":11,"dow":6,"m":3,"y":"NO_INJURY"},
  {"w":"CLEAR","l":"DAYLIGHT","s":"DRY","d":"NO DEFECTS","t":"TRAFFIC SIGNAL","tw":"DIVIDED - W/MEDIAN BARRIER","a":"STRAIGHT ON GRADE","i":"N","h":15,"dow":1,"m":5,"y":"NO_INJURY"},
  {"w":"CLEAR","l":"DAYLIGHT","s":"DRY","d":"NO DEFECTS","t":"TRAFFIC SIGNAL","tw":"ONE-WAY","a":"STRAIGHT AND LEVEL","i":"N","h":10,"dow":3,"m":7,"y":"NO_INJURY"},
  {"w":"CLEAR","l":"DAYLIGHT","s":"DRY","d":"NO DEFECTS","t":"STOP SIGN/FLASHER","tw":"NOT DIVIDED","a":"STRAIGHT AND LEVEL","i":"Y","h":13,"dow":5,"m":4,"y":"NO_INJURY"},
  {"w":"CLEAR","l":"DAYLIGHT","s":"DRY","d":"NO DEFECTS","t":"TRAFFIC SIGNAL","tw":"ONE-WAY","a":"STRAIGHT AND LEVEL","i":"N","h":16,"dow":2,"m":6,"y":"NO_INJURY"},
  {"w":"CLEAR","l":"DAYLIGHT","s":"DRY","d":"NO DEFECTS","t":"TRAFFIC SIGNAL","tw":"DIVIDED - W/MEDIAN BARRIER","a":"STRAIGHT AND LEVEL","i":"N","h":8,"dow":4,"m":9,"y":"NO_INJURY"},
  {"w":"CLEAR","l":"DAYLIGHT","s":"DRY","d":"NO DEFECTS","t":"YIELD","tw":"NOT DIVIDED","a":"STRAIGHT AND LEVEL","i":"N","h":12,"dow":3,"m":5,"y":"NO_INJURY"},
  {"w":"CLEAR","l":"DAYLIGHT","s":"DRY","d":"NO DEFECTS","t":"TRAFFIC SIGNAL","tw":"ONE-WAY","a":"STRAIGHT AND LEVEL","i":"Y","h":14,"dow":1,"m":7,"y":"NO_INJURY"},
  # MINOR cases (41-70)
  {"w":"RAIN","l":"DARKNESS","s":"WET","d":"NO DEFECTS","t":"STOP SIGN/FLASHER","tw":"NOT DIVIDED","a":"STRAIGHT AND LEVEL","i":"Y","h":22,"dow":6,"m":11,"y":"MINOR"},
  {"w":"FOG/SMOKE/HAZE","l":"DAWN","s":"WET","d":"NO DEFECTS","t":"TRAFFIC SIGNAL","tw":"DIVIDED - W/MEDIAN BARRIER","a":"STRAIGHT AND LEVEL","i":"Y","h":7,"dow":1,"m":10,"y":"MINOR"},
  {"w":"RAIN","l":"DARKNESS, LIGHTED ROAD","s":"WET","d":"NO DEFECTS","t":"TRAFFIC SIGNAL","tw":"NOT DIVIDED","a":"STRAIGHT AND LEVEL","i":"Y","h":21,"dow":6,"m":9,"y":"MINOR"},
  {"w":"RAIN","l":"DUSK","s":"WET","d":"NO DEFECTS","t":"TRAFFIC SIGNAL","tw":"NOT DIVIDED","a":"STRAIGHT AND LEVEL","i":"Y","h":19,"dow":5,"m":10,"y":"MINOR"},
  {"w":"CLOUDY/OVERCAST","l":"DARKNESS, LIGHTED ROAD","s":"WET","d":"NO DEFECTS","t":"TRAFFIC SIGNAL","tw":"NOT DIVIDED","a":"STRAIGHT AND LEVEL","i":"Y","h":20,"dow":4,"m":11,"y":"MINOR"},
  {"w":"RAIN","l":"DARKNESS","s":"WET","d":"NO DEFECTS","t":"STOP SIGN/FLASHER","tw":"NOT DIVIDED","a":"STRAIGHT AND LEVEL","i":"N","h":23,"dow":5,"m":10,"y":"MINOR"},
  {"w":"FOG/SMOKE/HAZE","l":"DARKNESS, LIGHTED ROAD","s":"WET","d":"NO DEFECTS","t":"TRAFFIC SIGNAL","tw":"NOT DIVIDED","a":"STRAIGHT AND LEVEL","i":"Y","h":6,"dow":2,"m":11,"y":"MINOR"},
  {"w":"RAIN","l":"DUSK","s":"WET","d":"NO DEFECTS","t":"TRAFFIC SIGNAL","tw":"DIVIDED - W/MEDIAN BARRIER","a":"STRAIGHT AND LEVEL","i":"N","h":18,"dow":3,"m":9,"y":"MINOR"},
  {"w":"CLOUDY/OVERCAST","l":"DARKNESS","s":"WET","d":"NO DEFECTS","t":"STOP SIGN/FLASHER","tw":"NOT DIVIDED","a":"STRAIGHT AND LEVEL","i":"Y","h":21,"dow":6,"m":10,"y":"MINOR"},
  {"w":"RAIN","l":"DARKNESS, LIGHTED ROAD","s":"WET","d":"NO DEFECTS","t":"TRAFFIC SIGNAL","tw":"NOT DIVIDED","a":"STRAIGHT ON GRADE","i":"Y","h":20,"dow":5,"m":11,"y":"MINOR"},
  {"w":"FOG/SMOKE/HAZE","l":"DAWN","s":"WET","d":"NO DEFECTS","t":"TRAFFIC SIGNAL","tw":"NOT DIVIDED","a":"STRAIGHT AND LEVEL","i":"N","h":7,"dow":1,"m":9,"y":"MINOR"},
  {"w":"RAIN","l":"DARKNESS","s":"WET","d":"NO DEFECTS","t":"TRAFFIC SIGNAL","tw":"DIVIDED - W/MEDIAN BARRIER","a":"STRAIGHT AND LEVEL","i":"Y","h":22,"dow":4,"m":10,"y":"MINOR"},
  {"w":"CLOUDY/OVERCAST","l":"DUSK","s":"WET","d":"NO DEFECTS","t":"STOP SIGN/FLASHER","tw":"NOT DIVIDED","a":"STRAIGHT AND LEVEL","i":"N","h":19,"dow":3,"m":11,"y":"MINOR"},
  {"w":"RAIN","l":"DARKNESS, LIGHTED ROAD","s":"WET","d":"NO DEFECTS","t":"TRAFFIC SIGNAL","tw":"NOT DIVIDED","a":"STRAIGHT AND LEVEL","i":"Y","h":21,"dow":6,"m":9,"y":"MINOR"},
  {"w":"FOG/SMOKE/HAZE","l":"DARKNESS","s":"WET","d":"NO DEFECTS","t":"TRAFFIC SIGNAL","tw":"NOT DIVIDED","a":"STRAIGHT AND LEVEL","i":"Y","h":6,"dow":2,"m":10,"y":"MINOR"},
  {"w":"RAIN","l":"DUSK","s":"WET","d":"NO DEFECTS","t":"STOP SIGN/FLASHER","tw":"DIVIDED - W/MEDIAN BARRIER","a":"STRAIGHT AND LEVEL","i":"N","h":18,"dow":5,"m":11,"y":"MINOR"},
  {"w":"CLOUDY/OVERCAST","l":"DARKNESS, LIGHTED ROAD","s":"WET","d":"NO DEFECTS","t":"TRAFFIC SIGNAL","tw":"NOT DIVIDED","a":"STRAIGHT ON GRADE","i":"Y","h":20,"dow":4,"m":9,"y":"MINOR"},
  {"w":"RAIN","l":"DARKNESS","s":"WET","d":"NO DEFECTS","t":"TRAFFIC SIGNAL","tw":"NOT DIVIDED","a":"STRAIGHT AND LEVEL","i":"N","h":23,"dow":3,"m":10,"y":"MINOR"},
  {"w":"FOG/SMOKE/HAZE","l":"DAWN","s":"WET","d":"NO DEFECTS","t":"STOP SIGN/FLASHER","tw":"NOT DIVIDED","a":"STRAIGHT AND LEVEL","i":"Y","h":7,"dow":1,"m":11,"y":"MINOR"},
  {"w":"RAIN","l":"DARKNESS, LIGHTED ROAD","s":"WET","d":"NO DEFECTS","t":"TRAFFIC SIGNAL","tw":"DIVIDED - W/MEDIAN BARRIER","a":"STRAIGHT AND LEVEL","i":"Y","h":21,"dow":6,"m":9,"y":"MINOR"},
  {"w":"CLOUDY/OVERCAST","l":"DARKNESS","s":"WET","d":"NO DEFECTS","t":"TRAFFIC SIGNAL","tw":"NOT DIVIDED","a":"STRAIGHT AND LEVEL","i":"N","h":22,"dow":5,"m":10,"y":"MINOR"},
  {"w":"RAIN","l":"DUSK","s":"WET","d":"NO DEFECTS","t":"TRAFFIC SIGNAL","tw":"NOT DIVIDED","a":"STRAIGHT AND LEVEL","i":"Y","h":19,"dow":4,"m":11,"y":"MINOR"},
  {"w":"FOG/SMOKE/HAZE","l":"DARKNESS, LIGHTED ROAD","s":"WET","d":"NO DEFECTS","t":"STOP SIGN/FLASHER","tw":"NOT DIVIDED","a":"STRAIGHT AND LEVEL","i":"N","h":6,"dow":2,"m":9,"y":"MINOR"},
  {"w":"RAIN","l":"DARKNESS","s":"WET","d":"NO DEFECTS","t":"TRAFFIC SIGNAL","tw":"DIVIDED - W/MEDIAN BARRIER","a":"STRAIGHT ON GRADE","i":"Y","h":20,"dow":3,"m":10,"y":"MINOR"},
  {"w":"CLOUDY/OVERCAST","l":"DUSK","s":"WET","d":"NO DEFECTS","t":"TRAFFIC SIGNAL","tw":"NOT DIVIDED","a":"STRAIGHT AND LEVEL","i":"Y","h":18,"dow":6,"m":11,"y":"MINOR"},
  {"w":"RAIN","l":"DARKNESS, LIGHTED ROAD","s":"WET","d":"NO DEFECTS","t":"STOP SIGN/FLASHER","tw":"NOT DIVIDED","a":"STRAIGHT AND LEVEL","i":"N","h":21,"dow":5,"m":9,"y":"MINOR"},
  {"w":"FOG/SMOKE/HAZE","l":"DAWN","s":"WET","d":"NO DEFECTS","t":"TRAFFIC SIGNAL","tw":"NOT DIVIDED","a":"STRAIGHT AND LEVEL","i":"Y","h":7,"dow":1,"m":10,"y":"MINOR"},
  {"w":"RAIN","l":"DARKNESS","s":"WET","d":"NO DEFECTS","t":"TRAFFIC SIGNAL","tw":"NOT DIVIDED","a":"STRAIGHT AND LEVEL","i":"Y","h":22,"dow":4,"m":11,"y":"MINOR"},
  {"w":"CLOUDY/OVERCAST","l":"DARKNESS, LIGHTED ROAD","s":"WET","d":"NO DEFECTS","t":"TRAFFIC SIGNAL","tw":"DIVIDED - W/MEDIAN BARRIER","a":"STRAIGHT AND LEVEL","i":"N","h":20,"dow":3,"m":9,"y":"MINOR"},
  {"w":"RAIN","l":"DUSK","s":"WET","d":"NO DEFECTS","t":"STOP SIGN/FLASHER","tw":"NOT DIVIDED","a":"STRAIGHT AND LEVEL","i":"Y","h":19,"dow":2,"m":10,"y":"MINOR"},
  # SEVERE cases (71-100)
  {"w":"SNOW","l":"DARKNESS","s":"SNOW OR SLUSH","d":"RUT, HOLES","t":"NO CONTROLS","tw":"NOT DIVIDED","a":"CURVE ON GRADE","i":"N","h":2,"dow":7,"m":1,"y":"SEVERE"},
  {"w":"FREEZING RAIN/DRIZZLE","l":"DARKNESS","s":"ICE","d":"OTHER","t":"NO CONTROLS","tw":"NOT DIVIDED","a":"CURVE ON HILLCREST","i":"N","h":1,"dow":5,"m":12,"y":"SEVERE"},
  {"w":"RAIN","l":"DARKNESS","s":"WET","d":"OTHER","t":"NO CONTROLS","tw":"NOT DIVIDED","a":"CURVE ON GRADE","i":"N","h":0,"dow":6,"m":8,"y":"SEVERE"},
  {"w":"SNOW","l":"DARKNESS","s":"ICE","d":"RUT, HOLES","t":"NO CONTROLS","tw":"NOT DIVIDED","a":"CURVE ON GRADE","i":"N","h":3,"dow":7,"m":1,"y":"SEVERE"},
  {"w":"FREEZING RAIN/DRIZZLE","l":"DARKNESS","s":"ICE","d":"RUT, HOLES","t":"NO CONTROLS","tw":"NOT DIVIDED","a":"CURVE ON HILLCREST","i":"N","h":2,"dow":6,"m":12,"y":"SEVERE"},
  {"w":"SNOW","l":"DARKNESS","s":"SNOW OR SLUSH","d":"OTHER","t":"NO CONTROLS","tw":"NOT DIVIDED","a":"CURVE ON GRADE","i":"N","h":1,"dow":7,"m":2,"y":"SEVERE"},
  {"w":"RAIN","l":"DARKNESS","s":"WET","d":"RUT, HOLES","t":"NO CONTROLS","tw":"NOT DIVIDED","a":"CURVE ON GRADE","i":"N","h":23,"dow":5,"m":11,"y":"SEVERE"},
  {"w":"FREEZING RAIN/DRIZZLE","l":"DARKNESS","s":"ICE","d":"OTHER","t":"NO CONTROLS","tw":"NOT DIVIDED","a":"CURVE ON GRADE","i":"N","h":3,"dow":6,"m":1,"y":"SEVERE"},
  {"w":"SNOW","l":"DARKNESS","s":"ICE","d":"RUT, HOLES","t":"NO CONTROLS","tw":"NOT DIVIDED","a":"CURVE ON HILLCREST","i":"N","h":2,"dow":7,"m":12,"y":"SEVERE"},
  {"w":"RAIN","l":"DARKNESS","s":"WET","d":"OTHER","t":"NO CONTROLS","tw":"NOT DIVIDED","a":"CURVE ON GRADE","i":"N","h":1,"dow":5,"m":8,"y":"SEVERE"},
  {"w":"FREEZING RAIN/DRIZZLE","l":"DARKNESS","s":"SNOW OR SLUSH","d":"RUT, HOLES","t":"NO CONTROLS","tw":"NOT DIVIDED","a":"CURVE ON GRADE","i":"N","h":0,"dow":6,"m":12,"y":"SEVERE"},
  {"w":"SNOW","l":"DARKNESS","s":"ICE","d":"OTHER","t":"NO CONTROLS","tw":"NOT DIVIDED","a":"CURVE ON GRADE","i":"N","h":3,"dow":7,"m":1,"y":"SEVERE"},
  {"w":"RAIN","l":"DARKNESS","s":"WET","d":"RUT, HOLES","t":"NO CONTROLS","tw":"NOT DIVIDED","a":"CURVE ON HILLCREST","i":"N","h":2,"dow":5,"m":11,"y":"SEVERE"},
  {"w":"FREEZING RAIN/DRIZZLE","l":"DARKNESS","s":"ICE","d":"OTHER","t":"NO CONTROLS","tw":"NOT DIVIDED","a":"CURVE ON GRADE","i":"N","h":1,"dow":6,"m":12,"y":"SEVERE"},
  {"w":"SNOW","l":"DARKNESS","s":"SNOW OR SLUSH","d":"RUT, HOLES","t":"NO CONTROLS","tw":"NOT DIVIDED","a":"CURVE ON GRADE","i":"N","h":23,"dow":7,"m":2,"y":"SEVERE"},
  {"w":"RAIN","l":"DARKNESS","s":"WET","d":"OTHER","t":"NO CONTROLS","tw":"NOT DIVIDED","a":"CURVE ON GRADE","i":"N","h":3,"dow":5,"m":8,"y":"SEVERE"},
  {"w":"FREEZING RAIN/DRIZZLE","l":"DARKNESS","s":"ICE","d":"RUT, HOLES","t":"NO CONTROLS","tw":"NOT DIVIDED","a":"CURVE ON HILLCREST","i":"N","h":0,"dow":6,"m":1,"y":"SEVERE"},
  {"w":"SNOW","l":"DARKNESS","s":"ICE","d":"OTHER","t":"NO CONTROLS","tw":"NOT DIVIDED","a":"CURVE ON GRADE","i":"N","h":2,"dow":7,"m":12,"y":"SEVERE"},
  {"w":"RAIN","l":"DARKNESS","s":"WET","d":"RUT, HOLES","t":"NO CONTROLS","tw":"NOT DIVIDED","a":"CURVE ON GRADE","i":"N","h":1,"dow":5,"m":11,"y":"SEVERE"},
  {"w":"FREEZING RAIN/DRIZZLE","l":"DARKNESS","s":"SNOW OR SLUSH","d":"OTHER","t":"NO CONTROLS","tw":"NOT DIVIDED","a":"CURVE ON GRADE","i":"N","h":3,"dow":6,"m":12,"y":"SEVERE"},
  {"w":"SNOW","l":"DARKNESS","s":"ICE","d":"RUT, HOLES","t":"NO CONTROLS","tw":"NOT DIVIDED","a":"CURVE ON GRADE","i":"N","h":0,"dow":7,"m":1,"y":"SEVERE"},
  {"w":"RAIN","l":"DARKNESS","s":"WET","d":"OTHER","t":"NO CONTROLS","tw":"NOT DIVIDED","a":"CURVE ON HILLCREST","i":"N","h":2,"dow":5,"m":8,"y":"SEVERE"},
  {"w":"FREEZING RAIN/DRIZZLE","l":"DARKNESS","s":"ICE","d":"RUT, HOLES","t":"NO CONTROLS","tw":"NOT DIVIDED","a":"CURVE ON GRADE","i":"N","h":1,"dow":6,"m":12,"y":"SEVERE"},
  {"w":"SNOW","l":"DARKNESS","s":"SNOW OR SLUSH","d":"OTHER","t":"NO CONTROLS","tw":"NOT DIVIDED","a":"CURVE ON HILLCREST","i":"N","h":3,"dow":7,"m":2,"y":"SEVERE"},
  {"w":"RAIN","l":"DARKNESS","s":"WET","d":"RUT, HOLES","t":"NO CONTROLS","tw":"NOT DIVIDED","a":"CURVE ON GRADE","i":"N","h":23,"dow":5,"m":11,"y":"SEVERE"},
  {"w":"FREEZING RAIN/DRIZZLE","l":"DARKNESS","s":"ICE","d":"OTHER","t":"NO CONTROLS","tw":"NOT DIVIDED","a":"CURVE ON GRADE","i":"N","h":0,"dow":6,"m":1,"y":"SEVERE"},
  {"w":"SNOW","l":"DARKNESS","s":"ICE","d":"RUT, HOLES","t":"NO CONTROLS","tw":"NOT DIVIDED","a":"CURVE ON GRADE","i":"N","h":2,"dow":7,"m":12,"y":"SEVERE"},
  {"w":"RAIN","l":"DARKNESS","s":"WET","d":"OTHER","t":"NO CONTROLS","tw":"NOT DIVIDED","a":"CURVE ON GRADE","i":"N","h":1,"dow":5,"m":8,"y":"SEVERE"},
  {"w":"FREEZING RAIN/DRIZZLE","l":"DARKNESS","s":"SNOW OR SLUSH","d":"RUT, HOLES","t":"NO CONTROLS","tw":"NOT DIVIDED","a":"CURVE ON HILLCREST","i":"N","h":3,"dow":6,"m":12,"y":"SEVERE"},
  {"w":"SNOW","l":"DARKNESS","s":"ICE","d":"OTHER","t":"NO CONTROLS","tw":"NOT DIVIDED","a":"CURVE ON GRADE","i":"N","h":0,"dow":7,"m":1,"y":"SEVERE"},
]

# ── Build DataFrame ─────────────────────────────────────────────────────────
def build_df(cases):
    rows = []
    for c in cases:
        rows.append({
            "weather_condition":      c["w"],
            "lighting_condition":     c["l"],
            "roadway_surface_cond":   c["s"],
            "road_defect":            c["d"],
            "traffic_control_device": c["t"],
            "trafficway_type":        c["tw"],
            "alignment":              c["a"],
            "intersection_related_i": c["i"],
            "first_crash_type":       c.get("fc", "REAR END"),
            "prim_contributory_cause":c.get("pc", "FAILING TO YIELD RIGHT-OF-WAY"),
            "damage":                 c.get("dmg", "OVER $1,500"),
            "num_units":              c.get("nu", 2),
            "crash_hour":             c["h"],
            "crash_day_of_week":      c["dow"],
            "crash_month":            c["m"],
        })
    return pd.DataFrame(rows)

X = build_df(cases)
y_true = [c["y"] for c in cases]

# ── Models to test ───────────────────────────────────────────────────────────
MODEL_FILES = [
    "model3.pkl",
    "model4.pkl",
    "model_rf3_smote.pkl",
    "model_rf4.pkl",
    "model_knn_smote.pkl",
    "model_svm_smote.pkl",
    "model_svm.pkl",
]

# ── Run ──────────────────────────────────────────────────────────────────────
print(f"\n{'='*65}")
print(f"  BATCH TEST  —  {len(cases)} cases  |  {len(MODEL_FILES)} models")
print(f"{'='*65}")

results = []

for fname in MODEL_FILES:
    if not os.path.exists(fname):
        print(f"\n[SKIP] {fname} — file not found")
        continue
    try:
        with open(fname, "rb") as f:
            model = pickle.load(f)
        y_pred = model.predict(X)
        f1 = f1_score(y_true, y_pred, average="weighted", zero_division=0)
        results.append((fname, f1, y_pred))

        correct = sum(p == t for p, t in zip(y_pred, y_true))
        print(f"\n── {fname}")
        print(f"   Accuracy : {correct}/{len(cases)}  ({correct/len(cases)*100:.1f}%)")
        print(f"   F1 (weighted): {f1:.4f}")
        print(classification_report(y_true, y_pred, zero_division=0, digits=3))
    except Exception as e:
        print(f"\n[ERROR] {fname}: {e}")

# ── Summary ranking ──────────────────────────────────────────────────────────
if results:
    results.sort(key=lambda x: x[1], reverse=True)
    print(f"\n{'='*65}")
    print("  RANKING by weighted F1")
    print(f"{'='*65}")
    for rank, (fname, f1, _) in enumerate(results, 1):
        print(f"  {rank}. {fname:<35} F1 = {f1:.4f}")
    print(f"\n  Best model: {results[0][0]}")
    print(f"{'='*65}\n")

import "./App.css";
import { useState } from "react";

const API = import.meta.env.VITE_API_URL || "https://fede8rma-carcrashai.hf.space";

// ── Severity tips ────────────────────────────────────────────────────────────
const TIPS = {
  NO_INJURY: {
    headline: "Low Risk — Drive Safely",
    color: "#ABEBD2",
    icon: "✓",
    tips: [
      "Conditions look favourable — stay alert and maintain safe following distance.",
      "Even in low-risk scenarios, avoid distractions and keep to speed limits.",
      "Check mirrors regularly and signal early at intersections.",
    ],
  },
  MINOR: {
    headline: "Moderate Risk — Stay Cautious",
    color: "#FFC857",
    icon: "⚠",
    tips: [
      "Reduce speed — conditions increase stopping distance.",
      "Increase following distance to at least 4 seconds in wet or low-light conditions.",
      "Avoid sudden lane changes and use headlights if visibility is reduced.",
    ],
  },
  SEVERE: {
    headline: "High Risk — Extreme Caution",
    color: "#CA3C25",
    icon: "✕",
    tips: [
      "Consider delaying travel — current conditions are dangerous.",
      "If driving is necessary, reduce speed significantly and use hazard lights.",
      "Stay on main roads, avoid curves and grades, and never drive on ice without winter tyres.",
    ],
  },
};

// ── Risk factor logic ────────────────────────────────────────────────────────
function getRiskFactors(form, confidence) {
  const risks = [];

  if (["DARKNESS", "DUSK", "DAWN"].includes(form.lighting_condition))
    risks.push({ label: "Poor Lighting", weight: 85, color: "#CA3C25" });

  if (["WET", "SNOW OR SLUSH", "ICE"].includes(form.roadway_surface_cond))
    risks.push({ label: "Hazardous Surface", weight: 78, color: "#CA3C25" });

  if (["SNOW", "FREEZING RAIN/DRIZZLE", "FOG/SMOKE/HAZE"].includes(form.weather_condition))
    risks.push({ label: "Adverse Weather", weight: 72, color: "#FFC857" });

  if (form.intersection_related_i === "Y")
    risks.push({ label: "Intersection", weight: 60, color: "#FFC857" });

  if (["RUT, HOLES", "CONSTRUCTION", "WORN SURFACE", "OTHER"].includes(form.road_defect))
    risks.push({ label: "Road Defects", weight: 55, color: "#FFC857" });

  if (form.traffic_control_device === "NO CONTROLS")
    risks.push({ label: "No Traffic Control", weight: 65, color: "#CA3C25" });

  if (["CURVE ON GRADE", "CURVE ON HILLCREST", "CURVE, LEVEL"].includes(form.alignment))
    risks.push({ label: "Curved Road", weight: 50, color: "#FFC857" });

  if (["HEAD ON", "FIXED OBJECT", "PEDESTRIAN"].includes(form.first_crash_type))
    risks.push({ label: "High-Impact Crash Type", weight: 90, color: "#CA3C25" });

  if (form.num_units >= 3)
    risks.push({ label: "Multi-Vehicle Crash", weight: 68, color: "#FFC857" });

  if (form.crash_hour >= 22 || form.crash_hour <= 4)
    risks.push({ label: "Late Night Hours", weight: 58, color: "#FFC857" });

  // sort by weight desc, take top 4
  return risks.sort((a, b) => b.weight - a.weight).slice(0, 4);
}


export default function App() {
  const now = new Date();

  const [form, setForm] = useState({
    weather_condition: "",
    lighting_condition: "",
    roadway_surface_cond: "",
    road_defect: "",
    traffic_control_device: "",
    trafficway_type: "",
    alignment: "",
    intersection_related_i: "N",
    first_crash_type: "",
    prim_contributory_cause: "",
    damage: "",
    num_units: 1,
    crash_hour: 12,
    crash_day_of_week: now.getDay() + 1,
    crash_month: now.getMonth() + 1,
  });

  const [prediction, setPrediction] = useState(null);
  const [confidence, setConfidence] = useState({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const set = (key, val) => setForm(f => ({ ...f, [key]: val }));

  // returns className for a select based on whether it has a value
  const sel = (key) => form[key] ? "select-done" : "select-empty";

  const handlePredict = async () => {
    // basic validation
    const required = [
      "weather_condition", "lighting_condition", "roadway_surface_cond",
      "road_defect", "traffic_control_device", "trafficway_type", "alignment",
      "first_crash_type", "prim_contributory_cause", "damage"
    ];
    if (required.some(k => !form[k])) {
      setError("Please fill in all fields before predicting.");
      return;
    }

    setLoading(true);
    setError(null);
    setPrediction(null);

    try {
      const res = await fetch(`${API}/predict`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ ...form, crash_hour: Number(form.crash_hour) }),
      });

      if (!res.ok) throw new Error(`Server error: ${res.status}`);

      const data = await res.json();
      setPrediction(data.predicted_severity);
      setConfidence(data.confidence ?? {});
    } catch (err) {
      setError(err.message || "Failed to reach the prediction server.");
    } finally {
      setLoading(false);
    }
  };

  // derive CSS key from prediction string
  const severityKey = prediction
    ? prediction.toLowerCase().replace(/\s+/g, "_")
    : null;

  const tipData = prediction ? TIPS[prediction] : null;
  const riskFactors = getRiskFactors(form, confidence);

  return (
    <div className="app">

      <header className="topbar">
        <div className="topbar-title">
          <span className="title-main">Traffic Crashes</span><span className="title-ai">.AI</span>
        </div>
      </header>
      <div className="topbar-right">
          <div className="tags">
            <span>Real-time Analysis</span>
            <span>ML Powered</span>
            <span>Explainable AI</span>
          </div>
        </div>

      <main className="split-card">

        {/* LEFT — light panel */}
        <section className="panel panel-light">
          <h2>Crash Conditions</h2>
          <p className="panel-sub">Environmental &amp; road factors</p>

          <div className="field-group">

            <div className="field">
              <select className={sel("weather_condition")} value={form.weather_condition} onChange={e => set("weather_condition", e.target.value)}>
                <option value="" disabled>Weather</option>
                <option value="CLEAR">Clear</option>
                <option value="RAIN">Rain</option>
                <option value="SNOW">Snow</option>
                <option value="FOG/SMOKE/HAZE">Fog</option>
              </select>
            </div>

            <div className="field-row">
              <div className="field">
                <select className={sel("lighting_condition")} value={form.lighting_condition} onChange={e => set("lighting_condition", e.target.value)}>
                  <option value="" disabled>Lighting</option>
                  <option value="DAYLIGHT">Daylight</option>
                  <option value="DARKNESS">Darkness</option>
                  <option value="DUSK">Dusk</option>
                  <option value="DAWN">Dawn</option>
                </select>
              </div>
              <div className="field">
                <select className={sel("roadway_surface_cond")} value={form.roadway_surface_cond} onChange={e => set("roadway_surface_cond", e.target.value)}>
                  <option value="" disabled>Surface</option>
                  <option value="DRY">Dry</option>
                  <option value="WET">Wet</option>
                  <option value="SNOW OR SLUSH">Snow / Slush</option>
                  <option value="ICE">Ice</option>
                </select>
              </div>
            </div>

            <div className="field">
              <select className={sel("road_defect")} value={form.road_defect} onChange={e => set("road_defect", e.target.value)}>
                <option value="" disabled>Road Defect</option>
                <option value="NO DEFECTS">No Defects</option>
                <option value="RUT, HOLES">Ruts / Holes</option>
                <option value="CONSTRUCTION">Construction</option>
                <option value="WORN SURFACE">Worn Surface</option>
              </select>
            </div>

            <div className="field-row">
              <div className="field">
                <select className={sel("traffic_control_device")} value={form.traffic_control_device} onChange={e => set("traffic_control_device", e.target.value)}>
                  <option value="" disabled>Traffic Control</option>
                  <option value="TRAFFIC SIGNAL">Traffic Signal</option>
                  <option value="STOP SIGN/FLASHER">Stop Sign</option>
                  <option value="NO CONTROLS">No Control</option>
                  <option value="YIELD">Yield</option>
                </select>
              </div>
              <div className="field">
                <select className={sel("alignment")} value={form.alignment} onChange={e => set("alignment", e.target.value)}>
                  <option value="" disabled>Road Alignment</option>
                  <option value="STRAIGHT AND LEVEL">Straight &amp; Level</option>
                  <option value="STRAIGHT ON GRADE">Straight on Grade</option>
                  <option value="CURVE, LEVEL">Curve, Level</option>
                  <option value="CURVE ON GRADE">Curve on Grade</option>
                </select>
              </div>
            </div>

            <div className="field">
              <select className={sel("trafficway_type")} value={form.trafficway_type} onChange={e => set("trafficway_type", e.target.value)}>
                <option value="" disabled>Trafficway Type</option>
                <option value="DIVIDED - W/MEDIAN BARRIER">Divided w/ Barrier</option>
                <option value="NOT DIVIDED">Not Divided</option>
                <option value="ONE-WAY">One-Way</option>
                <option value="PARKING LOT">Parking Lot</option>
              </select>
            </div>

            <div className="field">
              <select className={sel("first_crash_type")} value={form.first_crash_type} onChange={e => set("first_crash_type", e.target.value)}>
                <option value="" disabled>First Crash Type</option>
                <option value="REAR END">Rear End</option>
                <option value="TURNING">Turning</option>
                <option value="ANGLE">Angle</option>
                <option value="SIDESWIPE SAME DIRECTION">Sideswipe Same Dir.</option>
                <option value="FIXED OBJECT">Fixed Object</option>
                <option value="PEDESTRIAN">Pedestrian</option>
                <option value="HEAD ON">Head On</option>
                <option value="PARKED MOTOR VEHICLE">Parked Vehicle</option>
              </select>
            </div>

            <div className="field">
              <select className={sel("prim_contributory_cause")} value={form.prim_contributory_cause} onChange={e => set("prim_contributory_cause", e.target.value)}>
                <option value="" disabled>Primary Cause</option>
                <option value="FAILING TO YIELD RIGHT-OF-WAY">Failing to Yield</option>
                <option value="FOLLOWING TOO CLOSELY">Following Too Closely</option>
                <option value="IMPROPER OVERTAKING/PASSING">Improper Passing</option>
                <option value="FAILING TO REDUCE SPEED">Failing to Reduce Speed</option>
                <option value="IMPROPER TURNING/NO SIGNAL">Improper Turning</option>
                <option value="DRIVING SKILLS/KNOWLEDGE/EXPERIENCE">Driver Inexperience</option>
                <option value="WEATHER">Weather</option>
                <option value="VISION OBSCURED (SIGNS, TREE LIMBS, BUILDINGS, ETC.)">Vision Obscured</option>
                <option value="NOT APPLICABLE">Not Applicable</option>
              </select>
            </div>

            <div className="field-row">
              <div className="field">
                <select className={sel("damage")} value={form.damage} onChange={e => set("damage", e.target.value)}>
                  <option value="" disabled>Damage</option>
                  <option value="OVER $1,500">Over $1,500</option>
                  <option value="$501 - $1,500">$501 – $1,500</option>
                  <option value="$500 OR LESS">$500 or Less</option>
                </select>
              </div>
              <div className="field">
                <label className="field-label">Units Involved</label>
                <input
                  type="number" min="1" max="10"
                  value={form.num_units}
                  onChange={e => set("num_units", Number(e.target.value))}
                  style={{ width: "100%", border: "none", borderBottom: "1.5px solid #d0d0d0", background: "transparent", fontSize: 14, padding: "4px 0", outline: "none", color: "#222" }}
                />
              </div>
            </div>

            <div className="field">
              <label className="field-label">Crash Hour — {form.crash_hour}:00</label>              <input
                type="range" min="0" max="23"
                value={form.crash_hour}
                onChange={e => set("crash_hour", Number(e.target.value))}
              />
            </div>

            <div className="field toggle-row">
              <span className="field-label">Intersection involved?</span>
              <label className="switch">
                <input
                  type="checkbox"
                  checked={form.intersection_related_i === "Y"}
                  onChange={e => set("intersection_related_i", e.target.checked ? "Y" : "N")}
                />
                <span className="slider"></span>
              </label>
            </div>

          </div>
        </section>

        {/* RIGHT — dark panel */}
        <section className="panel panel-dark">
          <h2>Analysis Results</h2>
          <p className="panel-sub">Predicted injury severity</p>

          <div className="result-box">
            {error && (
              <div className="error-msg">{error}</div>
            )}

            {!error && !prediction && !loading && (
              <div className="placeholder">
                <div className="circle"></div>
                <p>Fill in conditions and run the prediction.</p>
              </div>
            )}

            {loading && (
              <div className="placeholder">
                <div className="spinner"></div>
                <p>Analysing...</p>
              </div>
            )}

            {!loading && prediction && (
              <div className="prediction-area">
                <div className={`severity-badge ${severityKey}`}>
                  <span className="severity-icon">{tipData.icon}</span>
                  {prediction.replace(/_/g, " ")}
                </div>

                <div className="tip-box" style={{ borderColor: tipData.color }}>
                  <p className="tip-headline" style={{ color: tipData.color }}>{tipData.headline}</p>
                  <ul className="tip-list">
                    {tipData.tips.map((t, i) => <li key={i}>{t}</li>)}
                  </ul>
                </div>

                <div className="confidence-section">
                  {Object.entries(confidence).map(([label, pct]) => (
                    <div className="conf-row" key={label}>
                      <div className="conf-label-row">
                        <span>{label.replace(/_/g, " ")}</span>
                        <span className="conf-pct">{pct}%</span>
                      </div>
                      <div className="bar">
                        <div
                          className="fill"
                          style={{
                            width: `${pct}%`,
                            background:
                              label === "NO_INJURY" ? "#ABEBD2"
                              : label === "MINOR"   ? "#FFC857"
                              :                       "#CA3C25"
                          }}
                        ></div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>

          <button className="predict-btn" onClick={handlePredict} disabled={loading}>
            {loading ? "Predicting…" : "Predict Severity"}
          </button>

          <div className="bottom-stats">
            <div className="stat-block">
              <span className="stat-label">Distribution</span>
              <div
                className="pie-chart"
                style={Object.keys(confidence).length ? {
                  background: `conic-gradient(
                    #ABEBD2 0% ${confidence["NO_INJURY"] ?? 33}%,
                    #FFC857 ${confidence["NO_INJURY"] ?? 33}% ${(confidence["NO_INJURY"] ?? 33) + (confidence["MINOR"] ?? 33)}%,
                    #CA3C25 ${(confidence["NO_INJURY"] ?? 33) + (confidence["MINOR"] ?? 33)}% 100%
                  )`
                } : {}}
              ></div>
            </div>
            <div className="stat-block risk-block">
              <span className="stat-label">Top Risk Factors</span>
              {riskFactors.length === 0 ? (
                <p className="no-risks">Fill in the form to see risk factors.</p>
              ) : (
                riskFactors.map((r, i) => (
                  <div className="risk-item" key={i}>
                    <span>{r.label}</span>
                    <div className="bar">
                      <div className="fill" style={{ width: `${r.weight}%`, background: r.color }}></div>
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>
        </section>

      </main>
    </div>
  );
}

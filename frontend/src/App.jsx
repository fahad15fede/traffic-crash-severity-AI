import "./App.css";
import { useState, useEffect } from "react";
import { supabase } from "./lib/supabase";
import AuthModal from "./components/AuthModal";

const API = import.meta.env.VITE_API_URL || "https://fede8rma-carcrashai.hf.space";
const MODEL1_GUEST_LIMIT = 5; // after this many uses, nudge to sign in
// ── Severity tips ────────────────────────────────────────────────────────────

// Tips keyed by [leading_risk_factor][severity]
const FACTOR_TIPS = {
  "High-Impact Crash Type": {
    NO_INJURY: {
      headline: "High-Impact Type — Low Outcome",
      tips: [
        "Head-on and fixed-object crashes are serious — you were fortunate this time.",
        "Always wear a seatbelt; it's the single biggest factor in surviving high-impact crashes.",
        "Avoid distractions — reaction time is critical in these crash types.",
      ],
    },
    MINOR: {
      headline: "High-Impact Crash — Minor Injuries Likely",
      tips: [
        "Head-on and fixed-object crashes cause significant force — seek medical evaluation even for minor pain.",
        "Reduce speed on roads where fixed objects are close to the carriageway.",
        "Keep a safe lateral distance from barriers, poles, and parked vehicles.",
      ],
    },
    SEVERE: {
      headline: "High-Impact Crash — Severe Risk",
      tips: [
        "Head-on collisions and fixed-object impacts are among the deadliest crash types — avoid travel if possible.",
        "Never overtake on curves or crests where oncoming traffic is hidden.",
        "Ensure airbags and seatbelts are functional before every journey.",
      ],
    },
  },
  "Hazardous Surface": {
    NO_INJURY: {
      headline: "Slippery Surface — Stayed Safe",
      tips: [
        "Wet or icy roads reduce grip significantly — keep tyre tread above 3mm.",
        "Brake earlier and more gently than you would on dry roads.",
        "Avoid cruise control on wet or slippery surfaces.",
      ],
    },
    MINOR: {
      headline: "Hazardous Surface — Injury Risk",
      tips: [
        "Wet and icy roads triple stopping distances — slow down well in advance.",
        "Switch to winter tyres when temperatures drop below 7°C.",
        "Avoid sharp steering inputs on slippery surfaces to prevent skidding.",
      ],
    },
    SEVERE: {
      headline: "Hazardous Surface — Extreme Danger",
      tips: [
        "Ice and snow make roads extremely unpredictable — delay travel if possible.",
        "If you must drive, reduce speed by at least 50% and double following distance.",
        "Black ice is invisible — treat any wet-looking road in freezing temps as icy.",
      ],
    },
  },
  "Poor Lighting": {
    NO_INJURY: {
      headline: "Low Light — Safe Outcome",
      tips: [
        "Darkness reduces visibility significantly — always use headlights from dusk.",
        "Check that all lights are working before night drives.",
        "Reduce speed at night — your stopping distance often exceeds your visibility range.",
      ],
    },
    MINOR: {
      headline: "Poor Lighting — Injury Risk",
      tips: [
        "Darkness is a major factor in pedestrian and cyclist fatalities — scan intersections carefully.",
        "Use high beams on unlit roads but dip them for oncoming traffic.",
        "Fatigue increases sharply after midnight — take breaks on long night drives.",
      ],
    },
    SEVERE: {
      headline: "Poor Lighting — Severe Risk",
      tips: [
        "Night driving in adverse conditions is extremely dangerous — postpone if possible.",
        "Ensure windscreen is clean — smearing dramatically reduces night visibility.",
        "Never drive impaired at night; reaction time is already reduced by darkness.",
      ],
    },
  },
  "No Traffic Control": {
    NO_INJURY: {
      headline: "No Controls — Safe Outcome",
      tips: [
        "Uncontrolled junctions require full attention — treat every crossing as a potential conflict.",
        "Slow down and look both ways even when you have right of way.",
        "Be especially cautious at rural crossroads with no signage.",
      ],
    },
    MINOR: {
      headline: "No Traffic Control — Injury Risk",
      tips: [
        "Uncontrolled roads have higher conflict rates — reduce speed approaching any junction.",
        "Never assume other drivers will yield — make eye contact before proceeding.",
        "Rural roads with no controls are disproportionately dangerous at night.",
      ],
    },
    SEVERE: {
      headline: "No Traffic Control — Severe Risk",
      tips: [
        "High-speed uncontrolled roads are among the most dangerous — treat every junction as a stop.",
        "Avoid overtaking near uncontrolled junctions.",
        "Report missing or damaged road signs to local authorities.",
      ],
    },
  },
  "Adverse Weather": {
    NO_INJURY: {
      headline: "Adverse Weather — Safe Outcome",
      tips: [
        "Fog, snow, and rain reduce visibility and grip — always adjust speed accordingly.",
        "Use fog lights only in fog — they dazzle other drivers in clear conditions.",
        "Check weather forecasts before long journeys and plan alternate routes.",
      ],
    },
    MINOR: {
      headline: "Adverse Weather — Injury Risk",
      tips: [
        "Rain reduces tyre grip by up to 30% — increase following distance significantly.",
        "In fog, use dipped headlights and rear fog lights, and slow down.",
        "Never use cruise control in rain, snow, or fog.",
      ],
    },
    SEVERE: {
      headline: "Adverse Weather — Severe Risk",
      tips: [
        "Severe weather is a leading cause of fatal crashes — delay travel until conditions improve.",
        "If caught in a blizzard or heavy fog, pull over safely and wait it out.",
        "Keep an emergency kit in your car during winter months.",
      ],
    },
  },
  "Intersection": {
    NO_INJURY: {
      headline: "Intersection — Safe Outcome",
      tips: [
        "Intersections account for a large share of all crashes — always scan left, right, and ahead.",
        "Never run amber lights — the time saved is not worth the risk.",
        "Watch for cyclists and pedestrians who may not be visible from a distance.",
      ],
    },
    MINOR: {
      headline: "Intersection — Injury Risk",
      tips: [
        "Angle and turning crashes at intersections are very common — yield properly.",
        "Slow down when approaching intersections even on green.",
        "Check for red-light runners before proceeding on green.",
      ],
    },
    SEVERE: {
      headline: "Intersection — Severe Risk",
      tips: [
        "High-speed intersection crashes are frequently fatal — treat every crossing with full attention.",
        "Never speed up to beat a changing light.",
        "Be extra cautious at intersections with poor visibility or missing signals.",
      ],
    },
  },
  "Curved Road": {
    NO_INJURY: {
      headline: "Curved Road — Safe Outcome",
      tips: [
        "Curves require reduced speed — enter slower than you think necessary.",
        "Look through the curve to where you want to go, not at the edge.",
        "Avoid sudden braking mid-curve — brake before you enter.",
      ],
    },
    MINOR: {
      headline: "Curved Road — Injury Risk",
      tips: [
        "Curves on grades are especially dangerous — centrifugal force and gravity combine.",
        "Reduce speed significantly before entering any curve on a hill.",
        "Stay in your lane — drifting on curves is a leading cause of head-on crashes.",
      ],
    },
    SEVERE: {
      headline: "Curved Road — Severe Risk",
      tips: [
        "Curves on grades in poor conditions are extremely dangerous — slow to a crawl.",
        "Never overtake on a curve — you cannot see oncoming traffic.",
        "If you feel the car sliding on a curve, steer gently into the skid and ease off the accelerator.",
      ],
    },
  },
  "Road Defects": {
    NO_INJURY: {
      headline: "Road Defects — Safe Outcome",
      tips: [
        "Potholes and ruts can cause sudden loss of control — scan the road ahead.",
        "Reduce speed in construction zones — road surfaces are unpredictable.",
        "Report significant road defects to your local authority.",
      ],
    },
    MINOR: {
      headline: "Road Defects — Injury Risk",
      tips: [
        "Ruts and holes can cause tyre blowouts — avoid them or slow down significantly.",
        "Construction zones have uneven surfaces and unexpected lane changes — stay alert.",
        "Keep both hands on the wheel on roads with known defects.",
      ],
    },
    SEVERE: {
      headline: "Road Defects — Severe Risk",
      tips: [
        "Severe road defects combined with speed are a dangerous combination — slow down.",
        "A tyre blowout at high speed can be fatal — check tyre pressure regularly.",
        "Avoid roads with known severe defects until they are repaired.",
      ],
    },
  },
  "Multi-Vehicle Crash": {
    NO_INJURY: {
      headline: "Multi-Vehicle — Safe Outcome",
      tips: [
        "Multi-vehicle crashes escalate quickly — always maintain a safe following distance.",
        "In heavy traffic, increase your gap to allow reaction time.",
        "Avoid driving in another vehicle's blind spot.",
      ],
    },
    MINOR: {
      headline: "Multi-Vehicle — Injury Risk",
      tips: [
        "Chain-reaction crashes are common in wet or foggy conditions — increase following distance.",
        "If you see a crash ahead, slow down and signal early to warn drivers behind you.",
        "Never rubberneck at crash scenes — it causes secondary crashes.",
      ],
    },
    SEVERE: {
      headline: "Multi-Vehicle — Severe Risk",
      tips: [
        "Multi-vehicle pile-ups at speed are among the most deadly crash types.",
        "In fog or heavy rain on motorways, use the 4-second rule minimum.",
        "If involved in a multi-vehicle crash, move to safety and call emergency services immediately.",
      ],
    },
  },
  "Late Night Hours": {
    NO_INJURY: {
      headline: "Late Night — Safe Outcome",
      tips: [
        "Fatigue is as dangerous as drink-driving — take breaks every 2 hours on long drives.",
        "Late night roads have fewer cars but more impaired and fatigued drivers.",
        "Keep windows slightly open and music moderate to stay alert.",
      ],
    },
    MINOR: {
      headline: "Late Night — Injury Risk",
      tips: [
        "Between midnight and 4am, fatigue-related crashes peak — avoid driving if tired.",
        "Pedestrians and cyclists are harder to see at night — scan intersections carefully.",
        "If you feel drowsy, pull over safely and rest — no destination is worth your life.",
      ],
    },
    SEVERE: {
      headline: "Late Night — Severe Risk",
      tips: [
        "Late night driving in poor conditions is extremely high risk — delay if possible.",
        "Drunk and fatigued drivers are most common between midnight and 4am.",
        "If you must drive, stay on well-lit main roads and keep speed low.",
      ],
    },
  },
};

// Fallback tips when no specific factor dominates
const FALLBACK_TIPS = {
  NO_INJURY: {
    headline: "Low Risk — Drive Safely",
    tips: [
      "Conditions look favourable — stay alert and maintain safe following distance.",
      "Even in low-risk scenarios, avoid distractions and keep to speed limits.",
      "Check mirrors regularly and signal early at intersections.",
    ],
  },
  MINOR: {
    headline: "Moderate Risk — Stay Cautious",
    tips: [
      "Reduce speed — conditions increase stopping distance.",
      "Increase following distance to at least 4 seconds in wet or low-light conditions.",
      "Avoid sudden lane changes and use headlights if visibility is reduced.",
    ],
  },
  SEVERE: {
    headline: "High Risk — Extreme Caution",
    tips: [
      "Consider delaying travel — current conditions are dangerous.",
      "If driving is necessary, reduce speed significantly and use hazard lights.",
      "Stay on main roads, avoid curves and grades, and never drive on ice without winter tyres.",
    ],
  },
};

const SEVERITY_COLORS = {
  NO_INJURY: "#22c55e",
  MINOR: "#eab308",
  SEVERE: "#ef4444",
};

const SEVERITY_ICONS = {
  NO_INJURY: "✓",
  MINOR: "⚠",
  SEVERE: "✕",
};

function getTipData(prediction, riskFactors) {
  if (!prediction) return null;
  const topFactor = riskFactors.length > 0 ? riskFactors[0].label : null;
  const factorTips = topFactor && FACTOR_TIPS[topFactor]?.[prediction];
  const base = factorTips || FALLBACK_TIPS[prediction];
  return {
    ...base,
    color: SEVERITY_COLORS[prediction],
    icon: SEVERITY_ICONS[prediction],
  };
}

// ── Risk factor logic ────────────────────────────────────────────────────────
function getRiskFactors(form, confidence) {
  const risks = [];

  if (["DARKNESS", "DUSK", "DAWN"].includes(form.lighting_condition))
    risks.push({ label: "Poor Lighting", weight: 85, color: "#ef4444" });

  if (["WET", "SNOW OR SLUSH", "ICE"].includes(form.roadway_surface_cond))
    risks.push({ label: "Hazardous Surface", weight: 78, color: "#ef4444" });

  if (["SNOW", "FREEZING RAIN/DRIZZLE", "FOG/SMOKE/HAZE"].includes(form.weather_condition))
    risks.push({ label: "Adverse Weather", weight: 72, color: "#eab308" });

  if (form.intersection_related_i === "Y")
    risks.push({ label: "Intersection", weight: 60, color: "#eab308" });

  if (["RUT, HOLES", "CONSTRUCTION", "WORN SURFACE", "OTHER"].includes(form.road_defect))
    risks.push({ label: "Road Defects", weight: 55, color: "#eab308" });

  if (form.traffic_control_device === "NO CONTROLS")
    risks.push({ label: "No Traffic Control", weight: 65, color: "#ef4444" });

  if (["CURVE ON GRADE", "CURVE ON HILLCREST", "CURVE, LEVEL"].includes(form.alignment))
    risks.push({ label: "Curved Road", weight: 50, color: "#eab308" });

  if (["HEAD ON", "FIXED OBJECT", "PEDESTRIAN"].includes(form.first_crash_type))
    risks.push({ label: "High-Impact Crash Type", weight: 90, color: "#ef4444" });

  if (form.num_units >= 3)
    risks.push({ label: "Multi-Vehicle Crash", weight: 68, color: "#eab308" });

  if (form.crash_hour >= 22 || form.crash_hour <= 4)
    risks.push({ label: "Late Night Hours", weight: 58, color: "#eab308" });

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
  const [selectedModel, setSelectedModel] = useState(1);

  // auth state
  const [user, setUser] = useState(null);
  const [showAuth, setShowAuth] = useState(false);
  const [model1Uses, setModel1Uses] = useState(0);

  useEffect(() => {
    supabase.auth.getSession().then(({ data }) => setUser(data.session?.user ?? null));
    const { data: listener } = supabase.auth.onAuthStateChange((_e, session) => {
      setUser(session?.user ?? null);
    });
    return () => listener.subscription.unsubscribe();
  }, []);

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

    // track model 1 guest uses and nudge after limit
    if (selectedModel === 1 && !user) {
      const next = model1Uses + 1;
      setModel1Uses(next);
    }

    try {
      const res = await fetch(`${API}/predict`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ ...form, crash_hour: Number(form.crash_hour), model: selectedModel }),
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

  const riskFactors = getRiskFactors(form, confidence);
  const tipData = prediction ? getTipData(prediction, riskFactors) : null;

  return (
    <div className="app">

      <header className="topbar">
        <div className="topbar-title">
          <span className="title-main">Traffic Crashes</span><span className="title-ai">.AI</span>
        </div>
        <div className="tags">
          <span>Real-time Analysis</span>
          <span>ML Powered</span>
          <span>Explainable AI</span>
        </div>
        <div className="topbar-auth">
          {user ? (
            <>
              <span className="auth-email">{user.email}</span>
              <button className="auth-link" onClick={() => supabase.auth.signOut()}>Sign out</button>
            </>
          ) : (
            <button className="auth-link" onClick={() => setShowAuth(true)}>Sign in</button>
          )}
        </div>
      </header>

      {showAuth && (
        <AuthModal
          onClose={() => setShowAuth(false)}
          onSuccess={(u) => { setUser(u); setShowAuth(false); }}
        />
      )}

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
                <label className="field-label">Vehicles Involved</label>
                <div className="num-units-row">
                  <button className="num-btn" onClick={() => set("num_units", Math.max(1, form.num_units - 1))}>−</button>
                  <span className="num-val">{form.num_units}</span>
                  <button className="num-btn" onClick={() => set("num_units", Math.min(10, form.num_units + 1))}>+</button>
                </div>
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
                              label === "NO_INJURY" ? "#22c55e"
                              : label === "MINOR"   ? "#eab308"
                              :                       "#ef4444"
                          }}
                        ></div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>

          <div className="model-selector">
            <span className="model-label">Model</span>
            <div className="model-btns">
              <button
                className={`model-btn ${selectedModel === 1 ? "active" : ""}`}
                onClick={() => setSelectedModel(1)}
              >
                Model 1 — RF
              </button>
              <button
                className={`model-btn ${selectedModel === 2 ? "active" : ""}`}
                onClick={() => {
                  if (!user) { setShowAuth(true); return; }
                  setSelectedModel(2);
                }}
              >
                Model 2 — XGBoost
                {!user && <span className="lock-icon">🔒</span>}
              </button>
            </div>
            {!user && model1Uses >= MODEL1_GUEST_LIMIT && (
              <p className="nudge-msg">
                Want better accuracy?{" "}
                <button className="nudge-link" onClick={() => setShowAuth(true)}>
                  Sign in for Model 2
                </button>
              </p>
            )}
          </div>

          <button className="predict-btn" onClick={handlePredict} disabled={loading}>
            {loading ? "Predicting…" : "Predict Severity"}
          </button>

          <div className="bottom-stats">
            {prediction && (
              <div className="stat-block">
                <span className="stat-label">Distribution</span>
                <div
                  className="pie-chart"
                  style={{
                    background: `conic-gradient(
                      #22c55e 0% ${confidence["NO_INJURY"] ?? 33}%,
                      #eab308 ${confidence["NO_INJURY"] ?? 33}% ${(confidence["NO_INJURY"] ?? 33) + (confidence["MINOR"] ?? 33)}%,
                      #ef4444 ${(confidence["NO_INJURY"] ?? 33) + (confidence["MINOR"] ?? 33)}% 100%
                    )`
                  }}
                ></div>
              </div>
            )}
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

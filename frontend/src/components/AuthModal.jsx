import { useState } from "react";
import { supabase } from "../lib/supabase";

export default function AuthModal({ onClose, onSuccess }) {
  const [mode, setMode] = useState("login");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirm, setConfirm] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [closing, setClosing] = useState(false);

  const close = () => {
    setClosing(true);
    setTimeout(onClose, 220);
  };

  const switchMode = () => {
    setMode(m => m === "login" ? "signup" : "login");
    setError(null);
    setConfirm("");
  };

  const handle = async (e) => {
    e.preventDefault();
    setError(null);

    if (mode === "signup" && password !== confirm) {
      setError("Passwords do not match.");
      return;
    }

    setLoading(true);

    if (mode === "signup") {
      const { data, error } = await supabase.auth.signUp({ email, password });
      if (error) { setError(error.message); setLoading(false); return; }
      await supabase.from("profiles").insert({ id: data.user.id, email: data.user.email });
      onSuccess(data.user);
    } else {
      const { data, error } = await supabase.auth.signInWithPassword({ email, password });
      if (error) { setError(error.message); setLoading(false); return; }
      onSuccess(data.user);
    }

    setLoading(false);
  };

  return (
    <div className={`modal-overlay ${closing ? "modal-out" : "modal-in"}`} onClick={close}>
      <div className={`modal-card ${closing ? "card-out" : "card-in"}`} onClick={e => e.stopPropagation()}>

        <button className="modal-close" onClick={close}>✕</button>

        <h2 className="modal-title">
          {mode === "login" ? "Sign in" : "Create account"}
        </h2>
        <p className="modal-sub">
          {mode === "login"
            ? "Sign in to access Model 2 — XGBoost (unlimited predictions)."
            : "Free account. Unlock Model 2 and save your prediction history."}
        </p>

        <form onSubmit={handle} className="modal-form">
          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={e => setEmail(e.target.value)}
            required
            className="modal-input"
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={e => setPassword(e.target.value)}
            required
            className="modal-input"
          />
          {mode === "signup" && (
            <input
              type="password"
              placeholder="Confirm password"
              value={confirm}
              onChange={e => setConfirm(e.target.value)}
              required
              className="modal-input"
            />
          )}
          {error && <p className="modal-error">{error}</p>}
          <button type="submit" className="modal-btn" disabled={loading}>
            {loading ? "Please wait…" : mode === "login" ? "Sign in" : "Sign up"}
          </button>
        </form>

        <p className="modal-switch">
          {mode === "login" ? "No account? " : "Already have one? "}
          <button onClick={switchMode}>
            {mode === "login" ? "Sign up" : "Sign in"}
          </button>
        </p>
      </div>
    </div>
  );
}

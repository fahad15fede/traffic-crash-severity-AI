# Auth & Database Plan — Traffic Crashes.AI

## Goal

Replace localStorage token tracking with real user accounts, persistent token balances, and prediction history. Each user gets 10 Model 1 tokens on signup. Model 2 remains unlimited.

---

## Stack Decision

| Layer | Choice | Reason |
|---|---|---|
| Auth | Supabase Auth | Free tier, built-in email/OAuth, JWT out of the box |
| Database | Supabase Postgres | Same platform as auth, free tier, instant REST + realtime |
| Frontend | React + Supabase JS client | Minimal setup, handles sessions automatically |
| Backend | FastAPI + JWT verification | Verify Supabase JWT on every `/predict` call |

Supabase is chosen because it handles auth + database in one place with a generous free tier, and works well with both Vercel (frontend) and Hugging Face (backend).

---

## Database Schema

### `users` (managed by Supabase Auth)
Supabase creates this automatically. We extend it with a profile table.

### `profiles`
```sql
create table profiles (
  id          uuid primary key references auth.users(id) on delete cascade,
  email       text,
  model1_tokens int not null default 10,
  created_at  timestamptz default now()
);

-- Auto-create profile on signup
create function handle_new_user()
returns trigger as $$
begin
  insert into profiles (id, email)
  values (new.id, new.email);
  return new;
end;
$$ language plpgsql security definer;

create trigger on_auth_user_created
  after insert on auth.users
  for each row execute procedure handle_new_user();
```

### `predictions`
```sql
create table predictions (
  id            uuid primary key default gen_random_uuid(),
  user_id       uuid references profiles(id) on delete cascade,
  model_used    int not null,           -- 1 or 2
  severity      text not null,          -- NO_INJURY / MINOR / SEVERE
  confidence    jsonb,                  -- { NO_INJURY: 61.3, MINOR: 28.4, SEVERE: 10.3 }
  inputs        jsonb,                  -- full form payload
  created_at    timestamptz default now()
);
```

---

## Auth Flow

```
User visits site
  └─ Not logged in → show Login / Sign Up modal
       └─ Sign up with email + password
            └─ Supabase creates user
            └─ Trigger creates profile with 10 tokens
       └─ Log in
            └─ Supabase returns JWT
            └─ Frontend stores session (Supabase handles this)

User clicks Predict
  └─ Frontend sends JWT in Authorization header
  └─ Backend verifies JWT with Supabase public key
  └─ If Model 1:
       └─ Check profiles.model1_tokens > 0
       └─ Decrement token in DB (atomic update)
       └─ Run prediction
       └─ Save to predictions table
  └─ If Model 2:
       └─ Run prediction
       └─ Save to predictions table
  └─ Return result
```

---

## Backend Changes (`main.py`)

1. Add `python-jose` and `supabase` to requirements
2. Verify JWT on every `/predict` request
3. Check + decrement token from DB for Model 1
4. Save prediction to `predictions` table

```python
# New dependencies
from fastapi import Depends, HTTPException, Header
from jose import jwt
import httpx

SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_SERVICE_KEY"]  # service role key (backend only)
SUPABASE_JWT_SECRET = os.environ["SUPABASE_JWT_SECRET"]

async def get_current_user(authorization: str = Header(...)):
    token = authorization.replace("Bearer ", "")
    try:
        payload = jwt.decode(token, SUPABASE_JWT_SECRET, algorithms=["HS256"],
                             audience="authenticated")
        return payload["sub"]  # user UUID
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.post("/predict")
async def predict(data: AccidentInput, user_id: str = Depends(get_current_user)):
    if data.model == 1:
        # check tokens
        # decrement atomically
        # run prediction
        # save to DB
    ...
```

---

## Frontend Changes

### New files
```
frontend/src/
  lib/
    supabase.js        # supabase client init
  components/
    AuthModal.jsx      # login / signup modal
    TokenBadge.jsx     # shows remaining tokens, fetched from DB
  hooks/
    useAuth.js         # session state
    useTokens.js       # fetch + update token count
```

### Auth modal
- Email + password sign up / log in
- OAuth buttons (Google) optional
- Show on first visit if not logged in
- Persist session via Supabase (auto refresh)

### Token display
- Fetch `model1_tokens` from `profiles` on login
- Update in real time after each Model 1 prediction
- Remove all `localStorage` token logic

### Sending JWT
```js
const { data: { session } } = await supabase.auth.getSession();
const res = await fetch(`${API}/predict`, {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    "Authorization": `Bearer ${session.access_token}`,
  },
  body: JSON.stringify({ ...form, model: selectedModel }),
});
```

---

## Environment Variables

### Vercel (frontend)
```
VITE_SUPABASE_URL=https://xxxx.supabase.co
VITE_SUPABASE_ANON_KEY=eyJ...
VITE_API_URL=https://fede8rma-carcrashai.hf.space
```

### Hugging Face (backend secrets)
```
SUPABASE_URL=https://xxxx.supabase.co
SUPABASE_SERVICE_KEY=eyJ...   # service role, never expose to frontend
SUPABASE_JWT_SECRET=your-jwt-secret
```

---

## Implementation Order

1. Create Supabase project → get URL, anon key, service key, JWT secret
2. Run SQL schema (profiles + predictions tables + trigger)
3. Backend — add JWT verification + token check + DB writes
4. Frontend — add Supabase client, auth modal, replace localStorage with DB tokens
5. Set env vars on Vercel and HF
6. Test full flow: signup → predict with Model 1 → token decrements → Model 2 unlimited

---

## Row Level Security (RLS)

```sql
-- Users can only read/update their own profile
alter table profiles enable row level security;
create policy "own profile" on profiles
  for all using (auth.uid() = id);

-- Users can only read their own predictions
alter table predictions enable row level security;
create policy "own predictions" on predictions
  for select using (auth.uid() = user_id);
```

Backend uses the **service role key** which bypasses RLS — this is intentional so the backend can write predictions and update tokens server-side without being blocked.

---

## Estimated Effort

| Task | Time |
|---|---|
| Supabase setup + schema | 30 min |
| Backend JWT + DB integration | 1–2 hrs |
| Frontend auth modal + hooks | 2–3 hrs |
| Testing + env vars | 1 hr |
| **Total** | **~5 hrs** |

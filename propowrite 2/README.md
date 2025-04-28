
# PropoWrite – AI Proposal Writer for Landscape & Architecture Firms

**PropoWrite** is a turnkey micro‑SaaS template that delivers polished, client‑ready project proposals in minutes.  
You fill in project particulars via a simple form or API call; GPT‑4o drafts a bespoke scope-of‑work, timeline, fee table, and design approach – ready to send.

This repo contains:

| Path | Purpose |
|------|---------|
| `backend/main.py` | FastAPI app with `/generate-proposal` endpoint |
| `templates/proposal_prompt.txt` | System + user prompt template |
| `requirements.txt` | Python deps (FastAPI, OpenAI, Uvicorn, Pydantic) |
| `Dockerfile` | Container for Railway/Fly.io |
| `stripe_webhook.py` | (Optional) Stripe checkout & webhook skeleton |
| `README.md` | Setup & business guide |

---

## 1. Quick start (local)

```bash
git clone https://github.com/youruser/propowrite.git
cd propowrite
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

export OPENAI_API_KEY=sk-...
uvicorn backend.main:app --reload
```

Open `http://127.0.0.1:8000/docs`, fill in proposal details, hit **Execute**, and receive Markdown/HTML ready to email.

---

## 2. Deploy to Railway (free tier friendly)

```bash
railway init            # if you have the CLI
railway up
```

Railway detects the `Dockerfile`, builds, and exposes a public HTTPS URL.  
Add environment variables in the Railway dashboard:

| Key | Value |
|-----|-------|
| `OPENAI_API_KEY` | *your secret* |
| `STRIPE_SECRET_KEY` | *(optional – for paid plans)* |
| `STRIPE_WEBHOOK_SECRET` | *(optional)* |

---

## 3. SaaS‑ify in 3 steps

1. **Stripe Checkout** – `/subscribe` endpoint creates a Checkout Session for the \$29/mo “Studio” plan.  
2. **Stripe webhook** – `stripe_webhook.py` listens for `invoice.payment_succeeded` → marks user active in Postgres/Supabase.  
3. **Auth header** – Each `/generate-proposal` call checks a JWT from Supabase to ensure the subscription is active.

All boilerplate is scaffolded; you just plug in your keys and DB URL.

---

## 4. Cost & margins

| Component | Cost / 50 proposals | Notes |
|-----------|--------------------|-------|
| OpenAI API (gpt‑4o‑mini) | ~\$1.40 | ~3k input/out tokens × \$0.0005 |
| Railway container | \$0.00–\$12 | Depends on Hobby vs. Pro |
| Stripe fees | 2.9 % + 30¢ | Built into price |

At \$29/mo and 50 proposals/user you keep **~92 % gross margin**.

---

## 5. Prompt engineering

`templates/proposal_prompt.txt` combines:

* **System:** “You are an AIA‑award winning landscape architect...”  
* **User placeholders:** `{client_name}`, `{site_description}`, etc.  
* **XML tags** for structure → ensures headings, fee table, and next steps parse cleanly into PDF exports.

---

## 6. Roadmap suggestions

* **One‑click PDF** using WeasyPrint.  
* **Brand kit upload** to inject logo/colour palette.  
* **Version history** per client and diff view.

---

### Built 2025-04-28 – Happy proposals!

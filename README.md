# StatsForge

A locally-hosted web app for game designers to calculate and simulate combat stats. Built with Flask — no cloud required, no data leaves your machine.

![Python](https://img.shields.io/badge/Python-3.11%2B-blue?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0%2B-black?logo=flask)
![License](https://img.shields.io/badge/License-MIT-green)

---

## Features

| Input | Description |
|---|---|
| **Attack / Defense** | Base attack value reduced by defense to compute effective hit damage |
| **Crit Chance %** | Probability (0–100) that any given hit lands as a critical |
| **Crit Multiplier** | Damage multiplier applied on a critical hit |
| **Fire Rate** | Hits per second — used to compute effective DPS |
| **Simulate N Hits** | Number of hits to simulate and render on the chart (max 500) |

| Output | Description |
|---|---|
| **Effective DPS** | Expected damage per hit × fire rate |
| **Expected / Hit** | Weighted average damage accounting for crit probability |
| **Min / Max Damage** | Effective hit damage and crit-scaled maximum |
| **Simulated Chart** | Bar chart of N individually-rolled hits (seed 42, reproducible) |

---

## Requirements

### Software

| Requirement | Version | Notes |
|---|---|---|
| [Python](https://www.python.org/downloads/) | 3.11+ | Required |

### Python packages

All listed in `requirements.txt`:

```
flask>=3.0.0
flask-limiter>=3.5.0
gunicorn>=21.0.0
```

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/CMgameplays/StatsForge.git
cd StatsForge
```

### 2. Create and activate a virtual environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Python dependencies

```bash
pip install -r requirements.txt
```

---

## Running locally

```bash
python statsforge.py
```

The server starts on `http://127.0.0.1:5000`.

---

## Project structure

```
statsforge/
├── statsforge.py        # Flask app — all routes and business logic
├── requirements.txt     # Python dependencies
├── templates/
│   └── index.html       # Single-page UI (HTML + CSS + Vanilla JS + Chart.js)
```

---

## API Routes

| Method | Route | Description |
|---|---|---|
| `GET` | `/` | Main UI page |
| `POST` | `/api/calculate` | Run combat stat calculation and simulation |

### POST `/api/calculate`

**Request body (JSON):**

```json
{
  "attack": 100,
  "defense": 20,
  "crit_chance": 15,
  "crit_mult": 2.0,
  "fire_rate": 2,
  "n_hits": 20
}
```

**Response (JSON):**

```json
{
  "dps": 183.6,
  "expected_per_hit": 91.8,
  "min_damage": 80.0,
  "max_damage": 160.0,
  "simulated_hits": [80.0, 160.0, ...],
  "formula_steps": ["effective_hit = max(1, attack - defense)", "..."]
}
```

---

## Deployment

The app is production-ready with Gunicorn and can be deployed to any WSGI-compatible host.

**Render / Railway / Fly.io:**

```
web: gunicorn statsforge:app --workers 2 --timeout 60 --bind 0.0.0.0:$PORT
```

Just connect your GitHub repo and deploy — no extra configuration needed.

---

## License

MIT — see [LICENSE](LICENSE) for details.

© CMG Forge

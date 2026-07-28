# topg — Phase 2 Chart Assistant (No Auto-Trading)

This project is an offline, CSV-driven assistant for **XAUUSD** with **IST** assumptions.

It does **not** place orders and does not connect to broker APIs.

## What it does
- Marks swing levels (phase-1 behavior kept).
- Marks deterministic structure confirmations.
- Detects CHoCH with 2-candle close confirmation.
- Applies MTF Daily/4H/1H condition ladder.
- Applies IST news blackout windows.
- Applies R:R and risk guardrails.
- Exports valid/rejected setup files.

## Run (non-coder quick steps)
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m src.topg_agent.main --input data/sample_ohlc.csv --outdir outputs
```

## Outputs
- `outputs/levels.csv`
- `outputs/signals.csv`
- `outputs/valid_setups.csv`
- `outputs/rejected_setups.csv` (includes `reject_reason`)

## News schedule file
Edit `data/news_events.csv` in IST using columns:
- `event_name`
- `event_time_ist`
- `window_before_min`
- `window_after_min`

## Module map
- `src/topg_agent/config.py`
- `src/topg_agent/structure.py`
- `src/topg_agent/choch.py`
- `src/topg_agent/mtf.py`
- `src/topg_agent/news.py`
- `src/topg_agent/risk.py`
- `src/topg_agent/validation.py`
- `src/topg_agent/main.py`

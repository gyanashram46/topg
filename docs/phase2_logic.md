# Phase-2 Logic (XAUUSD, IST, Mode A)

Phase-2 keeps the assistant offline and CSV-driven. It **does not place trades**.

## Pipeline
1. Load candles from CSV.
2. Mark structure confirmations (`structure.py`).
3. Detect CHoCH with 2-candle close confirmation (`choch.py`).
4. Build candidate setups and baseline SL/TP/R:R (`validation.py`, `risk.py`).
5. Apply MTF condition ladder (`mtf.py`).
6. Apply IST news blackout filter (`news.py`).
7. Partition outputs into valid/rejected setup CSV files.

## Core assumptions
- Instrument profile defaults to **XAUUSD**.
- Timezone defaults to **Asia/Kolkata (IST)**.
- CHoCH requires 2 closes by default.
- Buffer for zone marking uses wick + 1% of candle body.
- Minimum R:R default is 2.0 (configurable in `config.py`).

## Output files
- `outputs/levels.csv`
- `outputs/signals.csv`
- `outputs/valid_setups.csv`
- `outputs/rejected_setups.csv` (always includes `reject_reason`)

## News blackout usage
- Manual news schedule file: `data/news_events.csv`
- Columns: `event_name,event_time_ist,window_before_min,window_after_min`
- If file is empty/missing, fallback placeholder event windows are used from config.

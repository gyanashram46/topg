# Strategy Rules (XAUUSD / IST Profile)

This repository is configured for:
- Instrument: **XAUUSD**
- Timezone: **IST (Asia/Kolkata)**
- Mode: **A (chart-assistant only, no auto-trading)**

## Phase-2 references
- Structure confirmations: `src/topg_agent/structure.py`
- CHoCH detection: `src/topg_agent/choch.py`
- MTF condition ladder: `src/topg_agent/mtf.py`
- News blackout windows: `src/topg_agent/news.py`
- Validation and reason codes: `src/topg_agent/validation.py`

## Validation reason codes
- `RR_BELOW_MIN`
- `NEWS_BLACKOUT`
- `MTF_FILTER_FAIL`
- `MISSING_STRUCTURE`
- `DAILY_RISK_OUT_OF_BOUNDS`

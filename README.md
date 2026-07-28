# topg — Phase 1 Trading Agent

Phase 1 provides a **mark-only + signal-only** architecture for your strategy.

This phase does **not** place live trades. It focuses on:

- loading candles from CSV,
- detecting structure levels (swing highs/lows),
- generating setup signals,
- exporting levels/signals for review.

## Project layout

- `docs/strategy_rules.md` — convert your strategy notes into strict, machine-readable rules.
- `data/sample_ohlc.csv` — sample candle data format.
- `src/topg_agent/config.py` — settings/dataclasses.
- `src/topg_agent/levels.py` — level detection logic.
- `src/topg_agent/signals.py` — signal generation logic.
- `src/topg_agent/io.py` — data load/save helpers.
- `src/topg_agent/main.py` — CLI entrypoint to run phase-1 pipeline.
- `tests/` — basic unit tests.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
python -m src.topg_agent.main --input data/sample_ohlc.csv --outdir outputs
```

Outputs:

- `outputs/levels.csv`
- `outputs/signals.csv`

## Next step

Fill `docs/strategy_rules.md` with your exact entry/exit/invalidation rules.
Then we map each rule into code modules incrementally.

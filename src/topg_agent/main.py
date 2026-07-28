from __future__ import annotations

import argparse
from pathlib import Path

from .choch import detect_choch_events
from .config import AppConfig
from .io import ensure_dir, load_ohlc_csv, save_csv
from .levels import detect_swing_levels
from .mtf import apply_mtf_filter, derive_mtf_biases
from .news import load_news_events
from .signals import generate_proximity_signals
from .structure import detect_structure
from .validation import build_candidate_setups, validate_setups


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="topg phase-2 chart assistant (no auto-trading)")
    p.add_argument("--input", required=True, help="Path to OHLC CSV")
    p.add_argument("--outdir", default="outputs", help="Output directory")
    return p


def main() -> None:
    args = build_parser().parse_args()
    cfg = AppConfig()

    candles = load_ohlc_csv(args.input)

    # Preserve phase-1 outputs.
    levels = detect_swing_levels(
        candles,
        left=cfg.swing.left_bars,
        right=cfg.swing.right_bars,
    )
    signals = generate_proximity_signals(
        candles,
        levels,
        threshold_pct=cfg.signal.proximity_threshold_pct,
    )

    # Phase-2 modules.
    structure = detect_structure(candles, retracement_candles=cfg.structure.retracement_candles)
    choch_events = detect_choch_events(
        candles,
        structure,
        two_candle_confirm=cfg.structure.choch_two_candle_confirm,
        wick_plus_body_buffer_pct=cfg.structure.wick_plus_body_buffer_pct,
    )

    candidates = build_candidate_setups(choch_events, candles, cfg)

    biases = derive_mtf_biases(candles, timezone=cfg.timezone)
    candidates = apply_mtf_filter(
        candidates,
        daily_bias=biases["daily_bias"],
        h4_bias=biases["h4_bias"],
        h1_bias=biases["h1_bias"],
    )

    news_events = load_news_events(cfg.news.news_events_csv)
    valid_setups, rejected_setups = validate_setups(candidates, cfg, news_events=news_events)

    outdir = ensure_dir(args.outdir)
    save_csv(levels, Path(outdir) / "levels.csv")
    save_csv(signals, Path(outdir) / "signals.csv")
    save_csv(valid_setups, Path(outdir) / "valid_setups.csv")
    save_csv(rejected_setups, Path(outdir) / "rejected_setups.csv")

    print(f"[topg] levels: {len(levels)} -> {Path(outdir) / 'levels.csv'}")
    print(f"[topg] signals: {len(signals)} -> {Path(outdir) / 'signals.csv'}")
    print(f"[topg] valid setups: {len(valid_setups)} -> {Path(outdir) / 'valid_setups.csv'}")
    print(f"[topg] rejected setups: {len(rejected_setups)} -> {Path(outdir) / 'rejected_setups.csv'}")


if __name__ == "__main__":
    main()

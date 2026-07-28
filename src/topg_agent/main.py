from __future__ import annotations

import argparse
from pathlib import Path

from .config import AppConfig
from .io import load_ohlc_csv, ensure_dir, save_csv
from .levels import detect_swing_levels
from .signals import generate_proximity_signals


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="topg phase-1 level marking agent")
    p.add_argument("--input", required=True, help="Path to OHLC CSV")
    p.add_argument("--outdir", default="outputs", help="Output directory")
    return p


def main() -> None:
    args = build_parser().parse_args()
    cfg = AppConfig()

    candles = load_ohlc_csv(args.input)

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

    outdir = ensure_dir(args.outdir)
    save_csv(levels, Path(outdir) / "levels.csv")
    save_csv(signals, Path(outdir) / "signals.csv")

    print(f"[topg] levels: {len(levels)} -> {Path(outdir) / 'levels.csv'}")
    print(f"[topg] signals: {len(signals)} -> {Path(outdir) / 'signals.csv'}")


if __name__ == "__main__":
    main()

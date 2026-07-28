from __future__ import annotations

import pandas as pd


def generate_proximity_signals(
    candles: pd.DataFrame,
    levels: pd.DataFrame,
    threshold_pct: float = 0.15,
) -> pd.DataFrame:
    """
    Generate signal rows when close is within threshold_pct of any level.
    threshold_pct means percentage distance from level price.
    """
    required_candle_cols = {"timestamp", "close"}
    required_level_cols = {"timestamp", "level_type", "price", "index"}

    if not required_candle_cols.issubset(candles.columns):
        raise ValueError("Candles must include: timestamp, close")
    if not required_level_cols.issubset(levels.columns):
        raise ValueError("Levels must include: timestamp, level_type, price, index")

    rows = []
    for _, candle in candles.iterrows():
        c_ts = candle["timestamp"]
        c_close = float(candle["close"])

        for _, lvl in levels.iterrows():
            l_price = float(lvl["price"])
            dist_pct = abs(c_close - l_price) / l_price * 100.0

            if dist_pct <= threshold_pct:
                rows.append(
                    {
                        "timestamp": c_ts,
                        "close": c_close,
                        "level_type": lvl["level_type"],
                        "level_price": l_price,
                        "distance_pct": round(dist_pct, 4),
                        "signal": "near_level",
                    }
                )

    if not rows:
        return pd.DataFrame(
            columns=[
                "timestamp",
                "close",
                "level_type",
                "level_price",
                "distance_pct",
                "signal",
            ]
        )

    return pd.DataFrame(rows).sort_values(by=["timestamp", "distance_pct"]).reset_index(drop=True)

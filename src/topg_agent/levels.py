from __future__ import annotations

import pandas as pd


def detect_swing_levels(df: pd.DataFrame, left: int = 2, right: int = 2) -> pd.DataFrame:
    """
    Detect simple swing highs/lows.

    A swing high at i means high[i] is the maximum in window [i-left, i+right].
    A swing low at i means low[i] is the minimum in that window.
    """
    if not {"high", "low", "timestamp"}.issubset(df.columns):
        raise ValueError("Input DataFrame must include: timestamp, high, low")

    highs = []
    lows = []

    for i in range(len(df)):
        l = i - left
        r = i + right
        if l < 0 or r >= len(df):
            continue

        window_high = df["high"].iloc[l : r + 1]
        window_low = df["low"].iloc[l : r + 1]

        if df["high"].iloc[i] == window_high.max():
            highs.append(
                {
                    "timestamp": df["timestamp"].iloc[i],
                    "level_type": "swing_high",
                    "price": float(df["high"].iloc[i]),
                    "index": i,
                }
            )

        if df["low"].iloc[i] == window_low.min():
            lows.append(
                {
                    "timestamp": df["timestamp"].iloc[i],
                    "level_type": "swing_low",
                    "price": float(df["low"].iloc[i]),
                    "index": i,
                }
            )

    out = pd.DataFrame(highs + lows)
    if out.empty:
        return pd.DataFrame(columns=["timestamp", "level_type", "price", "index"])

    return out.sort_values(by=["index", "level_type"]).reset_index(drop=True)

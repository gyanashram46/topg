from __future__ import annotations

import pandas as pd


_REQUIRED = {"timestamp", "open", "high", "low", "close"}


def _is_red(candle: pd.Series) -> bool:
    return float(candle["close"]) < float(candle["open"])


def _is_green(candle: pd.Series) -> bool:
    return float(candle["close"]) > float(candle["open"])


def detect_structure(df: pd.DataFrame, retracement_candles: int = 2) -> pd.DataFrame:
    """
    Deterministic market-structure approximation.

    Bullish confirmation:
    - previous N candles are red retracement candles
    - current close breaks above highs of retracement candles

    Bearish confirmation (mirror):
    - previous N candles are green retracement candles
    - current close breaks below lows of retracement candles
    """
    if not _REQUIRED.issubset(df.columns):
        raise ValueError("Input DataFrame must include: timestamp, open, high, low, close")

    rows: list[dict[str, object]] = []
    state = "neutral"
    last_confirmed_high: float | None = None
    last_confirmed_low: float | None = None

    for i in range(len(df)):
        candle = df.iloc[i]
        confirmed_high = None
        confirmed_low = None
        level_1 = None
        level_2 = None
        notes = ""

        if i >= retracement_candles:
            lookback = df.iloc[i - retracement_candles : i]
            retracement_high = float(lookback["high"].max())
            retracement_low = float(lookback["low"].min())

            if all(_is_red(lookback.iloc[j]) for j in range(len(lookback))) and float(candle["close"]) > retracement_high:
                state = "bullish"
                confirmed_high = float(candle["high"])
                last_confirmed_high = confirmed_high
                level_1 = retracement_high
                level_2 = retracement_low
                notes = "bullish confirmation: 2-red retracement + close-through"

            elif all(_is_green(lookback.iloc[j]) for j in range(len(lookback))) and float(candle["close"]) < retracement_low:
                state = "bearish"
                confirmed_low = float(candle["low"])
                last_confirmed_low = confirmed_low
                level_1 = retracement_low
                level_2 = retracement_high
                notes = "bearish confirmation: 2-green retracement + close-through"

        if confirmed_high is None:
            confirmed_high = last_confirmed_high
        if confirmed_low is None:
            confirmed_low = last_confirmed_low

        rows.append(
            {
                "timestamp": candle["timestamp"],
                "candle_index": i,
                "structure_state": state,
                "confirmed_high": confirmed_high,
                "confirmed_low": confirmed_low,
                "level_1": level_1,
                "level_2": level_2,
                "notes": notes,
            }
        )

    return pd.DataFrame(rows)

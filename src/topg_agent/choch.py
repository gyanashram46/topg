from __future__ import annotations

import math

import pandas as pd


_REQUIRED = {"timestamp", "open", "high", "low", "close"}


def _price_or_none(value: object) -> float | None:
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return None
    return float(value)


def detect_choch_events(
    candles: pd.DataFrame,
    structure: pd.DataFrame,
    two_candle_confirm: bool = True,
    wick_plus_body_buffer_pct: float = 1.0,
) -> pd.DataFrame:
    """
    Detect CHoCH events using confirmed structure levels.

    Bullish CHoCH: 2 closes above last confirmed resistance/high.
    Bearish CHoCH: 2 closes below last confirmed support/low.
    """
    if not _REQUIRED.issubset(candles.columns):
        raise ValueError("Candles must include: timestamp, open, high, low, close")
    if not {"timestamp", "confirmed_high", "confirmed_low"}.issubset(structure.columns):
        raise ValueError("Structure must include: timestamp, confirmed_high, confirmed_low")

    merged = candles.copy().reset_index(drop=True)
    merged["confirmed_high"] = structure["confirmed_high"].reset_index(drop=True)
    merged["confirmed_low"] = structure["confirmed_low"].reset_index(drop=True)
    merged["confirmed_high"] = merged["confirmed_high"].ffill()
    merged["confirmed_low"] = merged["confirmed_low"].ffill()

    rows: list[dict[str, object]] = []

    for i in range(1, len(merged)):
        row = merged.iloc[i]
        prev = merged.iloc[i - 1]

        resistance = _price_or_none(row["confirmed_high"])
        support = _price_or_none(row["confirmed_low"])

        close_now = float(row["close"])
        close_prev = float(prev["close"])
        open_now = float(row["open"])
        high_now = float(row["high"])
        low_now = float(row["low"])

        body = abs(close_now - open_now)
        buffer_points = body * (wick_plus_body_buffer_pct / 100.0)

        if resistance is not None:
            bullish_ok = close_now > resistance and (close_prev > resistance if two_candle_confirm else True)
            if bullish_ok:
                rows.append(
                    {
                        "timestamp": row["timestamp"],
                        "candle_index": i,
                        "direction": "bullish",
                        "reference_level": resistance,
                        "confirm_candle_1_ts": prev["timestamp"] if two_candle_confirm else row["timestamp"],
                        "confirm_candle_2_ts": row["timestamp"],
                        "zone_rbs": low_now - buffer_points,
                        "zone_sbr": None,
                        "zone_a_plus": (high_now + low_now) / 2.0,
                        "zone_db": min(open_now, close_now) - buffer_points,
                        "zone_dt": None,
                    }
                )

        if support is not None:
            bearish_ok = close_now < support and (close_prev < support if two_candle_confirm else True)
            if bearish_ok:
                rows.append(
                    {
                        "timestamp": row["timestamp"],
                        "candle_index": i,
                        "direction": "bearish",
                        "reference_level": support,
                        "confirm_candle_1_ts": prev["timestamp"] if two_candle_confirm else row["timestamp"],
                        "confirm_candle_2_ts": row["timestamp"],
                        "zone_rbs": None,
                        "zone_sbr": high_now + buffer_points,
                        "zone_a_plus": (high_now + low_now) / 2.0,
                        "zone_db": None,
                        "zone_dt": max(open_now, close_now) + buffer_points,
                    }
                )

    if not rows:
        return pd.DataFrame(
            columns=[
                "timestamp",
                "candle_index",
                "direction",
                "reference_level",
                "confirm_candle_1_ts",
                "confirm_candle_2_ts",
                "zone_rbs",
                "zone_sbr",
                "zone_a_plus",
                "zone_db",
                "zone_dt",
            ]
        )

    events = pd.DataFrame(rows)
    events = events.drop_duplicates(subset=["timestamp", "direction", "reference_level"])  # deterministic
    return events.sort_values(by=["candle_index", "direction"]).reset_index(drop=True)

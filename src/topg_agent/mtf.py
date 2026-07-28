from __future__ import annotations

from zoneinfo import ZoneInfo

import pandas as pd


def infer_bias_from_candles(df: pd.DataFrame) -> str:
    if df.empty:
        return "neutral"
    open_first = float(df["open"].iloc[0])
    close_last = float(df["close"].iloc[-1])
    if close_last > open_first:
        return "bullish"
    if close_last < open_first:
        return "bearish"
    return "neutral"


def derive_mtf_biases(candles: pd.DataFrame, timezone: str = "Asia/Kolkata") -> dict[str, str]:
    if candles.empty:
        return {"daily_bias": "neutral", "h4_bias": "neutral", "h1_bias": "neutral"}

    ts = pd.to_datetime(candles["timestamp"], utc=True).dt.tz_convert(ZoneInfo(timezone))
    temp = candles.copy()
    temp["_ts"] = ts
    temp = temp.set_index("_ts").sort_index()

    ohlc_map = {"open": "first", "high": "max", "low": "min", "close": "last"}

    d = temp.resample("1D").agg(ohlc_map).dropna()
    h4 = temp.resample("4h").agg(ohlc_map).dropna()
    h1 = temp.resample("1h").agg(ohlc_map).dropna()

    return {
        "daily_bias": infer_bias_from_candles(d.reset_index(drop=True)) if not d.empty else infer_bias_from_candles(candles),
        "h4_bias": infer_bias_from_candles(h4.reset_index(drop=True)) if not h4.empty else infer_bias_from_candles(candles),
        "h1_bias": infer_bias_from_candles(h1.reset_index(drop=True)) if not h1.empty else infer_bias_from_candles(candles),
    }


def classify_mtf_condition(daily_bias: str, h4_bias: str, h1_bias: str) -> tuple[str, str, bool]:
    daily = (daily_bias or "neutral").lower()
    h4 = (h4_bias or "neutral").lower()
    h1 = (h1_bias or "neutral").lower()

    tradable = {"bullish", "bearish"}
    if daily not in tradable or h4 not in tradable or h1 not in tradable:
        return "MTF_DATA_MISSING", "none", False

    if daily == h4 == h1:
        return "D_4H_1H_ALIGNED", "1m_or_5m_marker", True

    if daily == h4 and h1 != daily:
        return "H1_OPPOSITE_D_4H", "5m_choch", True

    if h1 == h4 and h1 != daily:
        return "H1_4H_OPPOSITE_D", "1H_choch", True

    return "MTF_FILTER_FAIL", "none", False


def apply_mtf_filter(
    setups: pd.DataFrame,
    daily_bias: str,
    h4_bias: str,
    h1_bias: str,
) -> pd.DataFrame:
    condition, required_tf, mtf_pass = classify_mtf_condition(daily_bias, h4_bias, h1_bias)

    out = setups.copy()
    out["daily_bias"] = daily_bias
    out["h4_bias"] = h4_bias
    out["h1_bias"] = h1_bias
    out["mtf_condition"] = condition
    out["required_confirmation_tf"] = required_tf
    out["mtf_pass"] = bool(mtf_pass)
    return out

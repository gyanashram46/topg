from __future__ import annotations

import math

import pandas as pd

from .config import AppConfig
from .news import is_blackout
from .risk import clamp_daily_risk_pct, compute_rr


def _pick_entry_sl_tp(row: pd.Series, min_rr: float) -> tuple[float, float, float]:
    entry = float(row.get("entry_price", row.get("close", 0.0)))
    ref = float(row.get("reference_level", entry))
    direction = str(row.get("direction", "")).lower()

    if direction == "bullish":
        floor = [x for x in [row.get("zone_rbs"), row.get("zone_db"), ref] if x is not None and not (isinstance(x, float) and math.isnan(x))]
        stop_loss = float(min(floor)) if floor else ref
        take_profit = entry + abs(entry - stop_loss) * min_rr
    else:
        ceiling = [x for x in [row.get("zone_sbr"), row.get("zone_dt"), ref] if x is not None and not (isinstance(x, float) and math.isnan(x))]
        stop_loss = float(max(ceiling)) if ceiling else ref
        take_profit = entry - abs(stop_loss - entry) * min_rr

    return entry, stop_loss, take_profit


def build_candidate_setups(choch_events: pd.DataFrame, candles: pd.DataFrame, cfg: AppConfig) -> pd.DataFrame:
    if choch_events.empty:
        return pd.DataFrame(
            columns=[
                "timestamp",
                "direction",
                "reference_level",
                "entry_price",
                "stop_loss",
                "take_profit",
                "rr",
                "daily_risk_pct",
            ]
        )

    candle_cols = candles[["timestamp", "close"]].rename(columns={"close": "entry_price"})
    merged = choch_events.merge(candle_cols, on="timestamp", how="left")

    rows: list[dict[str, object]] = []
    for _, row in merged.iterrows():
        entry, sl, tp = _pick_entry_sl_tp(row, cfg.risk.min_rr)
        rr = compute_rr(entry, sl, tp)
        daily_risk_pct = clamp_daily_risk_pct(cfg.risk.daily_risk_pct_min, cfg.risk.daily_risk_pct_min, cfg.risk.daily_risk_pct_max)

        out = row.to_dict()
        out.update(
            {
                "entry_price": entry,
                "stop_loss": sl,
                "take_profit": tp,
                "rr": rr,
                "daily_risk_pct": daily_risk_pct,
            }
        )
        rows.append(out)

    return pd.DataFrame(rows)


def validate_setups(setups: pd.DataFrame, cfg: AppConfig, news_events: pd.DataFrame | None = None) -> tuple[pd.DataFrame, pd.DataFrame]:
    if setups.empty:
        empty_cols = [
            "timestamp",
            "direction",
            "reference_level",
            "entry_price",
            "stop_loss",
            "take_profit",
            "rr",
            "daily_risk_pct",
            "mtf_condition",
            "required_confirmation_tf",
            "mtf_pass",
            "news_blackout",
            "news_reason",
            "is_valid",
            "reject_reason",
        ]
        empty = pd.DataFrame(columns=empty_cols)
        return empty.copy(), empty.copy()

    out = setups.copy()
    reject_reasons: list[str] = []
    is_valid_flags: list[bool] = []
    news_flags: list[bool] = []
    news_reasons: list[str] = []

    for _, row in out.iterrows():
        blackout, news_reason = is_blackout(
            str(row["timestamp"]),
            timezone=cfg.timezone,
            events=news_events,
            default_templates=cfg.news.default_blackout_templates,
        )
        news_flags.append(blackout)
        news_reasons.append(news_reason)

        reason = ""
        if pd.isna(row.get("reference_level")):
            reason = "MISSING_STRUCTURE"
        elif blackout:
            reason = "NEWS_BLACKOUT"
        elif not bool(row.get("mtf_pass", False)):
            reason = "MTF_FILTER_FAIL"
        elif float(row.get("rr", 0.0)) < cfg.risk.min_rr:
            reason = "RR_BELOW_MIN"
        elif not (cfg.risk.daily_risk_pct_min <= float(row.get("daily_risk_pct", 0.0)) <= cfg.risk.daily_risk_pct_max):
            reason = "DAILY_RISK_OUT_OF_BOUNDS"

        valid = reason == ""
        is_valid_flags.append(valid)
        reject_reasons.append(reason)

    out["news_blackout"] = news_flags
    out["news_reason"] = news_reasons
    out["is_valid"] = is_valid_flags
    out["reject_reason"] = reject_reasons

    valid_setups = out[out["is_valid"]].copy().reset_index(drop=True)
    rejected_setups = out[~out["is_valid"]].copy().reset_index(drop=True)

    return valid_setups, rejected_setups

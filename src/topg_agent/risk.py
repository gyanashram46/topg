from __future__ import annotations

import math


def compute_rr(entry_price: float, stop_loss: float, take_profit: float) -> float:
    risk = abs(entry_price - stop_loss)
    reward = abs(take_profit - entry_price)
    if risk <= 0:
        return 0.0
    return reward / risk


def clamp_daily_risk_pct(value: float, minimum: float, maximum: float) -> float:
    if math.isnan(value):
        return minimum
    return min(max(value, minimum), maximum)

import pandas as pd

from src.topg_agent.choch import detect_choch_events


def test_detect_choch_requires_two_candle_confirmation():
    candles = pd.DataFrame(
        [
            {"timestamp": "2026-01-01T09:15:00Z", "open": 100.0, "high": 101.0, "low": 99.5, "close": 100.4},
            {"timestamp": "2026-01-01T09:20:00Z", "open": 100.4, "high": 101.2, "low": 100.0, "close": 101.1},
            {"timestamp": "2026-01-01T09:25:00Z", "open": 101.1, "high": 101.8, "low": 100.9, "close": 101.4},
        ]
    )
    structure = pd.DataFrame(
        [
            {"timestamp": "2026-01-01T09:15:00Z", "confirmed_high": 101.0, "confirmed_low": None},
            {"timestamp": "2026-01-01T09:20:00Z", "confirmed_high": 101.0, "confirmed_low": None},
            {"timestamp": "2026-01-01T09:25:00Z", "confirmed_high": 101.0, "confirmed_low": None},
        ]
    )

    events = detect_choch_events(candles, structure, two_candle_confirm=True)

    assert len(events) == 1
    assert events.iloc[0]["direction"] == "bullish"
    assert events.iloc[0]["timestamp"] == "2026-01-01T09:25:00Z"

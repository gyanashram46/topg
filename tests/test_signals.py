from src.topg_agent.io import load_ohlc_csv
from src.topg_agent.levels import detect_swing_levels
from src.topg_agent.signals import generate_proximity_signals


def test_generate_proximity_signals_columns():
    candles = load_ohlc_csv("data/sample_ohlc.csv")
    levels = detect_swing_levels(candles, left=1, right=1)
    signals = generate_proximity_signals(candles, levels, threshold_pct=0.5)

    expected = {"timestamp", "close", "level_type", "level_price", "distance_pct", "signal"}
    assert expected.issubset(signals.columns)

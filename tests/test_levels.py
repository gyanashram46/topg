from src.topg_agent.levels import detect_swing_levels
from src.topg_agent.io import load_ohlc_csv


def test_detect_swing_levels_returns_dataframe_shape():
    df = load_ohlc_csv("data/sample_ohlc.csv")
    levels = detect_swing_levels(df, left=1, right=1)

    assert set(["timestamp", "level_type", "price", "index"]).issubset(levels.columns)

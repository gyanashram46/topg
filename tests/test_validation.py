import pandas as pd

from src.topg_agent.config import AppConfig
from src.topg_agent.validation import validate_setups


def test_validation_partitions_valid_and_rejected_with_reason():
    cfg = AppConfig()
    setups = pd.DataFrame(
        [
            {
                "timestamp": "2026-08-01T01:00:00Z",
                "direction": "bullish",
                "reference_level": 100.0,
                "entry_price": 101.0,
                "stop_loss": 100.0,
                "take_profit": 103.5,
                "rr": 2.5,
                "daily_risk_pct": 1.5,
                "mtf_pass": True,
                "mtf_condition": "D_4H_1H_ALIGNED",
                "required_confirmation_tf": "1m_or_5m_marker",
            },
            {
                "timestamp": "2026-08-01T01:10:00Z",
                "direction": "bearish",
                "reference_level": 100.0,
                "entry_price": 99.8,
                "stop_loss": 100.2,
                "take_profit": 99.4,
                "rr": 1.0,
                "daily_risk_pct": 1.5,
                "mtf_pass": True,
                "mtf_condition": "D_4H_1H_ALIGNED",
                "required_confirmation_tf": "1m_or_5m_marker",
            },
        ]
    )

    valid, rejected = validate_setups(setups, cfg, news_events=pd.DataFrame())

    assert len(valid) == 1
    assert len(rejected) == 1
    assert rejected.iloc[0]["reject_reason"] == "RR_BELOW_MIN"

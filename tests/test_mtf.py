from src.topg_agent.mtf import classify_mtf_condition


def test_mtf_classification_aligned():
    condition, required_tf, mtf_pass = classify_mtf_condition("bullish", "bullish", "bullish")
    assert condition == "D_4H_1H_ALIGNED"
    assert required_tf == "1m_or_5m_marker"
    assert mtf_pass is True


def test_mtf_classification_h1_opposite():
    condition, required_tf, mtf_pass = classify_mtf_condition("bullish", "bullish", "bearish")
    assert condition == "H1_OPPOSITE_D_4H"
    assert required_tf == "5m_choch"
    assert mtf_pass is True


def test_mtf_classification_fail_on_missing_data():
    condition, required_tf, mtf_pass = classify_mtf_condition("bullish", "neutral", "bearish")
    assert condition == "MTF_DATA_MISSING"
    assert required_tf == "none"
    assert mtf_pass is False

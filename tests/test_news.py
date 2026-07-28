from pathlib import Path

from src.topg_agent.news import is_blackout, load_news_events


def test_news_blackout_detection_from_csv(tmp_path: Path):
    csv_path = tmp_path / "news_events.csv"
    csv_path.write_text(
        "event_name,event_time_ist,window_before_min,window_after_min\n"
        "FOMC,2026-08-01 23:30:00,30,30\n",
        encoding="utf-8",
    )

    events = load_news_events(csv_path)
    blackout, reason = is_blackout("2026-08-01T18:05:00Z", timezone="Asia/Kolkata", events=events, default_templates=[])

    assert blackout is True
    assert reason == "NEWS_BLACKOUT:FOMC"

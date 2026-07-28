from __future__ import annotations

from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

import pandas as pd


_REQUIRED = {"event_name", "event_time_ist", "window_before_min", "window_after_min"}


def load_news_events(path: str | Path) -> pd.DataFrame:
    p = Path(path)
    if not p.exists():
        return pd.DataFrame(columns=sorted(_REQUIRED))

    df = pd.read_csv(p)
    missing = _REQUIRED - set(df.columns)
    if missing:
        raise ValueError(f"Missing required news columns: {sorted(missing)}")

    return df.copy()


def _parse_ist_timestamp(ts: str, timezone: str) -> datetime:
    dt = pd.to_datetime(ts, utc=True).to_pydatetime()
    return dt.astimezone(ZoneInfo(timezone))


def _build_template_windows(anchor: datetime, templates: list[dict[str, str | int]]) -> list[tuple[datetime, datetime, str]]:
    windows: list[tuple[datetime, datetime, str]] = []
    local_day = anchor.date()

    for item in templates:
        hh, mm = str(item["time_ist"]).split(":")
        event_dt = datetime(
            local_day.year,
            local_day.month,
            local_day.day,
            int(hh),
            int(mm),
            tzinfo=anchor.tzinfo,
        )
        before = int(item["window_before_min"])
        after = int(item["window_after_min"])
        start = event_dt - timedelta(minutes=before)
        end = event_dt + timedelta(minutes=after)
        windows.append((start, end, str(item["event_name"])))

    return windows


def is_blackout(
    timestamp: str,
    timezone: str = "Asia/Kolkata",
    events: pd.DataFrame | None = None,
    default_templates: list[dict[str, str | int]] | None = None,
) -> tuple[bool, str]:
    ts_ist = _parse_ist_timestamp(timestamp, timezone)

    if events is not None and not events.empty:
        for _, row in events.iterrows():
            event_time = pd.to_datetime(row["event_time_ist"])
            if event_time.tzinfo is None:
                event_time = event_time.tz_localize(ZoneInfo(timezone))
            else:
                event_time = event_time.tz_convert(ZoneInfo(timezone))

            start = event_time - timedelta(minutes=int(row["window_before_min"]))
            end = event_time + timedelta(minutes=int(row["window_after_min"]))
            if start <= ts_ist <= end:
                return True, f"NEWS_BLACKOUT:{row['event_name']}"

    if default_templates:
        for start, end, name in _build_template_windows(ts_ist, default_templates):
            if start <= ts_ist <= end:
                return True, f"NEWS_BLACKOUT:{name}"

    return False, ""

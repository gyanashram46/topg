from dataclasses import dataclass, field


@dataclass
class SwingConfig:
    left_bars: int = 2
    right_bars: int = 2


@dataclass
class SignalConfig:
    proximity_threshold_pct: float = 0.15


@dataclass
class StructureConfig:
    retracement_candles: int = 2
    choch_two_candle_confirm: bool = True
    wick_plus_body_buffer_pct: float = 1.0


@dataclass
class MTFConfig:
    daily_label: str = "1D"
    h4_label: str = "4H"
    h1_label: str = "1H"


@dataclass
class RiskConfig:
    daily_risk_pct_min: float = 1.0
    daily_risk_pct_max: float = 2.0
    min_rr: float = 2.0


@dataclass
class NewsConfig:
    news_events_csv: str = "data/news_events.csv"
    default_blackout_templates: list[dict[str, str | int]] = field(
        default_factory=lambda: [
            {"event_name": "FOMC_PLACEHOLDER", "time_ist": "23:30", "window_before_min": 30, "window_after_min": 30},
            {"event_name": "CPI_PLACEHOLDER", "time_ist": "18:00", "window_before_min": 30, "window_after_min": 30},
            {"event_name": "NFP_PLACEHOLDER", "time_ist": "18:00", "window_before_min": 30, "window_after_min": 30},
        ]
    )


@dataclass
class AppConfig:
    instrument: str = "XAUUSD"
    timezone: str = "Asia/Kolkata"
    mode: str = "A"
    swing: SwingConfig = field(default_factory=SwingConfig)
    signal: SignalConfig = field(default_factory=SignalConfig)
    structure: StructureConfig = field(default_factory=StructureConfig)
    mtf: MTFConfig = field(default_factory=MTFConfig)
    risk: RiskConfig = field(default_factory=RiskConfig)
    news: NewsConfig = field(default_factory=NewsConfig)

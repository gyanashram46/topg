from dataclasses import dataclass


@dataclass
class SwingConfig:
    left_bars: int = 2
    right_bars: int = 2


@dataclass
class SignalConfig:
    proximity_threshold_pct: float = 0.15


@dataclass
class AppConfig:
    swing: SwingConfig = SwingConfig()
    signal: SignalConfig = SignalConfig()

# Strategy Rules (Machine-Readable Template)

Fill this file with your exact trading strategy so the agent can execute it deterministically.

## 1) Instruments
- Symbols:
- Market type: (spot/futures/options)

## 2) Timeframes
- Higher timeframe (bias):
- Execution timeframe:
- Confirmation timeframe (optional):

## 3) Trading session filters
- Allowed days:
- Allowed time window (timezone):
- News/event blackout rules:

## 4) Levels to mark
- Daily high/low:
- Weekly high/low:
- Swing highs/lows:
- Other custom levels:

## 5) Market structure definitions
- Trend definition:
- Break of structure (BOS):
- Change of character (CHOCH):

## 6) Entry model
- Long entry conditions:
- Short entry conditions:
- Candle patterns required (if any):

## 7) Risk management
- Risk per trade (%):
- Max trades/day:
- Stop loss placement rule:
- Position sizing formula:

## 8) Exit model
- Take profit rule(s):
- Partial exits:
- Trailing stop logic:
- Invalidation/early exit:

## 9) Logging & alerts
- What should be alerted:
- Alert channel: (console/telegram/discord/email)

## 10) Non-negotiable constraints
- Do-not-trade conditions:
- Slippage/spread guardrails:
- Data quality checks:

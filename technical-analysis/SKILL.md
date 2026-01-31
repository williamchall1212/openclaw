---
name: technical_analysis
description: Calculate technical indicators (SMA, EMA, RSI, MACD, Bollinger Bands) for stock analysis and options trading
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["python3"] },
        "os": ["darwin", "linux", "win32"],
        "homepage": "https://github.com/twopirllc/pandas-ta",
      },
  }
---

# Technical Analysis Skill

Calculate technical indicators for stock analysis and options trading decisions.

## Installation

Install required Python libraries:

```bash
pip3 install yfinance pandas pandas-ta
```

Or using uv (faster):

```bash
uv pip install yfinance pandas pandas-ta
```

## Available Commands

### Calculate all key indicators

Get current technical setup with all major indicators:

```bash
python3 ./technical-analysis/scripts/analyze.py TICKER
```

Example:
```bash
python3 ./technical-analysis/scripts/analyze.py TSLA
```

Returns JSON with:
- Current price and recent price action
- SMA (20, 50, 200-day)
- EMA (12, 26-day)
- RSI (14-day)
- MACD (12, 26, 9)
- Bollinger Bands (20-day, 2 std dev)
- Support/resistance levels
- Price position relative to key moving averages
- Trend analysis

### Calculate indicators with custom period

Specify historical period for analysis:

```bash
python3 ./technical-analysis/scripts/analyze.py TICKER PERIOD
```

Supported periods: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max

Example:
```bash
python3 ./technical-analysis/scripts/analyze.py AAPL 1y
```

### Find support and resistance levels

Identify key price levels:

```bash
python3 ./technical-analysis/scripts/levels.py TICKER
```

Returns major support and resistance zones based on:
- Historical swing highs/lows
- Volume profile
- Moving average clusters

### Generate chart with indicators

Create a visual chart with price and all indicators:

```bash
python3 ./technical-analysis/scripts/chart.py TICKER PERIOD OUTPUT_FILE
```

Example:
```bash
python3 ./technical-analysis/scripts/chart.py SPY 6mo spy_chart.png
```

## Output Format

All commands return JSON for easy parsing by the agent. Example output:

```json
{
  "ticker": "TSLA",
  "current_price": 242.50,
  "price_change_1d": 2.3,
  "price_change_pct_1d": 0.96,
  "volume": 125000000,
  "sma_20": 238.75,
  "sma_50": 235.20,
  "sma_200": 220.45,
  "ema_12": 240.15,
  "ema_26": 237.80,
  "rsi_14": 58.3,
  "macd": 2.35,
  "macd_signal": 1.85,
  "macd_histogram": 0.50,
  "bb_upper": 252.30,
  "bb_middle": 238.75,
  "bb_lower": 225.20,
  "price_vs_sma_50": "above",
  "price_vs_sma_200": "above",
  "trend": "bullish",
  "support_levels": [235.20, 220.45, 210.00],
  "resistance_levels": [250.00, 265.50, 280.00]
}
```

## Use Cases for Options Trading

### Analyzing Options Flow

When you receive unusual options activity:

1. Get current technical setup:
   ```bash
   python3 ./technical-analysis/scripts/analyze.py TICKER
   ```

2. Identify if price is near key support/resistance:
   - Price above 200-day SMA = long-term bullish trend
   - Price below 50-day SMA = potential weakness
   - RSI > 70 = overbought, RSI < 30 = oversold
   - MACD crossover = momentum shift

3. Use support/resistance for strike selection:
   - Protective puts near support levels
   - Covered calls near resistance
   - Risk reversals using support (put) and resistance (call)

### Conservative Trade Scenarios

**Bullish Setup (Large Call Buying):**
- Price above 50-day and 200-day SMA
- RSI between 40-60 (not overbought)
- MACD positive and rising
- → Consider: Buying calls at ATM or slight OTM, 60-90 DTE

**Bearish Setup (Large Put Buying):**
- Price below 50-day SMA
- RSI trending down
- MACD negative
- → Consider: Protective puts at support levels, 30-60 DTE

**Range-Bound Setup:**
- Price oscillating between support/resistance
- RSI cycling between 30-70
- → Consider: Iron condor or risk reversal using the range

## Notes

- All data sourced from Yahoo Finance (free, no API key)
- Indicators calculated using pandas-ta library
- Historical data cached for performance
- Works with US stocks, ETFs, crypto (BTC-USD), and forex
- For international stocks, use proper suffix (.L for London, .TO for Toronto, etc.)

## Dependencies

- yfinance: Yahoo Finance data fetching
- pandas: Data manipulation and analysis
- pandas-ta: Technical analysis indicator library

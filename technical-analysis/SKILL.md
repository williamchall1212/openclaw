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
- EMA (8, 10, 21-day)
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
  "day_label": "today",
  "volume": 125000000,
  "sma_20": 238.75,
  "sma_50": 235.20,
  "sma_200": 220.45,
  "ema_8": 241.30,
  "ema_10": 240.15,
  "ema_21": 237.80,
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

### Intelligent Date Handling

The `day_label` field automatically handles market hours:
- On weekdays when the market was open: `"today"`
- On weekends or after-hours: the actual day name (e.g., `"Friday"`)

When formatting responses, always use the `day_label` field instead of hardcoding "today":

**Correct formatting:**
```
Current Price: $242.50 (+$2.30 / +0.96% today)          # When day_label = "today"
Current Price: $242.50 (+$2.30 / +0.96% Friday)         # When day_label = "Friday"
```

**Incorrect formatting:**
```
Current Price: $242.50 (+$2.30 / +0.96% today)          # On Saturday (misleading!)
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

**Bearish Setup (Selling Calls / Call Spreads):**
- Price below 50-day SMA (confirmed downtrend)
- Price below 20-day SMA (short-term weakness)
- → Consider: Selling naked calls or bear call spreads at or above resistance levels, 30-45 DTE
- Strike selection: Sell the short call at or just above the nearest resistance level
- For call spreads: Buy a further OTM call as a hedge (spread width of $5-$10 depending on stock price)
- Higher conviction if price is also below 200-day SMA (long-term bearish)
- Avoid if RSI < 20 (oversold bounce risk) or if earnings are within the expiration window

**Range-Bound Setup:**
- Price oscillating between support/resistance
- RSI cycling between 30-70
- → Consider: Iron condor or risk reversal using the range

## Notes

- All data sourced from Yahoo Finance (free, no API key)
- Indicators calculated using pandas-ta library
- **Intelligent incremental caching:**
  - Cache stored in `technical-analysis/.cache/` directory
  - Historical data cached permanently (it never changes)
  - New trading days automatically fetched and appended to cache
  - Each query uses cached data + fetches only new data since last cache update
  - Result: Always up-to-date data with minimal API calls
  - Cache files are automatically managed (no manual cleanup needed)
  - To force a full refresh, delete the cache file: `rm technical-analysis/.cache/TICKER_PERIOD.pkl`
- Works with US stocks, ETFs, crypto (BTC-USD), and forex
- For international stocks, use proper suffix (.L for London, .TO for Toronto, etc.)

## Dependencies

- yfinance: Yahoo Finance data fetching
- pandas: Data manipulation and analysis
- pandas-ta: Technical analysis indicator library

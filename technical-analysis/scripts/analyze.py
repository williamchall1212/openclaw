#!/usr/bin/env python3
"""
Technical analysis script for stock data.
Fetches stock data and calculates key technical indicators.
"""

import sys
import json
import os
import pickle
from datetime import datetime, timedelta
from pathlib import Path
import yfinance as yf
import pandas as pd
import pandas_ta as ta


# Cache configuration
# Incremental caching: historical data cached permanently, new data appended
CACHE_DIR = Path(__file__).parent.parent / '.cache'


def get_cache_path(ticker, period):
    """Get the cache file path for a ticker and period."""
    CACHE_DIR.mkdir(exist_ok=True)
    return CACHE_DIR / f"{ticker.upper()}_{period}.pkl"


def get_cached_data(ticker, period):
    """Retrieve cached data if it exists."""
    cache_file = get_cache_path(ticker, period)

    if not cache_file.exists():
        return None

    try:
        with open(cache_file, 'rb') as f:
            cached = pickle.load(f)
        return cached['data']
    except Exception:
        # If cache is corrupted, ignore it
        return None


def set_cached_data(ticker, period, data):
    """Store data in cache with timestamp."""
    cache_file = get_cache_path(ticker, period)

    try:
        cached = {
            'timestamp': datetime.now().timestamp(),
            'data': data
        }
        with open(cache_file, 'wb') as f:
            pickle.dump(cached, f)
    except Exception:
        # If caching fails, continue without it
        pass


def safe_round(value, decimals=2):
    """Safely round a value if it's not NaN, otherwise return None."""
    return round(value, decimals) if pd.notna(value) else None


def safe_get(series, column, decimals=2):
    """Safely get and round a value from a series if column exists and is not NaN."""
    if column in series and pd.notna(series[column]):
        return round(series[column], decimals)
    return None


def get_market_day_label(data):
    """
    Intelligently determine the label for the most recent trading day.
    Returns "today" if market was open today, otherwise returns the day name.
    """
    # Get the most recent data point timestamp
    latest_date = data.index[-1]

    # Convert to datetime if it's a timestamp
    if hasattr(latest_date, 'date'):
        latest_date = latest_date.date()
    else:
        latest_date = pd.to_datetime(latest_date).date()

    today = datetime.now().date()

    # If the latest data is from today, market was open today
    if latest_date == today:
        return "today"

    # Otherwise, return the day of the week
    day_names = {
        0: "Monday",
        1: "Tuesday",
        2: "Wednesday",
        3: "Thursday",
        4: "Friday",
        5: "Saturday",
        6: "Sunday"
    }

    # Get the weekday (0=Monday, 6=Sunday)
    weekday = latest_date.weekday()
    day_name = day_names[weekday]

    return day_name


def analyze_stock(ticker, period="1y"):
    """
    Analyze a stock and return technical indicators.
    Uses incremental caching: cached historical data + new data since last fetch.

    Args:
        ticker: Stock ticker symbol
        period: Data period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)

    Returns:
        Dictionary with technical analysis data
    """
    try:
        # Try to get cached data first
        cached_data = get_cached_data(ticker, period)
        stock = yf.Ticker(ticker)

        if cached_data is not None:
            # We have cached data - fetch only new data since last cache
            last_date = cached_data.index[-1]

            # Fetch data from the day after last cached date
            new_data = stock.history(start=last_date + timedelta(days=1))

            if not new_data.empty:
                # Append new data to cached data
                data = pd.concat([cached_data, new_data])
                # Remove duplicates (keep most recent)
                data = data[~data.index.duplicated(keep='last')]
                # Update cache with combined data
                set_cached_data(ticker, period, data)
            else:
                # No new data available, use cached data as-is
                data = cached_data
        else:
            # No cache exists - fetch full period
            data = stock.history(period=period)

            if data.empty:
                return {"error": f"No data found for ticker {ticker}"}

            # Cache the fresh data
            set_cached_data(ticker, period, data)

        if data.empty:
            return {"error": f"No data found for ticker {ticker}"}

        # Get current price and previous close
        current_price = data['Close'].iloc[-1]
        prev_close = data['Close'].iloc[-2] if len(data) > 1 else current_price

        # Calculate price change
        price_change = current_price - prev_close
        price_change_pct = (price_change / prev_close) * 100

        # Get intelligent day label
        day_label = get_market_day_label(data)

        # Calculate technical indicators
        # SMAs
        data['SMA_20'] = ta.sma(data['Close'], length=20)
        data['SMA_50'] = ta.sma(data['Close'], length=50)
        data['SMA_200'] = ta.sma(data['Close'], length=200)

        # EMAs
        data['EMA_8'] = ta.ema(data['Close'], length=8)
        data['EMA_10'] = ta.ema(data['Close'], length=10)
        data['EMA_21'] = ta.ema(data['Close'], length=21)

        # RSI
        data['RSI_14'] = ta.rsi(data['Close'], length=14)

        # MACD
        macd = ta.macd(data['Close'], fast=12, slow=26, signal=9)
        if macd is not None:
            data = pd.concat([data, macd], axis=1)

        # Bollinger Bands
        bbands = ta.bbands(data['Close'], length=20, std=2)
        if bbands is not None:
            data = pd.concat([data, bbands], axis=1)

        # Get latest values
        latest = data.iloc[-1]

        # Determine trend
        trend = "neutral"
        sma_50_val = latest['SMA_50'] if pd.notna(latest['SMA_50']) else None
        sma_200_val = latest['SMA_200'] if pd.notna(latest['SMA_200']) else None

        if sma_50_val and sma_200_val:
            if current_price > sma_50_val and current_price > sma_200_val:
                trend = "bullish"
            elif current_price < sma_50_val and current_price < sma_200_val:
                trend = "bearish"

        # Position relative to SMAs
        price_vs_sma_50 = "above" if sma_50_val and current_price > sma_50_val else ("below" if sma_50_val else "N/A")
        price_vs_sma_200 = "above" if sma_200_val and current_price > sma_200_val else ("below" if sma_200_val else "N/A")

        # Find support and resistance levels (simplified)
        highs = data['High'].tail(50)
        lows = data['Low'].tail(50)

        resistance_levels = sorted(highs.nlargest(3).tolist(), reverse=True)
        support_levels = sorted(lows.nsmallest(3).tolist())

        # Build result
        result = {
            "ticker": ticker.upper(),
            "current_price": round(current_price, 2),
            "price_change_1d": round(price_change, 2),
            "price_change_pct_1d": round(price_change_pct, 2),
            "day_label": day_label,  # This is the key field for intelligent date handling
            "volume": int(latest['Volume']),
            "sma_20": safe_round(latest['SMA_20']),
            "sma_50": safe_round(latest['SMA_50']),
            "sma_200": safe_round(latest['SMA_200']),
            "ema_8": safe_round(latest['EMA_8']),
            "ema_10": safe_round(latest['EMA_10']),
            "ema_21": safe_round(latest['EMA_21']),
            "rsi_14": safe_round(latest['RSI_14']),
            "macd": safe_get(latest, 'MACD_12_26_9', decimals=4),
            "macd_signal": safe_get(latest, 'MACDs_12_26_9', decimals=4),
            "macd_histogram": safe_get(latest, 'MACDh_12_26_9', decimals=4),
            "bb_upper": safe_get(latest, 'BBU_20_2.0'),
            "bb_middle": safe_get(latest, 'BBM_20_2.0'),
            "bb_lower": safe_get(latest, 'BBL_20_2.0'),
            "price_vs_sma_50": price_vs_sma_50,
            "price_vs_sma_200": price_vs_sma_200,
            "trend": trend,
            "support_levels": [round(x, 2) for x in support_levels],
            "resistance_levels": [round(x, 2) for x in resistance_levels]
        }

        return result

    except Exception as e:
        return {"error": str(e)}


def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: analyze.py TICKER [PERIOD]"}))
        sys.exit(1)

    ticker = sys.argv[1]
    period = sys.argv[2] if len(sys.argv) > 2 else "1y"

    result = analyze_stock(ticker, period)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

import pandas as pd
import numpy as np
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
OUT_DIR = BASE_DIR / "outputs"
OUT_DIR.mkdir(exist_ok=True)

PRICES_RAW = DATA_DIR / "prices_raw.csv"

TICKERS = ["SPY", "AAPL", "MSFT", "NVDA", "TSLA"]

# Settings
ROLL_VOL_WINDOW = 20      # 20 trading days ~ 1 month
MA_FAST = 20
MA_SLOW = 50

def compute_drawdown(value_series: pd.Series) -> pd.Series:
    peak = value_series.cummax()
    dd = (value_series / peak) - 1.0
    return dd

def main():
    df = pd.read_csv(PRICES_RAW, parse_dates=["date"])

    # Basic cleaning
    df = df[df["ticker"].isin(TICKERS)].copy()
    df = df.sort_values(["ticker", "date"])
    df = df.dropna(subset=["adj_close"])

    # Remove duplicates if any
    df = df.drop_duplicates(subset=["ticker", "date"], keep="last")

    # Per-ticker metrics
    df["daily_return"] = df.groupby("ticker")["adj_close"].pct_change()

    # Moving averages on price
    df[f"ma_{MA_FAST}"] = df.groupby("ticker")["adj_close"].transform(lambda s: s.rolling(MA_FAST).mean())
    df[f"ma_{MA_SLOW}"] = df.groupby("ticker")["adj_close"].transform(lambda s: s.rolling(MA_SLOW).mean())

    # Rolling volatility (std of daily returns)
    df[f"roll_vol_{ROLL_VOL_WINDOW}"] = df.groupby("ticker")["daily_return"].transform(
        lambda s: s.rolling(ROLL_VOL_WINDOW).std()
    )

    # Equity curve per ticker (start at 100)
    df["equity_100"] = df.groupby("ticker")["daily_return"].transform(
        lambda r: (1 + r.fillna(0)).cumprod() * 100
    )

    # Drawdown per ticker
    df["drawdown"] = df.groupby("ticker")["equity_100"].transform(compute_drawdown)

    # ========== Portfolio (equal weight, daily rebalanced for simplicity) ==========
    # Pivot returns: rows=date, cols=ticker
    ret_pivot = df.pivot(index="date", columns="ticker", values="daily_return").sort_index()

    # Equal-weight: mean of available returns each day (skip NaNs)
    portfolio_ret = ret_pivot.mean(axis=1, skipna=True)
    portfolio = pd.DataFrame({"date": portfolio_ret.index, "portfolio_daily_return": portfolio_ret.values})

    # Portfolio equity curve
    portfolio["portfolio_equity_100"] = (1 + portfolio["portfolio_daily_return"].fillna(0)).cumprod() * 100

    # Portfolio drawdown
    portfolio["portfolio_drawdown"] = compute_drawdown(portfolio["portfolio_equity_100"])

    # Portfolio rolling vol
    portfolio[f"portfolio_roll_vol_{ROLL_VOL_WINDOW}"] = portfolio["portfolio_daily_return"].rolling(ROLL_VOL_WINDOW).std()

    # ========== Data Quality table ==========
    dq = []
    for t in TICKERS:
        sub = df[df["ticker"] == t].copy()
        dq.append({
            "ticker": t,
            "rows": int(sub.shape[0]),
            "start_date": sub["date"].min().date().isoformat(),
            "end_date": sub["date"].max().date().isoformat(),
            "missing_returns": int(sub["daily_return"].isna().sum()),
            "missing_adj_close": int(sub["adj_close"].isna().sum()),
        })
    dq_df = pd.DataFrame(dq)

    # Save outputs
    prices_clean_path = DATA_DIR / "prices_clean.csv"
    portfolio_path = DATA_DIR / "portfolio_daily.csv"
    dq_path = DATA_DIR / "data_quality.csv"

    df.to_csv(prices_clean_path, index=False)
    portfolio.to_csv(portfolio_path, index=False)
    dq_df.to_csv(dq_path, index=False)

    print(f"Saved: {prices_clean_path}")
    print(f"Saved: {portfolio_path}")
    print(f"Saved: {dq_path}")
    print("\nPortfolio preview:")
    print(portfolio.head(10))

if __name__ == "__main__":
    main()
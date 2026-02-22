import pandas as pd
import yfinance as yf
from pathlib import Path

TICKERS = ["SPY", "AAPL", "MSFT", "NVDA", "TSLA"]
PERIOD = "5y"
INTERVAL = "1d"

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

def _flatten_cols(df: pd.DataFrame) -> pd.DataFrame:
    # yfinance can return MultiIndex columns; flatten to strings
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = ["_".join([str(x) for x in col if x is not None]).strip() for col in df.columns.values]
    df.columns = [str(c).lower().strip().replace(" ", "_") for c in df.columns]
    return df

def _standardize_for_ticker(df: pd.DataFrame, ticker: str) -> pd.DataFrame:
    """
    Your yfinance output looks like: open_spy, high_spy, ... date_
    We normalize that to: date, open, high, low, close, adj_close, volume
    """
    t = ticker.lower()

    # Fix date column variations like "date_"
    if "date" not in df.columns:
        date_candidates = [c for c in df.columns if c.startswith("date")]
        if date_candidates:
            df = df.rename(columns={date_candidates[0]: "date"})

    # If columns are suffixed by ticker, map them back
    rename_map = {}
    for base in ["open", "high", "low", "close", "adj_close", "volume"]:
        suffixed = f"{base}_{t}"
        if suffixed in df.columns:
            rename_map[suffixed] = base

    df = df.rename(columns=rename_map)

    # If adj_close missing, try to find any adj_close-like column and use it
    if "adj_close" not in df.columns:
        adj_candidates = [c for c in df.columns if "adj" in c and "close" in c]
        if adj_candidates:
            df = df.rename(columns={adj_candidates[0]: "adj_close"})

    # Final validation (fallback adj_close to close if needed)
    required = ["date", "open", "high", "low", "close", "volume"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise RuntimeError(
            f"Still missing columns for {ticker}: {missing}. Got columns: {list(df.columns)}"
        )

    if "adj_close" not in df.columns:
        df["adj_close"] = df["close"]

    df["ticker"] = ticker

    keep = ["date", "ticker", "open", "high", "low", "close", "adj_close", "volume"]
    df = df[keep].copy()
    return df

def main():
    all_rows = []

    for t in TICKERS:
        raw = yf.download(
            t,
            period=PERIOD,
            interval=INTERVAL,
            auto_adjust=False,
            progress=False,
            group_by="column",
        )

        if raw is None or raw.empty:
            raise RuntimeError(f"No data returned for {t}")

        df = raw.reset_index()
        df = _flatten_cols(df)
        df = _standardize_for_ticker(df, t)

        all_rows.append(df)

    out = pd.concat(all_rows, ignore_index=True)
    out = out.sort_values(["ticker", "date"])

    out_path = DATA_DIR / "prices_raw.csv"
    out.to_csv(out_path, index=False)

    print(f"Saved: {out_path}")
    print(out.head(10))

if __name__ == "__main__":
    main()
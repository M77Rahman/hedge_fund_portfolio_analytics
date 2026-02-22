import pandas as pd
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
OUT_DIR = BASE_DIR / "outputs"
OUT_DIR.mkdir(exist_ok=True)

DB_PATH = OUT_DIR / "market_data.sqlite"

FILES = {
    "prices_raw": DATA_DIR / "prices_raw.csv",
    "prices_clean": DATA_DIR / "prices_clean.csv",
    "portfolio_daily": DATA_DIR / "portfolio_daily.csv",
    "data_quality": DATA_DIR / "data_quality.csv",
}

def main():
    # Basic check
    for name, path in FILES.items():
        if not path.exists():
            raise FileNotFoundError(f"Missing {name} at {path}. Run the previous step first.")

    conn = sqlite3.connect(DB_PATH)

    try:
        for table, path in FILES.items():
            df = pd.read_csv(path)
            df.to_sql(table, conn, if_exists="replace", index=False)
            print(f"Loaded {table} ({len(df):,} rows)")

        # Indexes for performance
        cur = conn.cursor()
        cur.execute("CREATE INDEX IF NOT EXISTS idx_pricesclean_ticker_date ON prices_clean(ticker, date);")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_pricesraw_ticker_date ON prices_raw(ticker, date);")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_portfolio_date ON portfolio_daily(date);")
        conn.commit()

        print(f"\nSaved SQLite DB: {DB_PATH}")
    finally:
        conn.close()

if __name__ == "__main__":
    main()
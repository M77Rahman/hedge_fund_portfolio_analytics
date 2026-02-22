import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
OUT_DIR = BASE_DIR / "outputs"
OUT_DIR.mkdir(exist_ok=True)

sns.set_style("whitegrid")

# Load data
prices = pd.read_csv(DATA_DIR / "prices_clean.csv", parse_dates=["date"])
portfolio = pd.read_csv(DATA_DIR / "portfolio_daily.csv", parse_dates=["date"])

# -------- Portfolio Equity Curve --------
plt.figure(figsize=(10,6))
plt.plot(portfolio["date"], portfolio["portfolio_equity_100"])
plt.title("Portfolio Equity Curve (Base 100)")
plt.xlabel("Date")
plt.ylabel("Equity Value")
plt.tight_layout()
plt.savefig(OUT_DIR / "portfolio_equity.png")
plt.close()

# -------- Portfolio Drawdown --------
plt.figure(figsize=(10,6))
plt.plot(portfolio["date"], portfolio["portfolio_drawdown"])
plt.title("Portfolio Drawdown")
plt.xlabel("Date")
plt.ylabel("Drawdown")
plt.tight_layout()
plt.savefig(OUT_DIR / "portfolio_drawdown.png")
plt.close()

# -------- Asset Comparison --------
plt.figure(figsize=(10,6))
for ticker in prices["ticker"].unique():
    subset = prices[prices["ticker"] == ticker]
    plt.plot(subset["date"], subset["equity_100"], label=ticker)

plt.title("Asset Equity Curves (Base 100)")
plt.xlabel("Date")
plt.ylabel("Equity Value")
plt.legend()
plt.tight_layout()
plt.savefig(OUT_DIR / "asset_equity_comparison.png")
plt.close()

# -------- Rolling Volatility --------
plt.figure(figsize=(10,6))
for ticker in prices["ticker"].unique():
    subset = prices[prices["ticker"] == ticker]
    plt.plot(subset["date"], subset["roll_vol_20"], label=ticker)

plt.title("20-Day Rolling Volatility")
plt.xlabel("Date")
plt.ylabel("Volatility")
plt.legend()
plt.tight_layout()
plt.savefig(OUT_DIR / "rolling_volatility.png")
plt.close()

print("Charts generated in outputs/")
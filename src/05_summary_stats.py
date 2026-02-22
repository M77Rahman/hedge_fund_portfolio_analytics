import pandas as pd
import numpy as np
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
OUT_DIR = BASE_DIR / "outputs"
OUT_DIR.mkdir(exist_ok=True)

portfolio = pd.read_csv(DATA_DIR / "portfolio_daily.csv", parse_dates=["date"])
prices = pd.read_csv(DATA_DIR / "prices_clean.csv", parse_dates=["date"])

TRADING_DAYS = 252

def annualised_return(equity_series: pd.Series) -> float:
    start = float(equity_series.iloc[0])
    end = float(equity_series.iloc[-1])
    n_days = len(equity_series)
    years = n_days / TRADING_DAYS
    return (end / start) ** (1 / years) - 1

def annualised_vol(daily_ret: pd.Series) -> float:
    return float(daily_ret.dropna().std()) * np.sqrt(TRADING_DAYS)

def sharpe_ratio(ann_ret: float, ann_vol: float, rf: float = 0.0) -> float:
    if ann_vol == 0:
        return np.nan
    return (ann_ret - rf) / ann_vol

def max_drawdown(drawdown_series: pd.Series) -> float:
    return float(drawdown_series.min())

def main():
    # Portfolio stats
    port_equity = portfolio["portfolio_equity_100"]
    port_ret = portfolio["portfolio_daily_return"]
    port_dd = portfolio["portfolio_drawdown"]

    port_ann_ret = annualised_return(port_equity)
    port_ann_vol = annualised_vol(port_ret)
    port_sharpe = sharpe_ratio(port_ann_ret, port_ann_vol, rf=0.0)
    port_mdd = max_drawdown(port_dd)
    port_total_ret = (float(port_equity.iloc[-1]) / float(port_equity.iloc[0])) - 1

    summary = {
        "metric": [
            "Start date",
            "End date",
            "Total return",
            "Annualised return",
            "Annualised volatility",
            "Sharpe (rf=0)",
            "Max drawdown",
            "Assets",
            "Rebalance",
        ],
        "value": [
            portfolio["date"].min().date().isoformat(),
            portfolio["date"].max().date().isoformat(),
            f"{port_total_ret:.2%}",
            f"{port_ann_ret:.2%}",
            f"{port_ann_vol:.2%}",
            f"{port_sharpe:.2f}",
            f"{port_mdd:.2%}",
            ", ".join(sorted(prices["ticker"].unique())),
            "Daily (equal-weight, simple mean of available returns)"
        ],
    }

    summary_df = pd.DataFrame(summary)
    out_path = OUT_DIR / "performance_summary.csv"
    summary_df.to_csv(out_path, index=False)

    print(f"Saved: {out_path}")
    print(summary_df)

if __name__ == "__main__":
    main()
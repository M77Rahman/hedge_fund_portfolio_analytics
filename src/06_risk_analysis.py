import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
OUT_DIR = BASE_DIR / "outputs"

prices = pd.read_csv(DATA_DIR / "prices_clean.csv", parse_dates=["date"])
returns = prices.pivot(index="date", columns="ticker", values="daily_return").dropna()

# --- Correlation Matrix ---
corr = returns.corr()
plt.figure(figsize=(8, 6))
sns.heatmap(corr, annot=True, center=0)
plt.title("Asset Correlation Matrix")
plt.tight_layout()
plt.savefig(OUT_DIR / "correlation_matrix.png")
plt.close()

# --- Risk Contribution (equal weight) ---
tickers = list(returns.columns)
n = len(tickers)
weights = np.array([1/n] * n)

cov_matrix = returns.cov() * 252  # annualised covariance
portfolio_vol = float(np.sqrt(weights.T @ cov_matrix @ weights))

marginal_contrib = (cov_matrix @ weights) / portfolio_vol
risk_contrib = weights * marginal_contrib

risk_df = pd.DataFrame({
    "ticker": tickers,
    "weight": weights,
    "risk_contribution": risk_contrib,
})

risk_df["risk_contribution_pct"] = risk_df["risk_contribution"] / risk_df["risk_contribution"].sum()
risk_df = risk_df.sort_values("risk_contribution_pct", ascending=False)

risk_df.to_csv(OUT_DIR / "risk_contribution.csv", index=False)

# Bar chart
plt.figure(figsize=(9, 5))
plt.bar(risk_df["ticker"], risk_df["risk_contribution_pct"])
plt.title("Risk Contribution by Asset (% of Total Portfolio Risk)")
plt.xlabel("Ticker")
plt.ylabel("Risk Contribution (%)")
plt.tight_layout()
plt.savefig(OUT_DIR / "risk_contribution_bar.png")
plt.close()

print("Saved correlation_matrix.png")
print("Saved risk_contribution.csv")
print("Saved risk_contribution_bar.png")
print(risk_df)
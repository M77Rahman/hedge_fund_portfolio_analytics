Equity Portfolio Risk & Performance Analytics
Overview

This project analyses a multi-asset equity portfolio using 5 years of daily historical market data.

The objective was to replicate core analytical workflows used in asset management environments:

Data ingestion and cleaning

Return calculation

Rolling volatility estimation

Drawdown tracking

Portfolio aggregation

Risk-adjusted performance evaluation

Correlation and risk contribution analysis

Assets Analysed

AAPL

MSFT

NVDA

SPY

TSLA

Portfolio Construction

Equal-weight allocation

Daily rebalancing (simple average of available returns)

Performance Summary

Period analysed: 2021-02-22 to 2026-02-20

Metric	Value
Total Return	233.95%
Annualised Return	27.37%
Annualised Volatility	29.58%
Sharpe Ratio (rf = 0)	0.93
Maximum Drawdown	-43.25%
Key Observations

Despite equal weighting, NVDA and TSLA contributed disproportionately to total portfolio risk.

The portfolio experienced a maximum drawdown of -43%, reflecting high exposure to volatile growth equities.

Correlation analysis shows clustering among technology stocks, reducing diversification benefits during stress periods.

Risk-adjusted performance (Sharpe 0.93) indicates strong returns but with elevated volatility.

Risk Analysis
Correlation Matrix

Risk Contribution by Asset

Risk contribution was calculated using:

Annualised covariance matrix

Marginal contribution to risk

Component contribution to total portfolio volatility

Visual Outputs
Portfolio Equity Curve

Portfolio Drawdown

Asset Equity Comparison

20-Day Rolling Volatility

Technical Architecture

Historical price data pulled using yfinance

Data cleaned and validated using pandas

Returns, volatility, and drawdowns computed programmatically

Portfolio aggregated from individual asset returns

SQLite database generated for structured querying

Automated visual reports exported as PNG files

Metrics Implemented

Daily returns

Compounded equity curves

Rolling 20-day volatility

Maximum drawdown

Annualised return

Annualised volatility

Sharpe ratio

Correlation matrix

Component risk contribution

Data Quality Controls

Duplicate date-ticker pairs removed

Missing values tracked

Validation of required columns

Separate data quality summary table generated

Limitations & Assumptions

Equal-weight portfolio (no optimisation applied)

No transaction costs included

Risk-free rate assumed to be 0%

No survivorship bias adjustments

Daily rebalancing assumption may overstate turnover

How To Reproduce
pip install -r requirements.txt
python src/01_pull_data.py
python src/02_build_metrics.py
python src/03_load_sqlite.py
python src/04_generate_charts.py
python src/05_summary_stats.py
python src/06_risk_analysis.py
Tools Used

Python

pandas

numpy

matplotlib

seaborn

SQLite

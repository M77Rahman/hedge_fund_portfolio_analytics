Hedge Fund Portfolio Analytics Dashboard
Overview

This project simulates a multi-asset equity portfolio and evaluates its performance and risk characteristics over a 5-year period.

The objective was to replicate core analytical workflows used in hedge fund and asset management environments:

Historical price ingestion

Data cleaning and validation

Return calculation

Rolling volatility analysis

Drawdown tracking

Portfolio construction (equal-weight)

Risk-adjusted performance metrics

Assets included:
AAPL, MSFT, NVDA, SPY, TSLA

Rebalancing approach:
Daily equal-weight portfolio (mean of available daily returns)

Performance Summary

Start Date: 2021-02-22

End Date: 2026-02-20

Total Return: 233.95%

Annualised Return: 27.37%

Annualised Volatility: 29.58%

Sharpe Ratio (rf=0): 0.93

Maximum Drawdown: -43.25%

Key Visual Outputs
Portfolio Equity Curve

Portfolio Drawdown

Asset Equity Comparison

20-Day Rolling Volatility

Technical Stack

Python
pandas
numpy
matplotlib
SQLite

Architecture

Data pulled using yfinance

Cleaned and transformed with pandas

Returns and rolling metrics computed

Portfolio returns aggregated

SQLite database generated for structured querying

Visual outputs generated programmatically

Risk & Analytics Concepts Applied

Compounded returns

Rolling standard deviation

Maximum drawdown

Risk-adjusted performance (Sharpe ratio)

Portfolio aggregation logic

Data quality validation

How To Reproduce
pip install -r requirements.txt
python src/01_pull_data.py
python src/02_build_metrics.py
python src/03_load_sqlite.py
python src/04_generate_charts.py
python src/05_summary_stats.py
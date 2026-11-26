# Restaurant Sales Dashboard (PS 77)

Language: Python 3 | Concepts: Pandas, Matplotlib, CSV, GroupBy

## Problem
Read `restaurant_sales.csv` with Pandas, calculate Sales = Quantity x Price, and use
GroupBy to show sales by category, by date, and the top item by quantity and by revenue,
with charts. Invalid rows are skipped with a warning.

## Setup & Run
```
pip install pandas matplotlib
python restaurant_sales_dashboard.py              # uses restaurant_sales.csv
python restaurant_sales_dashboard.py other.csv    # use another file
```
Menu: 1 Sales by category, 2 Top items, 3 Daily sales, 4 Top items and daily sales, 5 Exit.

## How it works
- `load_data()` - reads CSV, skips invalid rows (text / negative / missing values) with a warning, adds `Sales` column.
- `sales_by_category()` - `groupby("Category")`, bar chart.
- `top_items()` - `groupby("Item")` on Quantity and Sales, two bar charts.
- `daily_sales()` - `groupby("Date")`, line chart, best day.
- `main()` - menu loop.

## Test cases
| # | Input | Result |
|---|-------|--------|
| 1 | restaurant_sales.csv, Sales by category | Main 6300, Starter 4840, Dessert 3600, Total 14740 |
| 2 | test_data/test_boundary.csv, Top items | Total 220, Paneer Tikka (1 unit), Rs. 220 |
| 3a | test_data/test_invalid.csv | Warning: Row 8 skipped - Quantity must be a number. |
| 3b | sales2025.csv | Error: File 'sales2025.csv' not found. |
| 4 | restaurant_sales.csv, Top items and daily sales | Gulab Jamun (45 units), Paneer Tikka (Rs. 4840), 7700 / 7040, best day 2026-10-01 |

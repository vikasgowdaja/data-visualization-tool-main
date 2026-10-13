# KPI Analysis

This branch focuses on turning cleaned sales data into business-ready metrics.

## What this branch teaches
- Revenue and order-value calculations
- Grouped KPI summaries by region and channel
- Exporting metric tables for reporting and dashboards

## How to run
```bash
python -m pip install -r requirements.txt
python scripts/03_kpi_summary.py
```

## Expected outputs
- `outputs/kpi_summary.csv` with top-level KPI values
- `outputs/kpi_by_region.csv` with grouped metrics
- `outputs/kpi_notes.md` summarizing the metric definitions and business interpretation

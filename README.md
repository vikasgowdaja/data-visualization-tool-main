# Clean and Validate

This branch teaches the second stage of the analytics workflow: cleaning messy source data, fixing common data quality issues, and validating the result before dashboarding.

## What this branch teaches
- Handling missing values
- Parsing dates and numeric fields
- Normalizing category values
- Removing duplicate and invalid rows
- Writing a validated clean dataset

## How to run
```bash
python -m pip install -r requirements.txt
python scripts/02_clean_and_validate.py
```

## Expected outputs
- `data/retail_sales_clean.csv` with cleaned records
- `outputs/clean_validation_report.txt` summarizing the cleaning decisions
- `outputs/cleaning_decisions.md` explaining what was fixed and why

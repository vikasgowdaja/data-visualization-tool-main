# Data Visualization Learning Path

This branch introduces the first stage of the analytics pipeline: loading the raw dataset and inspecting its structure.

## What this branch teaches
- Reading a CSV into a pandas DataFrame
- Checking schema, nulls, and dtypes
- Running a basic profile of the dataset

## How to run
```bash
python -m pip install -r requirements.txt
python scripts/01_dataframe_profile.py
```

## Expected outputs
- Console summary of row count, columns, missing values, and dtypes
- `outputs/profile_summary.txt` with a quick data profile
- `data/retail_sales_raw.csv` as the working dataset for the next steps

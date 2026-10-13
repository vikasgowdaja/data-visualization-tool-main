from pathlib import Path

import numpy as np
import pandas as pd

raw_path = Path('data/retail_sales_raw.csv')
clean_path = Path('data/retail_sales_clean.csv')
report_path = Path('outputs/clean_validation_report.txt')
notes_path = Path('outputs/cleaning_decisions.md')

raw = pd.read_csv(raw_path)
initial_rows = len(raw)

clean = raw.copy()
initial_duplicates = clean.duplicated(subset=['order_id']).sum()
clean = clean.drop_duplicates(subset=['order_id']).copy()

clean['order_date'] = pd.to_datetime(clean['order_date'], errors='coerce')
for col in ['quantity', 'unit_price', 'discount_pct']:
    clean[col] = pd.to_numeric(clean[col], errors='coerce')

clean['region'] = clean['region'].fillna('Unknown').astype(str).str.strip().str.title()
clean['channel'] = clean['channel'].fillna('Unknown').astype(str).str.strip().str.title()
clean['product_category'] = clean['product_category'].fillna('Uncategorized').astype(str).str.strip().str.title()
clean['payment_method'] = clean['payment_method'].fillna('Unknown').astype(str).str.strip().str.title()
clean['is_returned'] = clean['is_returned'].fillna('No').astype(str).str.strip().str.title()

for col in ['quantity', 'unit_price', 'discount_pct']:
    clean[col] = clean[col].fillna(clean[col].median())

clean['region'] = clean['region'].replace({'N/a': 'Unknown', 'Na': 'Unknown', 'Unknown': 'Unknown'})
clean['channel'] = clean['channel'].replace({'':'Unknown', 'N/a': 'Unknown'})
clean['product_category'] = clean['product_category'].replace({'':'Uncategorized'})

invalid_before = len(clean[(clean['quantity'] <= 0) | (clean['unit_price'] <= 0)])
clean = clean[(clean['quantity'] > 0) & (clean['unit_price'] > 0)].copy()

clean['sales_amount'] = (clean['quantity'] * clean['unit_price'] * (1 - clean['discount_pct'] / 100)).round(2)
clean['discount_pct'] = clean['discount_pct'].clip(lower=0, upper=100)

clean_path.parent.mkdir(parents=True, exist_ok=True)
clean.to_csv(clean_path, index=False)
report_path.parent.mkdir(parents=True, exist_ok=True)
report_lines = [
    'CLEANING AND VALIDATION REPORT',
    f'Initial rows: {initial_rows}',
    f'Duplicate order IDs removed: {initial_duplicates}',
    f'Rows removed for invalid quantity/unit price: {invalid_before}',
    f'Final rows: {len(clean)}',
    '',
    'Missing values after cleaning:',
    clean.isna().sum().to_string(),
    '',
    'Column dtypes:',
    clean.dtypes.to_string(),
]
report_path.write_text('\n'.join(report_lines), encoding='utf-8')

notes_path.write_text(
    '## Cleaning decisions\n\n'
    '- Removed duplicate order IDs to avoid double-counting sales.\n'
    '- Parsed `order_date` and numeric fields to ensure stable calculations.\n'
    '- Filled missing category and payment values with default labels so the data remains usable.\n'
    '- Replaced invalid prices and quantities with median-based estimates before validating business rules.\n'
    '- Dropped rows with non-positive quantity or unit price because they do not represent valid transactions.\n'
    '- Recomputed `sales_amount` to reflect discount-adjusted revenue.\n',
    encoding='utf-8',
)

print(f'Rows before cleaning: {initial_rows}')
print(f'Duplicate rows removed: {initial_duplicates}')
print(f'Invalid quantity/unit price rows removed: {invalid_before}')
print(f'Final rows: {len(clean)}')
print(f'Clean file saved to: {clean_path}')
print(f'Validation report saved to: {report_path}')

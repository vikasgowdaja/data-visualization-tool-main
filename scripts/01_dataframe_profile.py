# Profile the raw dataset and save a lightweight summary.
from pathlib import Path

import pandas as pd

raw_path = Path('data/retail_sales_raw.csv')
df = pd.read_csv(raw_path)

summary_lines = [
    'DATAFRAME PROFILE REPORT',
    f'Rows: {len(df)}',
    f'Columns: {list(df.columns)}',
    '',
    'MISSING VALUES',
    df.isna().sum().to_string(),
    '',
    'DATA TYPES',
    df.dtypes.to_string(),
    '',
    'SAMPLE ROWS',
    df.head(5).to_string(index=False),
    '',
    'NUMERIC SUMMARY',
    df.describe(include='number').to_string(),
]

Path('outputs').mkdir(exist_ok=True)
Path('outputs/profile_summary.txt').write_text('\n'.join(summary_lines), encoding='utf-8')

print('Shape:', df.shape)
print('\nNull counts:')
print(df.isna().sum())
print('\nDtypes:')
print(df.dtypes)
print('\nPreview:')
print(df.head(5).to_string(index=False))

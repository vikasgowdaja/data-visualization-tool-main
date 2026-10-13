from pathlib import Path

import pandas as pd

clean_path = Path('data/retail_sales_clean.csv')
df = pd.read_csv(clean_path)
df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
df['revenue'] = (df['quantity'] * df['unit_price'] * (1 - df['discount_pct'] / 100)).round(2)

kpi_summary = {
    'metric': [
        'total_revenue',
        'total_orders',
        'avg_order_value',
        'avg_quantity_per_order',
        'returned_orders',
        'return_rate'
    ],
    'value': [
        round(df['revenue'].sum(), 2),
        df['order_id'].nunique(),
        round(df['revenue'].mean(), 2),
        round(df['quantity'].mean(), 2),
        int(df['is_returned'].eq('Yes').sum()),
        round(df['is_returned'].eq('Yes').mean(), 4),
    ],
}
summary_df = pd.DataFrame(kpi_summary)

region_summary = (
    df.groupby(['region', 'channel'], as_index=False)
      .agg(revenue=('revenue', 'sum'), orders=('order_id', 'nunique'))
      .sort_values(['revenue', 'orders'], ascending=[False, False])
)

Path('outputs').mkdir(exist_ok=True)
summary_df.to_csv('outputs/kpi_summary.csv', index=False)
region_summary.to_csv('outputs/kpi_by_region.csv', index=False)

notes = '''# KPI notes

- Total revenue shows the overall sales amount after discounts.
- Average order value helps compare order size across channels.
- Return rate highlights the share of orders marked as returned.
- Region and channel summaries help identify the strongest business segments.
'''
Path('outputs/kpi_notes.md').write_text(notes, encoding='utf-8')

print(summary_df.to_string(index=False))
print('\nTop region/channel KPI summary:')
print(region_summary.head(10).to_string(index=False))

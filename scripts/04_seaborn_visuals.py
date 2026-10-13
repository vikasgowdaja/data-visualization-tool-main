import matplotlib
matplotlib.use('Agg')

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

clean_path = Path('data/retail_sales_clean.csv')
df = pd.read_csv(clean_path)
df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
df['revenue'] = df['quantity'] * df['unit_price'] * (1 - df['discount_pct'] / 100)

def save_chart(fig, name):
    out_dir = Path('outputs/charts')
    out_dir.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(out_dir / name, dpi=200)
    plt.close(fig)

region_summary = df.groupby('region', as_index=False)['revenue'].sum().sort_values('revenue', ascending=False)
fig, ax = plt.subplots(figsize=(9, 5))
sns.barplot(data=region_summary, x='region', y='revenue', palette='viridis', ax=ax)
ax.set_title('Revenue by Region')
ax.set_xlabel('Region')
ax.set_ylabel('Revenue')
ax.tick_params(axis='x', rotation=20)
save_chart(fig, 'revenue_by_region.png')

monthly_summary = (
    df.assign(month=df['order_date'].dt.to_period('M').astype(str))
      .groupby('month', as_index=False)['revenue']
      .sum()
      .sort_values('month')
)
fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(data=monthly_summary, x='month', y='revenue', marker='o', ax=ax)
ax.set_title('Monthly Revenue Trend')
ax.set_xlabel('Month')
ax.set_ylabel('Revenue')
ax.tick_params(axis='x', rotation=35)
save_chart(fig, 'monthly_revenue.png')

notes = '''# Chart interpretation notes

- The revenue-by-region chart shows which business areas are generating the most sales.
- The monthly trend helps identify seasonality or spikes in demand over time.
- Use these charts as the first layer of exploratory analysis before building interactive views.
'''
Path('outputs/chart_interpretation.md').write_text(notes, encoding='utf-8')

print('Saved revenue_by_region.png')
print('Saved monthly_revenue.png')
print('Saved chart_interpretation.md')

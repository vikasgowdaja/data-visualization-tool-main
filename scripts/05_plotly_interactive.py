from pathlib import Path

import pandas as pd
import plotly.express as px

clean_path = Path('data/retail_sales_clean.csv')
df = pd.read_csv(clean_path)
df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
df['revenue'] = df['quantity'] * df['unit_price'] * (1 - df['discount_pct'] / 100)

region_channel = (
    df.groupby(['region', 'channel'], as_index=False)['revenue']
      .sum()
      .sort_values('revenue', ascending=False)
)

bar_fig = px.bar(
    region_channel,
    x='region',
    y='revenue',
    color='channel',
    barmode='group',
    title='Interactive Revenue by Region and Channel',
    hover_name='channel',
    labels={'revenue': 'Revenue', 'region': 'Region', 'channel': 'Channel'},
)
bar_fig.update_layout(template='plotly_white', legend_title='Channel')

monthly = (
    df.assign(month=df['order_date'].dt.to_period('M').astype(str))
      .groupby(['month', 'channel'], as_index=False)['revenue']
      .sum()
)
line_fig = px.line(
    monthly,
    x='month',
    y='revenue',
    color='channel',
    markers=True,
    title='Monthly Revenue Trend by Channel',
    labels={'month': 'Month', 'revenue': 'Revenue', 'channel': 'Channel'},
)
line_fig.update_layout(template='plotly_white', legend_title='Channel')

out_dir = Path('outputs')
out_dir.mkdir(exist_ok=True)
bar_fig.write_html(out_dir / 'interactive_revenue_dashboard.html', include_plotlyjs='cdn')
Path('outputs/plotly_interpretation.md').write_text(
    '- Hover over each bar or line to inspect exact values.\n'
    '- Use the legend to filter channel segments quickly.\n'
    '- This interactive view is a good bridge between static charts and the final Streamlit dashboard.\n',
    encoding='utf-8',
)

print('Interactive dashboard saved to outputs/interactive_revenue_dashboard.html')

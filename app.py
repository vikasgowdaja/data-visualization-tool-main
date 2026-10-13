from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title='Sales Dashboard', layout='wide')

DATA_PATH = Path('data/retail_sales_clean.csv')

df = pd.read_csv(DATA_PATH)
df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
df['revenue'] = df['quantity'] * df['unit_price'] * (1 - df['discount_pct'] / 100)

df = df.sort_values('order_date').reset_index(drop=True)

st.title('Retail Sales Dashboard')
st.caption('Student learning pipeline: load -> clean -> KPI -> visualization')

regions = ['All'] + sorted(df['region'].dropna().unique().tolist())
channels = ['All'] + sorted(df['channel'].dropna().unique().tolist())
selected_region = st.sidebar.selectbox('Region', regions)
selected_channel = st.sidebar.selectbox('Channel', channels)
selected_category = st.sidebar.selectbox('Product category', ['All'] + sorted(df['product_category'].dropna().unique().tolist()))

filtered_df = df.copy()
if selected_region != 'All':
    filtered_df = filtered_df[filtered_df['region'] == selected_region]
if selected_channel != 'All':
    filtered_df = filtered_df[filtered_df['channel'] == selected_channel]
if selected_category != 'All':
    filtered_df = filtered_df[filtered_df['product_category'] == selected_category]

revenue = round(filtered_df['revenue'].sum(), 2)
orders = filtered_df['order_id'].nunique()
avg_order = round(filtered_df['revenue'].mean(), 2) if not filtered_df.empty else 0
return_rate = round(filtered_df['is_returned'].eq('Yes').mean(), 4) if not filtered_df.empty else 0

col1, col2, col3, col4 = st.columns(4)
col1.metric('Revenue', f'${revenue:,.2f}')
col2.metric('Orders', f'{orders}')
col3.metric('Avg Order Value', f'${avg_order:,.2f}')
col4.metric('Return Rate', f'{return_rate:.1%}')

region_summary = filtered_df.groupby('region', as_index=False)['revenue'].sum().sort_values('revenue', ascending=False)
bar_fig = px.bar(
    region_summary,
    x='region',
    y='revenue',
    title='Revenue by Region',
    labels={'region': 'Region', 'revenue': 'Revenue'},
    color='region',
    template='plotly_white',
)
bar_fig.update_layout(showlegend=False)

monthly_summary = (
    filtered_df.assign(month=filtered_df['order_date'].dt.to_period('M').astype(str))
    .groupby('month', as_index=False)['revenue']
    .sum()
    .sort_values('month')
)
line_fig = px.line(
    monthly_summary,
    x='month',
    y='revenue',
    markers=True,
    title='Monthly Revenue Trend',
    labels={'month': 'Month', 'revenue': 'Revenue'},
    template='plotly_white',
)

left_col, right_col = st.columns(2)
with left_col:
    st.plotly_chart(bar_fig, use_container_width=True)
with right_col:
    st.plotly_chart(line_fig, use_container_width=True)

st.subheader('Filtered transactions')
st.dataframe(filtered_df[['order_id', 'order_date', 'region', 'channel', 'product_category', 'quantity', 'unit_price', 'revenue', 'is_returned']].sort_values('order_date').reset_index(drop=True), use_container_width=True)

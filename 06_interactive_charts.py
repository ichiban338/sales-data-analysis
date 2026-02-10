"""
Interactive Visualizations with Plotly
Author: Juan Esteban Agudelo Alonso
Project: Sales Data Analysis Portfolio
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

print("=" * 70)
print("GENERATING INTERACTIVE PLOTLY VISUALIZATIONS")
print("=" * 70)

# Load data
df = pd.read_csv('sales_data.csv')
df['sale_date'] = pd.to_datetime(df['sale_date'])
df['year_month'] = df['sale_date'].dt.to_period('M').astype(str)

# ==========================================
# CHART 1: Interactive Revenue Trend
# ==========================================

print("\n1. Creating interactive revenue trend...")

monthly_revenue = df.groupby('year_month')['revenue'].sum().reset_index()

fig1 = px.line(
    monthly_revenue,
    x='year_month',
    y='revenue',
    title='📈 Monthly Revenue Trend 2024 (Interactive)',
    labels={'year_month': 'Month', 'revenue': 'Revenue ($)'},
    markers=True
)

fig1.update_traces(
    line_color='#2E86AB',
    line_width=3,
    marker=dict(size=12, line=dict(width=2, color='white'))
)

fig1.update_layout(
    hovermode='x unified',
    plot_bgcolor='white',
    font=dict(size=12, family='Arial'),
    title_font_size=20,
    title_x=0.5,
    hoverlabel=dict(bgcolor="white", font_size=14),
    xaxis=dict(showgrid=True, gridwidth=1, gridcolor='lightgray'),
    yaxis=dict(showgrid=True, gridwidth=1, gridcolor='lightgray')
)

fig1.write_html('interactive_revenue_trend.html')
print("   ✅ Saved: interactive_revenue_trend.html")

# ==========================================
# CHART 2: Interactive Top Products
# ==========================================

print("2. Creating interactive top products chart...")

top_10_products = df.groupby('product')['revenue'].sum().sort_values(ascending=False).head(10).reset_index()

fig2 = px.bar(
    top_10_products,
    x='revenue',
    y='product',
    orientation='h',
    title='🏆 Top 10 Products by Revenue (Interactive)',
    labels={'revenue': 'Revenue ($)', 'product': 'Product'},
    color='revenue',
    color_continuous_scale='Viridis'
)

fig2.update_layout(
    showlegend=False,
    plot_bgcolor='white',
    font=dict(size=12, family='Arial'),
    title_font_size=20,
    title_x=0.5,
    hoverlabel=dict(bgcolor="white", font_size=14),
    xaxis=dict(showgrid=True, gridwidth=1, gridcolor='lightgray')
)

fig2.write_html('interactive_top_products.html')
print("   ✅ Saved: interactive_top_products.html")

# ==========================================
# CHART 3: Sunburst Chart
# ==========================================

print("3. Creating interactive sunburst chart...")

category_product = df.groupby(['product_category', 'product'])['revenue'].sum().reset_index()

fig3 = px.sunburst(
    category_product,
    path=['product_category', 'product'],
    values='revenue',
    title='🎯 Revenue Distribution: Categories → Products (Interactive)',
    color='revenue',
    color_continuous_scale='RdYlGn',
    hover_data={'revenue': ':,.0f'}
)

fig3.update_layout(
    font=dict(size=12, family='Arial'),
    title_font_size=20,
    title_x=0.5
)

fig3.write_html('interactive_category_sunburst.html')
print("   ✅ Saved: interactive_category_sunburst.html")

# ==========================================
# CHART 4: Treemap
# ==========================================

print("4. Creating interactive treemap...")

fig4 = px.treemap(
    category_product,
    path=['product_category', 'product'],
    values='revenue',
    title='📦 Revenue Treemap by Category and Product',
    color='revenue',
    color_continuous_scale='Blues',
    hover_data={'revenue': ':,.0f'}
)

fig4.update_layout(
    font=dict(size=12, family='Arial'),
    title_font_size=20,
    title_x=0.5
)

fig4.write_html('interactive_treemap.html')
print("   ✅ Saved: interactive_treemap.html")

# ==========================================
# CHART 5: Combined Dashboard
# ==========================================

print("5. Creating combined interactive dashboard...")

fig_dashboard = make_subplots(
    rows=2, cols=2,
    subplot_titles=(
        'Monthly Revenue Trend',
        'Revenue by Category',
        'Top 5 Products',
        'Revenue Distribution'
    ),
    specs=[
        [{"type": "scatter"}, {"type": "bar"}],
        [{"type": "bar"}, {"type": "pie"}]
    ],
    vertical_spacing=0.12,
    horizontal_spacing=0.10
)

# 1. Revenue trend
fig_dashboard.add_trace(
    go.Scatter(
        x=monthly_revenue['year_month'],
        y=monthly_revenue['revenue'],
        mode='lines+markers',
        name='Revenue',
        line=dict(color='#2E86AB', width=3),
        marker=dict(size=10)
    ),
    row=1, col=1
)

# 2. Revenue by category
category_revenue = df.groupby('product_category')['revenue'].sum().sort_values(ascending=False).reset_index()
fig_dashboard.add_trace(
    go.Bar(
        x=category_revenue['product_category'],
        y=category_revenue['revenue'],
        name='Category Revenue',
        marker_color='#A23B72',
        showlegend=False
    ),
    row=1, col=2
)

# 3. Top 5 products
fig_dashboard.add_trace(
    go.Bar(
        y=top_10_products.head(5)['product'],
        x=top_10_products.head(5)['revenue'],
        orientation='h',
        name='Top Products',
        marker_color='#F18F01',
        showlegend=False
    ),
    row=2, col=1
)

# 4. Pie chart
fig_dashboard.add_trace(
    go.Pie(
        labels=category_revenue['product_category'],
        values=category_revenue['revenue'],
        name='Category Share',
        marker=dict(colors=['#F18F01', '#C73E1D', '#6A994E', '#A7C957', '#2E86AB'])
    ),
    row=2, col=2
)

fig_dashboard.update_layout(
    height=900,
    title_text="📊 Sales Analysis Dashboard - 2024",
    title_font_size=24,
    title_x=0.5,
    showlegend=False,
    plot_bgcolor='white',
    font=dict(size=11, family='Arial')
)

fig_dashboard.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
fig_dashboard.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')

fig_dashboard.write_html('interactive_dashboard.html')
print("   ✅ Saved: interactive_dashboard.html")

# ==========================================
# SUMMARY
# ==========================================

print("\n" + "=" * 70)
print("✅ ALL INTERACTIVE VISUALIZATIONS CREATED!")
print("=" * 70)
print("\nGenerated files:")
print("  📊 interactive_revenue_trend.html")
print("  📊 interactive_top_products.html")
print("  📊 interactive_category_sunburst.html")
print("  📊 interactive_treemap.html")
print("  📊 interactive_dashboard.html")
print("\n💡 Open any .html file in your web browser to interact with the charts")
print("   Features: Hover for details, Zoom, Pan, Download as PNG")
print("=" * 70)
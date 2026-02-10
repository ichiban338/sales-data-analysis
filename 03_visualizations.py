"""
Static Visualizations Script
Author: Juan Esteban Agudelo Alonso
Project: Sales Data Analysis Portfolio
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Configuration
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")

# Load data
df = pd.read_csv('sales_data.csv')
df['sale_date'] = pd.to_datetime(df['sale_date'])
df['year_month'] = df['sale_date'].dt.to_period('M')

print("=" * 70)
print("GENERATING STATIC VISUALIZATIONS")
print("=" * 70)

# ==========================================
# CHART 1: Monthly Revenue Trend
# ==========================================

print("\n1. Creating monthly revenue trend chart...")

monthly_revenue = df.groupby('year_month')['revenue'].sum().reset_index()
monthly_revenue['year_month_str'] = monthly_revenue['year_month'].astype(str)

plt.figure(figsize=(16, 7))
plt.plot(monthly_revenue['year_month_str'], 
         monthly_revenue['revenue'],
         marker='o', 
         linewidth=3, 
         markersize=12,
         color='#2E86AB',
         label='Monthly Revenue')

plt.fill_between(range(len(monthly_revenue)), 
                 monthly_revenue['revenue'], 
                 alpha=0.2, 
                 color='#2E86AB')

plt.title('Monthly Revenue Trend - 2024', 
          fontsize=18, 
          fontweight='bold', 
          pad=20)
plt.xlabel('Month', fontsize=14, fontweight='bold')
plt.ylabel('Revenue ($)', fontsize=14, fontweight='bold')
plt.xticks(rotation=45, ha='right')
plt.grid(True, alpha=0.3)
plt.legend(fontsize=12)

for i, row in monthly_revenue.iterrows():
    plt.text(i, row['revenue'], 
             f"${row['revenue']/1000:.0f}K", 
             ha='center', 
             va='bottom', 
             fontsize=10,
             fontweight='bold')

plt.tight_layout()
plt.savefig('revenue_over_time.png', dpi=300, bbox_inches='tight')
print("   ✅ Saved: revenue_over_time.png")
plt.close()

# ==========================================
# CHART 2: Top 10 Products
# ==========================================

print("2. Creating top products chart...")

top_10_products = df.groupby('product')['revenue'].sum().sort_values(ascending=False).head(10)

plt.figure(figsize=(14, 9))

colors = plt.cm.viridis(np.linspace(0.2, 0.9, len(top_10_products)))

bars = plt.barh(range(len(top_10_products)), 
                top_10_products.values,
                color=colors,
                edgecolor='black',
                linewidth=1.5)

plt.yticks(range(len(top_10_products)), top_10_products.index, fontsize=12)
plt.xlabel('Revenue ($)', fontsize=14, fontweight='bold')
plt.title('Top 10 Products by Revenue', 
          fontsize=18, 
          fontweight='bold', 
          pad=20)
plt.grid(axis='x', alpha=0.3)

total_revenue = df['revenue'].sum()
for i, (product, revenue) in enumerate(top_10_products.items()):
    pct = (revenue / total_revenue) * 100
    plt.text(revenue, i, 
             f' ${revenue/1000:.0f}K ({pct:.1f}%)', 
             va='center', 
             fontsize=11, 
             fontweight='bold')

# Highlight top 3
for i in range(3):
    bars[i].set_color('#FF6B6B')

plt.tight_layout()
plt.savefig('top_products.png', dpi=300, bbox_inches='tight')
print("   ✅ Saved: top_products.png")
plt.close()

# ==========================================
# CHART 3: Revenue by Category
# ==========================================

print("3. Creating category revenue charts...")

category_revenue = df.groupby('product_category')['revenue'].sum().sort_values(ascending=False)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 7))

colors_cat = ['#F18F01', '#C73E1D', '#6A994E', '#A7C957', '#2E86AB']

# Bar chart
bars = ax1.bar(range(len(category_revenue)), 
               category_revenue.values,
               color=colors_cat,
               edgecolor='black',
               linewidth=1.5)

ax1.set_xticks(range(len(category_revenue)))
ax1.set_xticklabels(category_revenue.index, rotation=45, ha='right', fontsize=12)
ax1.set_ylabel('Revenue ($)', fontsize=13, fontweight='bold')
ax1.set_title('Revenue by Product Category', fontsize=15, fontweight='bold')
ax1.grid(axis='y', alpha=0.3)

for i, (category, revenue) in enumerate(category_revenue.items()):
    pct = (revenue / total_revenue) * 100
    ax1.text(i, revenue, 
             f'${revenue/1000:.0f}K\n({pct:.1f}%)', 
             ha='center', 
             va='bottom', 
             fontsize=11, 
             fontweight='bold')

# Pie chart
wedges, texts, autotexts = ax2.pie(category_revenue.values, 
                                     labels=category_revenue.index,
                                     autopct='%1.1f%%',
                                     startangle=90,
                                     colors=colors_cat,
                                     textprops={'fontsize': 12, 'fontweight': 'bold'},
                                     wedgeprops={'edgecolor': 'black', 'linewidth': 1.5})

ax2.set_title('Revenue Distribution by Category', fontsize=15, fontweight='bold')

plt.tight_layout()
plt.savefig('revenue_by_category.png', dpi=300, bbox_inches='tight')
print("   ✅ Saved: revenue_by_category.png")
plt.close()

# ==========================================
# CHART 4: Top Customers
# ==========================================

print("4. Creating top customers chart...")

top_20_customers = df.groupby('customer_id')['revenue'].sum().sort_values(ascending=False).head(20)

plt.figure(figsize=(16, 8))

bars = plt.bar(range(len(top_20_customers)), 
               top_20_customers.values,
               color='#2D6A4F',
               alpha=0.8,
               edgecolor='black',
               linewidth=1.2)

for i in range(3):
    bars[i].set_color('#FF6B6B')

plt.xlabel('Customer Rank', fontsize=14, fontweight='bold')
plt.ylabel('Total Revenue ($)', fontsize=14, fontweight='bold')
plt.title('Top 20 Customers by Revenue', 
          fontsize=18, 
          fontweight='bold', 
          pad=20)
plt.xticks(range(len(top_20_customers)), range(1, 21))
plt.grid(axis='y', alpha=0.3)

top_20_pct = (top_20_customers.sum() / total_revenue) * 100
plt.text(0.5, 0.95, 
         f'Top 20 customers = {top_20_pct:.1f}% of total revenue',
         transform=plt.gca().transAxes,
         fontsize=13, 
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.7),
         verticalalignment='top',
         fontweight='bold')

plt.tight_layout()
plt.savefig('top_customers.png', dpi=300, bbox_inches='tight')
print("   ✅ Saved: top_customers.png")
plt.close()

print("\n" + "=" * 70)
print("✅ ALL VISUALIZATIONS GENERATED SUCCESSFULLY!")
print("=" * 70)
print("\nGenerated files:")
print("  📊 revenue_over_time.png")
print("  📊 top_products.png")
print("  📊 revenue_by_category.png")
print("  📊 top_customers.png")
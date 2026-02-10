"""
KPI Calculations Script
Author: Juan Esteban Agudelo Alonso
Project: Sales Data Analysis Portfolio
"""

import pandas as pd

# Load data
df = pd.read_csv('sales_data.csv')
df['sale_date'] = pd.to_datetime(df['sale_date'])
df['year_month'] = df['sale_date'].dt.to_period('M')

print("=" * 70)
print("KEY PERFORMANCE INDICATORS (KPIs)")
print("=" * 70)

# ==========================================
# KPI 1: Total Revenue
# ==========================================

total_revenue = df['revenue'].sum()

print(f"\n1. TOTAL REVENUE: ${total_revenue:,.2f}")
print("   → Primary measure of business performance")
print("   → Baseline for growth targets")

# ==========================================
# KPI 2: Transaction Metrics
# ==========================================

total_transactions = len(df)
unique_customers = df['customer_id'].nunique()

print(f"\n2. TRANSACTION METRICS:")
print(f"   Total Transactions: {total_transactions:,}")
print(f"   Unique Customers: {unique_customers:,}")
print(f"   Avg Transactions per Customer: {total_transactions/unique_customers:.2f}")
print("   → Volume indicators for market penetration")

# ==========================================
# KPI 3: Average Order Value (AOV)
# ==========================================

aov = df['revenue'].mean()
median_ov = df['revenue'].median()

print(f"\n3. AVERAGE ORDER VALUE (AOV): ${aov:,.2f}")
print(f"   Median Order Value: ${median_ov:,.2f}")
print("   → Target for upselling and bundling strategies")
print("   → Benchmark for pricing optimization")

# ==========================================
# KPI 4: Customer Value Metrics
# ==========================================

avg_customer_value = total_revenue / unique_customers

print(f"\n4. CUSTOMER VALUE METRICS:")
print(f"   Average Customer Value: ${avg_customer_value:,.2f}")
print("   → Estimate for customer acquisition cost comparison")
print("   → Baseline for retention program ROI")

# ==========================================
# KPI 5: Product Mix Metrics
# ==========================================

avg_items_per_transaction = df['quantity'].mean()
single_item_pct = (df['quantity'] == 1).sum() / len(df) * 100

print(f"\n5. PRODUCT MIX METRICS:")
print(f"   Avg Items per Transaction: {avg_items_per_transaction:.2f}")
print(f"   Single-item Transactions: {single_item_pct:.1f}%")
print(f"   Multi-item Transactions: {100-single_item_pct:.1f}%")
print("   → Indicates cross-sell and bundling effectiveness")

# ==========================================
# KPI 6: Monthly Growth Rate
# ==========================================

monthly_revenue = df.groupby('year_month')['revenue'].sum()
monthly_growth = monthly_revenue.pct_change() * 100

print(f"\n6. MONTHLY REVENUE GROWTH RATE:")
print("   Latest 6 months:")
for month, growth in monthly_growth.tail(6).items():
    if pd.notna(growth):
        direction = "📈" if growth > 0 else "📉"
        print(f"   {month}: {growth:+.2f}% {direction}")

avg_growth = monthly_growth.mean()
print(f"\n   Average Monthly Growth: {avg_growth:.2f}%")
print("   → Indicates business momentum and trajectory")

# ==========================================
# KPI 7: Revenue by Category
# ==========================================

print(f"\n7. REVENUE BY CATEGORY:")
category_revenue = df.groupby('product_category')['revenue'].sum().sort_values(ascending=False)

for category, revenue in category_revenue.items():
    pct = (revenue / total_revenue) * 100
    print(f"   {category}: ${revenue:,.2f} ({pct:.1f}%)")

print("   → Shows portfolio diversification")
print("   → Identifies category growth opportunities")

# ==========================================
# KPI SUMMARY TABLE
# ==========================================

print("\n" + "=" * 70)
print("📊 KPI SUMMARY TABLE")
print("=" * 70)

kpi_summary = pd.DataFrame({
    'KPI': [
        'Total Revenue',
        'Total Transactions',
        'Unique Customers',
        'Average Order Value',
        'Avg Customer Value',
        'Avg Items/Transaction',
        'Single-Item Transaction %',
        'Avg Monthly Growth %'
    ],
    'Value': [
        f'${total_revenue:,.2f}',
        f'{total_transactions:,}',
        f'{unique_customers:,}',
        f'${aov:,.2f}',
        f'${avg_customer_value:,.2f}',
        f'{avg_items_per_transaction:.2f}',
        f'{single_item_pct:.1f}%',
        f'{avg_growth:.2f}%'
    ],
    'Business Use': [
        'Overall performance benchmark',
        'Volume indicator',
        'Market penetration metric',
        'Upselling target',
        'CAC comparison baseline',
        'Cross-sell effectiveness',
        'Bundling opportunity indicator',
        'Growth momentum tracker'
    ]
})

print(kpi_summary.to_string(index=False))

print("\n" + "=" * 70)
print("✅ KPI CALCULATIONS COMPLETE")
print("=" * 70)
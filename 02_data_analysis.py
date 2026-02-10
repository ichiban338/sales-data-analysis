"""
Exploratory Data Analysis Script
Author: Juan Esteban Agudelo Alonso
Project: Sales Data Analysis Portfolio
"""

import pandas as pd
import numpy as np

# Load data
print("=" * 70)
print("EXPLORATORY DATA ANALYSIS")
print("=" * 70)

df = pd.read_csv('sales_data.csv')
df['sale_date'] = pd.to_datetime(df['sale_date'])
df['year_month'] = df['sale_date'].dt.to_period('M')

# ==========================================
# DATA QUALITY CHECKS
# ==========================================

print("\n🔍 DATA QUALITY ASSESSMENT")
print("-" * 70)

print("\n1. Missing Values:")
missing = df.isnull().sum()
if missing.sum() == 0:
    print("   ✅ No missing values")
else:
    print(missing[missing > 0])

print(f"\n2. Duplicate Transactions: {df.duplicated(subset='transaction_id').sum()}")
print("   ✅ No duplicates" if df.duplicated(subset='transaction_id').sum() == 0 else "   ⚠️  Duplicates found")

revenue_valid = (df['quantity'] * df['unit_price'] == df['revenue']).all()
print(f"\n3. Revenue Calculation Valid: {revenue_valid}")
print("   ✅ All calculations correct" if revenue_valid else "   ⚠️  Issues found")

# ==========================================
# DESCRIPTIVE STATISTICS
# ==========================================

print("\n" + "=" * 70)
print("📊 DESCRIPTIVE STATISTICS")
print("=" * 70)

print(f"\nTotal Transactions: {len(df):,}")
print(f"Date Range: {df['sale_date'].min().date()} to {df['sale_date'].max().date()}")
print(f"Unique Customers: {df['customer_id'].nunique():,}")
print(f"Unique Products: {df['product'].nunique()}")
print(f"Product Categories: {df['product_category'].nunique()}")

print("\n💰 Revenue Statistics:")
print(f"  Total Revenue: ${df['revenue'].sum():,.2f}")
print(f"  Average Transaction: ${df['revenue'].mean():,.2f}")
print(f"  Median Transaction: ${df['revenue'].median():,.2f}")
print(f"  Max Transaction: ${df['revenue'].max():,.2f}")
print(f"  Min Transaction: ${df['revenue'].min():,.2f}")

print("\n📦 Quantity Statistics:")
print(df['quantity'].describe())

# ==========================================
# TIME-SERIES ANALYSIS
# ==========================================

print("\n" + "=" * 70)
print("📅 TIME-SERIES ANALYSIS")
print("=" * 70)

monthly_revenue = df.groupby('year_month')['revenue'].sum().reset_index()
monthly_revenue['year_month'] = monthly_revenue['year_month'].astype(str)

print("\nMonthly Revenue:")
for _, row in monthly_revenue.iterrows():
    print(f"  {row['year_month']}: ${row['revenue']:,.2f}")

monthly_revenue_series = df.groupby('year_month')['revenue'].sum()
monthly_growth = monthly_revenue_series.pct_change() * 100

print("\nMonth-over-Month Growth (%):")
for month, growth in monthly_growth.items():
    if pd.notna(growth):
        print(f"  {month}: {growth:+.2f}%")

# ==========================================
# PRODUCT ANALYSIS
# ==========================================

print("\n" + "=" * 70)
print("🏆 PRODUCT PERFORMANCE")
print("=" * 70)

top_products = df.groupby('product')['revenue'].sum().sort_values(ascending=False).head(10)

print("\nTop 10 Products by Revenue:")
for i, (product, revenue) in enumerate(top_products.items(), 1):
    pct = (revenue / df['revenue'].sum()) * 100
    print(f"  {i}. {product}: ${revenue:,.2f} ({pct:.1f}%)")

# ==========================================
# CATEGORY ANALYSIS
# ==========================================

print("\n" + "=" * 70)
print("📦 CATEGORY PERFORMANCE")
print("=" * 70)

category_revenue = df.groupby('product_category')['revenue'].sum().sort_values(ascending=False)

print("\nRevenue by Category:")
total_revenue = df['revenue'].sum()
for category, revenue in category_revenue.items():
    pct = (revenue / total_revenue) * 100
    print(f"  {category}: ${revenue:,.2f} ({pct:.1f}%)")

# ==========================================
# CUSTOMER ANALYSIS
# ==========================================

print("\n" + "=" * 70)
print("👥 CUSTOMER ANALYSIS")
print("=" * 70)

top_customers = df.groupby('customer_id')['revenue'].sum().sort_values(ascending=False).head(10)

print("\nTop 10 Customers by Revenue:")
for i, (customer, revenue) in enumerate(top_customers.items(), 1):
    print(f"  {i}. {customer}: ${revenue:,.2f}")

customer_frequency = df.groupby('customer_id').size()
print("\nCustomer Purchase Frequency:")
print(customer_frequency.describe())

print("\n" + "=" * 70)
print("✅ ANALYSIS COMPLETE")
print("=" * 70)
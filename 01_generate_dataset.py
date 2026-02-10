"""
Sales Dataset Generation Script
Author: Juan Esteban Agudelo Alonso
Project: Sales Data Analysis Portfolio
Description: Generates synthetic sales data for portfolio demonstration
"""

import pandas as pd
import numpy as np
from datetime import datetime

# Configuration
np.random.seed(42)
n_transactions = 2500

print("=" * 70)
print("SALES DATASET GENERATION")
print("=" * 70)

# ==========================================
# PRODUCT CATALOG
# ==========================================

products_catalog = {
    'Laptops': [
        ('MacBook Pro 14"', 1899),
        ('Dell XPS 13', 1299),
        ('HP Pavilion 15', 749),
        ('Lenovo ThinkPad', 1099)
    ],
    'Smartphones': [
        ('iPhone 15 Pro', 999),
        ('Samsung Galaxy S24', 899),
        ('Google Pixel 8', 699),
        ('OnePlus 12', 649)
    ],
    'Tablets': [
        ('iPad Air', 599),
        ('Samsung Tab S9', 549),
        ('Microsoft Surface Go', 449)
    ],
    'Accessories': [
        ('Wireless Mouse', 29),
        ('USB-C Cable', 19),
        ('Laptop Stand', 49),
        ('Webcam HD', 79),
        ('Bluetooth Headphones', 149)
    ],
    'Monitors': [
        ('Dell 27" 4K Monitor', 399),
        ('LG UltraWide 34"', 549),
        ('Samsung 24" FHD', 179)
    ]
}

print("\n📦 Product Catalog Loaded")
print(f"   Categories: {len(products_catalog)}")
total_products = sum(len(prods) for prods in products_catalog.values())
print(f"   Total Products: {total_products}")

# ==========================================
# GENERATE DATES (with seasonality)
# ==========================================

print("\n📅 Generating transaction dates...")

dates = []
for _ in range(n_transactions):
    # Higher probability in Q4 (holiday season)
    month = np.random.choice(
        range(1, 13),
        p=[0.07, 0.07, 0.08, 0.08, 0.08, 0.08, 
           0.08, 0.08, 0.09, 0.09, 0.10, 0.10]
    )
    day = np.random.randint(1, 29)
    dates.append(datetime(2024, month, day))

print(f"   ✅ Generated {len(dates):,} transaction dates")

# ==========================================
# GENERATE PRODUCTS AND CATEGORIES
# ==========================================

print("\n🏷️  Assigning products to transactions...")

categories = []
products = []
unit_prices = []

for _ in range(n_transactions):
    # Category selection with realistic distribution
    category = np.random.choice(
        list(products_catalog.keys()),
        p=[0.25, 0.30, 0.12, 0.23, 0.10]  # Smartphones highest
    )
    
    # Product selection within category
    product, price = products_catalog[category][
        np.random.randint(0, len(products_catalog[category]))
    ]
    
    categories.append(category)
    products.append(product)
    unit_prices.append(price)

print(f"   ✅ Products assigned")

# ==========================================
# GENERATE QUANTITIES
# ==========================================

print("\n📊 Generating purchase quantities...")

# Most orders are 1-2 items, occasional bulk
quantities = np.random.choice(
    [1, 2, 3, 4, 5],
    n_transactions,
    p=[0.60, 0.25, 0.10, 0.03, 0.02]
)

print(f"   ✅ Quantities generated")
print(f"   Single-item purchases: {(quantities == 1).sum()} ({(quantities == 1).sum()/len(quantities)*100:.1f}%)")

# ==========================================
# GENERATE CUSTOMER IDs
# ==========================================

print("\n👥 Generating customer data...")

# Simulate repeat customers
n_unique_customers = 800
customer_ids = [
    f'CUST{str(i).zfill(4)}' 
    for i in np.random.randint(1, n_unique_customers + 1, n_transactions)
]

print(f"   ✅ {n_unique_customers:,} unique customers")
print(f"   ✅ {n_transactions:,} total transactions")

# ==========================================
# CREATE DATAFRAME
# ==========================================

print("\n🔧 Building dataset...")

df = pd.DataFrame({
    'transaction_id': [f'TXN{str(i).zfill(5)}' for i in range(1, n_transactions + 1)],
    'sale_date': dates,
    'product': products,
    'product_category': categories,
    'customer_id': customer_ids,
    'quantity': quantities,
    'unit_price': unit_prices
})

# Calculate revenue
df['revenue'] = df['quantity'] * df['unit_price']

# Sort by date
df = df.sort_values('sale_date').reset_index(drop=True)

# ==========================================
# SAVE DATASET
# ==========================================

print("\n💾 Saving dataset...")

df.to_csv('sales_data.csv', index=False)

print("   ✅ Saved as: sales_data.csv")

# ==========================================
# SUMMARY STATISTICS
# ==========================================

print("\n" + "=" * 70)
print("📊 DATASET SUMMARY")
print("=" * 70)

print(f"\n📌 Dimensions: {len(df):,} rows × {len(df.columns)} columns")
print(f"📅 Date Range: {df['sale_date'].min().date()} to {df['sale_date'].max().date()}")
print(f"💰 Total Revenue: ${df['revenue'].sum():,.2f}")
print(f"📊 Average Transaction: ${df['revenue'].mean():,.2f}")
print(f"👥 Unique Customers: {df['customer_id'].nunique():,}")
print(f"📦 Unique Products: {df['product'].nunique()}")

print("\n📋 First 5 Rows:")
print(df.head())

print("\n📋 Revenue by Category:")
category_revenue = df.groupby('product_category')['revenue'].sum().sort_values(ascending=False)
for cat, rev in category_revenue.items():
    pct = (rev / df['revenue'].sum()) * 100
    print(f"   {cat}: ${rev:,.2f} ({pct:.1f}%)")

print("\n" + "=" * 70)
print("✅ DATASET GENERATION COMPLETE!")
print("=" * 70)
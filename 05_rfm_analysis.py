"""
RFM Customer Segmentation Analysis
Author: Juan Esteban Agudelo Alonso
Project: Sales Data Analysis Portfolio
Description: Segments customers using RFM methodology for targeted marketing
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
df = pd.read_csv('sales_data.csv')
df['sale_date'] = pd.to_datetime(df['sale_date'])

# Reference date (day after last transaction)
reference_date = df['sale_date'].max() + pd.Timedelta(days=1)

print("=" * 70)
print("RFM CUSTOMER SEGMENTATION ANALYSIS")
print("=" * 70)

# ==========================================
# CALCULATE RFM METRICS
# ==========================================

print("\n📊 Calculating RFM metrics...")

rfm = df.groupby('customer_id').agg({
    'sale_date': lambda x: (reference_date - x.max()).days,  # Recency
    'transaction_id': 'count',  # Frequency
    'revenue': 'sum'  # Monetary
}).reset_index()

rfm.columns = ['customer_id', 'recency', 'frequency', 'monetary']

print(f"   ✅ Analyzed {len(rfm):,} customers")
print(f"\n   Recency range: {rfm['recency'].min()}-{rfm['recency'].max()} days")
print(f"   Frequency range: {rfm['frequency'].min()}-{rfm['frequency'].max()} transactions")
print(f"   Monetary range: ${rfm['monetary'].min():,.0f}-${rfm['monetary'].max():,.0f}")

# ==========================================
# CALCULATE RFM SCORES (1-5)
# ==========================================

print("\n🎯 Calculating RFM scores (1-5 scale)...")

# Recency: lower is better (bought recently)
rfm['R_score'] = pd.qcut(rfm['recency'], q=5, labels=[5, 4, 3, 2, 1])

# Frequency: higher is better
rfm['F_score'] = pd.qcut(rfm['frequency'].rank(method='first'), q=5, labels=[1, 2, 3, 4, 5])

# Monetary: higher is better
rfm['M_score'] = pd.qcut(rfm['monetary'], q=5, labels=[1, 2, 3, 4, 5])

# Convert to numeric
rfm['R_score'] = rfm['R_score'].astype(int)
rfm['F_score'] = rfm['F_score'].astype(int)
rfm['M_score'] = rfm['M_score'].astype(int)

# Combined RFM score
rfm['RFM_score'] = rfm['R_score'] + rfm['F_score'] + rfm['M_score']

print("   ✅ RFM scores calculated")

# ==========================================
# SEGMENT CUSTOMERS
# ==========================================

print("\n🏷️  Segmenting customers...")

def segment_customer(row):
    """
    Assign customer segment based on RFM scores
    """
    r = row['R_score']
    f = row['F_score']
    m = row['M_score']
    
    # Champions: Best customers
    if r >= 4 and f >= 4 and m >= 4:
        return 'Champions'
    
    # Loyal Customers: Buy frequently, spend well
    elif f >= 4 and m >= 4:
        return 'Loyal Customers'
    
    # Potential Loyalists: Recent buyers with potential
    elif r >= 4 and f >= 2:
        return 'Potential Loyalists'
    
    # At Risk: Good customers who haven't bought recently
    elif r <= 2 and f >= 3 and m >= 3:
        return 'At Risk'
    
    # Can't Lose Them: High-value customers at risk
    elif r <= 2 and m >= 4:
        return "Can't Lose Them"
    
    # Hibernating: Inactive customers
    elif r <= 2 and f <= 2:
        return 'Hibernating'
    
    # New Customers: Recent first-time buyers
    elif r >= 4 and f <= 2:
        return 'New Customers'
    
    # Promising: New with potential
    elif r >= 3 and f == 1:
        return 'Promising'
    
    else:
        return 'Others'

rfm['segment'] = rfm.apply(segment_customer, axis=1)

print("   ✅ Segmentation complete")

# ==========================================
# SEGMENT ANALYSIS
# ==========================================

print("\n" + "=" * 70)
print("📊 SEGMENT ANALYSIS")
print("=" * 70)

segment_analysis = rfm.groupby('segment').agg({
    'customer_id': 'count',
    'recency': 'mean',
    'frequency': 'mean',
    'monetary': ['sum', 'mean']
}).round(2)

segment_analysis.columns = ['Customer Count', 'Avg Recency (days)', 'Avg Frequency', 'Total Revenue', 'Avg Customer Value']
segment_analysis = segment_analysis.sort_values('Total Revenue', ascending=False)
segment_analysis['Revenue %'] = (segment_analysis['Total Revenue'] / rfm['monetary'].sum() * 100).round(1)

print(segment_analysis.to_string())

# ==========================================
# VISUALIZATION 1: Customer Distribution
# ==========================================

print("\n📊 Generating visualizations...")

segment_counts = rfm['segment'].value_counts().sort_values(ascending=False)

plt.figure(figsize=(14, 7))

colors = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D', '#6A994E', '#A7C957', '#81B29A', '#F2CC8F']
bars = plt.barh(range(len(segment_counts)), 
                segment_counts.values, 
                color=colors[:len(segment_counts)],
                edgecolor='black',
                linewidth=1.2)

plt.yticks(range(len(segment_counts)), segment_counts.index, fontsize=12)
plt.xlabel('Number of Customers', fontsize=13, fontweight='bold')
plt.title('Customer Distribution by RFM Segment', fontsize=16, fontweight='bold', pad=20)
plt.grid(axis='x', alpha=0.3)

for i, (segment, count) in enumerate(segment_counts.items()):
    pct = (count / len(rfm)) * 100
    plt.text(count, i, f' {count} ({pct:.1f}%)', 
             va='center', fontsize=11, fontweight='bold')

plt.tight_layout()
plt.savefig('rfm_customer_distribution.png', dpi=300, bbox_inches='tight')
print("   ✅ Saved: rfm_customer_distribution.png")
plt.close()

# ==========================================
# VISUALIZATION 2: Revenue by Segment
# ==========================================

segment_revenue = segment_analysis.sort_values('Total Revenue', ascending=False)

plt.figure(figsize=(14, 7))

bars = plt.barh(range(len(segment_revenue)), 
                segment_revenue['Total Revenue'], 
                color=colors[:len(segment_revenue)],
                edgecolor='black',
                linewidth=1.2)

plt.yticks(range(len(segment_revenue)), segment_revenue.index, fontsize=12)
plt.xlabel('Total Revenue ($)', fontsize=13, fontweight='bold')
plt.title('Revenue Contribution by Customer Segment', fontsize=16, fontweight='bold', pad=20)
plt.grid(axis='x', alpha=0.3)

for i, (segment, row) in enumerate(segment_revenue.iterrows()):
    plt.text(row['Total Revenue'], i, 
             f" ${row['Total Revenue']/1000:.0f}K ({row['Revenue %']:.1f}%)", 
             va='center', fontsize=11, fontweight='bold')

plt.tight_layout()
plt.savefig('rfm_revenue_by_segment.png', dpi=300, bbox_inches='tight')
print("   ✅ Saved: rfm_revenue_by_segment.png")
plt.close()

# ==========================================
# VISUALIZATION 3: Scatter Plot
# ==========================================

plt.figure(figsize=(14, 9))

segments_unique = rfm['segment'].unique()
colors_scatter = plt.cm.tab10(np.linspace(0, 1, len(segments_unique)))

for i, segment in enumerate(segments_unique):
    segment_data = rfm[rfm['segment'] == segment]
    plt.scatter(segment_data['frequency'], 
                segment_data['monetary'],
                s=120, 
                alpha=0.6, 
                c=[colors_scatter[i]], 
                label=segment,
                edgecolors='black',
                linewidths=0.5)

plt.xlabel('Frequency (Number of Purchases)', fontsize=13, fontweight='bold')
plt.ylabel('Monetary (Total Revenue $)', fontsize=13, fontweight='bold')
plt.title('RFM Segmentation: Frequency vs Monetary Value', fontsize=16, fontweight='bold', pad=20)
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=10)
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('rfm_scatter.png', dpi=300, bbox_inches='tight')
print("   ✅ Saved: rfm_scatter.png")
plt.close()

# ==========================================
# STRATEGIC RECOMMENDATIONS
# ==========================================

print("\n" + "=" * 70)
print("🎯 STRATEGIC RECOMMENDATIONS BY SEGMENT")
print("=" * 70)

strategies = {
    'Champions': '🏆 VIP program, early product access, referral rewards, dedicated support',
    'Loyal Customers': '💎 Cross-sell premium products, exclusive offers, loyalty benefits',
    'Potential Loyalists': '⭐ Membership offers, volume discounts, engagement campaigns',
    'New Customers': '🎁 Onboarding series, second purchase discount (10% within 30 days)',
    'Promising': '🌱 Educational content, welcome bundles, nurture campaigns',
    'At Risk': '⚠️  Win-back campaign, satisfaction survey, special retention offers',
    "Can't Lose Them": '🚨 URGENT: Direct manager contact, aggressive retention, problem resolution',
    'Hibernating': '💤 Re-engagement email, "We miss you" discount (20% comeback offer)',
    'Others': '📊 Monitor and collect more data for better segmentation'
}

for segment in segment_counts.index:
    if segment in segment_analysis.index:
        count = segment_counts[segment]
        revenue = segment_analysis.loc[segment, 'Total Revenue']
        avg_value = segment_analysis.loc[segment, 'Avg Customer Value']
        
        print(f"\n{segment}")
        print(f"  Customers: {count} | Revenue: ${revenue:,.0f} | Avg Value: ${avg_value:,.0f}")
        print(f"  Strategy: {strategies.get(segment, 'N/A')}")

# ==========================================
# SAVE RESULTS
# ==========================================

print("\n" + "=" * 70)
print("💾 SAVING RESULTS")
print("=" * 70)

rfm.to_csv('rfm_customer_segments.csv', index=False)
print("   ✅ Saved: rfm_customer_segments.csv")

segment_analysis.to_csv('rfm_segment_summary.csv')
print("   ✅ Saved: rfm_segment_summary.csv")

# ==========================================
# EXECUTIVE SUMMARY
# ==========================================

print("\n" + "=" * 70)
print("📈 EXECUTIVE SUMMARY")
print("=" * 70)

champions_loyal = segment_counts.get('Champions', 0) + segment_counts.get('Loyal Customers', 0)
at_risk_total = segment_counts.get('At Risk', 0) + segment_counts.get("Can't Lose Them", 0)
new_promising = segment_counts.get('New Customers', 0) + segment_counts.get('Promising', 0)

print(f"\n🏆 Champions + Loyal Customers: {champions_loyal} customers")
print("   → Implement VIP retention program")
print("   → Protect high-value revenue stream")

print(f"\n🚨 At Risk + Can't Lose Them: {at_risk_total} customers")
print("   → URGENT: Launch win-back campaign within 7 days")
print("   → High revenue at stake")

print(f"\n🌱 New + Promising: {new_promising} customers")
print("   → Onboarding automation opportunity")
print("   → Growth potential segment")

print("\n" + "=" * 70)
print("✅ RFM ANALYSIS COMPLETE")
print("=" * 70)
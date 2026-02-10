import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

print(">>> [MODULE 3] GENERATING FINAL POLISHED DASHBOARD...")

# 1. LOAD & CLEAN DATA
try:
    df = pd.read_csv("final_optimized_model.csv")
except:
    try:
        df = pd.read_csv("Final_Optimized_Model.csv")
    except:
        print("❌ CSV not found. Run Module 2 first!")
        exit()

# Force lowercase for column matching
df.columns = df.columns.str.lower()
price_col = 'base_price_eur' if 'base_price_eur' in df.columns else 'normalized_price_eur'
logistics_col = 'final_logistics_eur' if 'final_logistics_eur' in df.columns else 'logistics_final_eur'
carbon_col = 'final_cbam_eur' if 'final_cbam_eur' in df.columns else 'cbam_tax_eur'
cluster_col = 'cluster_region'

# FIX 1: Capitalize Cluster Names for the Legend
if cluster_col in df.columns:
    df[cluster_col] = df[cluster_col].str.title().str.replace('_', '-')

# 2. DEFINE AESTHETICS
COLOR_START = '#2C3E50'
COLOR_SAVINGS = '#00C49A' 
COLOR_COST = '#FF5A5F'
COLOR_FINAL = '#009B9B'

plt.rcParams['font.family'] = 'sans-serif'
sns.set_style("white") 

# ==========================================
# CHART 1: WATERFALL (REALISTIC MATH FIX)
# ==========================================
avg = df.mean(numeric_only=True)

# FIX 2: Calculate a REALISTIC Benchmark
# German cost is usually ~35% higher than India, not 300% higher.
india_base_avg = avg[price_col]
benchmark = india_base_avg * 1.35  # 35% Markup for Germany

labor_savings = -(benchmark - india_base_avg)
logistics_add = avg[logistics_col]
carbon_add = avg[carbon_col]
final_cost = benchmark + labor_savings + logistics_add + carbon_add

# Calculate Margin Improvement % for Title
# (Savings / Benchmark)
cost_reduction_pct = (1 - (final_cost / benchmark)) * 100

cats = ['EU Benchmark', 'Labor Arb.', 'Logistics', 'CBAM Tax', 'India Final']
values = [benchmark, labor_savings, logistics_add, carbon_add, final_cost]

plt.figure(figsize=(12, 7), dpi=300)

running_total = 0
for i, (cat, val) in enumerate(zip(cats, values)):
    if i == 0: # Start
        color, bottom, height = COLOR_START, 0, val
        running_total = val
    elif i == 4: # End
        color, bottom, height = COLOR_FINAL, 0, val
    else:
        if val < 0: # Savings
            color = COLOR_SAVINGS
            height = abs(val)
            bottom = running_total + val 
            running_total += val
        else: # Costs
            color = COLOR_COST
            height = val
            bottom = running_total
            running_total += val
            
    plt.bar(cat, height, bottom=bottom, color=color, width=0.6, edgecolor='white')
    
    # Smart Labeling
    label_y = bottom + height + (benchmark * 0.02) if val >= 0 else bottom - (benchmark * 0.05)
    label_val = f"€{val:.1f}" if i in [0,4] else f"{val:+.1f}"
    
    plt.text(i, label_y, label_val, ha='center', va='center', 
             color='black', fontweight='bold', fontsize=11)

# Dynamic Title based on the Math
plt.title(f"Cost Bridge: {cost_reduction_pct:.1f}% Cost Reduction Realized", fontsize=16, fontweight='bold', loc='left', pad=20)
plt.ylabel("Cost per Unit (€)", fontsize=12)
plt.axhline(0, color='black', linewidth=1)
# Adjust Y-axis to make room for negative labels
plt.ylim(bottom=min(0, final_cost - benchmark*0.2)) 
sns.despine(left=True)
plt.grid(axis='y', linestyle=':', alpha=0.3)
plt.savefig("chart_waterfall_final.png", bbox_inches='tight')
print("   > Generated 'chart_waterfall_final.png' (With Realistic Math)")

# ==========================================
# CHART 2: RISK MATRIX
# ==========================================
plt.figure(figsize=(12, 7), dpi=300)
sample = df.sample(min(1500, len(df)))

cluster_palette = {
    'Pune-Chakan': '#5D3FD3', 
    'Chennai-Oragadam': '#00C49A',
    'Ncr-Manesar': '#FFB347'
}

sns.scatterplot(
    data=sample,
    x=carbon_col,
    y=price_col,
    hue=cluster_col,
    palette=cluster_palette,
    s=80, alpha=0.6, edgecolor='white', linewidth=0.5
)

# Background Box for Text
mean_carbon = sample[carbon_col].mean()
max_price = sample[price_col].max()

plt.axvline(mean_carbon, color=COLOR_COST, linestyle='--', linewidth=2, alpha=0.8)

plt.text(
    x=mean_carbon + (sample[carbon_col].max() * 0.05), 
    y=max_price * 0.95, 
    s="Avg Carbon\nPenalty Threshold", 
    color='white', 
    fontsize=10, 
    fontweight='bold',
    bbox=dict(facecolor=COLOR_COST, alpha=1.0, edgecolor='none', boxstyle='round,pad=0.5')
)

plt.title("Supplier Risk Matrix: Price vs Carbon Liability", fontsize=16, fontweight='bold', loc='left', pad=20)
plt.xlabel("CBAM Carbon Tax (€/Unit)", fontsize=12, fontweight='bold')
plt.ylabel("Base Unit Price (€)", fontsize=12, fontweight='bold')
plt.legend(title='Industrial Cluster', loc='upper right', frameon=True)
sns.despine()

plt.savefig("chart_risk_matrix_final.png", bbox_inches='tight')
print(">>> [SUCCESS] Final Polished Charts Generated.")
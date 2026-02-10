import pandas as pd
import numpy as np
import pulp # Linear Programming Solver
import sqlite3

# CONFIGURATION (Strategic Inputs)
EU_CARBON_PRICE_2026 = 85.0 # Euros per Ton
RISK_CAP_PCT = 0.30 # Strategy: "No Single Supplier > 30% Volume"

print(">>> [MODULE 2] INITIALIZING OPTIMIZATION ENGINE...")

# 1. RUNNING THE SQL LOGIC (Simulated via SQLite)
conn = sqlite3.connect(':memory:')

# Load Raw CSVs (Using lowercase filenames from Step 1)
try:
    pd.read_csv("raw_data/erp_supplier_master.csv").to_sql("erp_supplier_master", conn, index=False)
    pd.read_csv("raw_data/erp_procurement_data.csv").to_sql("erp_procurement_data", conn, index=False)
    pd.read_csv("raw_data/erp_logistics_rates.csv").to_sql("erp_logistics_rates", conn, index=False)
except FileNotFoundError:
    print("❌ ERROR: Raw CSVs not found. Run '01_generate_erp_data.py' first!")
    exit()

print("   > Executing SQL Logic (Quality Filtering & UOM Normalization)...")

# Mimicking the SQL Join/Filter using Pandas (matching lowercase schema)
suppliers = pd.read_sql("SELECT * FROM erp_supplier_master", conn)
procurement = pd.read_sql("SELECT * FROM erp_procurement_data", conn)
logistics = pd.read_sql("SELECT * FROM erp_logistics_rates", conn)

df = procurement.merge(suppliers, on='supplier_id').merge(logistics, on='cluster_region')

# Normalize Prices (UOM Fix)
df['normalized_price_eur'] = np.where(
    df['uom'] == 'ea',
    df['base_price_eur'] * df['weight_kg'],
    df['base_price_eur']
)
# Apply SQL Quality Gate (Using 'quality_ppm' from Step 1)
df = df[df['quality_ppm'] < 350] 

# 2. CALCULATING TOTAL LANDED COST (The "Scenario")
def calculate_landed_cost(row):
    # A. Logistics with Volatility (Monte Carlo Lite)
    shock_factor = np.random.uniform(1 - row['volatility_idx'], 1 + row['volatility_idx'])
    logistics_cost = (row['weight_kg'] * row['freight_rate'] * shock_factor) + row['handling_fee']

    # B. CBAM Tax (Tiered Logic)
    material_factor = 1.0 if 'steel' in row['material_type'] else 0.6
    emissions_ton = (row['weight_kg'] / 1000) * row['carbon_intensity'] * material_factor
    cbam_tax = emissions_ton * EU_CARBON_PRICE_2026

    return logistics_cost, cbam_tax

# Vectorized Application
results = df.apply(calculate_landed_cost, axis=1, result_type='expand')
df['final_logistics_eur'] = results[0]
df['final_cbam_eur'] = results[1]
df['total_landed_cost'] = df['normalized_price_eur'] + df['final_logistics_eur'] + df['final_cbam_eur']

# 3. THE SOLVER (Constrained Optimization)
print("   > Running PuLP Linear Solver for Strategic Allocation...")

# Group by Supplier to simplify the solver
supplier_agg = df.groupby('supplier_id').agg({
    'total_landed_cost': 'mean',
    'capacity_limit': 'max' # Matches 'capacity_limit' from Step 1
}).reset_index()

total_demand_units = 50000
suppliers_list = supplier_agg['supplier_id'].tolist()
costs = dict(zip(suppliers_list, supplier_agg['total_landed_cost']))
caps = dict(zip(suppliers_list, supplier_agg['capacity_limit']))

# Define LP Problem
prob = pulp.LpProblem("EuroLink_Risk_Allocator", pulp.LpMinimize)
allocation = pulp.LpVariable.dicts("Units", suppliers_list, lowBound=0, cat='Integer')

# Objective: Minimize Cost
prob += pulp.lpSum([allocation[i] * costs[i] for i in suppliers_list])

# Constraints
prob += pulp.lpSum([allocation[i] for i in suppliers_list]) == total_demand_units # Meet Demand
risk_limit = total_demand_units * RISK_CAP_PCT

for i in suppliers_list:
    prob += allocation[i] <= caps[i] # Physical Capacity
    prob += allocation[i] <= risk_limit # Strategic Risk Cap (30%)

prob.solve()
print(f"   > Optimization Status: {pulp.LpStatus[prob.status]}")

# 4. MAPPING RESULTS & CONSTRAINT STATUS
print("   > Assigning Constraint Status Flags...")

# Extract Solver Results into a Dictionary
optimized_volumes = {i: allocation[i].varValue for i in suppliers_list}

def get_status_label(supplier_id):
    vol = optimized_volumes.get(supplier_id, 0)
    max_cap = caps.get(supplier_id, 0)
    
    # Logic: Status Flags for Dashboard
    if vol >= risk_limit * 0.99: # Hit the 30% Strategy Cap
        return "Risk_Cap_Hit"
    elif vol >= max_cap * 0.95: # Hit the Physical Factory Limit
        return "Near_Physical_Limit"
    elif vol > 0:
        return "Optimal"
    else:
        return "Not_Selected"

# Apply Logic to Main DataFrame
df['allocated_volume'] = df['supplier_id'].map(optimized_volumes)
df['constraint_status'] = df['supplier_id'].apply(get_status_label)

# 5. EXPORT RESULTS
output_filename = "final_optimized_model.csv"
df.to_csv(output_filename, index=False)

print(f">>> [SUCCESS] Optimized Sourcing Plan exported to '{output_filename}'.")
print(f"   > Constraint breakdown:\n{df['constraint_status'].value_counts()}")
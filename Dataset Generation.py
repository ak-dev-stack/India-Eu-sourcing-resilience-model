import pandas as pd
import numpy as np
import os

# CONFIGURATION
np.random.seed(2026)
NUM_SKUS = 24500
NUM_SUPPLIERS = 120
OUTPUT_DIR = "raw_data"

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

print(f">>> [MODULE 1] GENERATING CLEAN ERP DATA ({NUM_SKUS} SKUs)...")

# --- 1. SUPPLIER MASTER (Lowercase Columns) ---
clusters = ['pune_chakan', 'chennai_oragadam', 'ncr_manesar']
supplier_ids = [f"sup_{np.random.choice(clusters)[:3]}_{i:03d}" for i in range(NUM_SUPPLIERS)]

df_suppliers = pd.DataFrame({
    'supplier_id': supplier_ids,
    'cluster_region': [np.random.choice(clusters, p=[0.45, 0.35, 0.2]) for _ in range(NUM_SUPPLIERS)],
    'quality_ppm': np.random.exponential(150, NUM_SUPPLIERS).astype(int), 
    'carbon_intensity': np.random.uniform(1.2, 2.5, NUM_SUPPLIERS), 
    'capacity_limit': np.random.randint(5000, 50000, NUM_SUPPLIERS)
})
df_suppliers.to_csv(f"{OUTPUT_DIR}/erp_supplier_master.csv", index=False)

# --- 2. PROCUREMENT DATA (Lowercase Columns) ---
df_procurement = pd.DataFrame({
    'sku_id': [f"sku_2026_{i:05d}" for i in range(NUM_SKUS)],
    'supplier_id': np.random.choice(supplier_ids, NUM_SKUS),
    'material_type': np.random.choice(['steel_forging', 'alum_casting', 'electronics'], NUM_SKUS),
    'uom': np.random.choice(['ea', 'kg'], NUM_SKUS, p=[0.8, 0.2]), 
    'weight_kg': np.random.gamma(2, 2.5, NUM_SKUS).round(2),
    'base_price_eur': np.random.uniform(5, 50, NUM_SKUS).round(2)
})
df_procurement.to_csv(f"{OUTPUT_DIR}/erp_procurement_data.csv", index=False)

# --- 3. LOGISTICS RATES (Lowercase Columns) ---
df_logistics = pd.DataFrame({
    'cluster_region': clusters,
    'freight_rate': [1.25, 0.85, 1.40], 
    'handling_fee': [0.15, 0.05, 0.10],
    'volatility_idx': [0.12, 0.08, 0.15] 
})
df_logistics.to_csv(f"{OUTPUT_DIR}/erp_logistics_rates.csv", index=False)

print(">>> [SUCCESS] Generated clean lowercase datasets in '/raw_data'.")
/* 
   PROJECT EURO-LINK: DATA EXTRACTION LAYER
   NOTE: All identifiers are strictly lowercase to match SQLite schema.
*/

WITH supplier_quality_rank AS (
    -- Rank suppliers by quality (Ascending = Lower is Better)
    SELECT 
        supplier_id,
        cluster_region,
        carbon_grid_inte,
        capacity_max_uni,
        quality_score_pp,
        RANK() OVER (PARTITION BY cluster_region ORDER BY quality_score_pp ASC) as quality_rank
    FROM erp_supplier_master
    WHERE capacity_max_uni > 5000
),

clean_data AS (
    SELECT 
        t1.sku_id,
        t1.supplier_id,
        t1.material_categor,
        -- Normalize UOM: If 'ea', multiply by weight
        CASE 
            WHEN t1.uom = 'ea' THEN (t1.base_price_eur * t1.unit_weight_kg)
            ELSE t1.base_price_eur 
        END AS normalized_price_eur,
        t1.unit_weight_kg,
        t2.cluster_region,
        t2.carbon_grid_inte,
        t3.base_freight_eur,
        t3.inland_handling_,
        t3.volatility_index
        -- REMOVED THE TRAILING COMMA HERE
    FROM erp_procurement_data t1
    JOIN supplier_quality_rank t2 ON t1.supplier_id = t2.supplier_id
    JOIN erp_logistics_rates t3 ON t2.cluster_region = t3.cluster_region
    WHERE t2.quality_rank <= 5 -- Top 5 Quality Suppliers only
)

SELECT * FROM clean_data;
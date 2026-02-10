# 🚗 Project Bridge  
### India–EU Sourcing & CBAM Optimization Engine  

> A constrained optimization engine that models cost-efficient, low-carbon sourcing decisions for EU-bound automotive supply chains under CBAM regulations and operational risk constraints.

---

## 📌 Executive Overview

As European OEMs diversify sourcing away from China, India offers strong labor arbitrage — but **logistics volatility**, **carbon taxation (CBAM)**, and **supplier concentration risk** distort headline savings.

**Project Bridge** simulates a realistic procurement environment and applies **linear programming optimization** to answer:

> **Which suppliers should we source from, in what volumes, to minimize total landed cost while managing carbon and operational risk?**

---

## 🧠 What This Engine Solves

✅ Total Landed Cost (TLC) modeling  
✅ CBAM carbon tax exposure pricing  
✅ Freight volatility injection  
✅ Supplier capacity & risk caps  
✅ Optimal allocation via LP solver  
✅ Governance-ready constraint flags  

---

## 🏗️ End-to-End Architecture

```text
📦 Synthetic ERP Data
      ↓
🧮 SQL ETL & Quality Gate
      ↓
💰 TLC + CBAM Engine
      ↓
📉 Linear Programming Solver
      ↓
📊 Risk Dashboards & Cost Bridge
```

---

## 📂 Repository Layout

```text
raw_data/
│  ├─ ERP_Supplier_Master.csv
│  ├─ ERP_Procurement_Data.csv
│  └─ ERP_Logistics_Rates.csv
│
engine.py
Final_Optimized_Model.csv
charts/
│  ├─ supplier_risk_matrix.png
│  └─ cost_bridge.png
README.md
```

---

## ⚙️ Engine Walkthrough

### 🔹 1. ERP Normalization & Quality Gate

✔ Multi-table joins  
✔ Unit-of-measure correction  
✔ Defect-rate filtering  

> Only auto-grade suppliers enter optimization.

---

### 🔹 2. Total Landed Cost Logic

```text
TLC = Base Price 
    + Logistics Cost (volatility-adjusted) 
    + CBAM Carbon Tax
```

---

### 🔹 3. Strategic Optimization (PuLP)

🎯 Objective  
Minimize total sourcing cost

📏 Constraints  

- Demand fulfillment  
- Factory capacity limits  
- **Risk cap: max 30% per supplier**

---

### 🔹 4. Governance Layer

Each supplier classified as:

| Status | Meaning |
|-------|--------|
| Optimal | Efficient allocation |
| Risk_Cap_Hit | Concentration limit reached |
| Near_Physical_Limit | Factory constrained |
| Not_Selected | Economically unviable |

---

## 📊 Visual Analytics

### 📍 Supplier Risk Matrix  
*Price vs Carbon Liability by industrial cluster*

### 📍 Cost Bridge (Waterfall)  
*Labor savings vs logistics + CBAM friction*

---

## 📈 Key Outcomes

| Metric | Impact |
|------|------|
| 💸 Net Cost Reduction | **8.0% realized** |
| 🌱 Carbon Risk | **€4.2M avoided** |
| 🏭 Supplier Base | **120 → 85** |
| ⚠ Risk Exposure | **<30% per supplier** |

---

## 🛠 Technology Stack

| Layer | Tools |
|------|------|
| Data | Pandas, NumPy |
| SQL | SQLite (ETL simulation) |
| Optimization | PuLP |
| Visualization | Matplotlib |
| Modeling | Python |

---

## 🎯 Business Applications

✔ Strategic sourcing decisions  
✔ ESG-compliant procurement  
✔ Supply-chain risk governance  
✔ Cost transformation programs  

---

## ⚠️ Disclaimer

Synthetic data used for modeling purposes only.  
This is a decision-support prototype aligned with CBAM and logistics frameworks.

---

## 👤 Author

**Ankit Kumar**  
Business Analytics | Operations Strategy | ESG Modeling  

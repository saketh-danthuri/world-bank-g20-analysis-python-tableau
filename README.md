# 🌍 World Bank G20 Data Analysis (Python API + Tableau)


## Table of Contents
- [Business Problem](#business-problem)
- [Data Gathering](#data-gathering)
- [Data Cleaning & Preparation](#data-cleaning--preparation)
- [Exploratory Data Analysis (EDA)](#exploratory-data-analysis-eda)
- [Research Questions & Key Findings](#research-questions--key-findings)
- [Dashboards](#dashboards)
- [Project Structure](#project-structure)
- [How to Run](#how-to-run)
- [Author](#author)

---

## Business Problem
Effective, comparable insights across **G20 economies** are essential for policy and investment decisions.  
This project asks whether **public services are keeping pace with growth** while also examining **trade, digital inclusion, and investment**.  
**Objectives:**
- Identify **growth leaders/laggards** across GDP and per‑capita metrics.
- Examine **trade balances** to understand external dependencies.
- Test whether **digital penetration aligns with income levels**.
- Assess if **public services** (electricity, literacy/education) keep up with growth.
- Summarize **FDI dynamics** and macro stability (inflation, unemployment).

---

## Data Gathering

Details on filtering World Bank datasets to include only G20 countries.

## Tools and Techniques

- Python (Pandas, Matplotlib, Seaborn)
- Tableau (Dashboards & Visuals)
- Jupyter Notebook for analysis
- World Bank API for data collection

## Project Structure

```
World-Bank-G20-Analysis
│   README.md
│
├── data
│   └── raw_data.csv
│
├── notebooks
│   └── G20_Countries_Analysis.ipynb
│
├── dashboards
│   ├── Dashboard_1.png
│   └── Dashboard_2.png
│
├── scripts
│   ├── data_cleaning.py
│   └── analysis.py
│
└── World_Bank_Project.twb
```

- Python (Pandas, Matplotlib, Seaborn)
- Tableau (Dashboards & Visuals)
- Jupyter Notebook for analysis
- World Bank API for data collection
- Source: **World Bank Open Data API** (`api.worldbank.org`)
- Countries: **G20 economies** only (filtered)
- Core Indicators (examples):
  - GDP total & per capita (`NY.GDP.MKTP.CD`, `NY.GDP.PCAP.CD`)
  - GNI per capita (`NY.GNP.PCAP.CD`)
  - Population (`SP.POP.TOTL`)
  - Life expectancy (`SP.DYN.LE00.IN`)
  - CO₂ per capita (`EN.ATM.CO2E.PC`)
  - Exports / Imports (`NE.EXP.GNFS.CD`, `NE.IMP.GNFS.CD`)
  - Mobile subscriptions per 100 (`IT.CEL.SETS.P2`)
  - Education spend & literacy (as available)
  - Access to electricity (as available)

> The **`scripts/fetch_data.py`** script automates pulling these indicators for 2000–2024.

---

## Data Cleaning & Preparation
- **Filter** to G20 economies only to ensure focused comparability.
- **Align years** (default 2015–2020) and **normalize country codes**.
- **Handle missingness**:
  - Drop columns with excessive nulls.
  - Fill remaining gaps by **median** (default) or **ffill/bfill**.
- Output: a tidy **wide** table `data/processed/g20_tidy.csv` and a **Tableau‑friendly long** file `data/processed/tableau_long.csv`.
- Scripts:
  - `scripts/clean_data.py` — shaping & imputation
  - `scripts/export_results.py` — exports for Tableau

---

## Exploratory Data Analysis (EDA)
**What we examined:**
- **GDP vs Gross Capital Formation** — investment intensity vs economy size.
- **Exports vs Imports** — export surplus/deficit patterns and exposure.
- **Mobile Subscriptions vs GNI** — **digital vs income** alignment.
- **FDI Distribution** — cross‑country dispersion and volatility.
- **Inflation & Unemployment** — macro stability signals.
- **Access to Electricity** — infrastructure reach and equity.
- **Education Spend vs Literacy** — efficiency of public services.

**Takeaways (high level):**
- Higher‑income members show **near‑saturation digital access**; emerging economies are **catching up fast**.
- **Trade imbalances** (e.g., persistent deficits or surpluses) indicate structural risks/opportunities.
- **FDI** is steadier in advanced economies; **volatility** is more common in emerging markets.
- **Public services** often lag pure income growth—**efficiency and policy** matter, not just spend.

---

## Research Questions & Key Findings
1. **Do higher digital penetration rates align with higher income?**  
   Yes—scatter of **GNI per capita vs mobile subscriptions/100** shows a positive alignment, with emerging members closing the gap.
2. **Are public services keeping pace with growth?**  
   Access to electricity is near‑universal for most, but **education outcomes** show **efficiency gaps** despite spend.
3. **How do trade balances affect sustainability?**  
   Export‑reliant economies (e.g., Germany, Korea) contrast with deficit economies (e.g., US); exposure differs.
4. **Where is FDI concentrating?**  
   Advanced economies attract **consistent inflows**; volatility in some emerging economies ties to policy & stability.

---

## Dashboards
### Dashboard — Growth, Trade, Digital, FDI
![Dashboard 1](dashboards/Dashboard_1.png)

### Dashboard — Inflation, Employment, Access, Education
![Dashboard 2](dashboards/Dashboard_2.png)

---

## Project Structure
```
.
├── data/
│   ├── raw/                      # Raw API downloads
│   └── processed/                # Cleaned outputs + Tableau-ready CSVs
├── notebooks/
│   └── G20_Countries_Analysis.ipynb
├── scripts/
│   ├── fetch_data.py             # World Bank API pulls (G20)
│   ├── clean_data.py             # Filter, align, impute; tidy wide
│   ├── analyze_data.py           # Correlations, hypothesis tests, snapshots
│   ├── visualize_data.py         # Reproducible matplotlib charts
│   └── export_results.py         # Exports for Tableau (long + per-indicator)
├── dashboards/
│   ├── World_Bank_Project.twb    # Tableau workbook
│   ├── Dashboard_1.png           # Snapshot for README
│   └── Dashboard_2.png           # Snapshot for README
├── reports/
│   └── World_Bank_G20_Analysis_Business_Report.pdf
├── requirements.txt
└── README.md
```

---

## How to Run
```bash
# 1) Install deps
pip install -r requirements.txt

# 2) Fetch World Bank indicators (G20, 2000–2024)
python scripts/fetch_data.py --start 2000 --end 2024 --verbose

# 3) Clean & prepare
python scripts/clean_data.py --fill median --verbose

# 4) Analyze
python scripts/analyze_data.py --latest_year_only --verbose

# 5) Visualize (PNG charts saved to reports/figures)
python scripts/visualize_data.py --latest_year_only

# 6) Export Tableau-friendly CSVs
python scripts/export_results.py --latest_year_only
```

---

## Author
**Saketh Danthuri**  
LinkedIn: https://www.linkedin.com/in/saketh-danthuri/


## Final Recommendations

- Encourage balanced trade policies to minimize export-import gaps.
- Strengthen education and digital infrastructure to keep pace with GDP growth.
- Support investment in renewable energy to ensure universal electricity access.
- Leverage mobile and digital penetration as a driver of inclusive growth.


## Authors

- **Saketh Danthuri**  
  [LinkedIn](https://www.linkedin.com/in/saketh-danthuri/)

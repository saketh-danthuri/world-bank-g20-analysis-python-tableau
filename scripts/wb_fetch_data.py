#!/usr/bin/env python3
"""
wb_fetch_data.py — Fetch World Bank indicators using wbdata like in the notebook.

Outputs:
- data/processed/g20_worldbankdata.csv
- data/processed/g20_worldbankdata.xlsx
"""
import os, argparse
import pandas as pd
import wbdata
from datetime import datetime

COUNTRIES = ['ARG','AUS','BRA','CAN','CHN','FRA','DEU','IND','IDN','ITA',
             'JPN','KOR','MEX','RUS','SAU','ZAF','TUR','GBR','USA']

INDICATOR_NAME_TO_ID = {
    'Gross Domestic Product (GDP)': 'NY.GDP.MKTP.CD',
    'Gross National Income (GNI)': 'NY.GNP.MKTP.CD',
    'Inflation rate': 'FP.CPI.TOTL.ZG',
    'Unemployment rate': 'SL.UEM.TOTL.ZS',
    'Poverty rate': 'SI.POV.NAHC',
    'Life expectancy': 'SP.DYN.LE00.IN',
    'Literacy rate': 'SE.ADT.LITR.ZS',
    'Access to electricity': 'EG.ELC.ACCS.ZS',
    'Mobile phone subscriptions': 'IT.CEL.SETS.P2',
    'Government expenditure on education': 'SE.XPD.TOTL.GB.ZS',
    'Foreign direct investment (FDI)': 'BX.KLT.DINV.WD.GD.ZS',
    'Exports of goods and services': 'NE.EXP.GNFS.ZS',
    'Imports of goods and services': 'NE.IMP.GNFS.ZS',
    'Gross capital formation': 'NE.GDI.TOTL.ZS',
    'Agricultural land (% of land area)': 'AG.LND.AGRI.ZS',
    'Food production index': 'AG.PRD.FOOD.XD',
}

def to_wb_mapping():
    # wbdata wants: {indicator_id: "Column Friendly Name"}
    return {v: k for k, v in INDICATOR_NAME_TO_ID.items()}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--start", default="2015-01-01")
    ap.add_argument("--end", default="2020-12-31")
    ap.add_argument("--outdir", default="data/processed")
    args = ap.parse_args()

    start = datetime.strptime(args.start, "%Y-%m-%d")
    end = datetime.strptime(args.end, "%Y-%m-%d")

    mapping = to_wb_mapping()
    df = wbdata.get_dataframe(mapping, country=COUNTRIES, date=(start, end))
    df = df.reset_index()  # bring 'country' and 'date' out of index

    os.makedirs(args.outdir, exist_ok=True)
    csv_path = os.path.join(args.outdir, "g20_worldbankdata.csv")
    xls_path = os.path.join(args.outdir, "g20_worldbankdata.xlsx")
    df.to_csv(csv_path, index=False)
    try:
        df.to_excel(xls_path, index=False)
    except Exception as e:
        print("Excel export skipped:", e)
    print("Wrote:", csv_path, "and", xls_path)

if __name__ == "__main__":
    main()

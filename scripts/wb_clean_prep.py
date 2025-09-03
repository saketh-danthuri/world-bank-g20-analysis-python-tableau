#!/usr/bin/env python3
"""
wb_clean_prep.py — Clean and prepare the fetched World Bank data like in the notebook.
- Parse dates
- Keep numeric columns
- Compute quick summary tables
- Save a tidy CSV ready for analysis & Tableau
"""
import os, argparse
import pandas as pd
import numpy as np

IN_PATH = "data/processed/g20_worldbankdata.csv"
OUT_DIR = "data/processed"
REPORTS_DIR = "reports"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", default=IN_PATH)
    ap.add_argument("--outdir", default=OUT_DIR)
    ap.add_argument("--reports", default=REPORTS_DIR)
    args = ap.parse_args()

    os.makedirs(args.outdir, exist_ok=True)
    os.makedirs(args.reports, exist_ok=True)

    df = pd.read_csv(args.input)
    # Parse "date" to datetime (same as notebook)
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")

    # Identify numeric indicator columns
    non_value_cols = [c for c in ["country", "countryiso3code", "date"] if c in df.columns]
    value_cols = [c for c in df.columns if c not in non_value_cols]

    # Convert numeric safely
    for c in value_cols:
        df[c] = pd.to_numeric(df[c], errors="coerce")

    # Save summary describe & skew like notebook
    desc = df[value_cols].describe().T.round(2)
    desc.to_csv(os.path.join(args.reports, "describe_transposed.csv"))
    skew = df[value_cols].skew().sort_values()
    skew.to_csv(os.path.join(args.reports, "skewness.csv"))

    # Save cleaned tidy file
    tidy_path = os.path.join(args.outdir, "g20_tidy.csv")
    df.to_csv(tidy_path, index=False)
    print("Wrote:", tidy_path)

if __name__ == "__main__":
    main()

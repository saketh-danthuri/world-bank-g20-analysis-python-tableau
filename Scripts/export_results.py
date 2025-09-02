#!/usr/bin/env python3
import os, argparse
import pandas as pd

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PROC = os.path.join(ROOT, "data", "processed", "g20_tidy.csv")
OUT = os.path.join(ROOT, "data", "processed")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", default=PROC)
    ap.add_argument("--outdir", default=OUT)
    ap.add_argument("--latest_year_only", action="store_true")
    args = ap.parse_args()

    os.makedirs(args.outdir, exist_ok=True)
    df = pd.read_csv(args.input)

    if args.latest_year_only:
        latest = df["year"].max()
        df = df[df["year"]==latest]

    value_cols = [c for c in df.columns if c not in ["countryiso3code","country","year"]]
    long = df.melt(id_vars=["countryiso3code","country","year"], value_vars=value_cols,
                   var_name="indicator", value_name="value")
    long.to_csv(os.path.join(args.outdir, "tableau_long.csv"), index=False)

    for col in value_cols:
        slim = df[["countryiso3code","country","year", col]].copy()
        slim.rename(columns={col: "value"}, inplace=True)
        slim.to_csv(os.path.join(args.outdir, f"indicator__{col}.csv"), index=False)

if __name__ == "__main__":
    main()

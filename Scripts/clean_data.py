#!/usr/bin/env python3
import os, argparse, logging
import pandas as pd
import numpy as np

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
RAW = os.path.join(ROOT, "data", "raw", "all_indicators.csv")
OUT = os.path.join(ROOT, "data", "processed")

INDICATOR_RENAMES = {
  "NY.GDP.MKTP.CD": "gdp_current_usd",
  "NY.GDP.PCAP.CD": "gdp_per_capita_current_usd",
  "SP.POP.TOTL": "population_total",
  "SP.DYN.LE00.IN": "life_expectancy_years",
  "EN.ATM.CO2E.PC": "co2_emissions_metric_tons_per_capita",
  "NY.GNS.ICTR.ZS": "gross_savings_pct_gdp",
  "NE.EXP.GNFS.CD": "exports_goods_services_current_usd",
  "NE.IMP.GNFS.CD": "imports_goods_services_current_usd",
  "IT.CEL.SETS.P2": "mobile_cellular_subscriptions_per_100",
  "NY.GNP.PCAP.CD": "gni_per_capita_current_usd"
}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", default=RAW)
    ap.add_argument("--outdir", default=OUT)
    ap.add_argument("--start", type=int, default=2000)
    ap.add_argument("--end", type=int, default=2024)
    ap.add_argument("--drop_missing_threshold", type=float, default=0.5)
    ap.add_argument("--fill", choices=["none","ffill","bfill","median"], default="median")
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()

    logging.basicConfig(level=logging.INFO if args.verbose else logging.WARNING,
                        format="%(asctime)s %(levelname)s %(message)s")
    os.makedirs(args.outdir, exist_ok=True)

    df = pd.read_csv(args.input)
    df = df[df["date"].astype(str).str.fullmatch(r"\d+")]
    df["year"] = df["date"].astype(int)
    df = df[(df["year"] >= args.start) & (df["year"] <= args.end)]

    df["indicator_slim"] = df["indicator"].map(INDICATOR_RENAMES).fillna(df["indicator"])
    wide = (df.pivot_table(index=["countryiso3code","country","year"],
                           columns="indicator_slim", values="value", aggfunc="first")
              .reset_index())

    miss_frac = wide.isna().mean()
    keep_cols = [c for c in wide.columns if miss_frac.get(c, 0) <= args.drop_missing_threshold]
    wide = wide[keep_cols]

    value_cols = [c for c in wide.columns if c not in ["countryiso3code","country","year"]]
    if args.fill == "ffill":
        wide = wide.sort_values(["countryiso3code","year"])
        wide[value_cols] = wide.groupby("countryiso3code")[value_cols].ffill()
    elif args.fill == "bfill":
        wide = wide.sort_values(["countryiso3code","year"])
        wide[value_cols] = wide.groupby("countryiso3code")[value_cols].bfill()
    elif args.fill == "median":
        for c in value_cols:
            median = wide[c].median(skipna=True)
            wide[c] = wide[c].fillna(median)

    out_path = os.path.join(args.outdir, "g20_tidy.csv")
    wide.to_csv(out_path, index=False)
    print(f"Wrote {out_path} with shape {wide.shape}")

if __name__ == "__main__":
    main()

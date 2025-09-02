#!/usr/bin/env python3
import os, argparse, logging
import pandas as pd
import numpy as np
from scipy import stats

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PROC = os.path.join(ROOT, "data", "processed", "g20_tidy.csv")
REPORTS = os.path.join(ROOT, "reports")

def corr_table(df, cols):
    corr = df[cols].corr(method="pearson")
    return corr

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", default=PROC)
    ap.add_argument("--outdir", default=REPORTS)
    ap.add_argument("--latest_year_only", action="store_true")
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()

    logging.basicConfig(level=logging.INFO if args.verbose else logging.WARNING,
                        format="%(asctime)s %(levelname)s %(message)s")
    os.makedirs(args.outdir, exist_ok=True)

    df = pd.read_csv(args.input)
    if args.latest_year_only:
        latest = df["year"].max()
        df = df[df["year"] == latest]

    cols = [c for c in ["gdp_current_usd","gdp_per_capita_current_usd","life_expectancy_years",
                        "co2_emissions_metric_tons_per_capita","mobile_cellular_subscriptions_per_100",
                        "gni_per_capita_current_usd"] if c in df.columns]
    if cols:
        ct = corr_table(df, cols)
        ct.to_csv(os.path.join(args.outdir, "correlations.csv"))

    if "gni_per_capita_current_usd" in df.columns and "life_expectancy_years" in df.columns:
        latest = df["year"].max()
        dfl = df[df["year"] == latest].copy()
        median_gni = dfl["gni_per_capita_current_usd"].median()
        dfl["group"] = np.where(dfl["gni_per_capita_current_usd"] >= median_gni, "advanced_like", "emerging_like")

        a = dfl.loc[dfl["group"]=="advanced_like","life_expectancy_years"].dropna()
        b = dfl.loc[dfl["group"]=="emerging_like","life_expectancy_years"].dropna()
        if len(a)>2 and len(b)>2:
            t, p = stats.ttest_ind(a, b, equal_var=False)
            with open(os.path.join(args.outdir, "hypothesis_test.md"), "w", encoding="utf-8") as f:
                f.write(f"# Hypothesis Test (Life Expectancy by Income Group)\n\n")
                f.write(f"Latest Year: {latest}\n")
                f.write(f"Groups: advanced_like (n={len(a)}) vs emerging_like (n={len(b)})\n\n")
                f.write(f"t = {t:.3f}, p = {p:.3g}\n")

    latest = df["year"].max()
    snap = df[df["year"]==latest].copy()
    snap.to_csv(os.path.join(args.outdir, "latest_snapshot.csv"), index=False)
    print("Analysis completed.")

if __name__ == "__main__":
    main()

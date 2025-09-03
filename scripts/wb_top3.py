#!/usr/bin/env python3
"""
wb_top3.py — Compute the "top 3 countries per year" for each indicator (like the notebook function).
Writes one CSV per indicator under reports/top3/ and a combined markdown summary.
"""
import os, argparse
import pandas as pd

IN_PATH = "data/processed/g20_tidy.csv"
OUTDIR = "reports/top3"

def top_3(data, parameter):
    year_list = data['date'].dt.year.sort_values().unique()
    result_df = pd.DataFrame(columns=year_list, index=[1,2,3])
    for year in year_list:
        df_year = data[data['date'].dt.year == year]
        value = (df_year.groupby('country')[parameter]
                        .sum()
                        .sort_values(ascending=False)
                        .head(3).index)
        result_df[year] = value
    return result_df

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", default=IN_PATH)
    ap.add_argument("--outdir", default=OUTDIR)
    args = ap.parse_args()

    os.makedirs(args.outdir, exist_ok=True)
    df = pd.read_csv(args.input)
    df["date"] = pd.to_datetime(df["date"])
    non_value_cols = [c for c in ["country","countryiso3code","date"] if c in df.columns]
    value_cols = [c for c in df.columns if c not in non_value_cols]

    # Write per-indicator top3 tables
    for col in value_cols:
        result = top_3(df, col)
        out = os.path.join(args.outdir, f"top3_{col.replace(' ', '_')}.csv")
        result.to_csv(out)

    # Write a compact winners list for the latest year
    latest = df["date"].dt.year.max()
    lines = ["# Top Winners (Latest Year {})\n".format(latest)]
    for col in value_cols:
        tmp = df[df["date"].dt.year == latest].groupby("country")[col].sum().sort_values(ascending=False)
        if not tmp.empty:
            lines.append(f"- **{col}** — {tmp.index[0]}")
    with open(os.path.join(args.outdir, "top_winners_latest.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print("Top-3 tables written to", args.outdir)

if __name__ == "__main__":
    main()

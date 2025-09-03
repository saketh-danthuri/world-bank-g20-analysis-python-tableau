#!/usr/bin/env python3
"""
wb_eda_plots.py — Recreate key visuals from the notebook:
- Histograms grid
- Boxplots grid
- Correlation heatmap
"""
import os, argparse
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

IN_PATH = "data/processed/g20_tidy.csv"
FIGDIR = "reports/figures"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", default=IN_PATH)
    ap.add_argument("--outdir", default=FIGDIR)
    args = ap.parse_args()

    os.makedirs(args.outdir, exist_ok=True)
    df = pd.read_csv(args.input)
    if "date" in df.columns:
        try:
            df["date"] = pd.to_datetime(df["date"])
        except Exception:
            pass

    non_value_cols = [c for c in ["country", "countryiso3code", "date"] if c in df.columns]
    value_cols = [c for c in df.columns if c not in non_value_cols]

    # Histograms grid
    n = len(value_cols)
    cols = 4
    rows = (n + cols - 1)//cols
    plt.figure(figsize=(4*cols, 3*rows))
    for i, col in enumerate(value_cols, start=1):
        plt.subplot(rows, cols, i)
        try:
            sns.histplot(df[col].dropna(), kde=True)
            plt.title(col, fontsize=9)
        except Exception:
            plt.title(col + " (skipped)")
    plt.tight_layout()
    plt.savefig(os.path.join(args.outdir, "histograms_grid.png"), bbox_inches="tight")
    plt.close()

    # Boxplots grid
    plt.figure(figsize=(4*cols, 3*rows))
    for i, col in enumerate(value_cols, start=1):
        plt.subplot(rows, cols, i)
        try:
            sns.boxplot(x=df[col].dropna())
            plt.title(col, fontsize=9)
        except Exception:
            plt.title(col + " (skipped)")
    plt.tight_layout()
    plt.savefig(os.path.join(args.outdir, "boxplots_grid.png"), bbox_inches="tight")
    plt.close()

    # Correlation heatmap
    corr = df[value_cols].corr()
    plt.figure(figsize=(max(8, len(value_cols)*0.6), max(6, len(value_cols)*0.6)))
    sns.heatmap(corr, annot=False, cmap="turbo")
    plt.title("Correlation Heatmap")
    plt.tight_layout();
    plt.savefig(os.path.join(args.outdir, "correlation_heatmap.png"), bbox_inches="tight")
    plt.close()

    print("Saved figures to", args.outdir)

if __name__ == "__main__":
    main()

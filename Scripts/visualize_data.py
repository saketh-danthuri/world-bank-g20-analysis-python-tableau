#!/usr/bin/env python3
import os, argparse
import pandas as pd
import matplotlib.pyplot as plt

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PROC = os.path.join(ROOT, "data", "processed", "g20_tidy.csv")
FIGDIR = os.path.join(ROOT, "reports", "figures")

def save_scatter(df, x, y, hue=None, title=None, outfile="scatter.png"):
    plt.figure()
    if hue and hue in df.columns:
        for k, sub in df.groupby(hue):
            plt.scatter(sub[x], sub[y], label=str(k))
        plt.legend()
    else:
        plt.scatter(df[x], df[y])
    plt.xlabel(x); plt.ylabel(y)
    if title: plt.title(title)
    os.makedirs(os.path.dirname(outfile), exist_ok=True)
    plt.savefig(outfile, bbox_inches="tight")
    plt.close()

def save_line(df, country_col, x, y, countries=None, title=None, outfile="line.png"):
    plt.figure()
    if countries:
        for c in countries:
            sub = df[df[country_col]==c]
            plt.plot(sub[x], sub[y], label=c)
        plt.legend()
    else:
        for c, sub in df.groupby(country_col):
            plt.plot(sub[x], sub[y], label=c, alpha=0.5)
    plt.xlabel(x); plt.ylabel(y)
    if title: plt.title(title)
    os.makedirs(os.path.dirname(outfile), exist_ok=True)
    plt.savefig(outfile, bbox_inches="tight")
    plt.close()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", default=PROC)
    ap.add_argument("--outdir", default=FIGDIR)
    ap.add_argument("--latest_year_only", action="store_true")
    args = ap.parse_args()

    os.makedirs(args.outdir, exist_ok=True)
    df = pd.read_csv(args.input)
    if args.latest_year_only:
        latest = df["year"].max()
        df = df[df["year"] == latest]

    if all(c in df.columns for c in ["gni_per_capita_current_usd","mobile_cellular_subscriptions_per_100"]):
        save_scatter(df, "gni_per_capita_current_usd", "mobile_cellular_subscriptions_per_100",
                     title="Digital Penetration vs Income", outfile=os.path.join(args.outdir, "digital_vs_income.png"))
    if all(c in df.columns for c in ["year","country","gdp_per_capita_current_usd"]):
        save_line(df, "country", "year", "gdp_per_capita_current_usd",
                  title="GDP per Capita Over Time", outfile=os.path.join(args.outdir, "gdp_capita_trends.png"))

if __name__ == "__main__":
    main()

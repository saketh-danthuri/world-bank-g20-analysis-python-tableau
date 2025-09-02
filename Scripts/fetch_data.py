#!/usr/bin/env python3
import os, sys, csv, json, time, argparse, logging
from typing import List, Dict
import requests

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
RAW_DIR = os.path.join(ROOT, "data", "raw")

G20_CODES = {
  "ARG": "Argentina",
  "AUS": "Australia",
  "BRA": "Brazil",
  "CAN": "Canada",
  "CHN": "China",
  "FRA": "France",
  "DEU": "Germany",
  "IND": "India",
  "IDN": "Indonesia",
  "ITA": "Italy",
  "JPN": "Japan",
  "KOR": "Republic of Korea",
  "MEX": "Mexico",
  "RUS": "Russia",
  "SAU": "Saudi Arabia",
  "ZAF": "South Africa",
  "TUR": "Turkiye",
  "GBR": "United Kingdom",
  "USA": "United States"
}
INDICATORS = {
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

API = "https://api.worldbank.org/v2/country/{iso3}/indicator/{indicator}?date={start}:{end}&format=json&per_page=20000"

def fetch_indicator(indicator: str, start: int, end: int, countries: List[str]) -> List[Dict]:
    rows = []
    for iso3 in countries:
        url = API.format(iso3=iso3, indicator=indicator, start=start, end=end)
        logging.info(f"GET {url}")
        r = requests.get(url, timeout=60)
        r.raise_for_status()
        data = r.json()
        if not data or len(data) < 2 or data[1] is None:
            logging.warning(f"No data for {indicator} {iso3}")
            continue
        for item in data[1]:
            if item is None: 
                continue
            rows.append({
                "countryiso3code": item.get("countryiso3code"),
                "country": (item.get("country") or {}).get("value"),
                "indicator": indicator,
                "date": item.get("date"),
                "value": item.get("value")
            })
        time.sleep(0.25)
    return rows

def write_csv(path: str, rows: List[Dict]):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if not rows:
        logging.warning(f"No rows to write for {path}"); 
        return
    keys = sorted({k for r in rows for k in r.keys()})
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=keys)
        w.writeheader()
        for r in rows:
            w.writerow(r)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", type=int, default=2000)
    parser.add_argument("--end", type=int, default=2024)
    parser.add_argument("--indicators", nargs="*", default=list(INDICATORS.keys()))
    parser.add_argument("--countries", nargs="*", default=list(G20_CODES.keys()))
    parser.add_argument("--out", default=RAW_DIR)
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO if args.verbose else logging.WARNING,
                        format="%(asctime)s %(levelname)s %(message)s")

    all_rows = []
    for ind in args.indicators:
        rows = fetch_indicator(ind, args.start, args.end, args.countries)
        out_path = os.path.join(args.out, f"wb_{ind.replace('.', '_')}.csv")
        write_csv(out_path, rows)
        all_rows.extend(rows)
        logging.info(f"Wrote {len(rows)} rows to {out_path}")

    write_csv(os.path.join(args.out, "all_indicators.csv"), all_rows)
    logging.info("Done.")

if __name__ == "__main__":
    main()

"""Pull second-source data from the Association of Mutual Funds in India (AMFI) website APIs
(the same calls made by https://www.amfiindia.com/ter-of-mf-schemes and
https://www.amfiindia.com/otherdata/tracking-error).

Writes:
  data/raw/amfi_ter_<month>.csv   daily Total Expense Ratio (TER) rows for our nine schemes
  data/raw/amfi_tracking_error_<date>.csv  tracking error rows for our five index funds
"""
import csv
import json
import pathlib
import urllib.request

OUT = pathlib.Path(__file__).resolve().parent.parent / "data" / "raw"
BASE = "https://www.amfiindia.com/api"
SCHEMES = [  # exact AMFI scheme names (lower case) for matching
    "parag parikh flexi cap fund",
    "icici prudential nifty next 50 index fund",
    "hdfc mid cap fund",
    "axis large & mid cap fund",
    "icici prudential nifty it index fund",
    "jioblackrock nifty smallcap 250 index fund",
    "jioblackrock flexi cap fund",
    "jioblackrock nifty next 50 index fund",
    "motilal oswal nifty 500 index fund",
]
TE_HOUSES = {20: "ICICI Prudential", 55: "Motilal Oswal", 82: "JioBlackRock"}
TER_HOUSES = {64: "PPFAS", 20: "ICICI Prudential", 9: "HDFC", 53: "Axis", 82: "JioBlackRock", 55: "Motilal Oswal"}


def get(path):
    req = urllib.request.Request(BASE + path, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read())


def ter(month):
    rows = []
    for mf in TER_HOUSES:
        page = 1
        while True:
            d = get(f"/populate-te-rdata-revised?MF_ID={mf}&Month={month}&strCat=-1&strType=-1&page={page}&pageSize=100")
            rows += [r for r in d["data"] if r["Scheme_Name"].strip().lower() in SCHEMES]
            if page >= d["meta"]["pageCount"] or not d["data"]:
                break
            page += 1
    f = OUT / f"amfi_ter_{month}.csv"
    keys = ["Scheme_Name", "SchemeCat_Desc", "TER_Date", "D_BER", "D_BrokerageCost", "D_TransactionCost",
            "D_StatutoryLevies", "D_TER", "R_TER", "MF_ID"]
    with f.open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(keys + ["source_url"])
        for r in sorted(rows, key=lambda r: (r["Scheme_Name"], r["TER_Date"])):
            w.writerow([r.get(k) for k in keys] + [BASE + f"/populate-te-rdata-revised?MF_ID={r['MF_ID']}&Month={month}&strCat=-1&strType=-1"])
    print(month, len(rows), "rows", sorted({r["Scheme_Name"] for r in rows}))


def tracking_error(date):
    f = OUT / f"amfi_tracking_error_{date}.csv"
    with f.open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["Scheme_Name", "Benchmark", "RegularPercent", "DirectPercent", "date", "source_url"])
        for mf in TE_HOUSES:
            url = f"/tracking-error-data?MF_ID={mf}&strdt={date}"
            for r in get(url)["data"]:
                if r["Scheme_Name"].strip().lower() in SCHEMES:
                    w.writerow([r["Scheme_Name"], r["Benchmark"], r["RegularPercent"], r["DirectPercent"], r["date"], BASE + url])
                    print(date, r["Scheme_Name"], r["Benchmark"], r["DirectPercent"])


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for m in ("09-2026", "10-2026"):
        ter(m)
    for d in ("30-sep-2026", "30-sep-2025"):
        tracking_error(d)

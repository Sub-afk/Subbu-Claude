"""Return, rolling return, downside capture, tracking error and tracking difference
calculations from daily NAVs (data/raw/nav_<code>.csv, AMFI via mfapi.in) and daily
Total Return Index values (data/raw/tri_<index>.csv, NSE Indices).

All figures are for the Direct Plan Growth option and are measured to 30 September 2026,
the date of the factsheets used for cross-checking. Writes:
  data/performance_trailing.csv
  data/performance_rolling_active.csv
  data/tracking_index_funds.csv
"""
import csv
import math
import pathlib

import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
END = pd.Timestamp("2026-09-30")

FUNDS = [  # code, name, type, benchmark file, benchmark label, benchmark source note
    (122639, "Parag Parikh Flexi Cap Fund", "active", "nifty_500", "NIFTY 500 TRI", "factsheet"),
    (118989, "HDFC Mid Cap Fund", "active", "nifty_midcap_150", "NIFTY Midcap 150 TRI", "factsheet"),
    (145110, "Axis Large & Mid Cap Fund", "active", "nifty_largemidcap_250", "NIFTY LargeMidcap 250 TRI", "factsheet"),
    (153859, "JioBlackRock Flexi Cap Fund", "active", "nifty_500", "NIFTY 500 TRI (reference only, benchmark not verified)", "not verified"),
    (120684, "ICICI Prudential Nifty Next 50 Index Fund", "index", "nifty_next_50", "Nifty Next 50 TRI", "factsheet and AMFI"),
    (150468, "ICICI Prudential Nifty IT Index Fund", "index", "nifty_it", "Nifty IT TRI", "factsheet and AMFI"),
    (153790, "JioBlackRock Nifty Smallcap 250 Index Fund", "index", "nifty_smallcap_250", "Nifty Smallcap 250 TRI", "AMFI"),
    (153789, "JioBlackRock Nifty Next 50 Index Fund", "index", "nifty_next_50", "Nifty Next 50 TRI", "AMFI"),
    (147625, "Motilal Oswal Nifty 500 Index Fund", "index", "nifty_500", "NIFTY 500 TRI", "AMFI"),
]


def series(path, col):
    df = pd.read_csv(path, parse_dates=["date"]).drop_duplicates("date").set_index("date")[col].astype(float)
    return df.sort_index()


def value_on(s, d):
    """Last available value on or before date d (funds and indices skip holidays)."""
    s = s[:d]
    return (s.index[-1], s.iloc[-1]) if len(s) else (None, None)


def cagr(s, start, end):
    d0, v0 = value_on(s, start)
    d1, v1 = value_on(s, end)
    if d0 is None or d0 < s.index[0] or start < s.index[0]:
        return None
    yrs = (end - start).days / 365.0
    return (v1 / v0) ** (1 / yrs) - 1 if yrs > 1 else v1 / v0 - 1


def rolling(nav, tri, years):
    """Daily rolling CAGR over `years`, for every date where both series have data."""
    both = pd.concat([nav, tri], axis=1, keys=["f", "b"], sort=True).dropna()
    both = both[:END]
    out = []
    for d in both.index:
        start = d - pd.DateOffset(years=years)
        if start < both.index[0]:
            continue
        p = both[:start]
        if p.empty:
            continue
        f0, b0 = p.iloc[-1]
        f1, b1 = both.loc[d]
        out.append(((f1 / f0) ** (1 / years) - 1, (b1 / b0) ** (1 / years) - 1))
    return pd.DataFrame(out, columns=["fund", "bench"])


def capture(nav, tri, years):
    """Monthly up and down capture ratios (geometric average method) over the last `years`."""
    m = pd.concat([nav, tri], axis=1, keys=["f", "b"], sort=True).dropna()[:END].resample("ME").last()
    m = m[m.index > END - pd.DateOffset(years=years) - pd.DateOffset(days=5)].pct_change().dropna()
    if len(m) < 12 * years - 1:
        return None, None, len(m)
    res = []
    for mask in (m["b"] < 0, m["b"] > 0):
        x = m[mask]
        gf = (1 + x["f"]).prod() ** (1 / len(x)) - 1
        gb = (1 + x["b"]).prod() ** (1 / len(x)) - 1
        res.append(100 * gf / gb)
    return res[0], res[1], len(m)


def tracking(nav, tri, years):
    both = pd.concat([nav, tri], axis=1, keys=["f", "b"], sort=True).dropna()[:END]
    start = END - pd.DateOffset(years=years)
    if both.index[0] > start + pd.Timedelta(days=5):
        return None, None
    w = both[both.index >= value_on(both["f"], start)[0]]
    r = w.pct_change().dropna()
    te = (r["f"] - r["b"]).std() * math.sqrt(252)
    td = cagr(both["f"], start, END) - cagr(both["b"], start, END)
    return td, te


def pct(x):
    return "" if x is None else round(100 * x, 2)


def main():
    trailing, roll, track = [], [], []
    for code, name, kind, bfile, blabel, bsrc in FUNDS:
        nav = series(RAW / f"nav_{code}.csv", "nav")
        tri = series(RAW / f"tri_{bfile}.csv", "tri")
        row = {"fund": name, "benchmark": blabel, "benchmark_source": bsrc,
               "nav_first_date": nav.index[0].date(), "nav_30sep2026": value_on(nav, END)[1]}
        for y in (1, 3, 5, 10):
            st = END - pd.DateOffset(years=y)
            row[f"fund_{y}y_pct"] = pct(cagr(nav, st, END))
            row[f"bench_{y}y_pct"] = pct(cagr(tri, st, END)) if row[f"fund_{y}y_pct"] != "" else ""
        trailing.append(row)
        if kind == "active":
            for y in (3, 5):
                r = rolling(nav, tri, y)
                dc, uc, n = capture(nav, tri, y)
                roll.append({
                    "fund": name, "benchmark": blabel, "window_years": y, "observations": len(r),
                    "fund_avg_pct": pct(r["fund"].mean()) if len(r) else "",
                    "bench_avg_pct": pct(r["bench"].mean()) if len(r) else "",
                    "fund_min_pct": pct(r["fund"].min()) if len(r) else "",
                    "bench_min_pct": pct(r["bench"].min()) if len(r) else "",
                    "fund_max_pct": pct(r["fund"].max()) if len(r) else "",
                    "share_of_windows_fund_beat_bench_pct": round(100 * (r["fund"] > r["bench"]).mean(), 1) if len(r) else "",
                    f"downside_capture_last_{y}y": round(dc, 1) if dc is not None else "",
                    f"upside_capture_last_{y}y": round(uc, 1) if uc is not None else "",
                    "months_used_for_capture": n,
                })
        else:
            for y in (1, 3):
                td, te = tracking(nav, tri, y)
                track.append({"fund": name, "index": blabel, "period_years": y,
                              "tracking_difference_pct": pct(td), "tracking_error_pct": pct(te),
                              "note": "" if td is not None else "fund younger than period"})
    for fname, rows in (("performance_trailing.csv", trailing), ("performance_rolling_active.csv", roll),
                        ("tracking_index_funds.csv", track)):
        keys = list(dict.fromkeys(k for r in rows for k in r))
        with (ROOT / "data" / fname).open("w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=keys)
            w.writeheader()
            w.writerows(rows)
        print(pd.DataFrame(rows).to_string(index=False))


if __name__ == "__main__":
    main()

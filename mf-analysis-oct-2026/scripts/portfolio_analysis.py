"""Portfolio-level analysis: stock overlap matrix, effective exposure by market cap, sector and
underlying stock, duplicate detection, concentration flag and weighted expense ratio.

Inputs:  data/holdings_2026-09.csv (scripts/build_holdings.py)
         data/raw/amfi_ter_10-2026.csv (scripts/fetch_amfi.py)
         data/raw/nse/*.pdf sector tables for the two index funds whose own portfolios were not
         obtained (Nifty 500 and Nifty Smallcap 250)
         HOLDINGS below, copied from the investor's brief (values as of October 2026)
Outputs: data/portfolio_holdings_values.csv, data/overlap_matrix.csv, data/overlap_common_stocks.csv,
         data/exposure_market_cap.csv, data/exposure_sector.csv, data/exposure_top20_stocks.csv,
         data/weighted_expense_ratio.csv
"""
import csv
import pathlib
import re
import subprocess
from collections import defaultdict

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

HOLDINGS = [  # fund, invested (Rs), current value (Rs), short label
    ("Parag Parikh Flexi Cap Fund", 27740, 27450, "PPFAS Flexi"),
    ("ICICI Prudential Nifty Next 50 Index Fund", 15320, 14920, "ICICI NN50"),
    ("HDFC Mid Cap Fund", 9250, 9070, "HDFC Mid"),
    ("Axis Large & Mid Cap Fund", 6000, 6230, "Axis L&M"),
    ("ICICI Prudential Nifty IT Index Fund", 3800, 3850, "ICICI IT"),
    ("JioBlackRock Nifty Smallcap 250 Index Fund", 2500, 2440, "Jio SC250"),
    ("JioBlackRock Flexi Cap Fund", 1500, 1420, "Jio Flexi"),
    ("JioBlackRock Nifty Next 50 Index Fund", 1000, 999, "Jio NN50"),
    ("Motilal Oswal Nifty 500 Index Fund", 1000, 952, "MO N500"),
]
NSE_SECTOR_PDF = {
    "Motilal Oswal Nifty 500 Index Fund": "ind_nifty_500.pdf",
    "JioBlackRock Nifty Smallcap 250 Index Fund": "ind_nifty_smallcap_250.pdf",
}


LUMP_SUM = {"Motilal Oswal Nifty 500 Index Fund": 4000, "HDFC Mid Cap Fund": 2500,
            "Parag Parikh Flexi Cap Fund": 2000, "JioBlackRock Nifty Smallcap 250 Index Fund": 1500}
SIP = dict(LUMP_SUM)  # monthly; HDFC total of Rs 2,500 includes the Rs 500 SIP already running
CAP_ORDER = ["Large Cap", "Mid Cap", "Small Cap", "Domestic equity, size not known", "Overseas equity",
             "REITs and InvITs", "Arbitrage positions (hedged, behave like cash)", "Debt and cash",
             "Fund portfolio not obtained (JioBlackRock Flexi Cap)"]


def cap_mix(rows, share):
    """Percent of the portfolio in each size bucket, given each fund's share (0 to 1)."""
    cap = defaultdict(float)
    for r in rows:
        if r["fund"] not in share:
            continue
        s, w = share[r["fund"]], r["w"] / 100
        ac = r["asset_class"]
        sc250 = r["fund"] == "JioBlackRock Nifty Smallcap 250 Index Fund"
        if ac == "arbitrage":
            key = "Arbitrage positions (hedged, behave like cash)"
        elif ac == "domestic_equity":
            # rest of the Nifty Smallcap 250 index is small cap by the index's own definition
            key = r["mcap_category"] or ("Small Cap" if sc250 else "Domestic equity, size not known")
        elif ac == "domestic_equity_undisclosed":
            key = "Small Cap" if sc250 else "Domestic equity, size not known"
        elif ac.startswith("overseas"):
            key = "Overseas equity"
        elif ac == "reit_invit":
            key = "REITs and InvITs"
        elif ac == "debt_cash":
            key = "Debt and cash"
        else:
            key = "Fund portfolio not obtained (JioBlackRock Flexi Cap)"
        cap[key] += 100 * s * w
    return cap


def write(name, header, rows):
    with (DATA / name).open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(header)
        w.writerows(rows)


def nse_sectors(pdf):
    txt = subprocess.run(["pdftotext", "-f", "1", "-l", "1", "-layout", str(DATA / "raw" / "nse" / pdf), "-"],
                         capture_output=True, text=True).stdout
    part = txt[txt.find("Sector Representation"):txt.find("## Based on")]
    out = {}
    for line in part.splitlines():
        m = re.match(r"^\s(\S[A-Za-z,&\s]+?)\s{5,}(\d+\.\d{2})(\s|$)", line)
        if m and m.group(1).strip() not in ("Sector",):
            out[m.group(1).strip()] = float(m.group(2))
    return out


def main():
    rows = list(csv.DictReader(open(DATA / "holdings_2026-09.csv")))
    for r in rows:
        r["w"] = float(r["weight_pct"])
    total = sum(h[2] for h in HOLDINGS)
    share = {f: v / total for f, _, v, _ in HOLDINGS}
    label = {f: l for f, _, _, l in HOLDINGS}

    # 1. portfolio weights, concentration flag
    write("portfolio_holdings_values.csv",
          ["fund", "invested_rs", "current_rs", "gain_rs", "gain_pct", "share_of_portfolio_pct", "above_40pct_flag"],
          [[f, i, v, v - i, round(100 * (v - i) / i, 2), round(100 * v / total, 2), "YES" if v / total > 0.40 else "no"]
           for f, i, v, _ in HOLDINGS] + [["TOTAL", sum(h[1] for h in HOLDINGS), total,
                                           total - sum(h[1] for h in HOLDINGS), "", 100.0, ""]])

    # 2. overlap matrix: sum over shared ISINs of the smaller of the two weights
    stock = defaultdict(lambda: defaultdict(float))
    names = {}
    for r in rows:
        if r["isin"] and r["asset_class"] in ("domestic_equity", "overseas_equity", "reit_invit"):
            stock[r["fund"]][r["isin"]] += r["w"]
            names[r["isin"]] = r["company_amfi"] or r["holding"]
    funds = [h[0] for h in HOLDINGS]
    matrix, common_rows = [], []
    for a in funds:
        line = [label[a]]
        for b in funds:
            if a == b:
                line.append(100.0 if stock[a] else "")
                continue
            shared = set(stock[a]) & set(stock[b])
            line.append(round(sum(min(stock[a][i], stock[b][i]) for i in shared), 2) if stock[a] and stock[b] else "")
            if a < b and shared:
                for i in sorted(shared, key=lambda i: -min(stock[a][i], stock[b][i])):
                    common_rows.append([label[a], label[b], names[i], i, round(stock[a][i], 2), round(stock[b][i], 2)])
        matrix.append(line)
    write("overlap_matrix.csv", ["fund"] + [label[f] for f in funds], matrix)
    write("overlap_common_stocks.csv", ["fund_a", "fund_b", "stock", "isin", "weight_in_a_pct", "weight_in_b_pct"],
          common_rows)

    # 3. effective exposure by market cap, now and under the recommended split
    cap = cap_mix(rows, share)
    write("exposure_market_cap.csv", ["bucket", "share_of_portfolio_pct", "rupees"],
          [[k, round(cap[k], 2), round(cap[k] * total / 100)] for k in CAP_ORDER if k in cap])
    per_fund = [[label[f]] + [round(cap_mix(rows, {f: 1.0})[k], 2) for k in CAP_ORDER] for f in funds]
    write("fund_market_cap_mix.csv", ["fund"] + CAP_ORDER, per_fund)
    scen_rows = []
    for name, months in (("today", None), ("after Rs 10,000 lump sum", 0), ("after lump sum + 12 SIP months", 12),
                         ("after lump sum + 36 SIP months", 36)):
        val = {f: v for f, _, v, _ in HOLDINGS}
        if months is not None:
            for f, a in LUMP_SUM.items():
                val[f] += a
            for f, a in SIP.items():
                val[f] += a * months
        t = sum(val.values())
        sh = {f: v / t for f, v in val.items()}
        c = cap_mix(rows, sh)
        scen_rows.append([name, round(t), round(100 * sh["Parag Parikh Flexi Cap Fund"], 2),
                          round(100 * (sh["ICICI Prudential Nifty Next 50 Index Fund"] + sh["JioBlackRock Nifty Next 50 Index Fund"]), 2),
                          round(100 * sh["ICICI Prudential Nifty IT Index Fund"], 2)] + [round(c.get(k, 0), 2) for k in CAP_ORDER])
    write("scenario_allocation.csv", ["scenario (contributions only, no market returns assumed)", "portfolio_rs",
                                      "ppfas_share_pct", "nifty_next_50_funds_share_pct", "nifty_it_share_pct"] + CAP_ORDER,
          scen_rows)

    # 4. effective exposure by sector (NSE Indices sector names)
    sec = defaultdict(float)
    for r in rows:
        f = r["fund"]
        if f in NSE_SECTOR_PDF:
            continue
        key = "Arbitrage positions (hedged, behave like cash)" if r["asset_class"] == "arbitrage" else \
            r["sector"] or ("Fund portfolio not obtained (JioBlackRock Flexi Cap)" if r["asset_class"] == "undisclosed"
                              else "Domestic equity, sector not disclosed")
        sec[key] += share[f] * r["w"]
    for f, pdf in NSE_SECTOR_PDF.items():
        for k, v in nse_sectors(pdf).items():
            sec[k] += share[f] * v
    write("exposure_sector.csv", ["sector", "share_of_portfolio_pct", "rupees"],
          [[k, round(v, 2), round(v * total / 100)] for k, v in sorted(sec.items(), key=lambda x: -x[1])])

    # 5. top 20 underlying stocks
    eff = defaultdict(float)
    via = defaultdict(list)
    for r in rows:
        if r["isin"] and r["asset_class"] in ("domestic_equity", "overseas_equity", "reit_invit"):
            e = share[r["fund"]] * r["w"]
            eff[r["isin"]] += e
            via[r["isin"]].append(f"{label[r['fund']]} {r['w']:.2f}%")
    top = sorted(eff.items(), key=lambda x: -x[1])[:20]
    write("exposure_top20_stocks.csv", ["rank", "stock", "isin", "share_of_portfolio_pct", "rupees", "held_through"],
          [[n + 1, names[i], i, round(v, 2), round(v * total / 100), "; ".join(via[i])] for n, (i, v) in enumerate(top)])

    # 6. weighted expense ratio, using the latest AMFI daily figure in October 2026
    ter = {}
    for r in csv.DictReader(open(DATA / "raw" / "amfi_ter_10-2026.csv")):
        if r["Scheme_Name"] not in ter or r["TER_Date"] > ter[r["Scheme_Name"]]["TER_Date"]:
            ter[r["Scheme_Name"]] = r
    out, wt, wb = [], 0.0, 0.0
    for f, _, v, _ in HOLDINGS:
        t = ter[f]
        wt += share[f] * float(t["D_TER"])
        wb += share[f] * float(t["D_BER"])
        out.append([f, t["TER_Date"][:10], t["D_BER"], t["D_TER"], round(100 * share[f], 2),
                    round(v * float(t["D_TER"]) / 100, 2)])
    out.append(["PORTFOLIO (value weighted)", "", round(wb, 3), round(wt, 3), 100.0, round(total * wt / 100, 2)])
    write("weighted_expense_ratio.csv", ["fund", "amfi_ter_date", "direct_base_expense_ratio_pct",
                                         "direct_total_expense_ratio_pct", "share_of_portfolio_pct",
                                         "annual_cost_rs_at_current_value"], out)
    for n in ("portfolio_holdings_values", "overlap_matrix", "exposure_market_cap", "fund_market_cap_mix",
              "scenario_allocation", "exposure_sector",
              "exposure_top20_stocks", "weighted_expense_ratio"):
        print(f"== {n}")
        print(open(DATA / f"{n}.csv").read())


if __name__ == "__main__":
    main()

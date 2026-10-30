"""Build one stock-level holdings table for all nine funds as of 30 September 2026.

Sources (every row records which one it came from):
  PPFAS       full monthly portfolio Excel (has ISINs)
  HDFC        September 2026 factsheet, full portfolio table
  Axis        September 2026 factsheet, every holding >= 0.50% (rest shown as one "other" line)
  ICICI       September 2026 passive factsheet, every holding >= 1% (rest shown as one line)
  Index proxy for funds whose own September portfolio could not be downloaded (JioBlackRock
              Nifty Next 50 uses the ICICI Nifty Next 50 holdings because both replicate the same
              index, JioBlackRock Nifty Smallcap 250 and Motilal Oswal Nifty 500 use the NSE
              Indices factsheet top 10 constituents). These rows are labelled basis=index_proxy.
  JioBlackRock Flexi Cap is an active fund with no holdings source, so it is one "undisclosed"
  row and stays out of the stock-level overlap.

Writes data/holdings_2026-09.csv and data/name_matches.csv (the name to ISIN matches, for audit).
"""
import csv
import difflib
import pathlib
import re
import sys

import openpyxl

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from pdf_holdings import read_block, read_sectioned  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"

SRC = {
    "ppfas": ("https://amc.ppfas.com/downloads/portfolio-disclosure/2026/"
              "PPFCF_PPFAS_Monthly_Portfolio_Report_September_30_2026.xlsx", "2026-09-30"),
    "hdfc": ("https://files.hdfcfund.com/s3fs-public/2026-10/HDFC%20MF%20Factsheet%20-%20September%202026.pdf"
             " (page 13)", "2026-09-30"),
    "axis": ("https://www.axismf.com/1/5/1423/1484/1487/2872/4655/Axis_Fund_Factsheet_September_2026_ab18df095e.pdf"
             " (page 11)", "2026-09-30"),
    "icici": ("https://www.icicipruamc.com/blob/downloads/Files/Historic%20Factsheets/2026-2027/"
              "Passive%20Fund%20Factsheet%20September%202026.pdf", "2026-09-30"),
    "nse500": ("https://www.niftyindices.com/Factsheet/ind_nifty_500.pdf", "2026-09-30"),
    "nse250": ("https://www.niftyindices.com/Factsheet/ind_nifty_smallcap_250.pdf", "2026-09-30"),
}

# AMFI industry (as printed by the fund houses) -> NSE Indices sector, so active and index
# funds can be added up on one sector scale.
SECTOR = {
    "banks": "Financial Services", "finance": "Financial Services", "insurance": "Financial Services",
    "capital markets": "Financial Services", "financial technology (fintech)": "Financial Services",
    "it - software": "Information Technology", "it - services": "Information Technology",
    "it - hardware": "Information Technology",
    "pharmaceuticals & biotechnology": "Healthcare", "healthcare services": "Healthcare",
    "automobiles": "Automobile and Auto Components", "auto components": "Automobile and Auto Components",
    "agricultural, commercial & construction vehicles": "Capital Goods",
    "aerospace & defense": "Capital Goods", "electrical equipment": "Capital Goods",
    "industrial products": "Capital Goods", "industrial manufacturing": "Capital Goods",
    "petroleum products": "Oil, Gas & Consumable Fuels", "gas": "Oil, Gas & Consumable Fuels",
    "oil": "Oil, Gas & Consumable Fuels", "consumable fuels": "Oil, Gas & Consumable Fuels",
    "diversified fmcg": "Fast Moving Consumer Goods", "personal products": "Fast Moving Consumer Goods",
    "food products": "Fast Moving Consumer Goods", "beverages": "Fast Moving Consumer Goods",
    "agricultural food & other products": "Fast Moving Consumer Goods",
    "household products": "Fast Moving Consumer Goods", "cigarettes & tobacco products": "Fast Moving Consumer Goods",
    "ferrous metals": "Metals & Mining", "non - ferrous metals": "Metals & Mining",
    "diversified metals": "Metals & Mining", "minerals & mining": "Metals & Mining",
    "power": "Power", "telecom - services": "Telecommunication", "telecom -services": "Telecommunication",
    "telecom - equipment & accessories": "Telecommunication",
    "retailing": "Consumer Services", "leisure services": "Consumer Services",
    "transport services": "Services", "commercial services & supplies": "Services",
    "transport infrastructure": "Services",
    "consumer durables": "Consumer Durables", "construction": "Construction",
    "cement & cement products": "Construction Materials",
    "chemicals & petrochemicals": "Chemicals", "fertilizers & agrochemicals": "Chemicals",
    "realty": "Realty", "textiles & apparels": "Textiles", "media": "Media, Entertainment & Publication",
    "entertainment": "Media, Entertainment & Publication", "diversified": "Diversified",
}

# Names that the automatic matcher cannot resolve on its own (checked by hand against AMFI's list).
ALIASES = {
    "tml commercial vehicles": "Tata Motors Limited",  # demerged commercial vehicle company, ISIN INE1TAE01010
    "ltimindtree": "LTM LIMITED",  # AMFI lists LTIMindtree (ISIN INE214T01019) under its new name
    "aster dm quality care": "Aster DM Healthcare Limited",  # ISIN INE914M01019 in AMFI's list
    "vardhman textiles": "Vardhman Textiles Limted",  # spelling as printed in AMFI's list
    "bharat petroleum": "Bharat Petroleum Corpn. Ltd.",
    "berger paints (i)": "Berger Paints India Ltd",
}


def norm(name):
    s = name.lower().replace("&", " and ").replace("’", "'")
    s = re.sub(r"\b(ltd|limited|the|co|company|corp|corporation|inc|plc)\b\.?", " ", s)
    s = re.sub(r"[^a-z0-9() ]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def load_amfi():
    rows = list(csv.DictReader(open(ROOT / "data" / "amfi_marketcap_jun2026.csv")))
    by_isin = {r["isin"]: r for r in rows}
    by_norm = {}
    for r in rows:  # keep the highest ranked company for each normalised name
        by_norm.setdefault(norm(r["company"]), r)
    return by_isin, by_norm


def match(name, by_norm, log):
    n = norm(name)
    for key in (n, norm(ALIASES[n]) if n in ALIASES else None):
        if key and key in by_norm:
            log.append([name, by_norm[key]["company"], by_norm[key]["isin"], "exact"])
            return by_norm[key]
    cand = difflib.get_close_matches(n, by_norm.keys(), n=1, cutoff=0.86)
    if cand:
        r = by_norm[cand[0]]
        log.append([name, r["company"], r["isin"], "fuzzy"])
        return r
    log.append([name, "", "", "unmatched"])
    return None


def row(fund, name, isin, pct, asset, industry, source, basis):
    return {"fund": fund, "holding": name, "isin": isin, "weight_pct": round(pct, 4), "asset_class": asset,
            "industry_as_disclosed": industry, "source_url": SRC[source][0], "as_of": SRC[source][1],
            "basis": basis}


PPFAS_NET_ASSETS_LAKH = 14507049.75  # "GRAND TOTAL" row of the same Excel file


def ppfas():
    wb = openpyxl.load_workbook(RAW / "ppfas" / "PPFCF_portfolio_2026-09-30.xlsx", data_only=True)
    out, section = [], None
    for r in wb.active.iter_rows(values_only=True):
        v = [c for c in r if c is not None]
        if not v:
            continue
        head = str(v[0])
        if head.startswith("Equity & Equity related Foreign"):
            section = "overseas_equity"
        elif head.startswith("Equity & Equity related"):
            section = "domestic_equity"
        elif head == "Arbitrage":
            section = "arbitrage"
        elif head.startswith("(b) Reits"):
            section = "reit_invit"
        elif head.startswith("Money Market") or head == "Others":
            section = "debt_cash"
        elif head.startswith("Derivatives"):
            break
        # fixed SEBI layout: code, name, ISIN, industry/rating, quantity, value (Rs lakh), % to net assets, YTM
        isin = r[2] if isinstance(r[2], str) and re.match(r"^(IN|US)[0-9A-Z]{10}$", r[2]) else None
        if isin and section:
            # holdings below 0.01% print as "$0.00%", so use market value / net assets for those
            pct = 100 * (r[6] if isinstance(r[6], (int, float)) else r[5] / PPFAS_NET_ASSETS_LAKH)
            out.append(row("Parag Parikh Flexi Cap Fund", r[1], isin, pct, section, r[3] or "", "ppfas", "disclosed"))
    eq = sum(r["weight_pct"] for r in out)
    # cash, TREPS, net receivables: remainder so the fund adds to 100
    out.append(row("Parag Parikh Flexi Cap Fund", "TREPS, cash and net receivables", "", 100 - eq, "debt_cash", "",
                   "ppfas", "disclosed"))
    return out


def hdfc():
    f = RAW / "hdfc" / "HDFC_MF_Factsheet_-_September_2026.pdf"
    rows = read_block(f, 13, (205, 292), (350, 380), (150, 712), ind_x=(292, 350)) + \
        read_block(f, 13, (380, 463), (520, 560), (140, 516), ind_x=(463, 520))
    out = [row("HDFC Mid Cap Fund", n, "", p, "domestic_equity", i, "hdfc", "disclosed") for n, i, p in rows]
    out.append(row("HDFC Mid Cap Fund", "Cash, cash equivalents and net current assets", "", 8.29, "debt_cash", "",
                   "hdfc", "disclosed"))
    return out


def axis():
    f = RAW / "axis" / "Axis_Fund_Factsheet_September_2026.pdf"
    rows = read_block(f, 11, (335, 445), (500, 530), (115, 700), ind_x=(445, 500), nearest=True)
    out, asset = [], "domestic_equity"
    skip = {"Domestic Equities", "International Exchange Traded Funds", "International Equities", "Grand Total"}
    for n, i, p in rows:
        if n.startswith("International Exchange"):
            asset = "overseas_etf"
        elif n.startswith("International Equities"):
            asset = "overseas_equity"
        if n in skip:
            continue
        if n.startswith("Other Domestic Equity"):
            out.append(row("Axis Large & Mid Cap Fund", "Undisclosed domestic equity (each < 0.50%)", "", p,
                           "domestic_equity_undisclosed", "", "axis", "disclosed"))
        elif n.startswith("Other International Equity"):
            out.append(row("Axis Large & Mid Cap Fund", "Undisclosed overseas equity (each < 0.50%)", "", p,
                           "overseas_equity", "", "axis", "disclosed"))
        elif n.startswith("Debt, Cash"):
            out.append(row("Axis Large & Mid Cap Fund", n, "", p, "debt_cash", "", "axis", "disclosed"))
        else:
            out.append(row("Axis Large & Mid Cap Fund", n, "", p, asset, i, "axis", "disclosed"))
    return out


def icici():
    f = RAW / "icici" / "Passive_Fund_Factsheet_September_2026.pdf"
    h, _, cur = read_sectioned(f, 52, [(30, 205), (205, 380)], (395, 790), "MSXZRX")
    h2, _, _ = read_sectioned(f, 53, [(30, 205)], (60, 400), "MSXZRX", current=cur)
    nn50 = [(re.sub(r"^.*% to NAV\s*", "", n), i, p) for n, i, p in h + h2]
    it, _, _ = read_sectioned(f, 72, [(30, 205)], (395, 790), "MSXZRX")
    out = []
    for fund, rows, other, cash in (("ICICI Prudential Nifty Next 50 Index Fund", nn50, 3.08, 0.04),
                                    ("ICICI Prudential Nifty IT Index Fund", it, 0.0, 0.12)):
        out += [row(fund, n, "", p, "domestic_equity", i, "icici", "disclosed") for n, i, p in rows]
        if other:
            out.append(row(fund, "Undisclosed domestic equity (each < 1%)", "", other, "domestic_equity_undisclosed",
                           "", "icici", "disclosed"))
        out.append(row(fund, "Short term debt and net current assets", "", cash, "debt_cash", "", "icici", "disclosed"))
    # JioBlackRock Nifty Next 50 Index Fund: same index, so ICICI's replica is used as the proxy
    for r in [r for r in out if r["fund"] == "ICICI Prudential Nifty Next 50 Index Fund"]:
        p = dict(r, fund="JioBlackRock Nifty Next 50 Index Fund", basis="index_proxy")
        out.append(p)
    return out


def nse_top10(fund, pdf, key, total_equity=100.0):
    import subprocess
    txt = subprocess.run(["pdftotext", "-f", "1", "-l", "1", "-layout", str(RAW / "nse" / pdf), "-"],
                         capture_output=True, text=True).stdout
    part = txt[txt.find("Top constituents by weightage"):]
    rows = re.findall(r"\s{3,}([A-Z][A-Za-z0-9&'’.,() -]+?(?:Ltd\.|Limited|India))\s{3,}(\d+\.\d{2})\s*$", part, re.M)
    out = [row(fund, n.strip(), "", float(p), "domestic_equity", "", key, "index_proxy") for n, p in rows[:10]]
    rest = total_equity - sum(float(p) for _, p in rows[:10])
    out.append(row(fund, "Rest of index (outside top 10, weights not published)", "", rest,
                   "domestic_equity_undisclosed", "", key, "index_proxy"))
    return out


def main():
    by_isin, by_norm = load_amfi()
    rows = ppfas() + hdfc() + axis() + icici() + \
        nse_top10("JioBlackRock Nifty Smallcap 250 Index Fund", "ind_nifty_smallcap_250.pdf", "nse250") + \
        nse_top10("Motilal Oswal Nifty 500 Index Fund", "ind_nifty_500.pdf", "nse500")
    rows.append({"fund": "JioBlackRock Flexi Cap Fund", "holding": "Portfolio not obtained (see report)", "isin": "",
                 "weight_pct": 100.0, "asset_class": "undisclosed", "industry_as_disclosed": "",
                 "source_url": "", "as_of": "", "basis": "missing"})
    log = []
    for r in rows:
        r["company_amfi"], r["mcap_category"], r["amfi_rank"] = "", "", ""
        if r["asset_class"] in ("domestic_equity", "arbitrage"):
            a = by_isin.get(r["isin"]) if r["isin"] else match(r["holding"], by_norm, log)
            if a:
                r["isin"] = r["isin"] or a["isin"]
                r["company_amfi"], r["mcap_category"], r["amfi_rank"] = a["company"], a["category"], a["rank"]
            elif r["isin"]:
                r["mcap_category"] = "Small Cap"  # not in AMFI's top 250, so small cap by SEBI's definition
        ind = r["industry_as_disclosed"].lower().replace("it -software", "it - software").strip()
        if r["asset_class"].startswith("overseas"):
            r["sector"] = "Overseas equity"
        elif r["asset_class"] == "reit_invit":
            r["sector"] = "REITs and InvITs"
        elif r["asset_class"] == "debt_cash":
            r["sector"] = "Debt and cash"
        else:
            r["sector"] = SECTOR.get(ind, "")
    keys = ["fund", "holding", "company_amfi", "isin", "weight_pct", "asset_class", "industry_as_disclosed", "sector",
            "mcap_category", "amfi_rank", "basis", "as_of", "source_url"]
    with (ROOT / "data" / "holdings_2026-09.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=keys, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    with (ROOT / "data" / "name_matches.csv").open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["name_in_factsheet", "amfi_company", "isin", "match_type"])
        w.writerows(log)
    totals = {}
    for r in rows:
        totals[r["fund"]] = totals.get(r["fund"], 0) + r["weight_pct"]
    for f, t in totals.items():
        print(f"{f:45s} rows={sum(r['fund'] == f for r in rows):4d} total={t:7.2f}")
    print("unmatched:", [l[0] for l in log if l[3] == "unmatched"])
    print("fuzzy:", [(l[0], l[1]) for l in log if l[3] == "fuzzy"])
    print("no sector:", sorted({(r["fund"][:12], r["industry_as_disclosed"]) for r in rows
                                if not r["sector"] and r["asset_class"] == "domestic_equity" and r["basis"] == "disclosed"}))


if __name__ == "__main__":
    main()

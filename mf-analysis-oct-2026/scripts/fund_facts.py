"""Write data/fund_facts.csv: one row per (fund, metric) with the value, date and source URL,
plus a second source where one was found, and a status:
  two_sources_agree | two_sources_differ | single_source | calculated | missing

Values are copied from the documents in data/raw (factsheet pages are noted in the URL column) or
from the CSV files produced by the other scripts. Nothing here is estimated.
"""
import csv
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent

PPFAS = "https://amc.ppfas.com/downloads/factsheet/2026/ppfas-mf-factsheet-for-September-2026.pdf (p2-5)"
PPFAS_X = "https://amc.ppfas.com/downloads/portfolio-disclosure/2026/PPFCF_PPFAS_Monthly_Portfolio_Report_September_30_2026.xlsx"
ICICI = "https://www.icicipruamc.com/blob/downloads/Files/Historic%20Factsheets/2026-2027/Passive%20Fund%20Factsheet%20September%202026.pdf"
ICICI_NN = ICICI + " (p52-53)"
ICICI_IT = ICICI + " (p72)"
HDFC = "https://files.hdfcfund.com/s3fs-public/2026-10/HDFC%20MF%20Factsheet%20-%20September%202026.pdf"
AXIS = "https://www.axismf.com/1/5/1423/1484/1487/2872/4655/Axis_Fund_Factsheet_September_2026_ab18df095e.pdf"
TER = "https://www.amfiindia.com/ter-of-mf-schemes (data/raw/amfi_ter_*.csv)"
TE = "https://www.amfiindia.com/otherdata/tracking-error (data/raw/amfi_tracking_error_30-sep-2026.csv)"
NAVF = "https://portal.amfiindia.com/spages/NAVAll.txt"
COIN = "https://coin.zerodha.com/mf/fund/"
CALC = "calculated: scripts/performance.py (AMFI NAV via api.mfapi.in, NSE Indices TRI)"
HOLD = "calculated: scripts/build_holdings.py + portfolio_analysis.py"
SEP, OCT = "2026-09-30", "2026-10-29"

F = {
    "PPFAS": "Parag Parikh Flexi Cap Fund", "ICNN": "ICICI Prudential Nifty Next 50 Index Fund",
    "HDFC": "HDFC Mid Cap Fund", "AXIS": "Axis Large & Mid Cap Fund", "ICIT": "ICICI Prudential Nifty IT Index Fund",
    "JSC": "JioBlackRock Nifty Smallcap 250 Index Fund", "JFX": "JioBlackRock Flexi Cap Fund",
    "JNN": "JioBlackRock Nifty Next 50 Index Fund", "MO": "Motilal Oswal Nifty 500 Index Fund",
}
ISIN = {"PPFAS": "INF879O01027", "ICNN": "INF109K01Y80", "HDFC": "INF179K01XQ0", "AXIS": "INF846K01J46",
        "ICIT": "INF109KC13E2", "JSC": "INF22M001051", "JFX": "INF22M001093", "JNN": "INF22M001085", "MO": "INF247L01957"}

# fund, metric, value, as_of, source, second value, second as_of, second source, status
ROWS = [
    # ---------- Parag Parikh Flexi Cap
    ("PPFAS", "category", "Equity Scheme - Flexi Cap Fund", SEP, PPFAS, "Equity Scheme - Flexi Cap Fund", OCT, NAVF, "two_sources_agree"),
    ("PPFAS", "benchmark", "NIFTY 500 TRI", SEP, PPFAS, "Nifty 500 TRI (AMFI Tier I)", SEP, PPFAS_X, "single_source"),
    ("PPFAS", "inception date", "24 May 2013", SEP, PPFAS, "13 May 2013 (launch date)", OCT, COIN + ISIN["PPFAS"], "two_sources_differ"),
    ("PPFAS", "lead fund manager and tenure", "Rajeev Thakkar, since inception (May 2013), about 13.4 years", SEP, PPFAS, "Rajeev Thakkar", OCT, COIN + ISIN["PPFAS"], "two_sources_agree"),
    ("PPFAS", "direct base expense ratio %", "0.53", SEP, PPFAS, "0.53", OCT, TER, "two_sources_agree"),
    ("PPFAS", "direct total expense ratio % (incl. brokerage, levies)", "0.69", OCT, TER, "0.69 (30 Sep)", SEP, TER, "single_source"),
    ("PPFAS", "AUM Rs crore", "1,45,070.50", SEP, PPFAS, "145070", OCT, COIN + ISIN["PPFAS"], "two_sources_agree"),
    ("PPFAS", "3y rolling return, direct, average %", "19.07 (Nifty 500 TRI 14.86)", SEP, PPFAS + " p5", "19.09 (14.87)", SEP, CALC, "two_sources_agree"),
    ("PPFAS", "3y rolling return, direct, minimum %", "0.74 (Nifty 500 TRI -6.31)", SEP, PPFAS + " p5", "0.74 (-6.31)", SEP, CALC, "two_sources_agree"),
    ("PPFAS", "5y rolling return, direct, average %", "19.12 (Nifty 500 TRI 14.54)", SEP, PPFAS + " p5", "19.13 (14.54)", SEP, CALC, "two_sources_agree"),
    ("PPFAS", "5y rolling return, direct, minimum %", "4.09 (Nifty 500 TRI -1.05)", SEP, PPFAS + " p5", "4.09 (-1.06)", SEP, CALC, "two_sources_agree"),
    ("PPFAS", "share of rolling windows beating benchmark %", "3y: 95.1, 5y: 100.0", SEP, CALC, "", "", "", "calculated"),
    ("PPFAS", "downside capture % (monthly)", "3y: 44.7, 5y: 57.3", SEP, CALC, "", "", "", "calculated"),
    ("PPFAS", "portfolio turnover", "17.09% excluding arbitrage, 42.73% including", SEP, PPFAS, "17.09 / 42.73", SEP, PPFAS_X, "two_sources_agree"),
    ("PPFAS", "top 10 holdings combined %", "51.01", SEP, HOLD, "", "", "", "calculated"),
    ("PPFAS", "market cap split % (domestic)", "Large 64.27, Mid 8.29, Small 5.77 (fund counts REITs inside mid/small)", SEP, PPFAS + " p4",
     "Large 64.27, Mid 3.62, Small 4.17, REIT/InvIT 6.27", SEP, HOLD + " with AMFI June 2026 list", "two_sources_agree"),
    ("PPFAS", "overseas equity %", "11.90", SEP, PPFAS, "11.90", SEP, PPFAS_X, "two_sources_agree"),
    ("PPFAS", "REIT and InvIT %", "6.27", SEP, PPFAS, "6.27", SEP, PPFAS_X, "two_sources_agree"),
    ("PPFAS", "arbitrage (hedged) %", "1.44", SEP, PPFAS, "1.44", SEP, PPFAS_X, "two_sources_agree"),
    ("PPFAS", "debt, money market and cash %", "8.33", SEP, PPFAS, "8.32", SEP, PPFAS_X, "two_sources_agree"),
    ("PPFAS", "exit load", "10% of units free; 2% if redeemed within 365 days; 1% from 366 to 730 days; nil after 730 days", SEP, PPFAS, "", "", "", "single_source"),
    ("PPFAS", "minimum lump sum / SIP Rs", "1,000 / 1,000 monthly", SEP, PPFAS, "1,000 (Coin minimum)", OCT, COIN + ISIN["PPFAS"], "two_sources_agree"),
    # ---------- ICICI Nifty Next 50
    ("ICNN", "category", "Index Fund (Other Scheme - Index Funds)", SEP, ICICI_NN, "Other Scheme - Index Funds", OCT, NAVF, "two_sources_agree"),
    ("ICNN", "benchmark", "Nifty Next 50 TRI", SEP, ICICI_NN, "Nifty Next 50 TRI", SEP, TE, "two_sources_agree"),
    ("ICNN", "inception date", "25 June 2010", SEP, ICICI_NN, "", "", "", "single_source"),
    ("ICNN", "lead fund manager and tenure", "Nishit Patel, since January 2021, about 5.7 years", SEP, ICICI_NN, "Nishit Patel", OCT, COIN + ISIN["ICNN"], "two_sources_agree"),
    ("ICNN", "direct base expense ratio %", "0.26", SEP, ICICI_NN, "0.26", OCT, TER, "two_sources_agree"),
    ("ICNN", "direct total expense ratio %", "0.41", OCT, TER, "0.37 (30 Sep)", SEP, TER, "two_sources_differ"),
    ("ICNN", "AUM Rs crore", "9,743.95 (month end)", SEP, ICICI_NN, "9744", OCT, COIN + ISIN["ICNN"], "two_sources_agree"),
    ("ICNN", "tracking error % 1y / 3y", "0.14 / 0.17", SEP, ICICI_NN, "AMFI 1y 0.14; calculated 0.14 / 0.17", SEP, TE, "two_sources_agree"),
    ("ICNN", "tracking difference % 1y / 3y (direct)", "-0.50 / -0.62", SEP, ICICI_NN, "-0.50 / -0.62", SEP, CALC, "two_sources_agree"),
    ("ICNN", "portfolio turnover", "0.30 times", SEP, ICICI_NN, "", "", "", "single_source"),
    ("ICNN", "top 10 holdings combined %", "33.69", SEP, HOLD, "", "", "", "calculated"),
    ("ICNN", "market cap split %", "Large 92.85, Mid 4.01, not classified 3.08 (holdings under 1% not listed)", SEP, HOLD + " with AMFI June 2026 list", "", "", "", "calculated"),
    ("ICNN", "cash, debt, overseas, REIT %", "short term debt and net current assets 0.04; overseas 0; REIT 0", SEP, ICICI_NN, "", "", "", "single_source"),
    ("ICNN", "exit load", "Nil", SEP, ICICI_NN, "", "", "", "single_source"),
    ("ICNN", "minimum lump sum / SIP Rs", "100 and thereafter / SIP minimum not stated in factsheet", SEP, ICICI_NN, "100 (Coin minimum)", OCT, COIN + ISIN["ICNN"], "two_sources_agree"),
    # ---------- HDFC Mid Cap
    ("HDFC", "category", "Equity Scheme - Mid Cap Fund", SEP, HDFC + " (p13)", "Equity Scheme - Mid Cap Fund", OCT, NAVF, "two_sources_agree"),
    ("HDFC", "benchmark", "NIFTY Midcap 150 TRI", SEP, HDFC + " (p13)", "", "", "", "single_source"),
    ("HDFC", "inception date", "25 June 2007", SEP, HDFC + " (p13)", "", "", "", "single_source"),
    ("HDFC", "lead fund manager and tenure", "Chirag Setalvad, since 25 June 2007, about 19.3 years", SEP, HDFC + " (p13)", "Chirag Setalvad", OCT, COIN + ISIN["HDFC"], "two_sources_agree"),
    ("HDFC", "direct expense ratio %", "0.71 (base ratio including statutory levies on it, as defined by HDFC)", SEP, HDFC + " (p13)",
     "AMFI base 0.61, total 0.76 on 30 Sep; base 0.60, total 0.74 on 30 Oct", SEP, TER, "two_sources_differ"),
    ("HDFC", "AUM Rs crore", "1,01,856.06", SEP, HDFC + " (p13)", "101856", OCT, COIN + ISIN["HDFC"], "two_sources_agree"),
    ("HDFC", "3y rolling return, direct, average %", "21.15 (Midcap 150 TRI 20.09)", SEP, CALC, "", "", "", "calculated"),
    ("HDFC", "3y rolling return, direct, minimum %", "-8.36 (Midcap 150 TRI -8.30)", SEP, CALC, "", "", "", "calculated"),
    ("HDFC", "5y rolling return, direct, average %", "19.56 (Midcap 150 TRI 19.01)", SEP, CALC, "", "", "", "calculated"),
    ("HDFC", "share of rolling windows beating benchmark %", "3y: 56.1, 5y: 64.4", SEP, CALC, "", "", "", "calculated"),
    ("HDFC", "downside capture % (monthly)", "3y: 80.0, 5y: 77.2", SEP, CALC, "", "", "", "calculated"),
    ("HDFC", "1y / 3y / 5y benchmark return %", "4.57 / 13.67 / 14.75", SEP, HDFC + " (p14)", "4.57 / 13.68 / 14.75", SEP, CALC, "two_sources_agree"),
    ("HDFC", "portfolio turnover", "2.87% (equity), 2.87% (total)", SEP, HDFC + " (p13)", "", "", "", "single_source"),
    ("HDFC", "top 10 holdings combined %", "31.29", SEP, HOLD, "", "", "", "calculated"),
    ("HDFC", "market cap split %", "Large 10.40, Mid 64.14, Small 17.20", SEP, HDFC + " (p106)", "Large 10.40, Mid 64.10, Small 17.21", SEP, HOLD, "two_sources_agree"),
    ("HDFC", "cash, debt, overseas, REIT %", "cash, cash equivalents and net current assets 8.29; no overseas, REIT or debt holdings listed", SEP, HDFC + " (p13)", "", "", "", "single_source"),
    ("HDFC", "exit load", "1% if redeemed within 1 year; nil after 1 year", SEP, HDFC + " (p13)", "1 (Coin field)", OCT, COIN + ISIN["HDFC"], "two_sources_agree"),
    ("HDFC", "minimum lump sum / SIP Rs", "100 and any amount thereafter (purchase and additional purchase)", SEP, HDFC + " (p104)", "100 (Coin minimum)", OCT, COIN + ISIN["HDFC"], "two_sources_agree"),
    # ---------- Axis Large & Mid Cap
    ("AXIS", "category", "Equity Scheme - Large & Mid Cap Fund (formerly Axis Growth Opportunities Fund)", SEP, AXIS + " (p11)", "Equity Schemes - Large & Mid Cap Fund", OCT, NAVF, "two_sources_agree"),
    ("AXIS", "benchmark", "NIFTY Large Midcap 250 TRI", SEP, AXIS + " (p11)", "", "", "", "single_source"),
    ("AXIS", "inception date", "22 October 2018", SEP, AXIS + " (p11)", "1 October 2018 (launch date)", OCT, COIN + ISIN["AXIS"], "two_sources_differ"),
    ("AXIS", "lead fund manager and tenure", "Shreyash Devalkar, since 4 August 2023, about 3.2 years (co-manager Mayank Hyanki since 3 July 2026)", SEP, AXIS + " (p11)", "Shreyash Devalkar", OCT, COIN + ISIN["AXIS"], "two_sources_agree"),
    ("AXIS", "direct base / total expense ratio %", "0.54 / 0.83", SEP, AXIS + " (p139)", "0.54 / 0.83 (30 Sep); 0.55 / 0.83 (29 Oct)", SEP, TER, "two_sources_agree"),
    ("AXIS", "AUM Rs crore", "16,438.32 (month end)", SEP, AXIS + " (p11)", "16438", OCT, COIN + ISIN["AXIS"], "two_sources_agree"),
    ("AXIS", "1y / 3y / 5y direct return %", "5.10 / 14.30 / 11.54", SEP, AXIS + " (p11)", "5.10 / 14.31 / 11.54", SEP, CALC, "two_sources_agree"),
    ("AXIS", "3y rolling return, direct, average %", "21.35 (Large Midcap 250 TRI 20.78)", SEP, CALC, "", "", "", "calculated"),
    ("AXIS", "5y rolling return, direct, average %", "21.48 (Large Midcap 250 TRI 20.91)", SEP, CALC, "", "", "", "calculated"),
    ("AXIS", "share of rolling windows beating benchmark %", "3y: 42.9, 5y: 64.0", SEP, CALC, "", "", "", "calculated"),
    ("AXIS", "downside capture % (monthly)", "3y: 85.5, 5y: 94.5", SEP, CALC, "", "", "", "calculated"),
    ("AXIS", "portfolio turnover", "0.61 times (1 year)", SEP, AXIS + " (p11)", "", "", "", "single_source"),
    ("AXIS", "top 10 holdings combined %", "26.12", SEP, HOLD, "", "", "", "calculated"),
    ("AXIS", "market cap split %", "Large 51.25, Mid 35.64, Small 8.49, cash and others 4.62", SEP, AXIS + " (p11)",
     "Large 44.45, Mid 31.95, Small 7.55 on listed holdings; 6.24 domestic not listed", SEP, HOLD, "two_sources_differ"),
    ("AXIS", "overseas %", "international equities 5.22 + international ETFs 1.47 = 6.69", SEP, AXIS + " (p11)", "", "", "", "single_source"),
    ("AXIS", "debt, cash and other current assets %", "3.11", SEP, AXIS + " (p11)", "", "", "", "single_source"),
    ("AXIS", "exit load", "Nil", SEP, AXIS + " (p11)", "blank on Coin", OCT, COIN + ISIN["AXIS"], "single_source"),
    ("AXIS", "minimum lump sum Rs", "100", OCT, COIN + ISIN["AXIS"], "", "", "", "single_source"),
    # ---------- ICICI Nifty IT
    ("ICIT", "category", "Index Fund (sector index)", SEP, ICICI_IT, "Other Scheme - Index Funds", OCT, NAVF, "two_sources_agree"),
    ("ICIT", "benchmark", "Nifty IT TRI", SEP, ICICI_IT, "Nifty IT TRI", SEP, TE, "two_sources_agree"),
    ("ICIT", "inception date", "18 August 2022", SEP, ICICI_IT, "28 July 2022 (launch date)", OCT, COIN + ISIN["ICIT"], "two_sources_differ"),
    ("ICIT", "lead fund manager and tenure", "Nishit Patel, since August 2022, about 4.2 years", SEP, ICICI_IT, "Nishit Patel", OCT, COIN + ISIN["ICIT"], "two_sources_agree"),
    ("ICIT", "direct base expense ratio %", "0.22", SEP, ICICI_IT, "0.22 (total 0.40)", OCT, TER, "two_sources_agree"),
    ("ICIT", "AUM Rs crore", "422.63 (month end)", SEP, ICICI_IT, "423", OCT, COIN + ISIN["ICIT"], "two_sources_agree"),
    ("ICIT", "tracking error % 1y / 3y", "0.11 / 0.12", SEP, ICICI_IT, "AMFI 0.10; calculated 0.10 / 0.11", SEP, TE, "two_sources_differ"),
    ("ICIT", "tracking difference % 1y / 3y (direct)", "-0.23 / -0.38", SEP, ICICI_IT, "-0.23 / -0.38", SEP, CALC, "two_sources_agree"),
    ("ICIT", "portfolio turnover", "0.51 times", SEP, ICICI_IT, "", "", "", "single_source"),
    ("ICIT", "top 10 holdings combined %", "99.87 (index has 10 stocks; Infosys alone 31.26)", SEP, ICICI_IT, "", "", "", "single_source"),
    ("ICIT", "exit load", "Nil", SEP, ICICI_IT, "", "", "", "single_source"),
    ("ICIT", "minimum lump sum Rs", "1,000 (plus multiples of Re 1)", SEP, ICICI_IT, "1000", OCT, COIN + ISIN["ICIT"], "two_sources_agree"),
    # ---------- JioBlackRock Nifty Smallcap 250
    ("JSC", "category", "Index Funds - Equity Funds", OCT, NAVF, "", "", "", "single_source"),
    ("JSC", "benchmark", "Nifty Smallcap 250 TRI", SEP, TE, "", "", "", "single_source"),
    ("JSC", "inception date", "5 August 2025 (launch date)", OCT, COIN + ISIN["JSC"], "first NAV in AMFI history 22 August 2025", OCT, NAVF, "two_sources_differ"),
    ("JSC", "fund manager", "Tanvi Kacheria (tenure not verified)", OCT, COIN + ISIN["JSC"], "", "", "", "single_source"),
    ("JSC", "direct base / total expense ratio %", "0.19 / 0.34 (30 Sep); 0.19 / 0.41 (30 Oct)", SEP, TER, "base 0.19", OCT, COIN + ISIN["JSC"], "two_sources_agree"),
    ("JSC", "AUM Rs crore", "393", OCT, COIN + ISIN["JSC"], "", "", "", "single_source"),
    ("JSC", "tracking error % 1y", "0.13", SEP, TE, "0.13", SEP, CALC, "two_sources_agree"),
    ("JSC", "tracking difference % 1y", "-0.43", SEP, CALC, "", "", "", "calculated"),
    ("JSC", "top 10 holdings combined % (index)", "12.73", SEP, "https://www.niftyindices.com/Factsheet/ind_nifty_smallcap_250.pdf", "", "", "", "single_source"),
    ("JSC", "exit load", "not verified from a primary source", "", "", "", "", "", "missing"),
    ("JSC", "minimum lump sum Rs", "500", OCT, COIN + ISIN["JSC"], "", "", "", "single_source"),
    # ---------- JioBlackRock Flexi Cap
    ("JFX", "category", "Equity Schemes - Flexi Cap Fund", OCT, NAVF, "", "", "", "single_source"),
    ("JFX", "benchmark", "not verified", "", "", "", "", "", "missing"),
    ("JFX", "inception date", "23 September 2025 (launch date)", OCT, COIN + ISIN["JFX"], "first NAV in AMFI history 17 October 2025", OCT, NAVF, "two_sources_differ"),
    ("JFX", "fund manager", "Tanvi Kacheria (tenure not verified)", OCT, COIN + ISIN["JFX"], "", "", "", "single_source"),
    ("JFX", "direct base / total expense ratio %", "0.50 / 1.10 (30 Sep); 0.50 / 1.11 (30 Oct)", SEP, TER, "base 0.50", OCT, COIN + ISIN["JFX"], "two_sources_agree"),
    ("JFX", "AUM Rs crore", "3,175", OCT, COIN + ISIN["JFX"], "", "", "", "single_source"),
    ("JFX", "return since first NAV (17 Oct 2025 to 30 Sep 2026) %", "-4.82 (Nifty 500 TRI over same dates -5.63, shown for reference only)", SEP, CALC, "", "", "", "calculated"),
    ("JFX", "rolling 3y and 5y returns, holdings, sectors, cap split, turnover, exit load", "not available", "", "", "", "", "", "missing"),
    ("JFX", "minimum lump sum Rs", "500", OCT, COIN + ISIN["JFX"], "", "", "", "single_source"),
    # ---------- JioBlackRock Nifty Next 50
    ("JNN", "category", "Index Funds - Equity Funds", OCT, NAVF, "", "", "", "single_source"),
    ("JNN", "benchmark", "Nifty Next 50 TRI", SEP, TE, "", "", "", "single_source"),
    ("JNN", "inception date", "5 August 2025 (launch date)", OCT, COIN + ISIN["JNN"], "first NAV in AMFI history 22 August 2025", OCT, NAVF, "two_sources_differ"),
    ("JNN", "direct base / total expense ratio %", "0.19 / 0.37 (30 Sep); 0.19 / 0.41 (30 Oct)", SEP, TER, "base 0.19", OCT, COIN + ISIN["JNN"], "two_sources_agree"),
    ("JNN", "AUM Rs crore", "220", OCT, COIN + ISIN["JNN"], "", "", "", "single_source"),
    ("JNN", "tracking error % 1y", "0.16", SEP, TE, "0.17", SEP, CALC, "two_sources_differ"),
    ("JNN", "tracking difference % 1y", "-0.22", SEP, CALC, "", "", "", "calculated"),
    ("JNN", "holdings", "own portfolio not obtained; ICICI Nifty Next 50 holdings used as an index proxy", SEP, ICICI_NN, "", "", "", "missing"),
    ("JNN", "minimum lump sum Rs", "500", OCT, COIN + ISIN["JNN"], "", "", "", "single_source"),
    # ---------- Motilal Oswal Nifty 500
    ("MO", "category", "Other Scheme - Index Funds", OCT, NAVF, "", "", "", "single_source"),
    ("MO", "benchmark", "NIFTY 500 Total Return Index", SEP, TE, "", "", "", "single_source"),
    ("MO", "inception date", "19 August 2019 (launch date)", OCT, COIN + ISIN["MO"], "first NAV in AMFI history 11 September 2019", OCT, NAVF, "two_sources_differ"),
    ("MO", "fund manager", "Swapnil P Mayekar (tenure not verified)", OCT, COIN + ISIN["MO"], "", "", "", "single_source"),
    ("MO", "direct base / total expense ratio %", "0.13 / 0.23", SEP, TER, "base 0.13", OCT, COIN + ISIN["MO"], "two_sources_agree"),
    ("MO", "AUM Rs crore", "3,086", OCT, COIN + ISIN["MO"], "", "", "", "single_source"),
    ("MO", "tracking error % 1y", "0.04 (0.05 a year earlier)", SEP, TE, "0.04 (3y 0.09)", SEP, CALC, "two_sources_agree"),
    ("MO", "tracking difference % 1y / 3y", "-0.09 / -0.27", SEP, CALC, "", "", "", "calculated"),
    ("MO", "top 10 holdings combined % (index)", "28.50", SEP, "https://www.niftyindices.com/Factsheet/ind_nifty_500.pdf", "", "", "", "single_source"),
    ("MO", "market cap split", "not available from a primary source", "", "", "", "", "", "missing"),
    ("MO", "exit load", "Coin shows 1; third-party sites say 1% within 15 days; not verified from SID or KIM", OCT, COIN + ISIN["MO"], "", "", "", "single_source"),
    ("MO", "minimum lump sum Rs", "500", OCT, COIN + ISIN["MO"], "", "", "", "single_source"),
]


def main():
    with (ROOT / "data" / "fund_facts.csv").open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["fund", "metric", "value", "as_of", "source", "second_value", "second_as_of", "second_source", "status"])
        for k, *rest in ROWS:
            w.writerow([F[k]] + rest)
    from collections import Counter
    print(len(ROWS), Counter(r[-1] for r in ROWS))


if __name__ == "__main__":
    main()

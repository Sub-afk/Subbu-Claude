"""Parse AMFI's half-yearly market capitalisation list (six months ended 30 June 2026,
https://portal.amfiindia.com/spages/AverageMarketCapitalization30Jun2026.pdf) into
data/amfi_marketcap_jun2026.csv. Rank 1-100 = Large Cap, 101-250 = Mid Cap, 251+ = Small Cap
(SEBI circular dated 6 October 2017)."""
import csv
import pathlib
import re
import subprocess

ROOT = pathlib.Path(__file__).resolve().parent.parent
PDF = ROOT / "data" / "raw" / "amfi" / "AverageMarketCapitalization30Jun2026.pdf"
LINE = re.compile(r"^\s*(\d+)\s+(.+?)\s*(IN[EF][0-9A-Z]{9})\s*(.*?)\s+(Large Cap|Mid Cap|Small Cap)\s*$")


def main():
    txt = subprocess.run(["pdftotext", "-layout", str(PDF), "-"], capture_output=True, text=True).stdout
    rows = []
    for line in txt.splitlines():
        m = LINE.match(line)
        if not m:
            continue
        rank, name, isin, rest, cat = m.groups()
        nums = re.findall(r"\d[\d,]*\.\d+", rest)
        syms = [t for t in rest.split() if not re.match(r"^[\d,.-]+$", t)]
        rows.append([int(rank), name.strip(), isin, syms[1] if len(syms) > 1 else (syms[0] if syms else ""),
                     nums[-1].replace(",", "") if nums else "", cat])
    with (ROOT / "data" / "amfi_marketcap_jun2026.csv").open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["rank", "company", "isin", "nse_symbol", "avg_mcap_cr_all_exchanges", "category"])
        w.writerows(rows)
    print(len(rows), "rows; categories:", {c: sum(r[5] == c for r in rows) for c in ("Large Cap", "Mid Cap", "Small Cap")})
    print(rows[98:102])


if __name__ == "__main__":
    main()

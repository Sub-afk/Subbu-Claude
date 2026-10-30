"""Save the server-rendered fund summary from Zerodha Coin (coin.zerodha.com/mf/fund/<ISIN>)
for each fund. Coin is where the investor transacts, so its minimum amounts matter.
Writes data/raw/coin_pages.csv."""
import csv
import html
import pathlib
import re
import urllib.request

OUT = pathlib.Path(__file__).resolve().parent.parent / "data" / "raw"
ISINS = {
    "INF879O01027": "Parag Parikh Flexi Cap Fund",
    "INF109K01Y80": "ICICI Prudential Nifty Next 50 Index Fund",
    "INF179K01XQ0": "HDFC Mid Cap Fund",
    "INF846K01J46": "Axis Large & Mid Cap Fund",
    "INF109KC13E2": "ICICI Prudential Nifty IT Index Fund",
    "INF22M001051": "JioBlackRock Nifty Smallcap 250 Index Fund",
    "INF22M001093": "JioBlackRock Flexi Cap Fund",
    "INF22M001085": "JioBlackRock Nifty Next 50 Index Fund",
    "INF247L01957": "Motilal Oswal Nifty 500 Index Fund",
}
FIELDS = ["NAV", "AUM", "Expense Ratio", "Fund Manager", "Launch Date", "Min Investment",
          "Min Additional Investment", "Exit Load"]


def text(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    s = urllib.request.urlopen(req, timeout=60).read().decode("utf-8", "ignore")
    s = re.sub(r"<script.*?</script>|<style.*?</style>", "", s, flags=re.S)
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s)))


def main():
    with (OUT / "coin_pages.csv").open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["isin", "fund"] + FIELDS + ["source_url", "raw_text"])
        for isin, name in ISINS.items():
            url = f"https://coin.zerodha.com/mf/fund/{isin}"
            t = text(url)
            vals = []
            for i, f in enumerate(FIELDS):
                nxt = "|".join(re.escape(x) for x in FIELDS[i + 1:] + ["Dividend Type", "Settlement Type", "Category"])
                m = re.search(re.escape(f) + r":? (.*?) (?=" + nxt + r"|$)", t)
                vals.append(m.group(1).strip() if m else "")
            w.writerow([isin, name] + vals + [url, t[t.find(name.split()[0]):][:600]])
            print(isin, name, dict(zip(FIELDS, vals)))


if __name__ == "__main__":
    main()

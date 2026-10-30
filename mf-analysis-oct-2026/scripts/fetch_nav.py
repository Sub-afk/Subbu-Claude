"""Download full daily NAV history for each fund (Direct Plan, Growth) from api.mfapi.in,
which republishes Association of Mutual Funds in India (AMFI) NAV data, and the latest
NAV from AMFI's own NAVAll.txt file for a cross-check. Writes data/raw/nav_<code>.csv."""
import json
import pathlib
import urllib.request

OUT = pathlib.Path(__file__).resolve().parent.parent / "data" / "raw"
FUNDS = {
    122639: "Parag Parikh Flexi Cap Fund",
    120684: "ICICI Prudential Nifty Next 50 Index Fund",
    118989: "HDFC Mid Cap Fund",
    145110: "Axis Large & Mid Cap Fund",
    150468: "ICICI Prudential Nifty IT Index Fund",
    153790: "JioBlackRock Nifty Smallcap 250 Index Fund",
    153859: "JioBlackRock Flexi Cap Fund",
    153789: "JioBlackRock Nifty Next 50 Index Fund",
    147625: "Motilal Oswal Nifty 500 Index Fund",
}


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=90) as r:
        return r.read()


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    amfi = get("https://portal.amfiindia.com/spages/NAVAll.txt").decode("utf-8", "ignore")
    (OUT / "amfi_NAVAll.txt").write_text(amfi)
    amfi_latest = {}
    for line in amfi.splitlines():
        p = line.split(";")
        if len(p) >= 8 and p[0].strip().isdigit() and int(p[0]) in FUNDS:
            amfi_latest[int(p[0])] = (p[1], p[6], p[7])
    with (OUT / "nav_latest_crosscheck.csv").open("w") as fh:
        fh.write("scheme_code,fund,isin,amfi_nav,amfi_date,mfapi_nav_same_date\n")
        for code, name in FUNDS.items():
            d = json.loads(get(f"https://api.mfapi.in/mf/{code}"))
            with (OUT / f"nav_{code}.csv").open("w") as f:
                f.write("date,nav\n")
                for r in reversed(d["data"]):
                    dd, mm, yy = r["date"].split("-")
                    f.write(f"{yy}-{mm}-{dd},{r['nav']}\n")
            isin, nav, date = amfi_latest[code]
            dd = __import__("datetime").datetime.strptime(date, "%d-%b-%Y").strftime("%d-%m-%Y")
            m = next((r["nav"] for r in d["data"] if r["date"] == dd), "not in mfapi yet")
            fh.write(f"{code},{name},{isin},{nav},{date},{m}\n")
            print(code, name, isin, nav, date, m)


if __name__ == "__main__":
    main()

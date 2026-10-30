"""Download daily Total Return Index (TRI) values from NSE Indices (niftyindices.com).

Source endpoint: https://www.niftyindices.com/BackPage/getTotalReturnIndexString
(the same call the public page https://www.niftyindices.com/reports/historical-data makes).
Writes data/raw/tri_<index>.csv with columns date,tri.
"""
import datetime as dt
import json
import pathlib
import time
import urllib.request

OUT = pathlib.Path(__file__).resolve().parent.parent / "data" / "raw"
URL = "https://www.niftyindices.com/BackPage/getTotalReturnIndexString"
INDICES = ["NIFTY 500", "NIFTY NEXT 50", "NIFTY MIDCAP 150", "NIFTY LARGEMIDCAP 250",
           "NIFTY IT", "NIFTY SMALLCAP 250", "NIFTY 50"]


def fetch(name, start, end):
    cinfo = "{'name':'%s','startDate':'%s','endDate':'%s','indexName':'%s'}" % (
        name, start.strftime("%d-%b-%Y"), end.strftime("%d-%b-%Y"), name)
    req = urllib.request.Request(URL, data=json.dumps({"cinfo": cinfo}).encode(), headers={
        "Content-Type": "application/json; charset=utf-8", "User-Agent": "Mozilla/5.0",
        "Referer": "https://www.niftyindices.com/reports/historical-data"})
    with urllib.request.urlopen(req, timeout=90) as r:
        body = json.loads(r.read())
    if isinstance(body, dict) and "d" in body:
        body = json.loads(body["d"])
    return body


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    today = dt.date(2026, 10, 30)
    for name in INDICES:
        rows = {}
        y = 2012
        while y <= today.year:
            s, e = dt.date(y, 1, 1), min(dt.date(y, 12, 31), today)
            for rec in fetch(name, s, e):
                d = dt.datetime.strptime(rec["Date"], "%d %b %Y").date()
                rows[d] = float(rec["TotalReturnsIndex"].replace(",", ""))
            y += 1
            time.sleep(0.5)
        f = OUT / ("tri_" + name.lower().replace(" ", "_") + ".csv")
        with f.open("w") as fh:
            fh.write("date,tri\n")
            for d in sorted(rows):
                fh.write(f"{d.isoformat()},{rows[d]}\n")
        print(name, len(rows), min(rows), max(rows))


if __name__ == "__main__":
    main()

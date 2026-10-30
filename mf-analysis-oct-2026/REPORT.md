# Mutual fund portfolio review and allocation decision

Prepared 30 October 2026. Fund data is as of 30 September 2026 unless a row says otherwise. Your holding values are the October 2026 figures you supplied.

A note on names. Three fund house names began as abbreviations: Housing Development Finance Corporation (HDFC), Industrial Credit and Investment Corporation of India (ICICI), and Parag Parikh Financial Advisory Services (PPFAS), the Parag Parikh fund house. Today these are simply brand names.

This is analysis, not a promise about the future. Past returns do not tell you what will happen next. Every number below comes from a named source or from a script in this folder. Anything that could not be verified is listed in Section 5.

---

## 1. One page summary

### What to do with the ₹10,000 lump sum

| Fund | Amount | Why, in one line |
|---|---|---|
| Motilal Oswal Nifty 500 Index Fund | ₹4,000 | Cheapest fund you own and the most accurate index tracker. Covers about 500 Indian companies of all sizes. |
| HDFC Mid Cap Fund | ₹2,500 | Your only mid size company fund. Long record, and it has fallen less than its benchmark in down months. |
| Parag Parikh Flexi Cap Fund | ₹2,000 | Strongest long record of all your funds. A smaller addition brings it back under 40% of the portfolio. |
| JioBlackRock Nifty Smallcap 250 Index Fund | ₹1,500 | Your only small company fund, for long term growth. |

### What to do with the ₹10,000 monthly Systematic Investment Plan (SIP)

Use the same split every month. Motilal Oswal Nifty 500 gets ₹4,000, HDFC Mid Cap ₹2,500, Parag Parikh Flexi Cap ₹2,000 and JioBlackRock Nifty Smallcap 250 ₹1,500.

For HDFC Mid Cap, keep the ₹500 SIP that is already running and add a new ₹2,000 SIP, so HDFC receives ₹2,500 a month in total. This assumes your ₹10,000 includes the existing ₹500. If you meant ₹10,000 on top of it, HDFC's total becomes ₹3,000 and its long run share rises from 25% to about 29%. That is also acceptable, but the first reading keeps the plan simpler.

### Which funds to pause (no new money, nothing sold)

| Fund | Main reason |
|---|---|
| ICICI Prudential Nifty Next 50 Index Fund | Same index as the JioBlackRock Nifty Next 50 fund, and already 22% of the portfolio. |
| JioBlackRock Nifty Next 50 Index Fund | Duplicate of the ICICI fund above. |
| ICICI Prudential Nifty IT Index Fund | Single sector fund. Your Information Technology (IT) exposure is already about twice the market's weight. |
| Axis Large & Mid Cap Fund | Its job is already done by Motilal Oswal Nifty 500 plus HDFC Mid Cap, and it beat its benchmark in only 43% of 3 year periods. |
| JioBlackRock Flexi Cap Fund | Highest cost of your nine funds (1.11% a year), under 13 months of history, and its holdings could not be checked. Parag Parikh already does the same job. |

### Did the earlier recommendation survive testing?

Yes. The earlier split of ₹4,000, ₹2,500, ₹2,000 and ₹1,500 passed every decision rule against the verified data, so the amounts are unchanged. The checks are in Section 4.

Nothing should be sold. No fund met the "strong case" bar, so no capital gains tax or exit load arises.

### What changes over time (contributions only, no market growth assumed)

| Point in time | Portfolio | Parag Parikh share | Both Nifty Next 50 funds | Nifty IT fund |
|---|---|---|---|---|
| Today | ₹67,331 | 40.77% | 23.64% | 5.72% |
| After the lump sum | ₹77,331 | 38.08% | 20.59% | 4.98% |
| After 12 months of SIP | ₹1,97,331 | 27.09% | 8.07% | 1.95% |
| After 36 months of SIP | ₹4,37,331 | 23.20% | 3.64% | 0.88% |

Source: [data/scenario_allocation.csv](data/scenario_allocation.csv), produced by [scripts/portfolio_analysis.py](scripts/portfolio_analysis.py). Market movements will change these numbers. The table only shows where the money you add takes the portfolio.

---

## 2. Verified metrics for each fund

### How to read these tables

Some terms used throughout:

- **Net Asset Value (NAV)** is the price of one unit of the fund.
- **Total Return Index (TRI)** is a market index that includes dividends, which is the fair yardstick for a fund.
- **Expense ratio** is the yearly fee taken from the fund. Fund houses now report a **Base Expense Ratio (BER)**, which is the management and running fee. They also report a **Total Expense Ratio (TER)**, which adds brokerage, transaction costs and taxes on them. The Association of Mutual Funds in India (AMFI) publishes both every day. The total is what you actually pay.
- **Assets Under Management (AUM)** is the total money in the fund.
- **Tracking error** measures how much an index fund's daily returns wobble around its index. **Tracking difference** is the yearly gap between the fund's return and the index return. Smaller is better for both.
- **Rolling returns** take every possible 3 year (or 5 year) window, day by day, rather than one start date. They show how consistent a fund has been.
- **Downside capture** compares the fund with its benchmark in months when the benchmark fell. A downside capture of 80 means the fund fell about 80% as much.

The "Check" column uses these labels:

- **Two sources agree** means two independent sources matched.
- **Differ** means two sources gave different values. Both are shown.
- **One source** means only one source was found.
- **Calculated** means I computed it with the scripts from Association of Mutual Funds in India NAV data and National Stock Exchange (NSE) Indices TRI data.
- **Missing** means it could not be verified.

Every row, with full source addresses, is in [data/fund_facts.csv](data/fund_facts.csv).

The main sources used:

- **Parag Parikh:** [factsheet, September 2026](https://amc.ppfas.com/downloads/factsheet/2026/ppfas-mf-factsheet-for-September-2026.pdf) and [monthly portfolio file, 30 September 2026](https://amc.ppfas.com/downloads/portfolio-disclosure/2026/PPFCF_PPFAS_Monthly_Portfolio_Report_September_30_2026.xlsx).
- **ICICI:** [passive fund factsheet, September 2026](https://www.icicipruamc.com/blob/downloads/Files/Historic%20Factsheets/2026-2027/Passive%20Fund%20Factsheet%20September%202026.pdf).
- **HDFC:** [factsheet, September 2026](https://files.hdfcfund.com/s3fs-public/2026-10/HDFC%20MF%20Factsheet%20-%20September%202026.pdf).
- **Axis:** [factsheet, September 2026](https://www.axismf.com/1/5/1423/1484/1487/2872/4655/Axis_Fund_Factsheet_September_2026_ab18df095e.pdf).
- **AMFI:** [daily expense ratios](https://www.amfiindia.com/ter-of-mf-schemes), [tracking error](https://www.amfiindia.com/otherdata/tracking-error) and the [NAV file](https://portal.amfiindia.com/spages/NAVAll.txt).
- **NSE Indices:** [historical TRI data](https://www.niftyindices.com/reports/historical-data), the [methodology document, September 2026](https://www.niftyindices.com/Methodology/Method_NIFTY_Equity_Indices.pdf), and the factsheets for [Nifty 500](https://www.niftyindices.com/Factsheet/ind_nifty_500.pdf), [Nifty Smallcap 250](https://www.niftyindices.com/Factsheet/ind_nifty_smallcap_250.pdf), [Nifty Next 50](https://www.niftyindices.com/Factsheet/ind_next50.pdf) and [Nifty IT](https://www.niftyindices.com/Factsheet/ind_nifty_it.pdf).
- **Zerodha Coin:** each fund's page at `coin.zerodha.com/mf/fund/<code>`, where the code is the fund's International Securities Identification Number (ISIN), the unique code for each fund plan.

### 2.1 Parag Parikh Flexi Cap Fund (active, 40.77% of your portfolio)

| Metric | Value | Source and date | Check |
|---|---|---|---|
| Category and benchmark | Flexi Cap, NIFTY 500 TRI | Fund house factsheet, 30 September 2026. Category also in the AMFI NAV file. | Two sources agree |
| Inception | 24 May 2013 (Coin shows 13 May 2013 as launch) | Factsheet, Coin 29 October 2026 | Differ |
| Lead manager | Rajeev Thakkar, since inception, about 13.4 years | Factsheet, Coin | Two sources agree |
| Expense ratio, Direct plan | Base 0.53%, total 0.69% | Factsheet and AMFI, 29 October 2026 | Two sources agree |
| AUM | ₹1,45,070.50 crore | Factsheet, Coin | Two sources agree |
| 3 year rolling return, average | 19.07% vs 14.86% for the benchmark. Worst window 0.74% vs −6.31%. | Factsheet page 5. My calculation: 19.09% vs 14.87%. | Two sources agree |
| 5 year rolling return, average | 19.12% vs 14.54%. Worst window 4.09% vs −1.05%. | Factsheet page 5, my calculation | Two sources agree |
| Windows that beat the benchmark | 95.1% of 3 year windows, 100% of 5 year windows | Calculated | Calculated |
| Downside capture | 44.7 over 3 years, 57.3 over 5 years | Calculated | Calculated |
| Last 1, 3, 5 years (Direct) | −3.54%, 12.22%, 11.15% vs benchmark −2.03%, 9.51%, 9.04% | Factsheet shows −3.54, 12.21, 11.15 | Two sources agree |
| Portfolio turnover | 17.09% excluding arbitrage, 42.73% including | Factsheet and portfolio file | Two sources agree |
| Top 10 holdings | 51.01% of the fund | Calculated from the portfolio file | Calculated |
| Sectors | Financial services 26.24%, IT 9.39%, oil, gas and fuels 7.50% (domestic shares only) | Calculated, using NSE sector names | Calculated |
| Size split (Indian shares) | Large 64.27%, mid 8.29%, small 5.77%. The fund counts its property and infrastructure trusts inside mid and small. My split is large 64.27%, mid 3.62%, small 4.17%, trusts 6.27%. | Factsheet page 4, my script using the AMFI size list | Two sources agree (large cap matches exactly) |
| Overseas shares | 11.90% (Alphabet, Meta, Microsoft, Amazon) | Factsheet, portfolio file | Two sources agree |
| Real Estate Investment Trusts (REITs) and Infrastructure Investment Trusts (InvITs) | 6.27% | Factsheet, portfolio file | Two sources agree |
| Debt and cash | 8.33%, plus 1.44% hedged arbitrage that behaves like cash | Factsheet, portfolio file | Two sources agree |
| Exit load | 10% of units can leave free. Otherwise 2% within 365 days, 1% from 366 to 730 days, nil after 730 days. | Factsheet | One source |
| Minimum on Coin | Lump sum ₹1,000, monthly SIP ₹1,000 | Factsheet, Coin | Two sources agree |

### 2.2 ICICI Prudential Nifty Next 50 Index Fund (index, 22.16%)

| Metric | Value | Source and date | Check |
|---|---|---|---|
| Category and benchmark | Index fund, Nifty Next 50 TRI | ICICI factsheet pages 52 and 53, AMFI tracking error list | Two sources agree |
| Inception | 25 June 2010 | Factsheet | One source |
| Lead manager | Nishit Patel, since January 2021, about 5.7 years | Factsheet, Coin | Two sources agree |
| Expense ratio, Direct | Base 0.26%. Total 0.37% on 30 September, 0.41% on 29 October. | Factsheet, AMFI | Base agrees, total changed |
| AUM | ₹9,743.95 crore | Factsheet, Coin | Two sources agree |
| Tracking error | 0.14% over 1 year, 0.17% over 3 years | Factsheet. AMFI shows 0.14%. My calculation: 0.14% and 0.17%. | Two sources agree |
| Tracking difference, Direct | −0.50% over 1 year, −0.62% over 3 years | Factsheet. My calculation is identical. | Two sources agree |
| Portfolio turnover | 0.30 times | Factsheet | One source |
| Top 10 holdings | 33.69% | Calculated from factsheet | Calculated |
| Sectors | Capital goods 19.6%, financial services 16.2%, autos 9.8% | Calculated | Calculated |
| Size split | Large 92.85%, mid 4.01%, 3.08% unclassified (holdings under 1% are not listed) | Calculated | Calculated |
| Cash, debt, overseas, REIT | Debt and cash 0.04%, nothing else | Factsheet | One source |
| Exit load, minimum | Nil, ₹100 | Factsheet, Coin | Two sources agree |

### 2.3 HDFC Mid Cap Fund (active, 13.47%)

| Metric | Value | Source and date | Check |
|---|---|---|---|
| Category and benchmark | Mid Cap, NIFTY Midcap 150 TRI | HDFC factsheet page 13, AMFI NAV file | Two sources agree on category |
| Inception, manager | 25 June 2007. Chirag Setalvad since 25 June 2007, about 19.3 years. | Factsheet, Coin | Two sources agree |
| Expense ratio, Direct | HDFC prints 0.71%, which is the base plus the tax on it. AMFI shows base 0.61% and total 0.76% on 30 September, base 0.60% and total 0.74% on 30 October. | Factsheet, AMFI | Differ (different definitions, see 4.6) |
| AUM | ₹1,01,856.06 crore | Factsheet, Coin | Two sources agree |
| 3 year rolling return, average | 21.15% vs 20.09% for the benchmark. Worst window −8.36% vs −8.30%. | Calculated | Calculated |
| 5 year rolling return, average | 19.56% vs 19.01% | Calculated | Calculated |
| Windows that beat the benchmark | 56.1% of 3 year windows, 64.4% of 5 year windows | Calculated | Calculated |
| Downside capture | 80.0 over 3 years, 77.2 over 5 years | Calculated | Calculated |
| Benchmark return, 1, 3, 5 years | 4.57%, 13.67%, 14.75% | Factsheet page 14. My calculation: 4.57, 13.68, 14.75. | Two sources agree |
| Portfolio turnover | 2.87% | Factsheet | One source |
| Top 10 holdings | 31.29% | Calculated | Calculated |
| Sectors | Financial services 25.8%, healthcare 15.4%, autos 9.5% | Calculated | Calculated |
| Size split | Large 10.40%, mid 64.14%, small 17.20% | Factsheet page 106. My script: 10.40, 64.10, 17.21. | Two sources agree |
| Cash and other | Cash and net current assets 8.29%. No overseas, REIT or debt holdings. | Factsheet | One source |
| Exit load, minimum | 1% within 1 year, nil after. Minimum ₹100. | Factsheet pages 13 and 104, Coin | Two sources agree |

### 2.4 Axis Large & Mid Cap Fund (active, 9.25%)

| Metric | Value | Source and date | Check |
|---|---|---|---|
| Category and benchmark | Large & Mid Cap (formerly Axis Growth Opportunities Fund), NIFTY Large Midcap 250 TRI | Axis factsheet page 11, AMFI NAV file | Two sources agree on category |
| Inception | 22 October 2018 (Coin shows 1 October 2018) | Factsheet, Coin | Differ |
| Managers | Shreyash Devalkar since 4 August 2023 (about 3.2 years). Mayank Hyanki since 3 July 2026. Krishnaa N (overseas) since 1 March 2024. Pratik Tibrewal since 26 August 2026. | Factsheet | One source |
| Expense ratio, Direct | Base 0.54%, total 0.83% | Factsheet page 139, AMFI | Two sources agree |
| AUM | ₹16,438.32 crore | Factsheet, Coin | Two sources agree |
| Last 1, 3, 5 years (Direct) | 5.10%, 14.30%, 11.54% vs benchmark −0.37%, 10.79%, 10.95% | Factsheet. My calculation: 5.10, 14.31, 11.54. | Two sources agree |
| 3 and 5 year rolling, average | 21.35% vs 20.78% (3 years), 21.48% vs 20.91% (5 years) | Calculated | Calculated |
| Windows that beat the benchmark | 42.9% of 3 year windows, 64.0% of 5 year windows | Calculated | Calculated |
| Downside capture | 85.5 over 3 years, 94.5 over 5 years | Calculated | Calculated |
| Portfolio turnover | 0.61 times | Factsheet | One source |
| Top 10 holdings | 26.12% | Calculated | Calculated |
| Sectors | Financial services 24.8%, autos 10.6%, capital goods 9.9% | Calculated | Calculated |
| Size split | Factsheet: large 51.25%, mid 35.64%, small 8.49%, cash and others 4.62%. My script, on listed holdings only: large 44.45%, mid 31.95%, small 7.55%, plus 6.24% of small holdings not listed. | Factsheet page 11, calculated | Differ (holdings under 0.50% are not listed) |
| Overseas | 6.69% (5.22% overseas shares plus 1.47% overseas Exchange Traded Funds (ETFs)) | Factsheet | One source |
| Debt and cash | 3.11% | Factsheet | One source |
| Exit load, minimum | Nil (blank on Coin), ₹100 | Factsheet, Coin | One source |

### 2.5 ICICI Prudential Nifty IT Index Fund (sector index, 5.72%)

| Metric | Value | Source and date | Check |
|---|---|---|---|
| Category and benchmark | Index fund on a single sector, Nifty IT TRI | ICICI factsheet page 72, AMFI | Two sources agree |
| Inception, manager | 18 August 2022 (Coin shows 28 July 2022). Nishit Patel since August 2022. | Factsheet, Coin | Differ on date |
| Expense ratio, Direct | Base 0.22%, total 0.40% | Factsheet, AMFI | Two sources agree |
| AUM | ₹422.63 crore | Factsheet, Coin | Two sources agree |
| Tracking error | 0.11% over 1 year, 0.12% over 3 years | Factsheet. AMFI shows 0.10%. My calculation: 0.10% and 0.11%. | Differ (small) |
| Tracking difference, Direct | −0.23% over 1 year, −0.38% over 3 years | Factsheet. My calculation is identical. | Two sources agree |
| Last 1 and 3 years (Direct) | −16.14% and −2.80% a year | Calculated | Calculated |
| Turnover, holdings | 0.51 times. The index has only 10 stocks, and Infosys alone is 31.26%. | Factsheet, NSE methodology (Nifty IT has 10 companies) | Two sources agree |
| Exit load, minimum | Nil, ₹1,000 | Factsheet, Coin | Two sources agree |

### 2.6 JioBlackRock Nifty Smallcap 250 Index Fund (index, 3.62%)

| Metric | Value | Source and date | Check |
|---|---|---|---|
| Benchmark | Nifty Smallcap 250 TRI. By rule, this index holds the companies ranked 251 to 500 by full market value. | AMFI tracking error list, NSE methodology | Two sources agree |
| Inception, manager | Launched 5 August 2025. First NAV in AMFI history is 22 August 2025. Manager Tanvi Kacheria. | Coin, AMFI | Differ on date |
| Expense ratio, Direct | Base 0.19%. Total 0.34% on 30 September, 0.41% on 30 October. | AMFI, Coin | Base agrees |
| AUM | ₹393 crore | Coin | One source |
| Tracking error, 1 year | 0.13% | AMFI. My calculation: 0.13%. | Two sources agree |
| Tracking difference, 1 year | −0.43% | Calculated | Calculated |
| Top 10 holdings (index) | 12.73% | NSE Indices factsheet | One source |
| Sectors (index) | Financial services 19.46%, capital goods 16.45%, autos 10.57%, healthcare 10.54% | NSE Indices factsheet | One source |
| Exit load | Not verified | None | Missing |
| Minimum lump sum | ₹500 | Coin | One source |

### 2.7 JioBlackRock Flexi Cap Fund (active, 2.11%)

| Metric | Value | Source and date | Check |
|---|---|---|---|
| Category | Flexi Cap | AMFI NAV file | One source |
| Inception, manager | Launched 23 September 2025. First NAV 17 October 2025. Manager Tanvi Kacheria. | Coin, AMFI | Differ on date |
| Expense ratio, Direct | Base 0.50%. Total 1.10% on 30 September, 1.11% on 30 October. The highest of your nine funds. | AMFI, Coin | Base agrees |
| AUM | ₹3,175 crore | Coin | One source |
| Return since first NAV (to 30 September 2026) | −4.82%, against −5.63% for the Nifty 500 TRI over the same dates. Shown for reference only, because the fund's own benchmark was not verified. | Calculated | Calculated |
| Benchmark, holdings, sectors, size split, turnover, exit load | Not obtained | None | Missing |
| Minimum lump sum | ₹500 | Coin | One source |

### 2.8 JioBlackRock Nifty Next 50 Index Fund (index, 1.48%)

| Metric | Value | Source and date | Check |
|---|---|---|---|
| Benchmark | Nifty Next 50 TRI | AMFI tracking error list | One source |
| Inception | Launched 5 August 2025. First NAV 22 August 2025. | Coin, AMFI | Differ |
| Expense ratio, Direct | Base 0.19%. Total 0.37% on 30 September, 0.41% on 30 October. | AMFI, Coin | Base agrees |
| AUM | ₹220 crore | Coin | One source |
| Tracking error, 1 year | 0.16% | AMFI. My calculation: 0.17%. | Differ (small) |
| Tracking difference, 1 year | −0.22% | Calculated | Calculated |
| Holdings | The fund's own portfolio was not obtained. ICICI's Nifty Next 50 holdings are used as a stand-in because both funds copy the same index. | Section 5 | Missing |
| Minimum lump sum | ₹500 | Coin | One source |

### 2.9 Motilal Oswal Nifty 500 Index Fund (index, 1.41%)

| Metric | Value | Source and date | Check |
|---|---|---|---|
| Benchmark | NIFTY 500 TRI. By rule, the 500 largest eligible companies by full market value. | AMFI tracking error list, NSE methodology | Two sources agree |
| Inception, manager | Launched 19 August 2019. First NAV 11 September 2019. Manager Swapnil P Mayekar. | Coin, AMFI | Differ on date |
| Expense ratio, Direct | Base 0.13%, total 0.23%. The lowest of your nine funds. | AMFI, Coin | Two sources agree |
| AUM | ₹3,086 crore | Coin | One source |
| Tracking error | 0.04% over 1 year (0.05% a year earlier), 0.09% over 3 years | AMFI, calculated | Two sources agree |
| Tracking difference | −0.09% over 1 year, −0.27% over 3 years | Calculated | Calculated |
| Top 10 holdings (index) | 28.50% | NSE Indices factsheet | One source |
| Sectors (index) | Financial services 30.58%, capital goods 7.50%, autos 7.42%, healthcare 7.31%, IT 6.02% | NSE Indices factsheet | One source |
| Size split | Not available from a primary source | None | Missing |
| Exit load | Coin shows "1". Third-party sites say 1% within 15 days. Not checked against the Scheme Information Document. | Coin | One source |
| Minimum lump sum | ₹500 | Coin | One source |

---

## 3. Overlap and effective exposure

All of these come from [scripts/build_holdings.py](scripts/build_holdings.py) and [scripts/portfolio_analysis.py](scripts/portfolio_analysis.py). The stock level table with every holding is [data/holdings_2026-09.csv](data/holdings_2026-09.csv).

### 3.1 Stock overlap matrix

Overlap between two funds is the sum, across shares both funds own, of the smaller of the two weights. For example, 15% means 15% of each fund is invested in the same companies at the same weights. Shares were matched by ISIN, using AMFI's June 2026 company list. The name matches are in [data/name_matches.csv](data/name_matches.csv).

| | PPFAS Flexi | ICICI NN50 | HDFC Mid | Axis L&M | ICICI IT | Jio SC250 | Jio Flexi | Jio NN50 | MO N500 |
|---|---|---|---|---|---|---|---|---|---|
| **PPFAS Flexi** | 100 | 4.86 | 1.26 | 14.08 | 9.39 | 0 | n/a | 4.86 | 20.01* |
| **ICICI NN50** | 4.86 | 100 | 7.23 | 10.69 | 3.30 | 0 | n/a | **96.86**† | 0* |
| **HDFC Mid** | 1.26 | 7.23 | 100 | 15.08 | 6.37 | 4.25* | n/a | 7.23 | 0* |
| **Axis L&M** | 14.08 | 10.69 | 15.08 | 100 | 2.81 | 3.81* | n/a | 10.69 | 18.17* |
| **ICICI IT** | 9.39 | 3.30 | 6.37 | 2.81 | 100 | 0 | n/a | 3.30 | 1.83* |
| **Jio SC250** | 0 | 0 | 4.25* | 3.81* | 0 | 100 | n/a | 0 | 0* |
| **Jio Flexi** | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| **Jio NN50** | 4.86 | **96.86**† | 7.23 | 10.69 | 3.30 | 0 | n/a | 100 | 0* |
| **MO N500** | 20.01* | 0* | 0* | 18.17* | 1.83* | 0* | n/a | 0* | 100 |

Key to the labels and symbols:

- **Fund labels:** PPFAS Flexi is Parag Parikh Flexi Cap. NN50 is Nifty Next 50. L&M is Large & Mid Cap. SC250 is Nifty Smallcap 250. MO N500 is Motilal Oswal Nifty 500.
- **\*** Only the top 10 stocks of the Nifty 500 and Nifty Smallcap 250 indices are published. These figures are therefore minimums and the true overlap is higher. For example, the Nifty 500 contains every Nifty Next 50 stock by definition, so the real ICICI NN50 and MO N500 overlap is well above 0.
- **†** JioBlackRock Nifty Next 50 uses ICICI's holdings as a stand-in. Both copy the same index, so near total overlap is a fact about the funds' design, not a measured number.
- **n/a** means the JioBlackRock Flexi Cap portfolio could not be obtained.

The full list of shared stocks for each pair is in [data/overlap_common_stocks.csv](data/overlap_common_stocks.csv).

### 3.2 Your effective exposure by company size

This is your whole mutual fund portfolio, looking through each fund to the shares inside it. Sizes follow the Securities and Exchange Board of India (SEBI) rule as applied in AMFI's list for January to June 2026: companies ranked 1 to 100 are large, 101 to 250 are mid, and the rest are small.

| Bucket | Share of portfolio | Rupees |
|---|---|---|
| Large companies | 58.72% | ₹39,535 |
| Mid size companies | 15.14% | ₹10,194 |
| Small companies | 8.28% | ₹5,575 |
| Indian shares, size not known (unlisted holdings and Nifty 500 outside its top 10) | 2.32% | ₹1,560 |
| Overseas shares and ETFs | 5.47% | ₹3,683 |
| REITs and InvITs | 2.56% | ₹1,721 |
| Hedged arbitrage (behaves like cash) | 0.59% | ₹398 |
| Debt and cash inside funds | 4.81% | ₹3,241 |
| JioBlackRock Flexi Cap (portfolio not obtained) | 2.11% | ₹1,420 |

Each fund's own size mix is in [data/fund_market_cap_mix.csv](data/fund_market_cap_mix.csv).

### 3.3 Your effective exposure by sector

Sectors use NSE Indices' names. Fund house industry labels were mapped to them in [scripts/build_holdings.py](scripts/build_holdings.py). For comparison, the right hand column shows the Nifty 500 index, which stands for the whole Indian market.

| Sector | Your portfolio | Nifty 500 index |
|---|---|---|
| Financial services | 21.44% | 30.58% |
| Information technology | **11.79%** | **6.02%** |
| Automobiles and auto components | 7.70% | 7.42% |
| Healthcare | 7.22% | 7.31% |
| Capital goods | 7.06% | 7.50% |
| Fast Moving Consumer Goods (FMCG) | 5.72% | 5.26% |
| Overseas shares | 5.47% | 0 |
| Oil, gas and consumable fuels | 5.41% | 6.77% |
| Debt and cash | 4.81% | 0 |
| Power | 4.70% | 3.41% |
| REITs and InvITs | 2.56% | 0 |
| Telecommunication | 2.35% | 3.69% |
| Metals and mining | 2.12% | 4.55% |
| Not known (JioBlackRock Flexi Cap 2.11%, unlisted holdings 1.31%) | 3.42% | 0 |
| All other sectors | 8.23% | 17.50% |

The full table is in [data/exposure_sector.csv](data/exposure_sector.csv).

### 3.4 Top 20 underlying companies

| Rank | Company | Share of portfolio | Held through |
|---|---|---|---|
| 1 | HDFC Bank | 3.55% | Parag Parikh, Axis, Motilal Oswal |
| 2 | Infosys | 3.01% | Parag Parikh, ICICI IT (31.26% of that fund), Motilal Oswal |
| 3 | ICICI Bank | 2.62% | Parag Parikh, Axis, Motilal Oswal |
| 4 | Bajaj Holdings & Investment | 2.47% | Parag Parikh, both Nifty Next 50 funds |
| 5 | HCL Technologies | 2.29% | Parag Parikh, ICICI IT |
| 6 | Power Grid Corporation | 2.28% | Parag Parikh |
| 7 | ITC | 2.24% | Parag Parikh |
| 8 | Coal India | 2.20% | Parag Parikh |
| 9 | Tata Consultancy Services | 2.11% | Parag Parikh, ICICI IT |
| 10 | Kotak Mahindra Bank | 1.83% | Parag Parikh, Motilal Oswal |
| 11 | Alphabet (Google), United States | 1.75% | Parag Parikh |
| 12 | Mahindra & Mahindra | 1.72% | Parag Parikh, Axis, Motilal Oswal |
| 13 | Bharti Airtel | 1.44% | Parag Parikh, Axis, Motilal Oswal |
| 14 | DLF | 1.42% | Parag Parikh, both Nifty Next 50 funds |
| 15 | Divi's Laboratories | 1.40% | Axis, both Nifty Next 50 funds |
| 16 | Axis Bank | 1.38% | Parag Parikh, Axis, Motilal Oswal |
| 17 | Meta Platforms, United States | 1.15% | Parag Parikh |
| 18 | Maruti Suzuki | 1.03% | Parag Parikh, Axis |
| 19 | TVS Motor | 1.02% | Axis, both Nifty Next 50 funds |
| 20 | Embassy Office Parks REIT | 1.02% | Parag Parikh |

The top 20 add up to about 37.9% of the portfolio, and no single company is above 3.6%. Your direct shares and Bitcoin are not included because their details were not provided. If you hold HDFC Bank, Infosys or ICICI Bank directly, your true exposure to them is higher than shown. Source: [data/exposure_top20_stocks.csv](data/exposure_top20_stocks.csv).

### 3.5 Duplicates, concentration and cost

- **Funds tracking the same index:** ICICI Prudential Nifty Next 50 and JioBlackRock Nifty Next 50 both follow the Nifty Next 50 TRI. This is confirmed by AMFI's tracking error list and both fund records.
- **Funds doing the same job:** Parag Parikh Flexi Cap and JioBlackRock Flexi Cap are both flexi cap funds, meaning they can buy companies of any size. Axis Large & Mid Cap covers ground that Motilal Oswal Nifty 500 and HDFC Mid Cap already cover together. That second point is a judgment, explained in 4.4.
- **Funds above 40% of the portfolio:** Parag Parikh Flexi Cap, at 40.77% (₹27,450 of ₹67,331). Source: [data/portfolio_holdings_values.csv](data/portfolio_holdings_values.csv).
- **Weighted average expense ratio, value weighted, Direct plans, AMFI 29 and 30 October 2026:** 0.62% total and 0.44% base. That is about ₹417 a year at today's value. The four funds receiving new money have a weighted total of 0.48% on the recommended split. Source: [data/weighted_expense_ratio.csv](data/weighted_expense_ratio.csv).

---

## 4. Reasoning for each decision

Each point is marked **[Fact]** (verified, with source above) or **[Judgment]** (my opinion based on the facts), with a confidence level.

### 4.1 Rule 1, existing funds only

All four destinations are funds you already hold. **[Fact, high confidence]**

### 4.2 Rule 2, never add to a duplicate

- The two Nifty Next 50 funds follow the same index. **[Fact, high confidence]**
- The rule allows at most one of them to receive new money. I recommend neither. Together they are already 23.64% of the portfolio. The Nifty 500 fund you will be adding to already contains all Nifty Next 50 companies, because the Nifty 500 includes the whole Nifty 100 by NSE's own rules. **[Fact for the index rule, judgment for the choice, high confidence]**
- If you ever want to add to a Nifty Next 50 fund again, the two are very close. Both have total expense ratios of 0.41% on 29 and 30 October. JioBlackRock has the lower base fee (0.19% vs 0.26%) and a smaller 1 year tracking difference (−0.22% vs −0.50%). ICICI's fund has a record going back to 2010. **[Fact for numbers, judgment that it is close, medium confidence]**

### 4.3 Rule 3, no core money into a sector fund

- ICICI Prudential Nifty IT is a single sector fund. The index holds only 10 companies and Infosys alone is 31.26%. **[Fact, high confidence]**
- Your look-through IT exposure is 11.79%, against 6.02% in the Nifty 500. That is roughly double the market weight. **[Fact, high confidence]**
- So it is paused. Its 1 year return of −16.14% is not the reason. Past returns of a sector do not predict the next ones. **[Judgment, high confidence]**

### 4.4 Rule 4, same exposure, prefer the cheaper fund with better tracking

- **Broad Indian market (core money).** Motilal Oswal Nifty 500 has the lowest total expense ratio of all nine funds, 0.23%. It also has the smallest tracking error, 0.04% for 1 year per AMFI, and the smallest tracking difference, −0.09% for 1 year. **[Fact, high confidence]**
- **Flexi cap.** Parag Parikh costs 0.69% a year against JioBlackRock's 1.11%. It has 13 years of history against under 13 months. It beat its benchmark in 95.1% of all 3 year windows and 100% of all 5 year windows. Its downside capture was 44.7 over 3 years, so it fell less than half as much as the market in falling months. **[Fact, high confidence]** Choosing Parag Parikh over JioBlackRock Flexi Cap follows directly. **[Judgment, high confidence]**
- **Large and mid companies.** Axis Large & Mid Cap costs 0.83%. It beat its benchmark in only 42.9% of 3 year windows and 64.0% of 5 year windows. Its average excess over the benchmark was about 0.6 percentage points a year. Its downside capture of 85.5 to 94.5 means it gave limited protection in falling months. **[Fact, high confidence]** Motilal Oswal Nifty 500 plus HDFC Mid Cap provide the same large and mid exposure. HDFC also has a longer record and better downside capture (77 to 80). Axis is paused. **[Judgment, medium confidence]** Its last 1 year return (5.10% against −0.37% for its benchmark) is strong. That is a reason not to sell it, but not enough on its own to keep adding.

### 4.5 Rule 5, reduce any fund above 40% through smaller additions

- Parag Parikh is 40.77% today. **[Fact, high confidence]**
- Adding ₹2,000 of the ₹10,000 (20%) brings it to 38.08% straight away. It falls to about 27% after 12 months and about 23% after 36 months of SIPs, with no market movement assumed. **[Fact, arithmetic in data/scenario_allocation.csv, high confidence]**
- Cutting Parag Parikh to zero was rejected. It has the best verified record in the portfolio. The rule asks for smaller additions, not none. **[Judgment, medium confidence]**
- Watch point: at a steady 40% of the SIP, Motilal Oswal Nifty 500 approaches 40% of the portfolio over many years. It reaches about 34% after 36 months. An index fund of 500 companies carries less single-manager risk than an active fund at the same share, but it is worth reviewing once a year. **[Judgment, medium confidence]**

### 4.6 Rule 6, keep a growth allocation for a 30 year horizon

- Today only 15.14% of the portfolio is in mid size and 8.28% in small companies. **[Fact, high confidence]**
- HDFC Mid Cap is your only mid size fund. It holds 64.14% mid, 17.20% small and 8.29% cash. Over 3 and 5 year windows it averaged 0.55 to 1.06 percentage points a year above its benchmark, beating it in 56% to 64% of windows. In falling months it dropped about 77% to 80% as much as the benchmark. **[Fact, high confidence]**
- Two points about HDFC Mid Cap for balance. First, it is very large (₹1,01,856 crore), and size can make it harder for a mid cap fund to stay ahead. Second, its 8.29% cash slightly dilutes its mid cap exposure. Neither changes the decision, because there is no other mid cap fund in your portfolio to use instead. **[Judgment, medium confidence]**
- On expense ratios, HDFC's factsheet figure of 0.71% includes the tax on the base fee. AMFI's base is 0.60% to 0.61% and its total, which includes brokerage, is 0.74% to 0.76%. These are different definitions and they agree once that is taken into account. The 0.74% total is used for cost comparisons. **[Fact, high confidence]**
- JioBlackRock Nifty Smallcap 250 is your only small company fund. It tracks its index closely, with a tracking error of 0.13% for 1 year per AMFI, matching my calculation. Its total expense ratio rose from 0.34% at the end of September to 0.41% at the end of October. The rise came from statutory levies (0.14% to 0.20%) and brokerage (0.01% to 0.02%), while its base fee stayed at 0.19%. It is young (launched August 2025) and small (₹393 crore). Because it copies an index, its age matters less than it would for an active fund. **[Fact for numbers, judgment for the last sentence, medium confidence]**
- After 36 months of the plan, mid and small companies grow to about 16.7% and 18.1% of the portfolio from the funds whose holdings are known. More sits inside the Nifty 500 fund, whose size split could not be verified. Small companies are the most volatile part of the market. A 15% SIP share is a meaningful growth tilt without dominating. **[Fact for the arithmetic, judgment for the level, medium confidence]**

### 4.7 Rule 7, minimum amounts

- Lump sum minimums on Coin are ₹500 (Motilal Oswal), ₹100 (HDFC), ₹1,000 (Parag Parikh) and ₹500 (JioBlackRock Smallcap 250). The smallest planned amount is ₹1,500, so every amount clears its minimum. **[Fact, Coin pages 29 and 30 October 2026, high confidence]**
- SIP minimums: Parag Parikh ₹1,000 a month is from its factsheet. HDFC's ₹100 covers purchases and additional purchases. For Motilal Oswal and JioBlackRock, only third-party sites give ₹500. Every planned SIP is ₹1,500 or more, so the plan works even if those minimums are as high as ₹1,000. **[Fact for verified items, medium confidence for the rest]**

### 4.8 Testing the earlier recommendation

I tried to break the earlier split rather than confirm it. These facts could have changed it, and here is what each showed:

1. **Is Motilal Oswal Nifty 500 really the cheapest and most accurate tracker?** Yes. It has the lowest total expense ratio (0.23%) and the lowest AMFI tracking error (0.04%) of all nine funds. **No change.**
2. **Does adding ₹2,000 to Parag Parikh break the 40% rule?** No. It reduces its share from 40.77% to 38.08%. **No change.**
3. **Is HDFC Mid Cap good enough to be the only mid cap destination?** The verified record is modest outperformance with clearly better downside protection. Its own factsheet confirms 64% mid and 17% small. **No change.**
4. **Did JioBlackRock Smallcap 250's cost increase matter?** Its total rose to 0.41%, which is still lower than any active fund you hold. There is no other small cap fund in the portfolio to switch to under Rule 1. **No change.**
5. **Should one Nifty Next 50 fund still get money?** No. The portfolio already holds 23.64% in that index, and the Nifty 500 fund covers those companies. **No change.**
6. **Is there a case to sell anything?** The largest unrealised loss is ₹400 (ICICI Nifty Next 50), and the sector fund is 5.72% of the portfolio. Pausing fixes the imbalance over a few months of SIPs without creating tax, exit loads or the risk of selling at a bad time. **No sale, so no tax or exit load calculation is needed.**

Result: the earlier lump sum split is confirmed unchanged. The only addition is how the monthly SIP and the existing ₹500 HDFC SIP fit together. **[Judgment, medium to high confidence]**

---

## 5. What I could not verify

1. **ICICI and HDFC monthly portfolio Excel files.** Both websites block automated downloads. Their September 2026 factsheets were used instead. HDFC's factsheet lists the full portfolio and its totals match exactly. ICICI's lists every holding of 1% or more. The 3.08% of the Nifty Next 50 fund in smaller holdings is not itemised.
2. **Axis holdings under 0.50%.** 6.24% of Indian shares and 2.36% of overseas shares are shown in the factsheet as single "other" lines. Axis's monthly portfolio file could not be found as a direct download.
3. **All three JioBlackRock funds.** No factsheet, portfolio file or Scheme Information Document (SID) could be read, because the website loads its documents through a script. This leaves several gaps:
   - Facts come only from AMFI and Coin.
   - JioBlackRock Flexi Cap's benchmark, holdings, sectors, size split, turnover and exit load are missing.
   - JioBlackRock Nifty Next 50 holdings are a stand-in from ICICI's fund.
   - JioBlackRock Smallcap 250 holdings are a stand-in from the NSE Indices top 10.
4. **Motilal Oswal Nifty 500.** No factsheet or portfolio could be found. Holdings are a stand-in from the NSE Indices Nifty 500 top 10 and sector table. The fund's large, mid and small split is missing. A third-party source gave about 71% large, 18.5% mid and 10% small for the Nifty 500, but that is from November 2024 and was not used.
5. **Scheme Information Documents and Key Information Memorandums (KIMs).** None were retrieved. Exit loads were taken from factsheets where available. Motilal Oswal's (Coin shows "1") and JioBlackRock's are unconfirmed.
6. **SIP minimums on Coin.** Coin's public page shows only the lump sum minimum. SIP minimums for Motilal Oswal and the JioBlackRock funds come from third-party sites only.
7. **Tracking difference from AMFI.** AMFI's tracking difference service returned no data for any date tried. The second source for tracking difference is ICICI's factsheet or my own calculation.
8. **AUM and fund manager tenure for JioBlackRock and Motilal Oswal.** These come from Coin only, and manager start dates were not found.
9. **Rolling returns for HDFC and Axis, and downside capture for all active funds.** The fund houses do not publish these in the documents found, so they are my calculations only. My method reproduced Parag Parikh's published rolling returns to within 0.02 percentage points, which supports the calculation.
10. **Inception dates.** Coin's "launch date" differs from factsheet allotment dates for several funds. Both are shown.
11. **Your purchase dates.** These are not known, so exit loads and tax on any sale cannot be calculated exactly. No sale is recommended, so this does not affect the plan.
12. **Your direct shares and Bitcoin.** Their details were not provided, so they are not in the overlap or exposure tables.
13. **Timing gap.** Fund holdings are as of 30 September 2026. Your values are October 2026. Index factsheets for Nifty Next 50 and Nifty IT are dated 30 October 2026, and those for Nifty 500 and Nifty Smallcap 250 are dated 30 September 2026.

---

## Files in this folder

| File | What it holds |
|---|---|
| `REPORT.md` | This report |
| `data/fund_facts.csv` | Every per-fund metric with value, date, source and second source |
| `data/holdings_2026-09.csv` | Stock level holdings for all funds, with ISIN, size, sector and source |
| `data/overlap_matrix.csv`, `data/overlap_common_stocks.csv` | Overlap matrix and the shared stocks behind it |
| `data/exposure_market_cap.csv`, `data/exposure_sector.csv`, `data/exposure_top20_stocks.csv`, `data/fund_market_cap_mix.csv` | Effective exposure tables |
| `data/portfolio_holdings_values.csv`, `data/weighted_expense_ratio.csv`, `data/scenario_allocation.csv` | Weights, the 40% check, costs and the allocation scenarios |
| `data/performance_trailing.csv`, `data/performance_rolling_active.csv`, `data/tracking_index_funds.csv` | Return, rolling return, capture and tracking calculations |
| `data/amfi_marketcap_jun2026.csv`, `data/name_matches.csv` | AMFI size list (5,411 companies) and the name to ISIN matches |
| `data/raw/` | Downloaded source files: factsheets, portfolio file, AMFI and NSE data, NAV and index histories |
| `scripts/` | All download and calculation scripts. Run them in this order: `fetch_nav.py`, `fetch_index_tri.py`, `fetch_amfi.py`, `fetch_coin.py`, `parse_amfi_marketcap.py`, `build_holdings.py`, `performance.py`, `portfolio_analysis.py`, `fund_facts.py`. |

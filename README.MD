# Netflix Content Strategy — Large-Scale EDA & Business Insights

Exploratory analysis of 8,807 Netflix titles, translating descriptive statistics into content-strategy recommendations for a non-technical stakeholder audience.

## Tech stack
`Python` · `pandas` · `NumPy` · `matplotlib` · `seaborn`

## What's in this repo
- `netflix_eda_v2.py` — full analysis pipeline: clean → engineer features → 7 charts → findings-to-recommendations writeup
- `charts/` — 7 presentation-ready visualizations (PNG)
- `findings.md` — each finding paired with an actionable recommendation
- `netflix_titles.csv` — source data (8,807 rows × 12 columns)

## Approach
1. **Clean** — parsed dates, split multi-value country/genre fields, audited missingness (director missing in ~30% of rows, flagged rather than silently dropped)
2. **Engineer** — primary country, year added, numeric movie runtime, TV season count
3. **Analyze** — descriptive statistics + a regional genre cross-tab (US vs. India) to surface content-strategy patterns, not just summary counts
4. **Communicate** — every chart title states the finding, not just the metric; every finding in `findings.md` is paired with a recommendation

## Key findings → recommendations (see `findings.md` for full detail)
- **Movies outnumber TV shows ~2:1**, consistently across years — the catalog's core identity, worth confirming still matches viewing behavior.
- **Content additions peaked in 2019** (2,016 titles), down 26% by 2021 — pattern consistent with industry-wide COVID production slowdowns.
- **India is a clear, established #2 content source** behind the US (1,008 vs. 3,211 titles) — not an emerging market, a proven one.
- **US and India audiences are served different genre mixes** (India: International Movies, Dramas; US: Dramas, Comedies, Documentaries) — regional strategy should lean into this, not flatten it.
- **51% of movies run 90–120 minutes** — a usable acquisition/production benchmark.

## How to reproduce
```bash
pip install pandas matplotlib seaborn
python3 netflix_eda_v2.py
```

## Data source
Netflix Movies and TV Shows dataset (community-mirrored on GitHub; originally sourced from Flixable/Kaggle).
# Netflix Content Intelligence — Historical Catalog Analysis

An interactive content-portfolio intelligence tool built on a historical Netflix catalog
snapshot (8,807 titles, data through **September 2021**). It surfaces patterns in what's in
the catalog, where it comes from, and how it's changed over time — and translates those
patterns into business questions worth investigating, rather than predictions or
recommendations the data can't support.

**This is historical catalog data, not a live Netflix feed.** The dashboard is explicit about
its data vintage throughout, and does not fabricate or imply any 2022–2026 activity.

## Project objective

Answer: *"What can we learn about Netflix's content portfolio from this historical catalog
snapshot?"* — for an audience like a content strategy analyst, content acquisition team, or
business/product analyst exploring a content portfolio.

## Data limitations (read this first)

- 8,807 titles, 12 columns, covering additions through **September 2021** only.
- No viewing hours, watch time, popularity, user ratings, subscriber engagement, retention,
  revenue, acquisition cost, licensing cost, production budget, or regional demand data.
- **Catalog presence is not audience demand.** Every insight in this project describes what's
  in the catalog, not how it performed.
- `director` is missing for ~29.9% of titles; `country` and `cast` for ~9.4% each. A handful of
  rows have a duration value shifted into the `rating` field (a known quirk of this dataset).

## Analytical questions the dashboard answers

- What's the content-type mix, and how has it held over time?
- How old is content, typically, when it enters the catalog (release year vs. date added)?
- Which markets supply the most content, and how does genre mix differ between them?
- Where is the catalog most concentrated, genre-wise?
- What does the audience/maturity profile look like?
- What's the standard movie runtime, and how tightly does the catalog cluster around it?

## Derived features (data model)

Computed once in a cached loader and reused across the app, rather than recalculated inline:

| Field | Description |
|---|---|
| `year_added` | Year parsed from `date_added` |
| `primary_country` | First country listed in the (sometimes multi-country) `country` field |
| `duration_min` | Numeric movie runtime parsed from `duration` |
| `content_age_at_addition` | `year_added - release_year` — how old a title was when it entered the catalog |
| `freshness_group` | `content_age_at_addition` bucketed into New release / 1–2 / 3–5 / 6–10 / 10+ years / Unknown |
| `rating_group` | `rating` mapped to Mature / Teen / Family-Kids / Unrated-Unknown (mapping documented in-app) |
| exploded genre table | `listed_in` split on multi-genre tags into a long-format table for genre-level analysis |

## Dashboard sections

1. **Executive Overview** — headline KPIs, calculated dynamically from active filters
2. **Key Content Insights** — four findings fixed to the full catalog
3. **Portfolio Composition** — movie/TV mix, audience/maturity profile, catalog-profile stats
4. **Content Acquisition & Freshness** — titles added by year, catalog age at addition
5. **Regional Intelligence** — top content-producing countries, interactive market comparison
6. **Genre Intelligence** — genre concentration, with a multi-tag caveat
7. **Strategic Opportunities to Investigate** — evidence-based, explicitly not predictions
8. **What This Dataset Cannot Tell Us**
9. **About the Data & Methodology**

## Key insights (see `Findings.MD` for observation → interpretation → strategic question detail)

- Movies outnumber TV shows roughly 2:1 (69.6% vs. 30.4%), consistently across the catalog.
- Catalog additions peaked in 2019 (2,016 titles), down 26% by 2021 — a pattern consistent with
  industry-wide production slowdowns, not confirmed as a deliberate spending cut.
- India is an established #2 content source behind the US (1,008 vs. 3,211 titles).
- US and India are served different genre mixes (India: International Movies, Dramas; US:
  Dramas, Comedies, Documentaries).
- 51% of movies run 90–120 minutes — a usable descriptive benchmark.

## Strategic opportunities to investigate

Framed as open questions, each explicitly requiring data this dataset doesn't have (viewing
hours, subscriber behavior, engagement, retention, acquisition/licensing cost, regional demand)
before being treated as a real recommendation:

1. Whether India's catalog representation still matches regional demand and acquisition priorities.
2. Whether "International Movies," the largest genre tag, aids discovery or masks underrepresented categories.
3. The intended balance between recent releases and library/back-catalog content.
4. Whether family-oriented content is underrepresented relative to any stated household-reach goals.
5. Using the 90–120 minute runtime band as a descriptive acquisition benchmark.

## Limitations

- Descriptive/exploratory analysis only — no predictive modeling, forecasting, or recommendation
  engine, by design.
- Rating and freshness groupings are analytical interpretations, documented in-app, not official
  Netflix categories.
- Genre shares are not mutually exclusive — titles can carry multiple genre tags.
- `director` coverage gap (~30% missing) means director-level analysis isn't attempted here.

## Technology stack

`Python` · `pandas` · `Plotly` · `Streamlit`

## How to run

```bash
pip install streamlit pandas plotly
streamlit run app.py
```

`netflix_eda_v2.py` remains available as the original static (matplotlib/seaborn) analysis
pipeline that produced the initial chart set and `Findings.MD`.

## Data source

Netflix Movies and TV Shows dataset (community-mirrored on GitHub; originally sourced from
Flixable/Kaggle). Historical catalog snapshot through September 2021.
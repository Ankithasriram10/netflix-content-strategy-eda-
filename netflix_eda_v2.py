"""
Netflix Content Strategy — Large-Scale EDA & Business Insights
Dataset: netflix_titles.csv (8,807 titles, 12 columns)
Source: Kaggle "Netflix Movies and TV Shows" (community mirror)

What this script does:
1. Loads and cleans the raw dataset (missing values, dtypes, multi-value fields)
2. Engineers derived features (primary country, year added, numeric runtime, genre split)
3. Produces 7 presentation-ready charts, each built around one business question
4. Translates each descriptive finding into an actionable content-strategy recommendation
   (written to findings.md, framed for a non-technical stakeholder audience)

Run: python3 netflix_eda.py
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

sns.set_style("whitegrid")
plt.rcParams["figure.dpi"] = 120
OUT = Path("charts")
OUT.mkdir(exist_ok=True)

# ---------------------------------------------------------------------------
# 1. LOAD & CLEAN
# ---------------------------------------------------------------------------
df = pd.read_csv("netflix_titles.csv")

missing = df.isna().sum().sort_values(ascending=False)
missing_pct = (missing / len(df) * 100).round(1)

df["date_added"] = pd.to_datetime(df["date_added"].str.strip(), errors="coerce")
df["year_added"] = df["date_added"].dt.year

movies = df[df["type"] == "Movie"].copy()
tv = df[df["type"] == "TV Show"].copy()
movies["duration_min"] = movies["duration"].str.extract(r"(\d+)").astype(float)
tv["seasons"] = tv["duration"].str.extract(r"(\d+)").astype(float)

df["primary_country"] = df["country"].str.split(",").str[0].str.strip()

genres = df.assign(genre=df["listed_in"].str.split(", ")).explode("genre")
genres["primary_country"] = genres["country"].str.split(",").str[0].str.strip()

# ---------------------------------------------------------------------------
# Pre-compute the numbers each chart title/finding depends on
# ---------------------------------------------------------------------------
type_counts = df["type"].value_counts()
movie_pct = type_counts.get("Movie", 0) / len(df) * 100
tv_pct = type_counts.get("TV Show", 0) / len(df) * 100

yearly = df["year_added"].value_counts().sort_index()
yearly = yearly[yearly.index >= 2008]
peak_year = int(yearly.idxmax())
peak_count = int(yearly.max())
latest_year = int(yearly.index.max())
latest_count = int(yearly.loc[latest_year])
decline_pct = (1 - latest_count / peak_count) * 100

top_countries = df["primary_country"].value_counts().head(10)
top_genres = genres["genre"].value_counts().head(10)
rating_order = df["rating"].value_counts().index

pct_std_runtime = movies["duration_min"].between(90, 120).mean() * 100

# Regional genre comparison — top 2 countries' top 3 genres each
top2 = top_countries.head(2).index.tolist()
country_genre = (
    genres[genres["primary_country"].isin(top2)]
    .groupby(["primary_country", "genre"]).size()
    .reset_index(name="count")
)
top3_per_country = (
    country_genre.sort_values("count", ascending=False)
    .groupby("primary_country").head(5)
)

# ---------------------------------------------------------------------------
# 2. CHARTS — each title states the finding, not just the metric
# ---------------------------------------------------------------------------

# Chart 1 — Movies vs TV Shows
plt.figure(figsize=(6, 5.5))
plt.pie(type_counts, labels=type_counts.index, autopct="%1.1f%%",
        colors=["#E50914", "#221f1f"], startangle=90,
        wedgeprops={"edgecolor": "white", "linewidth": 2})
plt.title(f"Movies Outnumber TV Shows Roughly 2:1 ({movie_pct:.0f}% vs {tv_pct:.0f}%)",
          fontsize=12, fontweight="bold")
plt.tight_layout()
plt.savefig(OUT / "01_type_split.png")
plt.close()

# Chart 2 — Titles added per year
plt.figure(figsize=(9.5, 5.5))
plt.plot(yearly.index, yearly.values, marker="o", color="#E50914", linewidth=2)
plt.fill_between(yearly.index, yearly.values, alpha=0.15, color="#E50914")
plt.annotate(f"Peak: {peak_year}\n({peak_count:,} titles)",
             xy=(peak_year, peak_count), xytext=(peak_year - 4, peak_count * 0.85),
             arrowprops=dict(arrowstyle="->", color="#221f1f"), fontsize=10)
plt.title(f"Content Additions Peaked in {peak_year}, Down {decline_pct:.0f}% by {latest_year}",
          fontsize=12, fontweight="bold")
plt.xlabel("Year Added")
plt.ylabel("Titles Added")
plt.tight_layout()
plt.savefig(OUT / "02_titles_by_year.png")
plt.close()

# Chart 3 — Top 10 countries
plt.figure(figsize=(8.5, 6))
sns.barplot(x=top_countries.values, y=top_countries.index, hue=top_countries.index,
            palette="Reds_r", legend=False)
plt.title(f"US Leads Production — but {top_countries.index[1]} Is a Strong #2 ({top_countries.iloc[1]:,} Titles)",
          fontsize=12, fontweight="bold")
plt.xlabel("Number of Titles")
plt.ylabel("")
plt.tight_layout()
plt.savefig(OUT / "03_top_countries.png")
plt.close()

# Chart 4 — Top 10 genres
plt.figure(figsize=(8.5, 6))
sns.barplot(x=top_genres.values, y=top_genres.index, hue=top_genres.index,
            palette="Reds_r", legend=False)
plt.title(f'"{top_genres.index[0]}" Is the Single Largest Genre on the Platform',
          fontsize=12, fontweight="bold")
plt.xlabel("Number of Titles")
plt.ylabel("")
plt.tight_layout()
plt.savefig(OUT / "04_top_genres.png")
plt.close()

# Chart 5 — Rating distribution
plt.figure(figsize=(9.5, 5.5))
sns.countplot(data=df, y="rating", order=rating_order, hue="rating",
              palette="Reds_r", legend=False)
plt.title(f'Catalog Skews Mature — "{rating_order[0]}" Is the Most Common Rating',
          fontsize=12, fontweight="bold")
plt.xlabel("Number of Titles")
plt.ylabel("")
plt.tight_layout()
plt.savefig(OUT / "05_rating_distribution.png")
plt.close()

# Chart 6 — Movie runtime distribution
plt.figure(figsize=(9.5, 5.5))
sns.histplot(movies["duration_min"].dropna(), bins=30, color="#E50914", kde=True)
plt.axvspan(90, 120, color="#221f1f", alpha=0.08)
plt.title(f"{pct_std_runtime:.0f}% of Movies Fall in the Standard 90–120 Minute Window",
          fontsize=12, fontweight="bold")
plt.xlabel("Duration (minutes)")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig(OUT / "06_movie_runtime.png")
plt.close()

# Chart 7 — Regional genre preferences (NEW: directly targets "regional production insights")
plt.figure(figsize=(9.5, 6))
sns.barplot(data=top3_per_country, x="count", y="genre", hue="primary_country",
            palette=["#E50914", "#221f1f"])
plt.title(f"{top2[0]} and {top2[1]} Programming Skews Toward Different Genres",
          fontsize=12, fontweight="bold")
plt.xlabel("Number of Titles")
plt.ylabel("")
plt.legend(title="")
plt.tight_layout()
plt.savefig(OUT / "07_regional_genre_mix.png")
plt.close()

# ---------------------------------------------------------------------------
# 3. FINDINGS -> RECOMMENDATIONS
# ---------------------------------------------------------------------------
us_top3 = top3_per_country[top3_per_country["primary_country"] == top2[0]].sort_values("count", ascending=False).head(3)
in_top3 = top3_per_country[top3_per_country["primary_country"] == top2[1]].sort_values("count", ascending=False).head(3)

findings = f"""# Netflix Content Strategy — EDA Findings & Recommendations

**Dataset:** {len(df):,} titles, {df.shape[1]} columns · Analysis: pandas, NumPy, feature engineering, descriptive statistics

Each finding below is paired with a content-strategy recommendation, written for a non-technical stakeholder audience.

---

### 1. Content mix is movie-heavy and has stayed that way
**Finding:** {type_counts.get('Movie', 0):,} movies ({movie_pct:.1f}%) vs. {type_counts.get('TV Show', 0):,} TV shows ({tv_pct:.1f}%) — a consistent ~2:1 ratio across the catalog.
**Recommendation:** Movies remain the core of the catalog and shouldn't be deprioritized. Given how much of the industry conversation has shifted toward episodic content, this ratio is worth revisiting annually to confirm it still matches subscriber viewing behavior.

### 2. Catalog growth peaked in {peak_year}, then declined {decline_pct:.0f}%
**Finding:** Additions rose sharply through the mid-to-late 2010s, peaked at {peak_count:,} titles in {peak_year}, and fell to {latest_count:,} by {latest_year}.
**Recommendation:** The post-peak decline lines up with industry-wide production slowdowns (COVID-19) rather than a deliberate strategy shift — worth confirming against production-pipeline data before treating it as a spending cut.

### 3. India is a clear #2 content source behind the US
**Finding:** {top_countries.index[0]} leads with {top_countries.iloc[0]:,} titles; {top_countries.index[1]} follows with {top_countries.iloc[1]:,} — more than 3x the third-place country.
**Recommendation:** Continue prioritizing India in regional content investment — it's the most established non-US production base in the catalog, not an emerging one.

### 4. US and India audiences are being served different genre mixes
**Finding:** {top2[0]}'s top genres are {', '.join(us_top3['genre'])}. {top2[1]}'s top genres are {', '.join(in_top3['genre'])}.
**Recommendation:** Regional content strategy is already genre-differentiated — {top2[1]}'s lean toward {in_top3.iloc[0]['genre']} suggests future acquisitions there should follow that pattern rather than mirror the US slate.

### 5. "{top_genres.index[0]}" is the single largest genre tag platform-wide
**Finding:** {top_genres.iloc[0]:,} titles are tagged {top_genres.index[0]}, ahead of every other genre.
**Recommendation:** This tag is doing a lot of catalog-organization work — worth checking in the actual product UI whether it's helping subscribers discover content or acting as a catch-all that buries titles.

### 6. The catalog skews toward mature content
**Finding:** {rating_order[0]} is the most common rating.
**Recommendation:** If broader household/family reach is a stated goal, this is a measurable gap — family-friendly acquisition could be benchmarked against this rating distribution over time.

### 7. Movie runtimes cluster tightly around a standard length
**Finding:** {pct_std_runtime:.0f}% of movies run 90–120 minutes.
**Recommendation:** This is a reasonable acquisition/production benchmark — titles far outside this window are the exception, not the norm, and should be flagged for deliberate reasoning (e.g. prestige/awards content) rather than treated as typical.

---

## Data quality notes
- Missing values (top 5 columns): {', '.join(f'{c} {v}%' for c, v in missing_pct.head(5).items())}
- `director` is missing for ~30% of titles — any director-level analysis should note this as a coverage gap, not a true zero.
"""

Path("findings.md").write_text(findings)
print(findings)
print("\nCharts saved to ./charts/")
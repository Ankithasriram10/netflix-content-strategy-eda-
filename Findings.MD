# Netflix Content Strategy — EDA Findings & Recommendations

**Dataset:** 8,807 titles, 14 columns · Analysis: pandas, NumPy, feature engineering, descriptive statistics

Each finding below is paired with a content-strategy recommendation, written for a non-technical stakeholder audience.

---

### 1. Content mix is movie-heavy and has stayed that way
**Finding:** 6,131 movies (69.6%) vs. 2,676 TV shows (30.4%) — a consistent ~2:1 ratio across the catalog.
**Recommendation:** Movies remain the core of the catalog and shouldn't be deprioritized. Given how much of the industry conversation has shifted toward episodic content, this ratio is worth revisiting annually to confirm it still matches subscriber viewing behavior.

### 2. Catalog growth peaked in 2019, then declined 26%
**Finding:** Additions rose sharply through the mid-to-late 2010s, peaked at 2,016 titles in 2019, and fell to 1,498 by 2021.
**Recommendation:** The post-peak decline lines up with industry-wide production slowdowns (COVID-19) rather than a deliberate strategy shift — worth confirming against production-pipeline data before treating it as a spending cut.

### 3. India is a clear #2 content source behind the US
**Finding:** United States leads with 3,211 titles; India follows with 1,008 — more than 3x the third-place country.
**Recommendation:** Continue prioritizing India in regional content investment — it's the most established non-US production base in the catalog, not an emerging one.

### 4. US and India audiences are being served different genre mixes
**Finding:** United States's top genres are Dramas, Comedies, Documentaries. India's top genres are International Movies, Dramas, Comedies.
**Recommendation:** Regional content strategy is already genre-differentiated — India's lean toward International Movies suggests future acquisitions there should follow that pattern rather than mirror the US slate.

### 5. "International Movies" is the single largest genre tag platform-wide
**Finding:** 2,752 titles are tagged International Movies, ahead of every other genre.
**Recommendation:** This tag is doing a lot of catalog-organization work — worth checking in the actual product UI whether it's helping subscribers discover content or acting as a catch-all that buries titles.

### 6. The catalog skews toward mature content
**Finding:** TV-MA is the most common rating.
**Recommendation:** If broader household/family reach is a stated goal, this is a measurable gap — family-friendly acquisition could be benchmarked against this rating distribution over time.

### 7. Movie runtimes cluster tightly around a standard length
**Finding:** 51% of movies run 90–120 minutes.
**Recommendation:** This is a reasonable acquisition/production benchmark — titles far outside this window are the exception, not the norm, and should be flagged for deliberate reasoning (e.g. prestige/awards content) rather than treated as typical.

---

## Data quality notes
- Missing values (top 5 columns): director 29.9%, country 9.4%, cast 9.4%, date_added 0.1%, rating 0.0%
- `director` is missing for ~30% of titles — any director-level analysis should note this as a coverage gap, not a true zero.

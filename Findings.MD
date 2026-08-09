# Netflix Content Intelligence — Findings & Strategic Questions

**Dataset:** 8,807 titles, 12 columns · historical catalog snapshot, data through September 2021
**Analysis:** pandas, feature engineering, descriptive statistics, cross-tabulation

Each finding below separates what the data shows (**Observation**) from a reasonable reading of
it (**Interpretation**) from an open question that would need additional data to answer
(**Strategic Question**). This structure is deliberate — it keeps descriptive findings from
being overstated as business conclusions.

---

### 1. Content mix is movie-heavy and has stayed that way
**Observation:** 6,131 movies (69.6%) vs. 2,676 TV shows (30.4%) — a consistent ~2:1 ratio across the catalog.
**Interpretation:** Movies are the core of the catalog, not a secondary format.
**Strategic question:** Given how much industry conversation has shifted toward episodic content, does this ratio still match current subscriber viewing behavior? (This dataset has no viewing data to confirm either way.)

### 2. Catalog growth peaked in 2019, then declined 26%
**Observation:** Additions rose sharply through the mid-to-late 2010s, peaked at 2,016 titles in 2019, and fell to 1,498 by 2021.
**Interpretation:** The post-peak decline is consistent with industry-wide production slowdowns (COVID-19) rather than an obvious deliberate strategy shift.
**Strategic question:** Does this pattern hold up against actual production-pipeline data, or does some of the decline reflect a genuine spending change? This dataset can't distinguish between the two.

### 3. India is a clear #2 content source behind the US
**Observation:** United States leads with 3,211 titles; India follows with 1,008 — more than 3x the third-place country.
**Interpretation:** India is an established, not emerging, non-US production base in this catalog.
**Strategic question:** Does this level of regional representation align with continued regional demand and acquisition priorities? Answering this needs subscriber and regional-demand data this dataset doesn't contain.

### 4. US and India audiences are being served different genre mixes
**Observation:** United States's top genres are Dramas, Comedies, Documentaries. India's top genres are International Movies, Dramas, Comedies.
**Interpretation:** Regional content strategy already appears genre-differentiated in this catalog rather than uniform.
**Strategic question:** Should future regional acquisition continue following each market's existing genre pattern, or is there a case for divergence? Requires engagement/demand data to evaluate.

### 5. "International Movies" is the single largest genre tag platform-wide
**Observation:** 2,752 titles are tagged International Movies, ahead of every other genre (titles can carry multiple genre tags, so this is not mutually exclusive with other genres).
**Interpretation:** This tag carries a large share of catalog-organization weight.
**Strategic question:** Does this concentration help subscribers discover content, or does it act as a catch-all that buries titles within it? Would need product-UI and discovery-behavior data to answer.

### 6. The catalog skews toward mature content
**Observation:** TV-MA is the most common individual rating; grouped, Mature-rated titles (TV-MA, R, NC-17) outnumber Family/Kids-rated titles (TV-PG, TV-Y7, TV-Y7-FV, TV-Y, TV-G, PG, G) in the catalog.
**Interpretation:** This is a measurable skew toward mature content, not a claim about intent.
**Strategic question:** If broader household/family reach is a stated goal, is family-oriented content underrepresented relative to that goal? Needs a stated target to benchmark against.

### 7. Movie runtimes cluster tightly around a standard length
**Observation:** 51% of movies run 90–120 minutes.
**Interpretation:** This is a usable descriptive acquisition/production benchmark — titles far outside this window are the exception, not the norm.
**Strategic question:** Should this range formally inform acquisition targets, or are today's outliers (e.g. prestige/awards content) intentional exceptions worth preserving? Needs qualitative context this dataset doesn't provide.

### 8. Content age at addition varies widely (new derived analysis)
**Observation:** Comparing `release_year` to `date_added`, catalog age at time of addition spans from same-year releases through 10+ year-old library content, with same-year and 1–2-year-old additions making up the largest share.
**Interpretation:** The catalog is a mix of recent-release and back-catalog/library content rather than being dominated by either.
**Strategic question:** What is the intended balance between fresh releases and library content, and does the current mix match that intent? This dataset shows the mix but not the acquisition rationale behind it.

---

## What this dataset cannot tell us

This catalog metadata does **not** include: viewing hours, watch time, popularity, user
ratings, subscriber engagement, retention, revenue, acquisition cost, licensing cost,
production budget, or regional demand. **Catalog presence should not be interpreted as
audience demand.** Every strategic question above is intentionally left open rather than
answered, because answering it would require data this dataset doesn't have.

## Data quality notes

- Missing values (top 5 columns): director 29.9%, country 9.4%, cast 9.4%, date_added 0.1%, rating 0.0%.
- `director` is missing for ~30% of titles — any director-level analysis should note this as a coverage gap, not a true zero.
- A small number of rows have a duration value shifted into the `rating` field (e.g. "74 min") — these are treated as unrated/unknown rather than guessed at, and are grouped separately from confirmed NR/UR ratings.
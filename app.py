"""
Netflix Content Intelligence — Historical Catalog Analysis
A content-portfolio intelligence tool built on a historical Netflix catalog
snapshot (8,807 titles, through September 2021). It surfaces patterns in
what's in the catalog, where it comes from, how it's changed over time, and
frames those patterns as business questions worth investigating — it does
not claim to reflect current Netflix data, viewing behavior, or strategy.

Run locally:  streamlit run app.py
Deploy free:  share.streamlit.io (connect this GitHub repo)
"""

from fractions import Fraction

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="Netflix Content Intelligence", layout="wide", page_icon="🎬")

# ---------------------------------------------------------------------------
# THEME — refined green / white executive-dashboard palette (unchanged)
# ---------------------------------------------------------------------------
GREEN_DARK = "#0E4A3C"      # primary emphasis
GREEN = "#17A673"           # positive / primary data
GREEN_MID = "#5FBF9B"       # secondary series
GREEN_LIGHT = "#E7F5EE"     # backgrounds / highlights
GREEN_FAINT = "#F3FAF7"
INK = "#1C2622"             # primary text
MUTED = "#71827A"           # secondary text
BG = "#F5F7F6"
CARD = "#FFFFFF"
BORDER = "#E6ECE9"

# One accent, one neutral — used sparingly for "this bar/segment matters" call-outs
CHART_NEUTRAL = "#CFE3DA"
AMBER = "#B8862E"           # used sparingly for "worth investigating" call-outs

st.markdown(f"""
<style>
    .stApp {{ background-color: {BG}; }}
    html, body, [class*="css"] {{ color: {INK}; font-family: 'Inter','Segoe UI',Arial,sans-serif; }}
    #MainMenu, footer {{ visibility: hidden; }}
    .block-container {{ padding-top: 2rem; padding-bottom: 2rem; }}

    /* Headings — !important guards against Streamlit's dark-theme text-color variables */
    h1, h2, h3, h4, h5, h6 {{ color: {INK} !important; }}
    h1 {{ font-weight: 800; letter-spacing: -0.5px; }}
    h2, h3 {{ font-weight: 700; }}

    /* Plain markdown text (chart titles/subtitles rendered via st.markdown, captions) */
    [data-testid="stMarkdownContainer"] {{ color: {INK} !important; }}
    [data-testid="stMarkdownContainer"] p {{ color: {INK} !important; }}
    [data-testid="stMarkdownContainer"] strong {{ color: {INK} !important; }}
    [data-testid="stMarkdownContainer"] li {{ color: {INK} !important; }}
    [data-testid="stCaptionContainer"], .stCaption, small {{ color: {MUTED} !important; }}

    /* Expander header + body text */
    [data-testid="stExpander"] summary,
    [data-testid="stExpander"] summary span,
    [data-testid="stExpander"] p,
    [data-testid="stExpander"] li,
    .streamlit-expanderHeader, .streamlit-expanderContent {{
        color: {INK} !important;
    }}
    [data-testid="stExpander"] {{ background-color: {CARD} !important; }}

    /* Select / multiselect dropdown text */
    [data-baseweb="select"] * {{ color: {INK} !important; }}
    [data-baseweb="popover"] * {{ color: {INK} !important; }}

    /* Generic card shell (filter bar, chart containers) */
    div[data-testid="stVerticalBlockBorderWrapper"] {{
        background-color: {CARD};
        border-radius: 16px;
        border: 1px solid {BORDER};
        box-shadow: 0 2px 10px rgba(14, 74, 60, 0.04);
    }}

    /* Buttons */
    .stButton button {{
        background-color: {CARD};
        color: {GREEN_DARK};
        border: 1px solid {BORDER};
        border-radius: 10px;
        font-weight: 600;
    }}
    .stButton button:hover {{
        border-color: {GREEN};
        color: {GREEN};
    }}

    /* Multiselect chips / slider */
    .stMultiSelect [data-baseweb="tag"] {{ background-color: {GREEN} !important; }}
    .stSlider [data-baseweb="slider"] div[role="slider"] {{ background-color: {GREEN} !important; }}

    /* Expander */
    .streamlit-expanderHeader {{
        background-color: {CARD};
        border-radius: 12px;
        font-weight: 600;
        color: {GREEN_DARK};
    }}

    hr {{ border-color: {BORDER}; }}

    /* Custom card classes */
    .kpi-card {{
        background-color: {CARD};
        border: 1px solid {BORDER};
        border-radius: 16px;
        padding: 18px 20px;
        box-shadow: 0 2px 10px rgba(14, 74, 60, 0.04);
        height: 100%;
    }}
    .kpi-label {{
        color: {MUTED};
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        margin-bottom: 6px;
    }}
    .kpi-value {{
        color: {INK};
        font-size: 2rem;
        font-weight: 800;
        line-height: 1.1;
    }}
    .kpi-sub {{
        color: {GREEN};
        font-size: 0.85rem;
        font-weight: 600;
        margin-top: 6px;
    }}

    .insight-card {{
        background-color: {CARD};
        border: 1px solid {BORDER};
        border-left: 4px solid {GREEN};
        border-radius: 12px;
        padding: 16px 18px;
        height: 100%;
        box-shadow: 0 2px 10px rgba(14, 74, 60, 0.04);
    }}
    .insight-title {{
        color: {GREEN_DARK};
        font-weight: 700;
        font-size: 0.98rem;
        margin-bottom: 6px;
    }}
    .insight-text {{
        color: {INK};
        font-size: 0.88rem;
        line-height: 1.45;
    }}

    .strategy-card {{
        background-color: {GREEN_FAINT};
        border: 1px solid {GREEN_LIGHT};
        border-radius: 12px;
        padding: 16px 18px;
        height: 100%;
    }}
    .strategy-label {{
        color: {GREEN_DARK};
        font-size: 0.72rem;
        font-weight: 800;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        margin-bottom: 8px;
    }}
    .strategy-text {{
        color: {INK};
        font-size: 0.9rem;
        line-height: 1.5;
    }}

    .chart-subtitle {{
        color: {MUTED};
        font-size: 0.85rem;
        margin-top: -8px;
        margin-bottom: 10px;
    }}

    /* Opportunity cards — same shell as strategy card, amber accent to read as "to investigate" */
    .opp-card {{
        background-color: {CARD};
        border: 1px solid {BORDER};
        border-left: 4px solid {AMBER};
        border-radius: 12px;
        padding: 16px 18px;
        height: 100%;
        box-shadow: 0 2px 10px rgba(14, 74, 60, 0.04);
    }}
    .opp-label {{
        color: {AMBER};
        font-size: 0.72rem;
        font-weight: 800;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        margin-bottom: 8px;
    }}
    .opp-text {{
        color: {INK};
        font-size: 0.9rem;
        line-height: 1.5;
    }}

    /* Snapshot / data-vintage badge under the header */
    .snapshot-badge {{
        display: inline-block;
        background-color: {GREEN_LIGHT};
        color: {GREEN_DARK};
        border: 1px solid {GREEN_MID};
        border-radius: 999px;
        padding: 4px 14px;
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.02em;
    }}

    .section-note {{
        color: {MUTED};
        font-size: 0.88rem;
        line-height: 1.5;
        margin-top: -4px;
        margin-bottom: 14px;
    }}
</style>
""", unsafe_allow_html=True)


def kpi_card(label, value, sub=None):
    sub_html = f"<div class='kpi-sub'>{sub}</div>" if sub else ""
    st.markdown(
        f"""<div class="kpi-card">
                <div class="kpi-label">{label}</div>
                <div class="kpi-value">{value}</div>
                {sub_html}
            </div>""",
        unsafe_allow_html=True,
    )


def insight_card(title, text):
    st.markdown(
        f"""<div class="insight-card">
                <div class="insight-title">{title}</div>
                <div class="insight-text">{text}</div>
            </div>""",
        unsafe_allow_html=True,
    )


def strategy_card(label, text):
    st.markdown(
        f"""<div class="strategy-card">
                <div class="strategy-label">{label}</div>
                <div class="strategy-text">{text}</div>
            </div>""",
        unsafe_allow_html=True,
    )


def opportunity_card(label, text):
    st.markdown(
        f"""<div class="opp-card">
                <div class="opp-label">{label}</div>
                <div class="opp-text">{text}</div>
            </div>""",
        unsafe_allow_html=True,
    )


def styled_fig(fig, show_legend=True):
    """Apply consistent green/white styling to a plotly figure."""
    fig.update_layout(
        paper_bgcolor=CARD,
        plot_bgcolor=CARD,
        font=dict(color=INK, family="Inter, Arial, sans-serif"),
        margin=dict(l=70, r=30, t=30, b=60),
        showlegend=show_legend,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
    )
    fig.update_xaxes(gridcolor="#EEF2F0", zerolinecolor="#EEF2F0",
                      tickfont=dict(color=INK), title_font=dict(color=INK),
                      automargin=True, title_standoff=18)
    fig.update_yaxes(gridcolor="#EEF2F0", zerolinecolor="#EEF2F0",
                      tickfont=dict(color=INK), title_font=dict(color=INK),
                      automargin=True, title_standoff=18)
    return fig


def approx_fraction(pct, max_denominator=6):
    """'69.6' -> '~2 in every 3' — a friendly, approximate reading of a share."""
    frac = Fraction(pct / 100).limit_denominator(max_denominator)
    if frac.denominator in (0, 1):
        return None
    return f"~{frac.numerator} in every {frac.denominator}"


# ---------------------------------------------------------------------------
# DATA MODEL — derived fields are computed once, cached, and reused
# everywhere below rather than recalculated inline per chart.
# ---------------------------------------------------------------------------

# Rating -> audience-profile group. Documented explicitly (also shown in the
# "About the Data" section) rather than left as a silent mapping.
RATING_GROUP_MAP = {
    "TV-MA": "Mature", "R": "Mature", "NC-17": "Mature",
    "TV-14": "Teen", "PG-13": "Teen",
    "TV-PG": "Family / Kids", "TV-Y7": "Family / Kids", "TV-Y": "Family / Kids",
    "PG": "Family / Kids", "TV-G": "Family / Kids", "G": "Family / Kids",
    "TV-Y7-FV": "Family / Kids",
    "NR": "Unrated / Unknown", "UR": "Unrated / Unknown",
}
RATING_GROUP_ORDER = ["Mature", "Teen", "Family / Kids", "Unrated / Unknown"]

FRESHNESS_ORDER = [
    "New release (same year)",
    "1–2 years old",
    "3–5 years old",
    "6–10 years old",
    "10+ years old",
    "Unknown",
]


def bucket_freshness(age):
    if pd.isna(age):
        return "Unknown"
    if age <= 0:
        return "New release (same year)"
    if age <= 2:
        return "1–2 years old"
    if age <= 5:
        return "3–5 years old"
    if age <= 10:
        return "6–10 years old"
    return "10+ years old"


@st.cache_data
def load_data():
    df = pd.read_csv("netflix_titles.csv")

    # --- core cleaning ---
    df["date_added"] = pd.to_datetime(df["date_added"].str.strip(), errors="coerce")
    df["year_added"] = df["date_added"].dt.year
    df["primary_country"] = df["country"].str.split(",").str[0].str.strip()
    df["duration_min"] = df["duration"].str.extract(r"(\d+)").astype(float)

    # --- derived: content age at addition (release_year vs. year the title
    # entered the catalog) — the core "catalog freshness" feature ---
    df["content_age_at_addition"] = df["year_added"] - df["release_year"]
    # A small number of rows have a computed age below zero (data entry
    # inconsistencies in the source dataset) — treat these as same-year
    # additions rather than dropping them.
    df.loc[df["content_age_at_addition"] < 0, "content_age_at_addition"] = 0
    df["freshness_group"] = df["content_age_at_addition"].apply(bucket_freshness)

    # --- derived: audience / maturity profile group ---
    df["rating_group"] = df["rating"].map(RATING_GROUP_MAP).fillna("Unrated / Unknown")

    # --- derived: exploded genre table (a title can carry multiple genre
    # tags, so genre-level analysis is done on this long-format table) ---
    genres = df.assign(genre=df["listed_in"].str.split(", ")).explode("genre")
    genres["primary_country"] = genres["country"].str.split(",").str[0].str.strip()

    return df, genres


df, genres_full = load_data()
all_genres_sorted = sorted(genres_full["genre"].dropna().unique().tolist())

# ---------------------------------------------------------------------------
# HEADER
# ---------------------------------------------------------------------------
st.markdown(
    f"""
    <h1 style="margin-bottom:6px;">Netflix Content Intelligence</h1>
    <p style="color:{INK};font-size:1.05rem;margin-bottom:10px;">
        A content-portfolio view of the Netflix catalog — what's in it, where it comes from,
        how it's changed over time, and what's worth investigating further.
    </p>
    <span class="snapshot-badge">Historical catalog snapshot · Data through September 2021</span>
    """,
    unsafe_allow_html=True,
)
st.markdown(
    f"<p style='color:{MUTED};font-size:0.85rem;margin-top:10px;'>"
    "This is not a live Netflix dashboard. It analyzes a fixed, point-in-time catalog export "
    "and does not reflect current Netflix titles, availability, or performance.</p>",
    unsafe_allow_html=True,
)

st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# FILTER BAR — horizontal, human-friendly labels, reset control
# ---------------------------------------------------------------------------
year_min, year_max = int(df["year_added"].min(skipna=True)), int(df["year_added"].max(skipna=True))
top_country_options = df["primary_country"].value_counts().head(20).index.tolist()
rating_options = sorted(df["rating"].dropna().unique().tolist())
type_options = df["type"].dropna().unique().tolist()

with st.container(border=True):
    st.markdown(f"<div style='font-weight:700;color:{GREEN_DARK};margin-bottom:6px;'>Filter the Catalog</div>", unsafe_allow_html=True)
    f1, f2, f3, f4, f5, f6 = st.columns([1.1, 1.3, 1.2, 1.2, 1.4, 0.8])

    with f1:
        type_filter = st.multiselect(
            "Content Type", options=type_options,
            default=type_options, key="flt_type",
        )
    with f2:
        year_range = st.slider(
            "Year Added", year_min, year_max, (2015, year_max), key="flt_year",
        )
    with f3:
        country_filter = st.multiselect(
            "Country (top 20 shown)", options=top_country_options,
            default=[], key="flt_country",
        )
    with f4:
        rating_filter = st.multiselect(
            "Rating", options=rating_options, default=[], key="flt_rating",
        )
    with f5:
        genre_filter = st.multiselect(
            "Genre", options=all_genres_sorted, default=[], key="flt_genre",
        )
    with f6:
        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
        if st.button("↺ Reset Filters", use_container_width=True):
            for k in ["flt_type", "flt_year", "flt_country", "flt_rating", "flt_genre"]:
                if k in st.session_state:
                    del st.session_state[k]
            st.rerun()

    st.caption("Changing any filter above updates every number and chart on this page (the Key Content Insights strip stays fixed to the full-catalog findings).")

# ---------------------------------------------------------------------------
# APPLY FILTERS
# ---------------------------------------------------------------------------
mask = (
    df["type"].isin(type_filter)
    & df["year_added"].between(year_range[0], year_range[1])
)
if country_filter:
    mask &= df["primary_country"].isin(country_filter)
if rating_filter:
    mask &= df["rating"].isin(rating_filter)
if genre_filter:
    genre_show_ids = genres_full.loc[genres_full["genre"].isin(genre_filter), "show_id"].unique()
    mask &= df["show_id"].isin(genre_show_ids)

filtered = df[mask]
filtered_genres = genres_full[genres_full["show_id"].isin(filtered["show_id"])]

if filtered.empty:
    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    st.warning(
        "No titles match this combination of filters. Try widening the year range, "
        "clearing the country, rating, or genre selection, or including both content types."
    )
    st.stop()

# Shared aggregates used across KPIs and charts
movie_count = int((filtered["type"] == "Movie").sum())
tv_count = int((filtered["type"] == "TV Show").sum())
total_count = len(filtered)
movie_pct = (movie_count / total_count * 100) if total_count else 0
tv_pct = 100 - movie_pct if total_count else 0

top_c = filtered["primary_country"].value_counts()
top_country_name = top_c.index[0] if len(top_c) else "—"
top_country_count = int(top_c.iloc[0]) if len(top_c) else 0

yearly = filtered["year_added"].value_counts().sort_index().reset_index()
yearly.columns = ["year", "count"]
if len(yearly):
    peak_row = yearly.loc[yearly["count"].idxmax()]
    peak_year, peak_year_count = int(peak_row["year"]), int(peak_row["count"])
else:
    peak_year, peak_year_count = "—", 0

# ---------------------------------------------------------------------------
# A. EXECUTIVE OVERVIEW
# ---------------------------------------------------------------------------
st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)
st.subheader("Executive Overview")
st.markdown(
    "<div class='section-note'>Headline numbers for the titles currently in view.</div>",
    unsafe_allow_html=True,
)

movie_frac = approx_fraction(movie_pct)
k1, k2, k3, k4, k5 = st.columns(5)
with k1:
    kpi_card("Total Titles", f"{total_count:,}")
with k2:
    kpi_card("Movie Share", f"{movie_pct:.1f}%", movie_frac + " titles" if movie_frac else None)
with k3:
    kpi_card("TV Share", f"{tv_pct:.1f}%", f"{tv_count:,} TV shows in view")
with k4:
    kpi_card("Top Content Source", top_country_name, f"{top_country_count:,} titles")
with k5:
    kpi_card("Peak Addition Year", str(peak_year), f"{peak_year_count:,} titles added")

# ---------------------------------------------------------------------------
# KEY CONTENT INSIGHTS — fixed to the full-catalog findings (not recalculated
# per filter), so the headline story stays stable while users explore.
# ---------------------------------------------------------------------------
st.markdown("<div style='height:26px'></div>", unsafe_allow_html=True)
st.subheader("Key Content Insights")
st.markdown(
    "<div class='section-note'>These four hold across the full catalog, regardless of the filters above.</div>",
    unsafe_allow_html=True,
)

i1, i2, i3, i4 = st.columns(4)
with i1:
    insight_card(
        "Movies remain the catalog's core",
        "6,131 movies make up 69.6% of the catalog — roughly a 2:1 ratio compared with TV shows.",
    )
with i2:
    insight_card(
        "Catalog additions peaked in 2019",
        "2,016 titles were added in 2019 before additions declined to 1,498 by 2021.",
    )
with i3:
    insight_card(
        "India is the catalog's #2 content source",
        "India contributes 1,008 titles, behind only the United States with 3,211.",
    )
with i4:
    insight_card(
        "Most movies follow a standard runtime",
        "51% of movies fall within the 90–120 minute range.",
    )

# ---------------------------------------------------------------------------
# B. PORTFOLIO COMPOSITION
# ---------------------------------------------------------------------------
st.markdown("<div style='height:30px'></div>", unsafe_allow_html=True)
st.subheader("Portfolio Composition")
st.markdown(
    "<div class='section-note'>What the catalog is made of: content type mix and audience/maturity profile. "
    "These are descriptive groupings, not official Netflix categories — see \"About the Data\" for how they're defined.</div>",
    unsafe_allow_html=True,
)

pc1, pc2 = st.columns(2)

with pc1:
    with st.container(border=True):
        st.markdown("**How Is the Catalog Split Between Movies and TV?**")
        st.markdown(
            f"<div class='chart-subtitle'>Movies still dominate — {movie_pct:.0f}% of titles in view vs {tv_pct:.0f}% TV shows</div>",
            unsafe_allow_html=True,
        )
        type_counts_df = filtered["type"].value_counts().reset_index()
        type_counts_df.columns = ["type", "count"]
        fig = px.pie(type_counts_df, names="type", values="count", hole=0.6,
                     color="type", color_discrete_map={"Movie": GREEN, "TV Show": GREEN_DARK})
        fig.update_traces(textinfo="percent+label", textfont_size=13)
        st.plotly_chart(styled_fig(fig, show_legend=False), use_container_width=True, theme=None)

with pc2:
    with st.container(border=True):
        st.markdown("**What Does the Audience / Maturity Profile Look Like?**")
        rg_counts = (
            filtered["rating_group"].value_counts()
            .reindex(RATING_GROUP_ORDER).fillna(0).astype(int).reset_index()
        )
        rg_counts.columns = ["rating_group", "count"]
        top_rg = rg_counts.loc[rg_counts["count"].idxmax(), "rating_group"] if rg_counts["count"].sum() else "—"
        st.markdown(
            f"<div class='chart-subtitle'>\"{top_rg}\" is the largest audience group in view</div>",
            unsafe_allow_html=True,
        )
        colors = [GREEN_DARK if g == top_rg else CHART_NEUTRAL for g in rg_counts["rating_group"]]
        fig = px.bar(rg_counts, x="count", y="rating_group", orientation="h")
        fig.update_traces(marker_color=colors)
        fig.update_layout(yaxis={"categoryorder": "total ascending"}, xaxis_title="Titles", yaxis_title="")
        st.plotly_chart(styled_fig(fig, show_legend=False), use_container_width=True, theme=None)
        with st.expander("How ratings are grouped"):
            st.markdown(
                "- **Mature:** TV-MA, R, NC-17\n"
                "- **Teen:** TV-14, PG-13\n"
                "- **Family / Kids:** TV-PG, TV-Y7, TV-Y7-FV, TV-Y, TV-G, PG, G\n"
                "- **Unrated / Unknown:** NR, UR, missing ratings, and a handful of rows where a "
                "duration value (e.g. \"74 min\") appears in the rating field due to a source-data "
                "shift — these are treated as unknown rather than guessed at."
            )

# --- Catalog profile stat strip — interpretive, explicitly labeled as such ---
st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
with st.container(border=True):
    st.markdown(
        f"<div style='font-weight:700;color:{GREEN_DARK};'>Catalog Profile</div>"
        f"<div class='section-note'>Descriptive analytical measures, not official Netflix metrics.</div>",
        unsafe_allow_html=True,
    )
    mature_pct = (filtered["rating_group"] == "Mature").mean() * 100 if total_count else 0
    family_pct = (filtered["rating_group"] == "Family / Kids").mean() * 100 if total_count else 0
    known_country = filtered["primary_country"].dropna()
    intl_pct = (known_country != "United States").mean() * 100 if len(known_country) else 0
    known_age = filtered[filtered["freshness_group"] != "Unknown"]
    fresh_pct = (
        known_age["freshness_group"].isin(["New release (same year)", "1–2 years old"]).mean() * 100
        if len(known_age) else 0
    )
    top_genre_counts_all = filtered_genres["genre"].value_counts()
    top_genre_share = (top_genre_counts_all.iloc[0] / total_count * 100) if len(top_genre_counts_all) and total_count else 0

    cp1, cp2, cp3, cp4 = st.columns(4)
    with cp1:
        kpi_card("Mature-Rated Share", f"{mature_pct:.0f}%", "of titles in view")
    with cp2:
        kpi_card("Family / Kids Share", f"{family_pct:.0f}%", "of titles in view")
    with cp3:
        kpi_card("International Content Share", f"{intl_pct:.0f}%", "titles outside the US")
    with cp4:
        kpi_card("Catalog Freshness", f"{fresh_pct:.0f}%", "added within 2 yrs of release")

# ---------------------------------------------------------------------------
# C. CONTENT ACQUISITION & FRESHNESS
# ---------------------------------------------------------------------------
st.markdown("<div style='height:30px'></div>", unsafe_allow_html=True)
st.subheader("Content Acquisition & Freshness")
st.markdown(
    "<div class='section-note'>How the catalog grew over time, and how old content tends to be when it enters the catalog.</div>",
    unsafe_allow_html=True,
)

af1, af2 = st.columns(2)

with af1:
    with st.container(border=True):
        st.markdown("**How Has Content Addition Changed Over Time?**")
        st.markdown(
            f"<div class='chart-subtitle'>Additions peaked at {peak_year_count:,} titles in {peak_year}</div>",
            unsafe_allow_html=True,
        )
        fig = px.area(yearly, x="year", y="count", color_discrete_sequence=[GREEN])
        fig.update_traces(fillcolor="rgba(23,166,115,0.15)", line=dict(color=GREEN, width=3))
        if len(yearly):
            fig.add_trace(go.Scatter(
                x=[peak_year], y=[peak_year_count], mode="markers+text",
                marker=dict(color=GREEN_DARK, size=11),
                text=[f"Peak: {peak_year}"], textposition="top center",
                textfont=dict(color=GREEN_DARK, size=12), showlegend=False,
            ))
        fig.update_layout(xaxis_title="Year Added", yaxis_title="Titles Added")
        st.plotly_chart(styled_fig(fig, show_legend=False), use_container_width=True, theme=None)
        if len(yearly) >= 2:
            last_two = yearly.tail(2)
            prev_count, latest_count = int(last_two.iloc[0]["count"]), int(last_two.iloc[1]["count"])
            change = latest_count - prev_count
            direction = "up" if change > 0 else ("down" if change < 0 else "flat")
            st.caption(
                f"Latest year in view ({int(last_two.iloc[1]['year'])}) is {direction} "
                f"{abs(change):,} titles vs. the prior year. The post-2019 decline in the full "
                f"catalog lines up with industry-wide production slowdowns — worth confirming "
                f"against production-pipeline data before reading it as a spending cut."
            )

with af2:
    with st.container(border=True):
        st.markdown("**How Old Is Content When It Enters the Catalog?**")
        st.markdown(
            "<div class='chart-subtitle'>Catalog age at time of addition — release_year vs. date_added</div>",
            unsafe_allow_html=True,
        )
        fresh_counts = (
            filtered["freshness_group"].value_counts()
            .reindex(FRESHNESS_ORDER).fillna(0).astype(int).reset_index()
        )
        fresh_counts.columns = ["freshness_group", "count"]
        fig = px.bar(fresh_counts, x="freshness_group", y="count", color_discrete_sequence=[GREEN])
        fig.update_layout(xaxis_title="", yaxis_title="Titles")
        st.plotly_chart(styled_fig(fig, show_legend=False), use_container_width=True, theme=None)
        st.caption(
            "These buckets describe catalog age at addition — they are not a claim about Netflix's "
            "official acquisition strategy."
        )

# ---------------------------------------------------------------------------
# D. REGIONAL & GENRE INTELLIGENCE
# ---------------------------------------------------------------------------
st.markdown("<div style='height:30px'></div>", unsafe_allow_html=True)
st.subheader("Regional Intelligence")
st.markdown(
    "<div class='section-note'>Where content comes from, and how genre mix differs across the top content-producing markets.</div>",
    unsafe_allow_html=True,
)

rg1, rg2 = st.columns(2)

with rg1:
    with st.container(border=True):
        st.markdown("**Which Countries Supply the Most Content?**")
        st.markdown(
            f"<div class='chart-subtitle'>{top_country_name} leads with {top_country_count:,} titles in view</div>",
            unsafe_allow_html=True,
        )
        top_countries_df = filtered["primary_country"].value_counts().head(10).reset_index()
        top_countries_df.columns = ["country", "count"]
        colors = [GREEN_DARK if c in ("United States", "India") else CHART_NEUTRAL
                  for c in top_countries_df["country"]]
        fig = px.bar(top_countries_df, x="count", y="country", orientation="h")
        fig.update_traces(marker_color=colors)
        fig.update_layout(yaxis={"categoryorder": "total ascending"}, xaxis_title="Titles", yaxis_title="")
        st.plotly_chart(styled_fig(fig, show_legend=False), use_container_width=True, theme=None)

with rg2:
    with st.container(border=True):
        st.markdown("**Compare Markets: How Does the Genre Mix Differ?**")
        market_options = filtered["primary_country"].value_counts().head(20).index.tolist()
        default_a = "United States" if "United States" in market_options else (market_options[0] if market_options else None)
        default_b = "India" if "India" in market_options else (market_options[1] if len(market_options) > 1 else None)
        mc1, mc2 = st.columns(2)
        with mc1:
            market_a = st.selectbox(
                "Market A", options=market_options,
                index=market_options.index(default_a) if default_a in market_options else 0,
                key="market_a",
            ) if market_options else None
        with mc2:
            b_options = [m for m in market_options if m != market_a] or market_options
            market_b = st.selectbox(
                "Market B", options=b_options,
                index=b_options.index(default_b) if default_b in b_options else 0,
                key="market_b",
            ) if b_options else None

        if market_a and market_b:
            compare_genres = (
                filtered_genres[filtered_genres["primary_country"].isin([market_a, market_b])]
                .groupby(["primary_country", "genre"]).size().reset_index(name="count")
            )
            top5_each = (
                compare_genres.sort_values("count", ascending=False)
                .groupby("primary_country").head(5)
            )
            st.markdown(
                f"<div class='chart-subtitle'>Top genre tags for {market_a} vs {market_b} in view</div>",
                unsafe_allow_html=True,
            )
            fig = px.bar(top5_each, x="count", y="genre", color="primary_country", orientation="h",
                         barmode="group", color_discrete_sequence=[GREEN_DARK, GREEN])
            fig.update_layout(yaxis={"categoryorder": "total ascending"}, xaxis_title="Titles",
                               yaxis_title="", legend_title_text="")
            st.plotly_chart(styled_fig(fig, show_legend=True), use_container_width=True, theme=None)
        else:
            st.info("Not enough countries in the current filter selection to compare markets.")

st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
st.subheader("Genre Intelligence")

with st.container(border=True):
    st.markdown("**Where Is the Catalog Most Concentrated?**")
    top_genres_df = filtered_genres["genre"].value_counts().head(10).reset_index()
    top_genres_df.columns = ["genre", "count"]
    top_genre_name = top_genres_df["genre"].iloc[0] if len(top_genres_df) else "—"
    top_genre_pct = (top_genres_df["count"].iloc[0] / total_count * 100) if len(top_genres_df) and total_count else 0
    st.markdown(
        f"<div class='chart-subtitle'>\"{top_genre_name}\" appears on {top_genre_pct:.0f}% of titles in view</div>",
        unsafe_allow_html=True,
    )
    fig = px.bar(top_genres_df, x="count", y="genre", orientation="h",
                 color_discrete_sequence=[GREEN])
    fig.update_layout(yaxis={"categoryorder": "total ascending"}, xaxis_title="Titles", yaxis_title="")
    st.plotly_chart(styled_fig(fig, show_legend=False), use_container_width=True, theme=None)
    st.caption(
        "Titles may belong to multiple genres, so genre percentages are not mutually exclusive "
        "and won't sum to 100%."
    )

# ---------------------------------------------------------------------------
# Runtime — kept from the original dashboard
# ---------------------------------------------------------------------------
st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
with st.container(border=True):
    st.markdown("**What's the Typical Movie Runtime?**")
    movie_runtimes = filtered[filtered["type"] == "Movie"]["duration_min"].dropna()
    if len(movie_runtimes):
        in_band = movie_runtimes.between(90, 120).mean() * 100
        st.markdown(
            f"<div class='chart-subtitle'>{in_band:.0f}% of movies in view run 90–120 minutes</div>",
            unsafe_allow_html=True,
        )
        fig = px.histogram(movie_runtimes, nbins=30, color_discrete_sequence=[CHART_NEUTRAL])
        fig.add_vrect(x0=90, x1=120, fillcolor=GREEN, opacity=0.18, line_width=0)
        fig.update_layout(showlegend=False, xaxis_title="Minutes", yaxis_title="Titles")
        st.plotly_chart(styled_fig(fig, show_legend=False), use_container_width=True, theme=None)
    else:
        st.markdown(
            "<div class='chart-subtitle'>No movies in the current filter selection</div>",
            unsafe_allow_html=True,
        )
        st.info("Adjust the filters above to include Movies and a wider year range to see runtime patterns.")

# ---------------------------------------------------------------------------
# F. STRATEGIC OPPORTUNITIES — areas worth investigating, not predictions
# ---------------------------------------------------------------------------
st.markdown("<div style='height:30px'></div>", unsafe_allow_html=True)
st.subheader("Strategic Opportunities to Investigate")
st.markdown(
    "<div class='section-note'>These are catalog-derived observations framed as open questions, not "
    "recommendations. Validating any of them would require data this dataset doesn't have — see "
    "\"What This Dataset Cannot Tell Us\" below.</div>",
    unsafe_allow_html=True,
)

o1, o2 = st.columns(2)
with o1:
    opportunity_card(
        "Regional Investment",
        "India is the established #2 content source in this catalog (1,008 titles vs. the "
        "United States' 3,211). Worth evaluating whether this level of representation still "
        "aligns with regional demand and acquisition priorities.",
    )
with o2:
    opportunity_card(
        "Genre Concentration",
        "\"International Movies\" is the single largest genre tag platform-wide. Worth assessing "
        "whether that concentration supports discovery or whether other categories are "
        "comparatively underrepresented.",
    )

st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
o3, o4 = st.columns(2)
with o3:
    opportunity_card(
        "Catalog Freshness",
        "Content age at addition varies widely across the catalog. Worth understanding the "
        "intended balance between recent releases and library/back-catalog content.",
    )
with o4:
    opportunity_card(
        "Family-Oriented Content",
        "The catalog skews toward mature-rated content. If broader household reach is a stated "
        "goal, this is worth investigating as a measurable representation gap.",
    )

st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
o5, _ = st.columns(2)
with o5:
    opportunity_card(
        "Runtime Benchmark",
        "51% of movies fall within a 90–120 minute band. Worth using this as a descriptive "
        "benchmark when evaluating new acquisitions, rather than a hard rule.",
    )

# ---------------------------------------------------------------------------
# WHAT THIS DATASET CANNOT TELL US
# ---------------------------------------------------------------------------
st.markdown("<div style='height:30px'></div>", unsafe_allow_html=True)
st.subheader("What This Dataset Cannot Tell Us")
with st.container(border=True):
    st.markdown(
        "This catalog metadata does **not** include: viewing hours, watch time, popularity, "
        "user ratings, subscriber engagement, retention, revenue, acquisition cost, licensing "
        "cost, production budget, or regional demand.\n\n"
        "**Catalog presence should not be interpreted as audience demand.** Every finding and "
        "opportunity above describes what's in the catalog — not how it performed."
    )

# ---------------------------------------------------------------------------
# G. DATA QUALITY & METHODOLOGY
# ---------------------------------------------------------------------------
st.markdown("<div style='height:22px'></div>", unsafe_allow_html=True)
with st.expander("ℹ️ About the Data & Methodology"):
    st.markdown(f"""
**Dataset:** 8,807 Netflix titles, 12 columns · historical catalog snapshot, data through September 2021.

**Missing data:** director ~29.9%, country ~9.4%, cast ~9.4%, date added ~0.1%, rating ~0.0%.
Director is missing for roughly 3 in 10 titles — treat any director-level analysis as a coverage
gap rather than a true zero. A small number of rows also have a duration value shifted into the
rating field (e.g. "74 min") — these are treated as unrated rather than guessed at.

**Methodology:**
1. Cleaned dates and categorical fields.
2. Extracted a primary country from the (sometimes multi-country) country field.
3. Split multi-value genre fields into a long-format table for genre-level analysis.
4. Derived numeric movie runtime from the duration field.
5. Compared release year with date added to derive catalog age at addition.
6. Used descriptive statistics and cross-tabulation (not predictive modeling) throughout.
7. Framed findings as observations and open questions, not confirmed business conclusions.

**Source:** Netflix Movies and TV Shows dataset (community-mirrored on GitHub; originally
sourced from Flixable/Kaggle).
""")

st.caption("Netflix Content Intelligence · Historical catalog snapshot · Built with pandas + Plotly + Streamlit")

# ---------------------------------------------------------------------------
# FOOTER — subtle, minimal, no card/background
# ---------------------------------------------------------------------------
st.markdown(
    f"""
    <div style="text-align:center; margin-top:36px; padding-top:16px;
                border-top:1px solid {BORDER}; color:{MUTED}; font-size:0.78rem; line-height:1.7;">
        Netflix Content Intelligence<br>
        Historical catalog snapshot · Data through September 2021<br>
        Built with Python · Pandas · Plotly · Streamlit<br>
        Built by Ankitha · 2026
    </div>
    """,
    unsafe_allow_html=True,
)
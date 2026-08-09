# Project & Interview Reference — Ankitha

Three projects, one reference. Everything you need for a resume line, a portfolio README, or a live interview answer, in one place. Where I don't have your exact numbers, I've marked `[FILL IN: ...]` — don't let an interviewer catch a made-up metric; drop in your real ones before you use these.

---

## 1. RAG Pipeline Builder — L&T Technology Services (GenAI Internship, Jun–Jul 2026)

**One-liner:** Built a retrieval-augmented generation pipeline (PlxAI) with LangChain + a vector DB, deployed on GCP, with an evaluation/test harness for output quality.

### STAR story
- **Situation:** Interning on the GenAI team at L&T Technology Services, Bengaluru, working on PlxAI — an internal RAG-based tool for `[FILL IN: what PlxAI does / who uses it]`.
- **Task:** `[FILL IN: what you were specifically asked to own — e.g. "improve retrieval accuracy," "stand up the eval pipeline," "reduce hallucination rate"]`.
- **Action:** Built the retrieval pipeline using LangChain, indexed documents into a vector database, iterated on prompt design/refinement to improve grounding, and deployed the service on GCP. Built out an evaluation/test pipeline to systematically measure output quality rather than eyeballing responses.
- **Result:** `[FILL IN: a concrete number — retrieval accuracy %, latency, eval pass rate, hallucination reduction, time saved]`.

### Full workflow
1. Document ingestion → chunking → embedding → vector DB indexing
2. Retriever design (similarity search, top-k tuning)
3. Prompt construction — grounding the LLM response in retrieved context
4. Prompt refinement loop — iterating on wording/structure to reduce hallucination and improve relevance
5. Evaluation harness — automated test cases checking output quality against expected answers/criteria
6. Deployment to GCP (service hosting, environment config)

### Key terms to have crisp definitions for
- **RAG (Retrieval-Augmented Generation)** — grounding an LLM's output in retrieved external documents instead of relying purely on parametric knowledge
- **Vector DB** — stores document embeddings for similarity search (which one did you use — Pinecone, Chroma, FAISS, Weaviate? `[FILL IN]`)
- **LangChain** — orchestration framework for chaining retrieval + prompting + LLM calls
- **Embeddings** — vector representations of text used for semantic similarity search
- **Prompt refinement** — iterative editing of prompt structure/wording to improve model output quality
- **Evaluation pipeline** — systematic, repeatable testing of LLM outputs (accuracy, relevance, groundedness) vs. ad hoc manual review

### Codebase / stack
- LangChain, a vector database (`[FILL IN which one]`), GCP for deployment
- `[FILL IN: repo name/link if you have one you can point to]`

---

## 2. Customer Churn Prediction — Askan Technologies (AI/ML Internship, May–Jul 2025)

**One-liner:** Built a churn prediction model to identify customers likely to leave, using applied ML on customer behavior data.

### STAR story
- **Situation:** AI/ML internship at Askan Technologies, Pondicherry, on a churn prediction problem for `[FILL IN: what kind of business/customer base]`.
- **Task:** `[FILL IN: what you owned — full pipeline, feature engineering, model selection, deployment?]`.
- **Action:** `[FILL IN: your actual steps — data cleaning, feature engineering, which model(s) you tried (logistic regression / random forest / XGBoost / etc.), how you validated it]`.
- **Result:** `[FILL IN: model accuracy/F1/AUC, or business impact if you had visibility into it]`.

### Full workflow (fill in the version you actually ran)
1. Data collection/cleaning — `[FILL IN: source, size, key cleaning steps]`
2. Exploratory analysis — identifying churn signals/patterns
3. Feature engineering — `[FILL IN: which features mattered]`
4. Model selection & training — `[FILL IN: algorithms tried]`
5. Evaluation — `[FILL IN: metrics used — accuracy, precision/recall, AUC-ROC]`
6. `[FILL IN: was there a deployment/dashboard/handoff step?]`

### Key terms to have crisp definitions for
- **Churn prediction** — classifying which customers are likely to stop using a product/service, usually a binary classification problem
- **Class imbalance** — churn datasets are typically imbalanced (few churners vs. many retained customers) — did you handle this (SMOTE, class weights)? `[FILL IN]`
- **Precision vs. recall trade-off** — in churn, missing a real churner (false negative) is usually costlier than a false alarm — be ready to explain which you optimized for
- **Feature importance** — which signals actually drove predictions in your model

### Codebase / stack
- `[FILL IN: Python/pandas/scikit-learn/XGBoost — whatever you actually used]`
- `[FILL IN: repo link if available]`

---

## 3. Netflix Content EDA — Personal Portfolio Project (built today)

**One-liner:** Exploratory analysis of 8,807 Netflix titles to surface content-strategy patterns — catalog growth, geographic mix, genre distribution, ratings, runtime.

### STAR story
- **Situation:** Wanted a self-directed data analysis project to demonstrate EDA and storytelling-with-data skills outside of internship work.
- **Task:** Analyze Netflix's public title catalog and extract concrete, defensible insights about content strategy.
- **Action:** Cleaned and parsed the raw dataset (handled missing values in director/cast/country, parsed multi-value genre and country fields, converted date fields), then built 6 visualizations answering specific questions about content mix, growth trend, geography, genre, ratings, and runtime.
- **Result:** Found that Netflix's catalog is 69.6% movies / 30.4% TV shows, that content additions peaked in 2019 (2,016 titles) before falling off in 2020–2021, that the US and India are the top two content sources, and that "International Movies" is the single largest genre tag — a data-backed read on Netflix's internationalization push.

### Full workflow
1. Sourced the dataset (8,807 rows × 12 columns) — public Netflix titles data
2. Cleaned data — parsed `date_added` to datetime, split multi-value `country`/`listed_in` fields, audited missing values (director 29.9%, country 9.4%, cast 9.4%)
3. Feature engineering — primary country, year added, movie runtime vs. TV season count
4. Built 6 charts: type split, titles-added-by-year trend, top 10 countries, top 10 genres, rating distribution, movie runtime distribution
5. Wrote up findings as a structured summary

### Key terms to have crisp definitions for
- **EDA (Exploratory Data Analysis)** — systematically profiling a dataset (distributions, missingness, relationships) before modeling or drawing conclusions
- **Multi-value field parsing** — genres/countries stored as comma-separated strings needed splitting/exploding before aggregation
- **Missing data audit** — quantifying and being explicit about what's missing (director 29.9% missing) rather than silently dropping rows

### Codebase / stack
- Python, pandas, matplotlib, seaborn
- Files: `netflix_eda.py` (analysis script), `charts/` (6 PNGs), `README.md`, `findings.md`, `netflix_titles.csv`
- Ready to push straight to a GitHub repo as-is

---

## Cross-project glossary (fast recall for interviews)

| Term | One-line definition |
|---|---|
| RAG | Grounding LLM output in retrieved external documents |
| Vector DB | Stores embeddings for semantic similarity search |
| LangChain | Framework for chaining retrieval + prompt + LLM steps |
| Prompt refinement | Iterating prompt wording/structure to improve output quality |
| Evaluation pipeline | Systematic, repeatable testing of model output quality |
| Churn prediction | Binary classification of who's likely to leave |
| Class imbalance | Few positive cases vs. many negative — needs special handling |
| EDA | Profiling a dataset's structure/quality before analysis or modeling |

## What's real vs. what needs work
- **Netflix EDA** — fully built today: script, charts, README, findings. Ready to push to GitHub as-is.
- **RAG Pipeline Builder & Churn Prediction** — real internship work, but the STAR stories above have placeholders where I don't have your actual metrics/tools. Fill those in from memory or your internship notes before an interview — an interviewer will probe for specifics, and "I don't remember the exact number" is a worse answer live than having it ready now.

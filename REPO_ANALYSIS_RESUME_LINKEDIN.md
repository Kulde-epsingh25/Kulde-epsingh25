# Kulde-epsingh25 — Full GitHub Repository Analysis (Account-Wide)

Scope: **all public repositories under `github.com/Kulde-epsingh25`**.

---

## 1) Complete Repository Inventory

| Repo | Primary Domain | Main Stack | Architecture Pattern | Working Condition |
|---|---|---|---|---|
| `Social` | AI social-media intelligence + posting | Python, Redis, NLP, LangGraph/CrewAI-style orchestration | Agent-based modular pipeline (`ingestion -> analysis -> compliance -> publishing`) | **Working (integration-heavy; needs API keys/infrastructure)** |
| `Kulde-epsingh25` | Multi-project monorepo (Dance + JS + React demos) | Python + HTML/CSS/JS + React | Monorepo with project folders | **Working mixed** (many demos complete; some starter/incomplete modules) |
| `project2` | Conversational AI + churn analytics | Python, scikit-learn, notebooks, dashboard assets | Data/ML pipeline with dashboard/report outputs | **Working (research/portfolio grade)** |
| `YouTubeEnhance.apk` | Android app distribution repo | APK release artifacts + docs | Release-centric repo (binary delivery via GitHub Releases) | **Working for distribution** |
| `school-pro` | School management SaaS MVP | Next.js/React, TypeScript, Express, MongoDB, Prisma | Full-stack modular web architecture (frontend + backend + role modules) | **Working MVP (broad feature scope)** |
| `natyaveda-analyzer` | Indian classical dance AI pipeline | Python, CV/ML tooling, Docker | End-to-end ML pipeline (`data -> features -> train -> eval -> infer`) | **Working (good engineering maturity)** |
| `Scyther-` | Security protocol verification + auth system | Python, Scyther CLI, SQLite, shell tooling | Dual architecture: formal protocol models + executable auth CLI | **Working (research + implementation)** |
| `Vedic-Intelligence-System-VIS-` | Knowledge/LLM platform for Vedic intelligence | Python, FastAPI, LangChain, vector DB + graph DB + SQL | Multi-store AI architecture (vector + graph + relational + API) | **Partially ready** (strong scaffold, docs/entrypoints still thin) |
| `project` | Crypto market forecasting platform | Python, time-series ML/DL, Streamlit | Multi-model forecasting pipeline + analytics dashboard | **Working (research/portfolio grade)** |

---

## 2) Detailed Analysis by Repository

## A) `Social`
**What it is:** Autonomous AI workflow for political/news analysis and controlled social posting.

**Strengths**
- Strong modular decomposition under `src/` (agents, compliance, orchestration, publishing, dashboard).
- Practical operations features: Human-in-the-Loop mode, daily limits, review queue.
- Clear CLI workflow and test suite.

**Architecture Summary**
- Event/data ingestion -> AI analysis -> compliance/fact-check filtering -> publication pipeline.
- Infrastructure dependency model (Redis required, Kafka optional).

**Working Condition**
- Technically solid structure; operational readiness depends on external credentials + infra.

**Resume/LinkedIn Keywords**
`Agentic AI`, `LLM Orchestration`, `Python Backend`, `Redis`, `NLP Pipeline`, `Compliance Automation`, `Human-in-the-Loop`, `CLI Systems`.

---

## B) `Kulde-epsingh25` (monorepo)
**What it is:** Combined repository containing:
- `DanceAnalyzer` (ML dataset/pipeline project)
- `HTML CSS JS REACT` (frontend mini-project set + React starters)

**Strengths**
- Demonstrates breadth: CV/data pipeline + frontend implementation.
- `DanceAnalyzer` has strong taxonomy, dataset structure, and script organization.

**Working Condition**
- Mixed maturity: multiple functional mini-projects, plus a few starter/incomplete areas.

**Keywords**
`Computer Vision`, `Dataset Engineering`, `Frontend Development`, `JavaScript Projects`, `React Basics`, `Project Portfolio`.

---

## C) `project2`
**What it is:** NexusAI-style suite for conversational AI plus customer/churn analytics.

**Strengths**
- Multi-model framing (classification + conversational intelligence).
- Good presentation orientation (dashboard/reporting assets, notebook workflows).

**Architecture Summary**
- Data ingestion -> preprocessing -> feature engineering -> model evaluation -> interactive reporting.

**Working Condition**
- Portfolio/research ready; likely strongest in analysis/demo context.

**Keywords**
`Predictive Analytics`, `Customer Churn`, `scikit-learn`, `NLP`, `Business Intelligence`, `Dashboarding`, `Data Science Workflow`.

---

## D) `YouTubeEnhance.apk`
**What it is:** APK-focused release repository for Android app distribution.

**Strengths**
- Clear value proposition and user-oriented README.
- Multi-architecture APK delivery links.

**Architecture Summary**
- Distribution-centric repo; source architecture is not primary in this repository.

**Working Condition**
- Works as release channel/landing repository.

**Keywords**
`Android Distribution`, `Release Engineering`, `APK Packaging`, `Product Documentation`, `User Experience`.

---

## E) `school-pro`
**What it is:** Multi-tenant school management MVP with broad module coverage.

**Strengths**
- Full-stack architecture with clear frontend/backend split.
- Enterprise-like modules: RBAC, analytics, attendance, fees, library, transport, hostel.

**Architecture Summary**
- Next.js frontend + Express API + MongoDB/Prisma data layer.
- Domain module decomposition for scalable feature expansion.

**Working Condition**
- Strong MVP; complexity suggests ongoing stabilization and hardening expected.

**Keywords**
`SaaS MVP`, `Next.js`, `TypeScript`, `Express.js`, `MongoDB`, `Prisma`, `RBAC`, `Multi-Tenant Architecture`, `EdTech`.

---

## F) `natyaveda-analyzer`
**What it is:** Indian classical dance recognition pipeline (v2) with end-to-end ML lifecycle.

**Strengths**
- Clean lifecycle commands (`download`, `refine`, `extract`, `split`, `train`, `evaluate`, `infer`).
- Includes Docker strategy, tests, docs, configs, and setup verification.

**Architecture Summary**
- Reproducible ML engineering pipeline with package structure + script entry points.

**Working Condition**
- High maturity for portfolio/research demonstration.

**Keywords**
`Machine Learning Pipeline`, `Computer Vision`, `MLOps Foundations`, `Docker`, `Model Evaluation`, `Inference Pipeline`, `Indian Classical Dance AI`.

---

## G) `Scyther-`
**What it is:** Security research platform combining formal protocol verification and executable auth CLI.

**Strengths**
- Bridges theory and practice: SPDL protocol proofs + practical auth controls.
- Includes attack graph generation and verification automation scripts.

**Architecture Summary**
- Parallel tracks:
  - Formal verification track (Scyther protocol models)
  - Operational auth track (Python CLI, SQLite, security controls)

**Working Condition**
- Strong as security-research showcase with practical implementation support.

**Keywords**
`Cybersecurity`, `Formal Verification`, `Scyther`, `Authentication`, `Authorization`, `Security Protocol Analysis`, `Threat Modeling`, `SQLite`.

---

## H) `Vedic-Intelligence-System-VIS-`
**What it is:** AI knowledge platform scaffold with Sanskrit processing + multi-database intelligence stack.

**Strengths**
- Ambitious architecture: FastAPI + LangChain + embeddings + vector DB + graph DB + SQL.
- Clear environment design for cloud-native components (Supabase, Neo4j, Pinecone, Redis).

**Architecture Summary**
- Retrieval + knowledge reasoning stack spanning vector, graph, and relational data stores.

**Working Condition**
- Early/partial implementation state from repository surface, but architecture blueprint is strong.

**Keywords**
`Knowledge Systems`, `RAG`, `LangChain`, `FastAPI`, `Vector Database`, `Graph Database`, `Neo4j`, `Pinecone`, `Sanskrit NLP`.

---

## I) `project` (CryptoForecast)
**What it is:** Multi-model crypto forecasting and analytics platform.

**Strengths**
- Combines statistical and deep learning models in a model-comparison workflow.
- Produces decision-friendly outputs (interactive dashboard + BI exports).

**Architecture Summary**
- Data acquisition -> feature engineering -> model competition -> backtesting -> reporting/UI.

**Working Condition**
- Portfolio-ready data science project with strong presentation value.

**Keywords**
`Time Series Forecasting`, `ARIMA`, `Prophet`, `LSTM`, `Backtesting`, `Streamlit`, `Financial Analytics`, `Model Benchmarking`.

---

## 3) Cross-Account Skill Map (What recruiters will infer)

From all repositories combined, your visible strengths are:
- **AI/ML Engineering:** data pipelines, model workflows, inference scripting, evaluation patterns
- **Applied NLP & Agentic Systems:** orchestration, analysis pipelines, HITL workflows
- **Frontend & Product Prototyping:** JavaScript/React demos and UI-heavy mini-apps
- **Full-Stack Delivery:** Next.js + Express + DB-backed SaaS MVP design
- **Security Research Orientation:** protocol verification + implementation-level auth controls

---

## 4) Resume + LinkedIn Keyword Bank (Account-Level)

Use these repeatedly in headline, about section, project bullets, and skills:

`Machine Learning Engineer`, `AI Engineer`, `Python Developer`, `Computer Vision`, `NLP`, `Agentic AI`, `Data Pipeline`, `MLOps`, `FastAPI`, `LangChain`, `Next.js`, `TypeScript`, `Express.js`, `MongoDB`, `Prisma`, `React`, `JavaScript`, `Security Research`, `Formal Verification`, `Time-Series Forecasting`, `Dashboard Analytics`.

---

## 5) Portfolio Readiness Prioritization

### Showcase First (highest impact)
1. `natyaveda-analyzer`
2. `school-pro`
3. `Social`
4. `Scyther-`
5. `project` / `project2` (pick based on role target)

### Showcase as Supporting Portfolio
- `Kulde-epsingh25` mini-project set (selected best demos)
- `YouTubeEnhance.apk` (product/release storytelling)

### Improve Next
- Add stronger root documentation and execution proof for `Vedic-Intelligence-System-VIS-`.
- Keep monorepo demos curated (highlight complete projects, hide unfinished ones in public portfolio narratives).


# 🏗️ Architecture Diagram - Veritas Finance

## System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         VERITAS FINANCE SYSTEM                          │
│                    Mis-selling Detection Platform                        │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                    ┌───────────────┴───────────────┐
                    │                               │
            ┌───────▼────────┐              ┌───────▼────────┐
            │   DATA LAYER   │              │  PRESENTATION  │
            │                │              │     LAYER      │
            │  • Mock Data   │              │                │
            │  • CSV Files   │              │  • Streamlit   │
            │  • JSON Docs   │              │  • Plotly      │
            │  • Reviews     │              │  • HTML Reports │
            └───────┬────────┘              └────────────────┘
                    │
                    │
        ┌───────────▼───────────┐
        │   PROCESSING LAYER    │
        │                       │
        │  ┌─────────────────┐  │
        │  │  MAIN PIPELINE  │  │
        │  │  Orchestrator   │  │
        │  └────────┬────────┘  │
        │           │           │
        │  ┌────────┼────────┐  │
        │  │        │        │  │
        │  ▼        ▼        ▼  │
        │ ┌────┐  ┌────┐  ┌────┐│
        │ │EXP │  │REAL│  │GAP ││
        │ │ENG │  │ENG │  │ANAL││
        │ └────┘  └────┘  └────┘│
        └───────────────────────┘
```

## Detailed Component Architecture

```
┌──────────────────────────────────────────────────────────────────────┐
│                          EXPECTATION ENGINE                          │
│  (Promise Extractor)                                                 │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  Input: Product Documents (JSON/PDF)                                │
│    │                                                                 │
│    ├─> Text Extraction                                               │
│    │   └─> spaCy NLP Processing                                      │
│    │                                                                 │
│    ├─> Pattern Matching                                              │
│    │   ├─> Returns: "X% p.a."                                       │
│    │   ├─> Risk: "Low/Moderate/High"                                 │
│    │   ├─> Fees: "Exit load X%"                                      │
│    │   ├─> Lock-in: "X years"                                        │
│    │   └─> Features: Key benefits                                    │
│    │                                                                 │
│    └─> Confidence Scoring                                             │
│                                                                      │
│  Output: FinancialPromise (Structured Data)                         │
│    • Product Name                                                    │
│    • Promised Returns                                                │
│    • Risk Category                                                   │
│    • Key Features                                                    │
│    • Warnings                                                        │
│    • Extraction Confidence                                           │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────────────┐
│                          REALITY ENGINE                              │
│  (Sentiment Analyzer)                                                │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  Input: Customer Reviews (CSV/Social Media)                         │
│    │                                                                 │
│    ├─> Sentiment Analysis                                            │
│    │   └─> DistilBERT Model                                          │
│    │       ├─> Positive/Negative/Neutral                              │
│    │       └─> Sentiment Score (0-1)                                 │
│    │                                                                 │
│    ├─> Topic Modeling                                                │
│    │   └─> BERTopic                                                  │
│    │       └─> Complaint Categories                                  │
│    │           • Hidden Charges                                       │
│    │           • Poor Returns                                         │
│    │           • Service Issues                                       │
│    │                                                                 │
│    ├─> Metrics Calculation                                           │
│    │   ├─> Dissatisfaction Index                                     │
│    │   ├─> Sentiment Trend                                            │
│    │   └─> Risk Score                                                │
│    │                                                                 │
│    └─> Financial Keyword Detection                                   │
│                                                                      │
│  Output: SentimentResult                                             │
│    • Average Sentiment                                               │
│    • Dissatisfaction Index                                           │
│    • Top Complaints                                                  │
│    • Sentiment Trend                                                 │
│    • Risk Score                                                      │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────────────┐
│                          GAP ANALYZER                                │
│  (Gap Detector)                                                      │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  Input: Promise Data + Sentiment Data                                │
│    │                                                                 │
│    ├─> Mismatch Detection                                            │
│    │   ├─> Returns Mismatch                                          │
│    │   │   Promise: "12% returns"                                     │
│    │   │   Reality: "Poor returns" complaints                        │
│    │   │                                                              │
│    │   ├─> Risk Mismatch                                             │
│    │   │   Promise: "Low risk"                                        │
│    │   │   Reality: "Lost money" complaints                          │
│    │   │                                                              │
│    │   ├─> Fees Mismatch                                             │
│    │   │   Promise: "No hidden charges"                               │
│    │   │   Reality: "Hidden fees" complaints                         │
│    │   │                                                              │
│    │   └─> Service Mismatch                                          │
│    │       Promise: "Good service"                                    │
│    │       Reality: "Bad service" complaints                         │
│    │                                                                 │
│    ├─> Severity Calculation                                           │
│    │   └─> Weighted scoring based on:                                │
│    │       • Mismatch frequency                                       │
│    │       • Sentiment intensity                                      │
│    │       • Aspect importance                                        │
│    │                                                                 │
│    ├─> Risk Level Assignment                                          │
│    │   └─> Low / Medium / High / Critical                            │
│    │                                                                 │
│    └─> Recommendation Generation                                      │
│                                                                      │
│  Output: GapAnalysisResult                                            │
│    • Mismatches (with evidence)                                      │
│    • Overall Risk Score                                              │
│    • Risk Level                                                      │
│    • Recommendations                                                 │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────────────┐
│                        REPORT GENERATOR                               │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  Input: Gap Analysis Results                                         │
│    │                                                                 │
│    ├─> Executive Summary                                             │
│    │   └─> Markdown Report                                           │
│    │                                                                 │
│    ├─> Interactive Dashboard                                          │
│    │   └─> HTML with Plotly Charts                                   │
│    │                                                                 │
│    ├─> Product Reports                                               │
│    │   └─> Individual Product Analysis                               │
│    │                                                                 │
│    └─> Data Exports                                                  │
│        └─> CSV Files                                                 │
│                                                                      │
│  Output: Reports & Visualizations                                    │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

## Data Flow Diagram

```
┌──────────────┐
│ Mock Data    │
│ Generator    │
└──────┬───────┘
       │
       ├─────────────────┬─────────────────┐
       │                 │                 │
       ▼                 ▼                 ▼
┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│ Product     │  │ Customer    │  │ Time Series │
│ Docs (JSON) │  │ Reviews     │  │ Data        │
└──────┬──────┘  └──────┬──────┘  └─────────────┘
       │                │
       │                │
       ▼                ▼
┌─────────────┐  ┌─────────────┐
│ Promise     │  │ Sentiment   │
│ Extractor   │  │ Analyzer    │
└──────┬──────┘  └──────┬──────┘
       │                │
       │                │
       └────────┬────────┘
                │
                ▼
         ┌─────────────┐
         │ Gap         │
         │ Detector    │
         └──────┬──────┘
                │
                ▼
         ┌─────────────┐
         │ Report      │
         │ Generator   │
         └──────┬──────┘
                │
                ├──────────┬──────────┬──────────┐
                │          │          │          │
                ▼          ▼          ▼          ▼
         ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐
         │Executive│ │Dashboard│ │ Product │ │  CSV    │
         │ Summary │ │  HTML   │ │ Reports │ │  Files  │
         └─────────┘ └─────────┘ └─────────┘ └─────────┘
```

## Technology Stack Diagram

```
┌─────────────────────────────────────────────────────────┐
│                    FRONTEND LAYER                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │  Streamlit   │  │    Plotly    │  │   HTML/CSS   │   │
│  │   Dashboard  │  │  Charts      │  │   Reports    │   │
│  └──────────────┘  └──────────────┘  └──────────────┘   │
└─────────────────────────────────────────────────────────┘
                            │
┌─────────────────────────────────────────────────────────┐
│                    APPLICATION LAYER                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │   Main       │  │  Promise     │  │  Sentiment   │   │
│  │  Pipeline    │  │  Extractor   │  │  Analyzer    │   │
│  └──────────────┘  └──────────────┘  └──────────────┘   │
│  ┌──────────────┐  ┌──────────────┐                     │
│  │   Gap         │  │  Report      │                     │
│  │  Detector     │  │  Generator   │                     │
│  └──────────────┘  └──────────────┘                     │
└─────────────────────────────────────────────────────────┘
                            │
┌─────────────────────────────────────────────────────────┐
│                      ML/AI LAYER                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │ Transformers │  │    spaCy     │  │  BERTopic    │   │
│  │ (DistilBERT) │  │   NLP        │  │  Topic Model │   │
│  └──────────────┘  └──────────────┘  └──────────────┘   │
│  ┌──────────────┐  ┌──────────────┐                     │
│  │  Sentence    │  │   Regex      │                     │
│  │ Transformers │  │  Patterns    │                     │
│  └──────────────┘  └──────────────┘                     │
└─────────────────────────────────────────────────────────┘
                            │
┌─────────────────────────────────────────────────────────┐
│                      DATA LAYER                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │   CSV Files  │  │  JSON Docs   │  │  Mock Data   │   │
│  └──────────────┘  └──────────────┘  └──────────────┘   │
└─────────────────────────────────────────────────────────┘
```

## Component Interaction Sequence

```
User/System
    │
    ├─> Generate Mock Data
    │   └─> mock_data_generator.py
    │
    ├─> Run Pipeline
    │   └─> main_pipeline.py
    │       │
    │       ├─> Step 1: Extract Promises
    │       │   └─> promise_extractor.py
    │       │       └─> Save: extracted_promises.csv
    │       │
    │       ├─> Step 2: Analyze Sentiment
    │       │   └─> sentiment_analyzer.py
    │       │       └─> Save: sentiment_analysis.csv
    │       │
    │       ├─> Step 3: Detect Gaps
    │       │   └─> gap_detector.py
    │       │       └─> Save: gap_analysis.csv
    │       │
    │       └─> Step 4: Generate Reports
    │           └─> Report Generator
    │               ├─> executive_summary.md
    │               ├─> interactive_dashboard.html
    │               └─> product_reports/*.md
    │
    └─> View Dashboard
        └─> streamlit run dashboard.py
            └─> Load processed data
                └─> Display visualizations
```

## Future Architecture (Proposed)

```
┌─────────────────────────────────────────────────────────────┐
│                    API GATEWAY                              │
│  (FastAPI + Authentication)                                 │
└──────────────────────┬──────────────────────────────────────┘
                       │
        ┌──────────────┼──────────────┐
        │              │              │
        ▼              ▼              ▼
┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│ Expectation │ │  Reality    │ │    Gap      │
│   Service   │ │   Service   │ │   Service   │
└──────┬──────┘ └──────┬──────┘ └──────┬──────┘
       │              │              │
       └──────────────┼──────────────┘
                      │
                      ▼
            ┌─────────────────┐
            │   Database      │
            │  (PostgreSQL)   │
            └─────────────────┘
                      │
        ┌─────────────┼─────────────┐
        │             │             │
        ▼             ▼             ▼
┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│   Redis     │ │   S3/Blob   │ │   Message   │
│   Cache     │ │   Storage   │ │    Queue    │
└─────────────┘ └─────────────┘ └─────────────┘
```

---

*Architecture Version: 1.0*
*Last Updated: 2025-01-12*


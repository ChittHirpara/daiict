# VERITAS Finance - AI-Powered Mis-Selling Detection System

## Overview

VERITAS Finance is an AI-powered system that automatically detects financial mis-selling by comparing marketing promises with actual customer experiences. The system helps regulators identify products that may be misleading customers before significant losses occur.

## How It Works

### Three-Engine Architecture

1. **Expectation Engine**
   - Extracts promises from product marketing documents (PDFs, brochures)
   - Identifies: returns, risk levels, fees, lock-in periods, features
   - Uses NLP and pattern recognition to extract structured data

2. **Reality Engine**
   - Analyzes customer sentiment from reviews, social media, complaints
   - Calculates dissatisfaction index
   - Identifies complaint topics and trends

3. **Gap Analyzer**
   - Compares promises vs reality
   - Detects mismatches and contradictions
   - Calculates risk scores (0-1 scale)
   - Generates alerts for high-risk products

### Workflow

```
Product Documents → Expectation Engine → Extracted Promises
                                                      ↓
Customer Reviews → Reality Engine → Sentiment Analysis
                                                      ↓
                                    Gap Analyzer → Risk Scores & Alerts
                                                      ↓
                                    Dashboard → Regulatory Action
```

## Quick Start

### Prerequisites
- Python 3.8+
- pip package manager

### Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Generate sample data:
```bash
python mock_data_generator.py
```

3. Run the analysis pipeline:
```bash
python main_pipeline.py
```

4. Launch the dashboard:
```bash
streamlit run dashboard.py
```

Or use the one-click launcher:
```bash
# Windows
launch.bat

# Mac/Linux
./launch.sh
```

5. Open browser to: http://localhost:8501

## Project Structure

```
daiict/
├── dashboard.py              # Main Streamlit dashboard
├── main_pipeline.py          # Complete AI analysis pipeline
├── presentation_mode.py      # Hackathon presentation mode
├── mock_data_generator.py    # Generate sample data
├── config.py                # Configuration settings
├── backend/
│   ├── expectation_engine/  # Promise extraction
│   ├── reality_engine/      # Sentiment analysis
│   └── gap_analyzer/        # Gap detection
├── data/
│   ├── mock/               # Sample product documents
│   └── processed/          # Analysis results (CSV)
└── reports/                # Generated reports
```

## Key Features

- **Real-time Monitoring**: Dashboard shows live risk scores and alerts
- **AI-Powered Analysis**: Uses BERT, Transformers, and NLP models
- **Multi-Source Data**: Integrates reviews, social media, complaints
- **Risk Scoring**: Automatic calculation of mis-selling risk (0-1 scale)
- **Evidence Generation**: Creates regulator-ready reports with proof

## Dashboard Pages

1. **Overview**: KPIs, risk distribution, top alerts
2. **Products Monitor**: List of all products with risk levels
3. **Expectation Engine**: View extracted promises from documents
4. **Reality Engine**: Customer sentiment analysis results
5. **Risk Flags**: Detailed mismatch analysis and evidence
6. **Reports & Evidence**: Generate regulatory reports

## Technology Stack

- **Frontend**: Streamlit, Plotly
- **Backend**: Python, FastAPI
- **AI/ML**: Transformers, spaCy, BERTopic, SentenceTransformers
- **Data Processing**: Pandas, NumPy
- **Visualization**: Plotly charts

## Usage Example

1. Upload a product document (PDF/brochure) in "Expectation Engine"
2. System extracts promises automatically
3. Customer reviews are analyzed in "Reality Engine"
4. "Risk Flags" page shows detected mismatches
5. Generate evidence report for regulatory action

## Output

The system generates:
- Risk scores for each product (0-1 scale)
- Mismatch details (what was promised vs reality)
- Evidence packages (PDF reports)
- Alerts for high-risk products

## Support

For issues or questions, check the error messages in the dashboard or review the code comments in each module.

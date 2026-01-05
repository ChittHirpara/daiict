# 📋 Quick Reference Guide - Veritas Finance

## 🚀 Quick Start

```bash
# 1. Generate mock data
python mock_data_generator.py

# 2. Run full pipeline
python main_pipeline.py

# 3. Launch dashboard
streamlit run dashboard.py
```

## 📁 Key Files & Their Purpose

| File | Purpose | Status |
|------|---------|--------|
| `main_pipeline.py` | Main orchestrator - runs all components | ✅ Core |
| `promise_extractor.py` | Extracts promises from product docs | ✅ Working |
| `sentiment_analyzer.py` | Analyzes customer sentiment | ✅ Working |
| `gap_detector.py` | Detects mismatches between promise & reality | ✅ Working |
| `dashboard.py` | Streamlit UI for visualization | ✅ Working |
| `mock_data_generator.py` | Generates sample data | ✅ Working |
| `config.py` | Configuration settings | ✅ Working |

## 🔧 Component Details

### 1. Expectation Engine
**File**: `backend/expectation_engine/promise_extractor.py`

**What it does:**
- Extracts financial promises from product documents
- Identifies: returns, risk, fees, lock-in periods, features

**Key Methods:**
- `extract_from_text()` - Extract from raw text
- `extract_from_json()` - Extract from JSON (simulating PDF)
- `batch_extract()` - Process multiple documents

**Output**: `FinancialPromise` dataclass with extracted fields

### 2. Reality Engine
**File**: `backend/reality_engine/sentiment_analyzer.py`

**What it does:**
- Analyzes customer reviews/complaints
- Calculates dissatisfaction index
- Identifies top complaint topics
- Tracks sentiment trends over time

**Key Methods:**
- `analyze_sentiment()` - Single text sentiment
- `batch_analyze()` - Process multiple reviews
- `analyze_product_sentiment()` - Complete product analysis
- `detect_complaint_topics()` - Topic modeling for complaints

**Output**: `SentimentResult` dataclass with metrics

### 3. Gap Analyzer
**File**: `backend/gap_analyzer/gap_detector.py`

**What it does:**
- Compares promises vs reality
- Detects mismatches with severity scoring
- Generates risk levels and recommendations

**Key Methods:**
- `detect_mismatches()` - Find contradictions
- `analyze_gap()` - Complete gap analysis
- `calculate_risk_score()` - Overall risk calculation

**Output**: `GapAnalysisResult` with mismatches and recommendations

## 📊 Data Flow

```
1. Mock Data Generation
   └─> Product Docs (JSON)
   └─> Customer Reviews (CSV)

2. Promise Extraction
   └─> Product Docs → Promise Extractor → Extracted Promises (CSV)

3. Sentiment Analysis
   └─> Customer Reviews → Sentiment Analyzer → Sentiment Results (CSV)

4. Gap Detection
   └─> Promises + Sentiment → Gap Detector → Gap Analysis (CSV)

5. Report Generation
   └─> Gap Analysis → Report Generator → HTML/Markdown Reports
```

## 🎯 Key Metrics Explained

### Dissatisfaction Index
- **Formula**: (Negative Reviews / Total Reviews) × 100
- **Range**: 0-100%
- **Interpretation**: Higher = more dissatisfied customers

### Risk Score
- **Formula**: Weighted average of mismatch severities + dissatisfaction
- **Range**: 0.0 - 1.0
- **Interpretation**: 
  - 0.0-0.3: Low Risk
  - 0.3-0.6: Medium Risk
  - 0.6-0.8: High Risk
  - 0.8-1.0: Critical Risk

### Extraction Confidence
- **Formula**: Sum of confidence factors (objective, returns, risk, features, warnings)
- **Range**: 0.0 - 1.0
- **Interpretation**: Higher = more reliable promise extraction

## 🐛 Common Issues & Solutions

### Issue: Models not loading
**Solution**: 
```bash
python -m spacy download en_core_web_sm
pip install transformers torch
```

### Issue: Memory errors
**Solution**: Reduce batch size in `sentiment_analyzer.py`

### Issue: CSV file not found
**Solution**: Run `mock_data_generator.py` first

### Issue: Dashboard shows no data
**Solution**: Ensure `main_pipeline.py` has run successfully

## 🔍 Debugging Tips

1. **Check Data Files**: Verify CSV files exist in `data/processed/`
2. **Check Logs**: Look for error messages in console output
3. **Test Components**: Run individual components separately
4. **Validate Input**: Ensure mock data is properly formatted

## 📈 Performance Benchmarks

| Operation | Time (approx) | Notes |
|-----------|---------------|-------|
| Promise Extraction (1 doc) | < 1 sec | Fast |
| Sentiment Analysis (100 reviews) | 10-30 sec | Depends on model loading |
| Gap Detection (1 product) | < 1 sec | Fast |
| Full Pipeline (5 products) | 1-2 min | Includes model loading |

## 🎨 Dashboard Features

### Main Dashboard
- Product overview metrics
- Risk distribution charts
- Recent alerts

### Product Analysis
- Promise vs Reality comparison
- Detailed mismatch breakdown
- Recommendations

### Risk Alerts
- High-risk product list
- Alert details and actions
- Risk level color coding

### Insights
- Sentiment trends over time
- Common mismatch patterns
- Regulatory impact estimates

## 🔐 Configuration

**File**: `config.py`

**Key Settings:**
- `RISK_THRESHOLD`: 0.7 (default)
- `MIN_COMPLAINTS`: 5 (minimum for analysis)
- `SENTIMENT_MODEL`: DistilBERT (default)

## 📝 Output Files

### Generated Reports
- `reports/executive_summary.md` - Overall summary
- `reports/interactive_dashboard.html` - Interactive charts
- `reports/product_reports/*.md` - Individual product reports

### Processed Data
- `data/processed/extracted_promises.csv` - Extracted promises
- `data/processed/sentiment_analysis.csv` - Sentiment results
- `data/processed/gap_analysis.csv` - Gap analysis results

## 🚨 Alert Thresholds

| Risk Level | Score Range | Action Required |
|------------|-------------|-----------------|
| Low | 0.0 - 0.3 | Monitor |
| Medium | 0.3 - 0.6 | Review |
| High | 0.6 - 0.8 | Investigate |
| Critical | 0.8 - 1.0 | Immediate Action |

## 💡 Best Practices

1. **Run Pipeline Regularly**: Set up scheduled runs for continuous monitoring
2. **Review Recommendations**: Always check generated recommendations
3. **Validate Results**: Cross-check high-risk products manually
4. **Update Models**: Periodically retrain models on new data
5. **Monitor Performance**: Track accuracy and false positive rates

## 🔗 Integration Points

### Future Integrations
- Twitter API (for real-time social media data)
- Reddit API (for discussion forums)
- Play Store API (for app reviews)
- Regulatory databases (for compliance checking)

## 📞 Support

For issues or questions:
1. Check `DEEP_ANALYSIS.md` for detailed analysis
2. Review code comments in source files
3. Check `JUDGES_README.md` for hackathon-specific info

---

*Last Updated: 2025-01-12*


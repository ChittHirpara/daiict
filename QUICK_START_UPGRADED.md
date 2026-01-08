# 🚀 QUICK START - Upgraded Veritas Finance

## 🎉 What's New (Major Upgrades)

Your project now has:
- ✅ **PostgreSQL Database** (with SQLite fallback)
- ✅ **Real API Integrations** (Twitter, Reddit, News APIs)
- ✅ **FastAPI REST Backend** (production-ready)
- ✅ **Database Manager** (easy data operations)
- ✅ **Professional Architecture** (scalable & maintainable)

---

## ⚡ Quick Setup (5 Minutes)

### Step 1: Install Upgraded Dependencies
```bash
pip install -r requirements_upgraded.txt
```

### Step 2: Setup Database
```bash
python setup_database.py
```
This creates the database schema (uses SQLite by default if PostgreSQL not available).

### Step 3: (Optional) Configure API Keys
Create a `.env` file in project root:
```env
# Database (Optional - uses SQLite if not set)
DATABASE_URL=postgresql://user:pass@localhost:5432/veritas_finance

# API Keys (Optional - uses mock data if not set)
TWITTER_BEARER_TOKEN=your_token_here
REDDIT_CLIENT_ID=your_id_here
REDDIT_CLIENT_SECRET=your_secret_here
NEWS_API_KEY=your_key_here
```

### Step 4: Start FastAPI Backend
```bash
cd api
python main.py
```
Or with uvicorn:
```bash
uvicorn api.main:app --reload
```

### Step 5: Access API Documentation
Open browser: **http://localhost:8000/docs**

You'll see interactive API documentation (Swagger UI)!

---

## 📚 How to Use the New Features

### Using Database Manager

```python
from database.db_manager import DatabaseManager

# Create manager
db = DatabaseManager()

# Get or create product
product = db.get_or_create_product(
    name="Alpha Growth MF",
    issuer="ABC Mutual Fund",
    category="Mutual Fund"
)

# Save promise extraction
promise_data = {
    'promised_returns': '15%',
    'risk_category': 'Low',
    'extraction_confidence': 0.95
}
db.save_promise(product.id, promise_data)

# Save reviews
reviews = [
    {
        'review_text': 'Very bad returns!',
        'source': 'twitter',
        'sentiment_score': -0.8
    }
]
db.save_reviews(product.id, reviews)

# Get statistics
stats = db.get_statistics()
print(f"Total products: {stats['total_products']}")

db.close()
```

### Using Real API Data Sources

```python
from backend.data_sources.api_client import DataSourceAggregator

# Create aggregator
aggregator = DataSourceAggregator()

# Check which APIs are configured
status = aggregator.get_status()
print(status)  # {'twitter': True, 'reddit': False, 'news': False}

# Fetch data from all sources
data = aggregator.fetch_all_sources("Alpha Growth Mutual Fund", max_per_source=50)
print(f"Fetched {len(data)} items")
```

### Using FastAPI Endpoints

#### Create Product:
```bash
curl -X POST "http://localhost:8000/api/v1/products" \
  -H "Content-Type: application/json" \
  -d '{"name": "Alpha Growth MF", "issuer": "ABC Fund"}'
```

#### Get All Products:
```bash
curl "http://localhost:8000/api/v1/products"
```

#### Fetch External Data:
```bash
curl -X POST "http://localhost:8000/api/v1/products/1/fetch-data"
```

#### Get Risk Analysis:
```bash
curl "http://localhost:8000/api/v1/products/1/risk"
```

---

## 🔄 Migrating from Old System

### Old Way (CSV Files):
```python
# Old: Save to CSV
df.to_csv("data/processed/gap_analysis.csv")
```

### New Way (Database):
```python
# New: Save to database
from database.db_manager import DatabaseManager
db = DatabaseManager()

gap_data = {
    'overall_risk_score': 0.85,
    'risk_level': 'high',
    'mismatches': [...]
}
db.save_gap_analysis(product_id, gap_data)
```

---

## 📊 API Endpoints Available

### Health & Status
- `GET /` - Root
- `GET /health` - Health check
- `GET /status` - System status

### Products
- `POST /api/v1/products` - Create product
- `GET /api/v1/products` - List all products
- `GET /api/v1/products/{id}` - Get product details

### Analysis
- `POST /api/v1/products/{id}/promise` - Save promise extraction
- `POST /api/v1/products/{id}/reviews` - Save reviews
- `GET /api/v1/products/{id}/risk` - Get risk analysis

### Data
- `POST /api/v1/products/{id}/fetch-data` - Fetch from APIs

### Alerts
- `GET /api/v1/alerts` - Get alerts

### Statistics
- `GET /api/v1/statistics` - Overall statistics
- `GET /api/v1/risk/products` - High-risk products

---

## 🎯 Next Steps

1. **Update your pipeline**: Modify `main_pipeline.py` to use database
2. **Test API**: Try endpoints in Swagger UI at `/docs`
3. **Add API keys**: Get real data from Twitter/Reddit
4. **Deploy**: Use Docker for production deployment

---

## 💡 Tips

- **No API keys?** System automatically uses mock data
- **No PostgreSQL?** System automatically uses SQLite
- **Need help?** Check API docs at `/docs` endpoint
- **Database issues?** Run `python setup_database.py --reset` to reset

---

**Your project is now production-ready! 🎉**

# 🆓 Free API Setup (Optional)

## ⚠️ **IMPORTANT: You Don't Need This!**

Your project **works perfectly with mock data** (100% free).  
This guide is **optional** if you want real data.

---

## 🟢 **Option 1: Reddit API (FREE)**

### Why Reddit?
- ✅ Completely free
- ✅ No rate limits (60/min is plenty)
- ✅ Easy setup

### Setup Steps:

1. **Create Reddit App** (Free):
   - Go to: https://www.reddit.com/prefs/apps
   - Scroll down, click "create another app"
   - Fill in:
     - Name: "Veritas Finance"
     - App type: "script"
     - Description: "Financial mis-selling detection"
     - About URL: (optional)
     - Redirect URI: `http://localhost:8080`
   - Click "create app"

2. **Get Credentials:**
   - You'll see:
     - **Client ID** (under app name)
     - **Secret** (click "secret")

3. **Add to Environment:**
   ```bash
   # Windows PowerShell
   $env:REDDIT_CLIENT_ID="your_client_id_here"
   $env:REDDIT_CLIENT_SECRET="your_secret_here"
   
   # Or create .env file:
   REDDIT_CLIENT_ID=your_client_id_here
   REDDIT_CLIENT_SECRET=your_secret_here
   ```

**That's it! Reddit API is now active (FREE).**

---

## 🟡 **Option 2: News API (Free Tier)**

### Why News API?
- ✅ Free tier: 100 requests/day
- ✅ Enough for demo
- ✅ Easy setup

### Setup Steps:

1. **Get Free API Key:**
   - Visit: https://newsapi.org/register
   - Sign up (free)
   - Get API key instantly

2. **Add to Environment:**
   ```bash
   $env:NEWS_API_KEY="your_api_key_here"
   
   # Or in .env:
   NEWS_API_KEY=your_api_key_here
   ```

**Limit:** 100 requests/day (free tier)

---

## ❌ **Skip Twitter API**

**Why Skip?**
- ❌ Twitter API v2 is **$100+/month**
- ✅ Mock data works perfectly
- ✅ No need for real Twitter data in demo

**Recommendation:** Use mock data for Twitter.

---

## 🎯 **Recommended: Mock Data Only**

**Best for Hackathon:**
- ✅ No setup
- ✅ No costs
- ✅ Works perfectly
- ✅ Professional demo

**You're already configured correctly!**

---

## ✅ **Check API Status**

Run this to see which APIs are active:

```python
from backend.data_sources.api_client import DataSourceAggregator

aggregator = DataSourceAggregator()
print(aggregator.get_status())
```

Output:
```
{
    'twitter': False,  # Using mock (free)
    'reddit': False,   # Using mock (free)
    'news': False      # Using mock (free)
}
```

**All False = All using mock data (100% free!)** ✅

---

## 💰 **Cost Summary**

| Setup | Cost | Status |
|-------|------|--------|
| **Mock Data Only** | **$0** | ✅ Recommended |
| Reddit API | $0 | Optional |
| News API Free | $0 | Optional |
| Twitter API | $100+/mo | ❌ Skip |

**Recommendation: Use mock data (already working)!** 🎉

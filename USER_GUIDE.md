# 📖 VERITAS Command Center - Complete User Guide

## 🎯 **What This Project Does (In Simple Terms)**

**Problem:** Financial companies sometimes lie or mislead customers about their products.

**Solution:** Our system automatically:
1. Reads what companies **promise** (from marketing documents)
2. Reads what customers **actually experience** (from reviews, social media)
3. **Compares** them to find mismatches
4. **Alerts** regulators if something looks wrong

**Think of it as:** A watchdog that automatically catches financial scams before customers lose money!

---

## 🚀 **Quick Start (3 Steps)**

### Step 1: Setup (One Time)
```bash
# Install dependencies
pip install -r requirements_upgraded.txt

# Setup database
python setup_database.py

# Generate sample data
python mock_data_generator.py
```

### Step 2: Run Pipeline (Analyze Products)
```bash
# This analyzes products and finds mis-selling
python main_pipeline_upgraded.py
```

### Step 3: Open Dashboard
```bash
# Start dashboard
streamlit run dashboard.py

# Open in browser: http://localhost:8501
```

---

## 📊 **Complete User Workflow**

### **Scenario: You're a Financial Regulator**

You want to monitor financial products to catch mis-selling. Here's how you use the system:

---

## 🎬 **STEP-BY-STEP WORKFLOW**

### **1. Dashboard Overview Page**

**What you see:**
- **KPI Cards:** 
  - How many products are being monitored
  - How many have high risk
  - Average risk score
  - Customer dissatisfaction level

**What you do:**
- Just look at the numbers
- See if anything looks concerning (high risk products)

**Example:**
```
Products Monitored: 5
High-Risk Products: 2  ← Uh oh! Something needs attention
Average Risk Score: 0.65
Dissatisfaction: 45%
```

---

### **2. Products Monitor Page**

**What you see:**
- List of all financial products being monitored
- Risk level for each product (Low/Medium/High/Critical)
- Risk scores

**What you do:**
1. Browse through products
2. Click on a high-risk product to see details
3. Filter by risk level if needed

**Example:**
```
Alpha Growth Mutual Fund
├─ Risk Level: HIGH
├─ Risk Score: 0.78
├─ Promise Confidence: 85%
└─ Sentiment Score: -0.45 (negative!)

SecureLife Insurance
├─ Risk Level: LOW
├─ Risk Score: 0.25
├─ Promise Confidence: 92%
└─ Sentiment Score: 0.32 (positive)
```

---

### **3. Expectation Engine Page**

**What it does:**
- Shows what the company **PROMISED** customers
- Extracted from marketing documents/PDFs

**What you see:**
- Investment objective
- Promised returns (e.g., "12% per year")
- Risk category (e.g., "Low Risk")
- Lock-in period
- Exit load/fees
- Key features

**What you learn:**
- What the product claimed to offer
- How confident we are about the extraction

**Example:**
```
Product: Alpha Growth Mutual Fund

PROMISED:
├─ Returns: 15% per annum
├─ Risk: Low
├─ Lock-in: 3 years
├─ Min Investment: ₹5,000
└─ Confidence: 85% (high confidence)
```

---

### **4. Reality Engine Page**

**What it does:**
- Shows what customers **ACTUALLY EXPERIENCED**
- Analyzes reviews, tweets, Reddit posts

**What you see:**
- Average sentiment (positive/negative)
- Total reviews analyzed
- Positive vs Negative count
- Dissatisfaction index
- Risk score based on complaints

**What you learn:**
- Are customers happy?
- What are they complaining about?
- How many are dissatisfied?

**Example:**
```
Product: Alpha Growth Mutual Fund

CUSTOMER REALITY:
├─ Average Sentiment: -0.45 (NEGATIVE!)
├─ Total Reviews: 1,234
├─ Positive: 123 (10%)
├─ Negative: 876 (71%)
├─ Dissatisfaction: 78%
└─ Risk Score: 0.82 (HIGH RISK)
```

---

### **5. Risk Intelligence Page** ⚠️ **MOST IMPORTANT!**

**What it does:**
- **Compares** what was promised vs reality
- **Detects mismatches** (gaps)
- **Calculates risk scores**
- **Shows evidence**

**What you see:**
- Overall risk score (0-1, higher = more risky)
- Risk level (Low/Medium/High/Critical)
- **Detected mismatches** (the problems!)
- Specific evidence for each mismatch

**What you learn:**
- **Is this product mis-selling?**
- **What specific promises were broken?**
- **How severe is the problem?**

**Example:**
```
Product: Alpha Growth Mutual Fund

RISK ANALYSIS:
├─ Overall Risk Score: 0.78 (HIGH)
├─ Risk Level: HIGH
│
├─ DETECTED MISMATCHES:
│   ├─ 1. Returns Promise Broken
│   │   ├─ Promised: 15% returns
│   │   ├─ Reality: Customers report 3% or losses
│   │   └─ Evidence: 456 complaints about poor returns
│   │
│   ├─ 2. Risk Category Misleading
│   │   ├─ Promised: Low Risk
│   │   ├─ Reality: High volatility reported
│   │   └─ Evidence: 234 complaints about market crashes
│   │
│   └─ 3. Hidden Charges
│       ├─ Promised: No hidden fees
│       ├─ Reality: Unexpected charges deducted
│       └─ Evidence: 189 complaints about fees
│
└─ RECOMMENDATION: Investigate immediately!
```

---

### **6. Evidence Vault Page**

**What it does:**
- Stores **immutable evidence** for each product
- Shows proof of mismatches
- Ready for regulatory investigation

**What you see:**
- Evidence ID for each product
- Promise extraction evidence
- Sentiment analysis evidence
- Gap analysis evidence
- All stored securely

**What you learn:**
- **Proof** for regulatory action
- **Evidence trail** that can't be disputed
- **Complete audit trail**

---

### **7. System Controls Page**

**What it does:**
- Shows data source status
- Configuration panel
- System health

**What you see:**
- Signal nodes (Twitter, Reddit, News)
- Signal strength
- Data freshness
- System status

**What you do:**
- Monitor if data sources are working
- Check system health

---

## 🎯 **Real-World Example Workflow**

### **Scenario: Monitoring a New Financial Product**

**Day 1: Setup**
1. You upload product documents (PDFs)
2. System extracts promises automatically
3. System starts monitoring social media

**Day 2-7: Monitoring**
1. System collects customer reviews daily
2. Analyzes sentiment
3. Compares with promises

**Day 8: Alert!**
1. Dashboard shows **HIGH RISK** alert
2. You click on the product
3. See mismatch: "Promised 15% returns, customers getting 3%"
4. Evidence shows 456 complaints
5. You investigate further

**Day 9: Action**
1. You use Evidence Vault to get proof
2. Generate regulatory report
3. Take action against the company

---

## 📋 **How to Use Each Feature**

### **Feature 1: Monitor Products**

**How:**
1. Products appear automatically after running pipeline
2. View in "Products Monitor" page
3. Filter by risk level if needed

**When to use:**
- Check which products need attention
- Find high-risk products quickly

---

### **Feature 2: Analyze Promises**

**How:**
1. Go to "Expectation Engine" page
2. See extracted promises for each product
3. Check confidence scores

**When to use:**
- Understand what was promised
- Verify promise extraction accuracy

---

### **Feature 3: Analyze Customer Sentiment**

**How:**
1. Go to "Reality Engine" page
2. See sentiment analysis results
3. Check dissatisfaction levels

**When to use:**
- Understand customer experience
- Find unhappy customers
- Identify complaint trends

---

### **Feature 4: Detect Mis-selling** ⭐ **MAIN FEATURE**

**How:**
1. Go to "Risk Intelligence" page
2. See risk scores for each product
3. Review detected mismatches
4. Check evidence

**When to use:**
- **This is the main feature!**
- Find which products are mis-selling
- Get specific evidence
- Decide on regulatory action

---

### **Feature 5: Get Evidence**

**How:**
1. Go to "Evidence Vault" page
2. Select a product
3. View all collected evidence
4. Export if needed

**When to use:**
- Need proof for investigation
- Building case against company
- Regulatory reporting

---

## 🎯 **Complete User Journey**

### **As a New User:**

**First Time:**
1. **Setup:** Run `setup_database.py` and `mock_data_generator.py`
2. **Generate Data:** Run `main_pipeline_upgraded.py`
3. **View Dashboard:** Open dashboard at http://localhost:8501

**Regular Use:**
1. **Check Dashboard:** See overview of all products
2. **Review Alerts:** Check high-risk products
3. **Investigate:** Click on risky products
4. **Analyze:** Review mismatches and evidence
5. **Take Action:** Use evidence for regulatory action

---

## 💡 **Key Features Explained**

### **1. Automatic Promise Extraction**
- **What:** Reads PDFs/marketing docs
- **Finds:** Returns, risks, fees, lock-in periods
- **How:** Uses AI (NLP) to extract information
- **Why:** Saves time vs manual reading

### **2. Sentiment Analysis**
- **What:** Analyzes customer reviews/complaints
- **Finds:** Positive, negative, neutral sentiment
- **How:** Uses AI to understand emotions
- **Why:** Understands customer experience automatically

### **3. Gap Detection**
- **What:** Compares promises vs reality
- **Finds:** Mismatches, contradictions
- **How:** Uses rules + AI to detect gaps
- **Why:** **This is the core feature - finds mis-selling!**

### **4. Risk Scoring**
- **What:** Calculates risk level (0-1)
- **Finds:** How risky is this product?
- **How:** Based on mismatches, complaints, sentiment
- **Why:** Prioritizes which products need attention

---

## 🎬 **Example: Complete Workflow**

### **Step 1: Start System**
```bash
python setup_database.py
python mock_data_generator.py
python main_pipeline_upgraded.py
streamlit run dashboard.py
```

### **Step 2: View Dashboard**
- Open http://localhost:8501
- See: "5 Products Monitored, 2 High Risk"

### **Step 3: Check High-Risk Product**
- Click "Products Monitor"
- See "Alpha Growth MF - HIGH RISK"
- Click on it

### **Step 4: See What Was Promised**
- Go to "Expectation Engine"
- See: "Promised 15% returns, Low Risk"

### **Step 5: See Customer Reality**
- Go to "Reality Engine"
- See: "78% dissatisfied, negative sentiment"

### **Step 6: View Mismatches** ⭐
- Go to "Risk Intelligence"
- See: "Returns Mismatch - Promised 15%, Got 3%"
- See evidence: "456 complaints"

### **Step 7: Get Evidence**
- Go to "Evidence Vault"
- Download evidence for investigation

---

## 🎯 **What This Solves**

### **Problem Before:**
- Regulators manually read thousands of complaints
- Takes 11 months to detect mis-selling
- Companies already scammed customers

### **Solution Now:**
- Automatic detection in 48 hours
- Catches problems before they explode
- Protects customers proactively

---

## 📊 **Dashboard Pages Summary**

| Page | What It Shows | When to Use |
|------|---------------|-------------|
| **Overview** | KPIs, summary | Check overall status |
| **Products Monitor** | List of products | Browse all products |
| **Expectation Engine** | What was promised | See marketing claims |
| **Reality Engine** | Customer experience | See complaints/sentiment |
| **Risk Intelligence** | ⭐ **Mis-selling detection** | **Find problems!** |
| **Evidence Vault** | Proof/evidence | Get evidence for action |
| **System Controls** | Data sources status | Check system health |

---

## ✅ **Quick Reference**

**Main Goal:** Find financial products that are mis-selling

**Main Feature:** Risk Intelligence page (shows mismatches)

**How It Works:**
1. Extract promises (from documents)
2. Analyze sentiment (from reviews)
3. Detect gaps (compare them)
4. Calculate risk (how bad is it?)

**What You Do:**
1. Run pipeline (analyzes products)
2. Open dashboard (view results)
3. Check Risk Intelligence (find problems)
4. Use Evidence Vault (get proof)

---

## 🎯 **Bottom Line**

**This system helps you:**
- ✅ Automatically find mis-selling
- ✅ Save time (automatic vs manual)
- ✅ Protect customers (catch scams early)
- ✅ Have evidence (for regulatory action)

**Just run the pipeline and check the dashboard!** 🚀

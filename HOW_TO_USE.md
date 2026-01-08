# 📚 How to Use VERITAS Command Center - Simple Guide

## 🎯 **What This Project Does (1 Minute Explanation)**

### **The Problem:**
Financial companies sometimes lie to customers:
- Promise: "You'll get 15% returns!"
- Reality: Customers lose money

### **The Solution:**
Our system automatically catches these lies:
1. Reads what company promised
2. Reads what customers experienced  
3. Finds the difference
4. Alerts you: "This product is mis-selling!"

---

## 🚀 **How to Use (Simple Steps)**

### **Step 1: Start the System**

```bash
# Setup (first time only)
python setup_database.py
python mock_data_generator.py

# Analyze products
python main_pipeline_upgraded.py

# Open dashboard
streamlit run dashboard.py
```

**Result:** Dashboard opens at http://localhost:8501

---

### **Step 2: Understand the Dashboard**

The dashboard has 7 pages. Here's what each does:

#### **📊 Page 1: Overview**
**What it shows:** Big numbers
- How many products you're watching
- How many have problems
- Overall risk level

**Think of it as:** Your control room overview

**Example:**
```
Products Monitored: 5
High-Risk Products: 2  ← These need attention!
```

---

#### **📦 Page 2: Products Monitor**
**What it shows:** List of all products

**What you do:** 
- See all products
- Find the risky ones
- Click to see details

**Example:**
```
✅ SecureLife Insurance - LOW RISK
⚠️ Alpha Growth MF - HIGH RISK  ← Click this!
✅ EasyInvest Savings - LOW RISK
```

---

#### **📄 Page 3: Expectation Engine**
**What it shows:** What companies **PROMISED**

**What you learn:** What the product claimed

**Example:**
```
Alpha Growth Mutual Fund PROMISED:
├─ Returns: 15% per year
├─ Risk: Low
├─ Fees: None
└─ Lock-in: 3 years
```

---

#### **😤 Page 4: Reality Engine**
**What it shows:** What customers **ACTUALLY GOT**

**What you learn:** Are customers happy?

**Example:**
```
Alpha Growth Mutual Fund REALITY:
├─ Sentiment: Negative (-0.45)
├─ Complaints: 876 negative reviews
├─ Dissatisfaction: 78%
└─ Experience: "Lost money!", "Scam!"
```

---

#### **⚠️ Page 5: Risk Intelligence** ⭐ **MOST IMPORTANT!**
**What it shows:** **THE PROBLEMS!**

**What you see:**
- Risk score (how bad is it?)
- Specific mismatches (what promises were broken)
- Evidence (proof)

**This is where you find mis-selling!**

**Example:**
```
Alpha Growth Mutual Fund - HIGH RISK (Score: 0.78)

MISMATCHES DETECTED:

1. Returns Promise Broken ❌
   Promised: 15% returns
   Reality: Only 3% or losses
   Evidence: 456 complaints

2. Risk Category False ❌
   Promised: Low risk
   Reality: High volatility
   Evidence: 234 complaints

3. Hidden Fees ❌
   Promised: No fees
   Reality: Unexpected charges
   Evidence: 189 complaints

RECOMMENDATION: Investigate immediately!
```

---

#### **🔒 Page 6: Evidence Vault**
**What it shows:** Proof/evidence for investigations

**What you use it for:** Getting evidence when you need to take action

**Example:**
```
Evidence for Alpha Growth MF:
├─ Promise Extraction: Confidence 85%
├─ Sentiment Analysis: 876 negative reviews
├─ Gap Analysis: 3 mismatches detected
└─ Risk Score: 0.78 (HIGH)
```

---

#### **⚙️ Page 7: System Controls**
**What it shows:** System status

**What you check:** Is everything working?

---

## 🎯 **Complete Usage Example**

### **Scenario: You want to check if a product is mis-selling**

**Step 1:** Open dashboard
- Go to http://localhost:8501

**Step 2:** Check Overview
- See "2 High-Risk Products"

**Step 3:** Go to Products Monitor
- See "Alpha Growth MF - HIGH RISK"
- Click on it

**Step 4:** Check what was promised
- Go to "Expectation Engine"
- See: "Promised 15% returns, Low Risk"

**Step 5:** Check customer experience
- Go to "Reality Engine"  
- See: "78% dissatisfied, negative sentiment"

**Step 6:** Find the problems ⭐
- Go to "Risk Intelligence"
- See: "3 mismatches detected"
- Read: "Returns promise broken - Promised 15%, got 3%"
- See evidence: "456 complaints"

**Step 7:** Get evidence
- Go to "Evidence Vault"
- Download evidence for your investigation

**Step 8:** Take action
- Use evidence to investigate the company

---

## 💡 **What Each Feature Does**

### **Feature 1: Automatic Promise Extraction**
- **Reads:** PDF documents, marketing materials
- **Finds:** What companies promised (returns, risk, fees)
- **Why useful:** Saves you from reading hundreds of pages

### **Feature 2: Sentiment Analysis**
- **Reads:** Customer reviews, tweets, Reddit posts
- **Finds:** Are customers happy or complaining?
- **Why useful:** Understands customer experience automatically

### **Feature 3: Gap Detection** ⭐ **MAIN FEATURE**
- **Does:** Compares promises vs reality
- **Finds:** Mismatches, broken promises
- **Why useful:** **This finds mis-selling automatically!**

### **Feature 4: Risk Scoring**
- **Does:** Calculates how risky a product is
- **Finds:** Which products need immediate attention
- **Why useful:** Prioritizes your work

---

## 📋 **Daily Workflow**

### **Morning Routine:**

1. **Open Dashboard**
   - Check Overview page
   - See how many products monitored
   - Check for new alerts

2. **Review Alerts**
   - Go to Products Monitor
   - Check high-risk products
   - Prioritize which to investigate

3. **Investigate**
   - Click on high-risk product
   - Review Risk Intelligence
   - Check mismatches and evidence

4. **Take Action**
   - If strong evidence, get from Evidence Vault
   - Generate report
   - Start investigation

---

## ✅ **Quick Reference**

| What You Want | Where to Go | What You'll Find |
|---------------|-------------|------------------|
| **Overall status** | Overview | Summary numbers |
| **List of products** | Products Monitor | All products with risk levels |
| **What was promised** | Expectation Engine | Company claims |
| **Customer experience** | Reality Engine | Reviews, sentiment |
| **⭐ Find mis-selling** | **Risk Intelligence** | **Mismatches, problems** |
| **Get evidence** | Evidence Vault | Proof for action |
| **Check system** | System Controls | Status, health |

---

## 🎯 **Main Goal**

**Find financial products that are mis-selling customers.**

**Main page to use:** **Risk Intelligence** - shows all problems!

---

## 🚀 **Start Using Now**

1. Run the setup commands above
2. Open dashboard
3. Go to "Risk Intelligence" page
4. See which products have problems

**That's it! You're using the system!** 🎉

---

## 📖 **Need More Details?**

- **Complete guide:** `USER_GUIDE.md`
- **Quick start:** `QUICK_START_USER.md`
- **Workflow:** `PROJECT_WORKFLOW.md`

**Start with the dashboard and explore!** 🚀

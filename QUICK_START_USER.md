# 🚀 Quick Start Guide - For Users

## 🎯 **What Is This Project?**

**Simple Answer:** An AI system that catches financial scams automatically.

**How:** 
- Reads what companies promise
- Reads what customers experience
- Finds the difference (mismatches)
- Alerts you if something's wrong

---

## ⚡ **5-Minute Quick Start**

### **Step 1: Setup (One Time)**
```bash
pip install -r requirements_upgraded.txt
python setup_database.py
python mock_data_generator.py
```

### **Step 2: Analyze Products**
```bash
python main_pipeline_upgraded.py
```
**What this does:** Analyzes products and finds mis-selling

### **Step 3: Open Dashboard**
```bash
streamlit run dashboard.py
```
**Then open:** http://localhost:8501

---

## 📱 **Using the Dashboard**

### **Page 1: Overview**
**What you see:** Summary numbers
- How many products monitored
- How many are risky
- Average risk score

**What to do:** Check if anything needs attention

---

### **Page 2: Products Monitor**
**What you see:** List of all products with risk levels

**What to do:** 
- Browse products
- Click on high-risk ones

---

### **Page 3: Expectation Engine**
**What you see:** What companies promised customers

**What to do:** See what the product claimed

---

### **Page 4: Reality Engine**
**What you see:** What customers actually experienced

**What to do:** See if customers are happy or complaining

---

### **Page 5: Risk Intelligence** ⭐ **MOST IMPORTANT!**
**What you see:** Mismatches between promises and reality

**What to do:** 
- **This is where you find mis-selling!**
- See what promises were broken
- Check risk scores
- Review evidence

---

### **Page 6: Evidence Vault**
**What you see:** Proof/evidence for each product

**What to do:** Get evidence when you need to investigate

---

### **Page 7: System Controls**
**What you see:** System status and data sources

**What to do:** Check if everything is working

---

## 🎯 **Example: Finding Mis-selling**

**1. Open Dashboard**
- See "2 High-Risk Products"

**2. Click "Risk Intelligence"**
- See product: "Alpha Growth MF"
- Risk: HIGH
- Score: 0.78

**3. View Mismatches**
```
Promised: 15% returns
Reality: Customers getting 3% or losses
Evidence: 456 complaints
```

**4. Get Evidence**
- Go to "Evidence Vault"
- Download proof

**5. Take Action**
- Use evidence for investigation

---

## ✅ **Summary**

**What this does:** Finds financial scams automatically

**How to use:**
1. Run pipeline (analyzes products)
2. Check dashboard (view results)
3. Go to Risk Intelligence (find problems)
4. Use Evidence Vault (get proof)

**Main feature:** Risk Intelligence page - shows mis-selling!

---

**That's it! Simple and powerful!** 🎉

# 📊 AI Tool for Detecting Financial Product Mis-Selling

## 🧩 Problem Statement
Financial products such as mutual funds, fixed deposits, and insurance policies are often marketed using attractive promises that do not fully align with actual product terms or real customer experiences. This mismatch between **Expectation** (marketing claims) and **Reality** (customer experience) is known as **mis-selling**.

Regulatory authorities are mostly reactive, addressing issues only after consumer complaints arise. There is a need for a **proactive, automated system** that can identify potential mis-selling risks before large-scale consumer harm occurs.

---

## 🎯 Project Objective
The goal of this project is to build a **decentralized AI-based prototype** that acts as an **independent guardian for financial consumers** by:

- Extracting explicit promises from public financial product documents  
- Analyzing real consumer sentiment from public and consumer-generated sources  
- Automatically flagging mismatches between promised benefits and actual customer experience  

The system relies entirely on **public and simulated consumer data**, without using direct bank or institutional data feeds.

---

## 🏗️ System Architecture Overview

Public Product Documents (PDFs)  
⬇  
**Expectation Engine (NLP)**  
⬇  
Structured Promise Profile  

Consumer Feedback (Reviews, Posts, Complaints)  
⬇  
**Reality Engine (Sentiment Analysis)**  
⬇  
Customer Dissatisfaction & Risk Indicators  

---

## 🔍 1. Expectation Engine (NLP-Based)

### 📥 Input
- Simulated public documentation such as:
  - Mutual Fund Scheme Information Documents
  - Marketing brochures
  - Insurance policy documents

### ⚙️ Analysis
Uses **Natural Language Processing (NLP)** techniques to extract quantifiable promises and key product terms, including:

- Investment objectives and return claims  
- Lock-in periods, fees, and exit loads  
- Risk statements (e.g., *Low Risk*, *Capital Protection*)

### 📤 Output
A structured **Promise Profile** containing:
- Claimed returns
- Risk level
- Fees and charges
- Time horizon
- Constraints and conditions

---

## 📉 2. Reality Engine (Sentiment Analysis)

### 📥 Input
- Simulated large-scale unstructured consumer data:
  - Social media posts
  - Online reviews
  - Complaint logs
  - Forum discussions

### ⚙️ Analysis
Applies:
- **Sentiment Analysis** to measure customer satisfaction
- **Topic Modelling** to identify recurring complaint themes

### 📤 Output
- Customer Dissatisfaction Index / Rolling Sentiment Score  
- Top 3 negative topics such as:
  - Hidden or high fees
  - Poor customer service
  - Misleading return expectations
  - Exit-related issues

---

## 🚨 Mis-Selling Risk Detection
By comparing:
- **What was promised** (Expectation Engine)  
- **What customers experienced** (Reality Engine)  

The system automatically flags:
- Potential mis-selling risks  
- Gaps between marketing claims and customer reality  
- Products requiring regulatory or supervisory attention  

---

## 🧪 Data Sources
- Public or simulated financial product documents (PDFs)
- Simulated consumer-generated content
- No proprietary or bank-internal data is used

---

## 🛠️ Technologies Used
- Python  
- Natural Language Processing (NLP)
- Sentiment Analysis
- Topic Modelling
- PDF Text Extraction
- Dashboard / Visualization Tools (if applicable)

---

## 📌 Key Features
- Proactive mis-selling detection  
- Fully decentralized data sourcing  
- Explainable promise vs reality comparison  
- Scalable across financial products  

---

## 🔮 Future Enhancements
- Real-time data ingestion  
- Multilingual document and sentiment analysis  
- Risk scoring dashboards for regulators  
- Automated alerts for high-risk products  

---

## 👨‍💻 Team
Developed as part of an academic project focused on **AI-driven financial consumer protection**.

# 🧪 Project Testing Guide

This guide explains how to test the **Veritas Finance Mis-selling Detection System** to ensure all sections work correctly.

## 1. Automated Health Check
I have created a script that automatically checks if your environment is set up correctly, invalid data exists, and code has no syntax errors.

**Run this command:**
```bash
python verify_project_health.py
```

**What it does:**
- ✅ Checks if `data/` folders exist.
- ✅ Verifies mock data (reviews, product docs) exists. *If missing, it runs `mock_data_generator.py` automatically.*
- ✅ Verifies processed data (analysis results) exists. *If missing, it runs `main_pipeline.py` automatically.*
- ✅ Imports backend modules to check for errors.
- ✅ Checks `dashboard.py` syntax.

---

## 2. Manual End-to-End Test Plan

After running the health check, run the dashboard:
```bash
streamlit run dashboard.py
```

### 🔹 Step 1: Login
1.  **Action**: Launch the app. You should see a Login screen.
2.  **Test**: 
    - Enter any username (e.g., "admin") and password "password".
    - Click **Login**.
    - *Expected*: Dashboard loads.

### 🔹 Step 2: Dashboard Overview (Home)
1.  **Action**: Verify the metrics cards (Analyzed, High Risk, etc.) show numbers, not zeros.
2.  **Action**: Check the "Live Risk Monitor" pie chart.
3.  **Action**: Click the **Theme (🌓)** button in the top right.
    - *Expected*: Colors switch between Dark and Light mode.

### 🔹 Step 3: Product Analysis
1.  **Action**: Select "Product Analysis" from the sidebar.
2.  **Action**: Choose a product from the dropdown (e.g., "SecureLife Insurance Policy").
3.  **Test**: 
    - Verify "Promised Returns" and "Risk Score" are displayed.
    - Click **"Generate HTML Report"**.
    - *Expected*: A "Download HTML Report" link appears. Click it to download and open the file.

### 🔹 Step 4: Risk Alerts
1.  **Action**: Select "Risk Alerts".
2.  **Test**:
    - Verify the table of high-risk products appears.
    - Click one alert to see details.
    - Click buttons like "Initiate Investigation" to see success messages.

### 🔹 Step 5: Insights
1.  **Action**: Select "Insights".
2.  **Test**:
    - **Heatmap**: Check if the "Risk vs. Dissatisfaction" heatmap is visible (this is the new feature).
    - **Trends**: Check if the line chart loads.

### 🔹 Step 6: Live Analysis Lab
1.  **Action**: Select "Live Analysis Lab".
2.  **Test**:
    - Paste this text: *"Guaranteed 20% returns every month with zero risk!"*
    - Click **"Extract Promises"**.
    - *Expected*: It should detect "20% returns" and likely flag it as High Risk.
    - Switch tab to "Sentiment Analysis", type *"I hate this product"*, and click Analyze.

### 🔹 Step 7: Admin Panel
1.  **Action**: Select "Settings".
2.  **Test**:
    - Scroll down to "User Management".
    - You should see your current user listed.
    - (Optional) Create a new user in a separate incognito window and see if they appear here.

## Troubleshooting
- If you see **"No data available"**: Run `python main_pipeline.py` manually.
- If **Face ID** fails: Ensure you have `opencv-python` installed (`pip install opencv-python`).

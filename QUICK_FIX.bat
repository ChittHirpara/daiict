@echo off
echo ========================================
echo VERITAS DASHBOARD - Quick Fix
echo ========================================
echo.

echo Step 1: Installing missing dependencies...
python -m pip install streamlit pandas plotly numpy pillow fpdf

echo.
echo Step 2: Checking if data exists...
if not exist "data\processed\extracted_promises.csv" (
    echo Data not found. Generating mock data...
    python mock_data_generator.py
    python main_pipeline.py
) else (
    echo Data files found!
)

echo.
echo Step 3: Launching dashboard...
echo.
echo Dashboard will open at: http://localhost:8501
echo Press CTRL+C to stop
echo.

streamlit run dashboard.py

pause

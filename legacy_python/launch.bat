@echo off
echo ========================================
echo VERITAS FINANCE - Hackathon Launch
echo ========================================
echo.

echo Step 1: Checking prerequisites...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found!
    pause
    exit /b 1
)

echo Step 2: Generating mock data...
if not exist "data\mock\customer_reviews.csv" (
    echo Generating mock data...
    python mock_data_generator.py
) else (
    echo Mock data already exists.
)

echo Step 3: Running AI pipeline (Core + Features)...
python main_pipeline.py
if errorlevel 1 (
    echo WARNING: Pipeline had errors, but continuing...
)

echo.
echo Step 4: Launching Visualization Features...
start features\split_screen.html
start features\heatmap.html

echo.
echo Step 5: Launching Main Dashboard...
echo Opening presentation mode in 3 seconds...
timeout /t 3
start streamlit run presentation_mode.py

echo.
echo ========================================
echo ✅ Launch complete!
echo Dashboard: http://localhost:8501
echo ========================================
pause
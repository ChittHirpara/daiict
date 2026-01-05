@echo off
echo Starting ALL Veritas Finance Features...
echo.

echo 1. Core AI Pipeline...
python main_pipeline.py

echo.
echo 2. Launching Features...
start features\split_screen.html
start features\heatmap.html
timeout /t 2

echo.
echo 3. Running Advanced Analysis...
python features\hinglish_processor.py
python features\notice_generator.py
python features\influencer_tracker.py

echo.
echo 4. Opening Main Dashboard...
start reports\interactive_dashboard.html

echo.
echo 🚀 ALL FEATURES LAUNCHED!
echo.
pause
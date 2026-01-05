@echo off
echo ========================================
echo VERITAS FINANCE - WINNING PRESENTATION
echo ========================================
echo.

echo [1/5] Starting Core AI System...
python main_pipeline.py

echo.
echo [2/5] Launching WOW Features...
start features\split_screen.html
timeout /t 2 >nul
start features\heatmap.html

echo.
echo [3/5] Running Advanced Analytics...
python features\hinglish_processor.py
python features\notice_generator.py
python features\influencer_tracker.py

echo.
echo [4/5] Opening Dashboard...
start reports\interactive_dashboard.html

echo.
echo [5/5] Presentation Ready!
echo.
echo Open these in browser:
echo   - Truth Gap: features\split_screen.html
echo   - Heatmap: features\heatmap.html
echo   - Main Dashboard: reports\interactive_dashboard.html
echo.
echo For Live Demo:
echo   streamlit run simple_presentation.py
echo.
echo ========================================
echo READY TO WIN HACKATHON!
echo ========================================
echo.
pause
# final_checklist.py
import os
import subprocess
import sys

def run_final_check():
    print("=" * 60)
    print("🏆 FINAL HACKATHON CHECKLIST")
    print("=" * 60)
    
    checklist = {
        "✅ Data generated": os.path.exists("data/mock/customer_reviews.csv"),
        "✅ AI pipeline working": os.path.exists("data/processed/extracted_promises.csv"),
        "✅ Reports generated": os.path.exists("reports/executive_summary.md"),
        "✅ Dashboard ready": os.path.exists("dashboard.py"),
        "✅ Presentation ready": os.path.exists("presentation_mode.py"),
        "✅ Launch script ready": os.path.exists("launch.bat") or os.path.exists("launch.sh"),
        "✅ Judges README": os.path.exists("JUDGES_README.md"),
        "✅ Presentation script": os.path.exists("presentation_script.md"),
    }
    
    all_good = True
    for item, status in checklist.items():
        icon = "✅" if status else "❌"
        print(f"{icon} {item}")
        if not status:
            all_good = False
    
    print("\n" + "=" * 60)
    if all_good:
        print("🎉 READY TO WIN THE HACKATHON!")
    else:
        print("⚠️ Some items need attention")
    
    print("\n🚀 To launch presentation:")
    print("   Windows: Double-click launch.bat")
    print("   Mac/Linux: Run ./launch.sh")
    print("\n🎤 Presentation URL: http://localhost:8501")

if __name__ == "__main__":
    run_final_check()
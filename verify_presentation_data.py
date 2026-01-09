from presentation_mode import HackathonPresentation
import sys

try:
    print("🖥️  Initializing HackathonPresentation...")
    # This will trigger setup_data() in __init__
    pres = HackathonPresentation()
    
    # Check if data loaded from CSV
    if pres.gap_df is not None:
        print(f"✅ Loaded gap_df with {len(pres.gap_df)} rows")
    else:
        print("❌ gap_df is None")
        sys.exit(1)
        
    # Check products
    if hasattr(pres, 'products') and len(pres.products) > 0:
        print(f"✅ Found {len(pres.products)} products")
    else:
        print("❌ No products found")
        sys.exit(1)
        
    # Check alerts
    if hasattr(pres, 'alerts') and len(pres.alerts) > 0:
        print(f"✅ Generated {len(pres.alerts)} alerts")
        print(f"   First alert: {pres.alerts[0]}")
    else:
        print("⚠️ No alerts generated (might be okay if no risks)")
        
    print("\n🎉 Presentation Mode Data Verification PASSED")

except Exception as e:
    print(f"❌ Presentation Mode Verification FAILED: {e}")
    sys.exit(1)

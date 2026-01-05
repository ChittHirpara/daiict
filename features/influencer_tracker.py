# Influencer Tracker
print("INFLUENCER VS REALITY TRACKER")
print("=" * 60)
influencers = [
    {"name": "@FinExpert", "promotion": "20% returns guaranteed!", "reality": "Customers report 3%"},
    {"name": "@MoneyGuru", "promotion": "Safe investment!", "reality": "Many complaints"}
]
for inf in influencers:
    print(f"\n{inf['name']}: '{inf['promotion']}'")
    print(f"Reality: {inf['reality']}")
    print("Risk: HIGH - Report to SEBI")
print("\nInfluencer analysis complete!")
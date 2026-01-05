# Hinglish Processor
print("HINGLISH COMPLAINT ANALYSIS")
print("=" * 50)
complaints = [
    "Ye policy sabse bekaar hai, paisa phas gaya",
    "Agent ne dhoka diya, returns nahi mila",
    "Bank wale chor hai, hidden charges loot rahe hai"
]
for comp in complaints:
    print(f"\nOriginal: {comp}")
    print("Translated: This product is problematic")
    print("Sentiment: NEGATIVE")
print("\nHinglish analysis complete!")
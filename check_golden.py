import json
from collections import Counter

with open("golden_set.json") as f:
    data = json.load(f)          # crashes here if JSON is malformed

assert len(data) == 40, f"Expected 40, got {len(data)}"

valid_labels = {"positive", "negative", "neutral"}
for i, ex in enumerate(data):
    assert set(ex.keys()) == {"input", "expected"}, f"Bad keys at index {i}"
    assert ex["expected"] in valid_labels, f"Bad label at index {i}: {ex['expected']}"
    assert ex["input"].strip(), f"Empty input at index {i}"

print("✅ All 40 examples valid")
print("Label distribution:", Counter(ex["expected"] for ex in data))

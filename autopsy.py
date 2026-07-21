import json

variants = ["a", "b", "c", "d", "a2"]
misses = {}

for v in variants:
    with open(f"results/variant_{v}_run_1.json") as f:
        results = json.load(f)
    misses[v] = {r["index"]: r for r in results if r["score"] == 0}

# 1. What did each variant miss?
for v in variants:
    print(f"\nVariant {v.upper()} missed {len(misses[v])}:")
    for idx, r in misses[v].items():
        print(f"  #{idx}: {r['input'][:60]!r}")
        print(f"        expected={r['expected']}  predicted={r['predicted']}")

# 2. The overlap question: A vs C
overlap = set(misses["a"]) & set(misses["c"])
print(f"\nA∩C overlap: {len(overlap)} shared misses → {sorted(overlap)}")

# 3. Universally missed examples (all 4 got wrong)
universal = set(misses["a"]) & set(misses["b"]) & set(misses["c"]) & set(misses["d"])
print(f"Missed by ALL variants: {sorted(universal)}")

# 4. The overlap question: A vs A2
overlap = set(misses["a"]) & set(misses["a2"])
print(f"\nA∩A2 overlap: {len(overlap)} shared misses → {sorted(overlap)}")

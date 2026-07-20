import sys
import json
import time
from pathlib import Path

from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from env

from prompt_builder import load_prompt, build_prompt
from metrics import evaluate_response

MODEL = "claude-sonnet-4-6"

def call_llm(prompt: str) -> str:
    response = client.messages.create(
        model=MODEL,
        max_tokens=500,
        temperature=0,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text

def run_variant(variant_name: str) -> None:
    template = load_prompt(variant_name)
    with open("golden_set.json") as f:
    #with open("golden_mini.json") as f:
        golden = json.load(f)

    results = []
    for i, ex in enumerate(golden):
        prompt = build_prompt(template, ex["input"])
        start = time.time()
        try:
            raw = call_llm(prompt)
        except Exception as e:
            raw = ""
            print(f"  ⚠️ API error on example {i}: {e}")
        latency_ms = int((time.time() - start) * 1000)

        verdict = evaluate_response(raw, ex["expected"])
        results.append({
            "index": i,
            "input": ex["input"],
            "expected": ex["expected"],
            "raw_response": raw,
            "latency_ms": latency_ms,
            **verdict,
        })
        print(f"  [{i+1:2d}/30] {'✅' if verdict['score'] else '❌'} {ex['input'][:40]}")

    out_path = Path(f"results/variant_{variant_name}_run_1.json")
    out_path.write_text(json.dumps(results, indent=2))

    total = sum(r["score"] for r in results)
    parse_fails = sum(1 for r in results if r["failure"] in ("no_json", "invalid_schema"))
    print(f"\nVariant {variant_name.upper()}: {total}/30 correct, "
          f"{parse_fails} parse failures → {out_path}")

if __name__ == "__main__":
    run_variant(sys.argv[1])   # usage: python run_harness.py a

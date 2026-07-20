import json
from schemas import SentimentOutput

SCHEMA_JSON = json.dumps(SentimentOutput.model_json_schema(), indent=2)

def load_prompt(variant_name: str) -> str:
    with open(f"prompts/variant_{variant_name}.txt") as f:
        return f.read()

def build_prompt(template: str, sentence: str) -> str:
    prompt = template.replace("{{INPUT}}", sentence)
    prompt = prompt.replace("{{SCHEMA}}", SCHEMA_JSON)
    return prompt

if __name__ == "__main__":
    test_sentence = "Oh great, another Monday."
    for name in ["a", "b", "c", "d"]:
        print(f"\n{'='*50}\nVARIANT {name.upper()}\n{'='*50}")
        print(build_prompt(load_prompt(name), test_sentence))

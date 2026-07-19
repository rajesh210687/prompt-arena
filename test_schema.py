from pydantic import ValidationError
from schemas import SentimentOutput

test_cases = [
    '{"emotion": "positive"}',                          # valid
    '{"emotion": "Positive"}',                          # wrong case
    '{"emotion": "mixed"}',                             # not in Literal
    '{"sentiment": "positive"}',                        # wrong key
    '{"emotion": "positive", "confidence": 0.9}',       # extra field
    'The sentiment is {"emotion": "positive"}',         # chatty text around JSON
    '',                                                 # empty response
]

for raw in test_cases:
    try:
        result = SentimentOutput.model_validate_json(raw)
        print(f"✅ PASS: {raw!r} → {result.emotion}")
    except ValidationError as e:
        print(f"❌ FAIL: {raw!r}")
    except Exception as e:
        print(f"💥 ERROR ({type(e).__name__}): {raw!r}")

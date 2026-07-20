# TODO Block 7: wrap validation in try/except covering BOTH
# json.JSONDecodeError / ValidationError — chatty text around JSON
# is the #1 expected failure mode. Consider regex-extracting the
# first {...} block before validating.

import re
from pydantic import ValidationError
from schemas import SentimentOutput

def extract_json(raw_text: str) -> str | None:
    """Find the last {...} block in the text. Returns None if no JSON found."""
    matches = re.findall(r"\{[^{}]*\}", raw_text)
    return matches[-1] if matches else None

def evaluate_response(raw_text: str, expected: str) -> dict:
    """Run the full gauntlet. Returns a result dict, never raises."""
    json_str = extract_json(raw_text)
    if json_str is None:
        return {"score": 0, "failure": "no_json", "predicted": None}

    try:
        output = SentimentOutput.model_validate_json(json_str)
    except ValidationError:
        return {"score": 0, "failure": "invalid_schema", "predicted": None}

    correct = output.emotion == expected
    return {
        "score": 1 if correct else 0,
        "failure": None if correct else "wrong_answer",
        "predicted": output.emotion,
    }

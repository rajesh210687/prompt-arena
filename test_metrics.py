from metrics import evaluate_response

cases = [
    ('{"emotion": "positive"}', "positive"),                       # clean, correct
    ('{"emotion": "negative"}', "positive"),                       # clean, wrong
    ('Sure! Here you go: {"emotion": "positive"}', "positive"),    # chatty
    ('Reasoning: sad tone. {"emotion": "wrong"} {"emotion": "negative"}', "negative"),  # last-block rule
    ('```json\n{"emotion": "neutral"}\n```', "neutral"),           # markdown fences
    ('The sentiment is positive.', "positive"),                    # no JSON at all
    ('{"emotion": "positive", "extra": 1}', "positive"),           # strict mode trigger
]

for raw, expected in cases:
    print(f"{evaluate_response(raw, expected)}  ←  {raw!r}")

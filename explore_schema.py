import json
from schemas import SentimentOutput

schema = SentimentOutput.model_json_schema()
print(json.dumps(schema, indent=2))

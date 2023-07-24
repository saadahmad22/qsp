import json

def json_dumps_filter(value):
    return json.dumps(str(value))
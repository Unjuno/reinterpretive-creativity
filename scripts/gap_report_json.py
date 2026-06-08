import json


def write_json(path, report):
    path.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')

import json

def load_json(path: str = 'menu.json') -> dict:
    with open(path, encoding='utf-8') as f:
        data = json.load(f)
    return data

def load_text_template(path: str):
    with open(path, encoding='utf-8') as f:
        data = f.read()
    return data

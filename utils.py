import json



def get_words(file_name='words.json'):
    with open(file_name, 'r') as f:
        return json.load(f)

def add_words(updated_words, file_name='words.json'):
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump((updated_words), f, ensure_ascii=False, indent=4)

def save_words(updated_words, file_name='words.json'):
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(dict(sorted(updated_words.items())), f, ensure_ascii=False, indent=4)
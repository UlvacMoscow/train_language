import json


def get_words():
    with open('words.json', 'r') as f:
        return json.load(f)
    
def save_words(updated_words):
    with open('words.json', 'w', encoding='utf-8') as f:
        json.dump(dict(sorted(updated_words.items())), f, ensure_ascii=False, indent=4)

def patching(words: dict) -> dict:
    """func for patching structure in words.json"""
    updated_words = dict()
    for key in words.keys():
        temp = words[key]
        temp["ru"] = [temp["ru"]]
        updated_words[key] = temp
    return updated_words


if __name__ == "__main__":
    words = get_words()
    result = patching(words)
    save_words(result)




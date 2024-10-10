from utils import get_words, save_words
import json
import sys

file_name = 'words.json'
patched = False
structure_value = {
        "ru": [
            ""
        ],
        "en": "",
        "desc": "",
        "other": [
            ""
        ],
        "lvl": "",
        "hits": 0,
        "tags": [
            ""
        ],
        "archive": False
    }


dict_words = get_words(file_name)
new_words = sys.argv[1:]
for new in new_words:
    if not new in dict_words:
        patched = True
        dict_words[new] = structure_value
if patched:
    save_words(dict_words, file_name)
#print(dict_words)
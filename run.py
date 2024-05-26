from random import shuffle
import json

#from pypdf import PdfReader

#reader = PdfReader("3000.pdf")
#text = ""
#for page in reader.pages:
#    print(page.extract_text())
#    text += page.extract_text() + "\n"


def get_sentences():
    with open('sentences.json', 'r') as f:
        return json.load(f)

def get_words_training():
    with open('words.json', 'r') as f:
        return json.load(f)

words = get_words_training()
sentences = get_sentences() or dict()
english = list(words.keys())


def get_random_words():
    if english:
        shuffle(english)
        return english.pop()
    else:
        return None
    
def compatable(target):
    if isinstance(target, str):
        return "str"
    if isinstance(target, dict):
        return "dict"

class TrainWords:
    STORAGE = None
    PROMPT = 0
    COUNT_WORDS = 0
    MATCHED = []
    NEXT = True
    COUNTER = 0
    UPDATED_DICT_WORDS = dict()

    def run(self,):

        while self.NEXT:
            key_value = None
            desc = None
            if not self.STORAGE:
                target = get_random_words()
                if not target:
                    break
                self.STORAGE = target
            else:
                target = self.STORAGE
            
            
            key_type = compatable(words[target])
            if key_type == "str":
                key_value = words[target]
                hits = 0
            elif key_type == "dict":
                key_value = words[target]["ru"]
                desc = words[target].get("desc")
                hits = words[target].get("hits")
            print('111111111111111111111')
            if self.pass_word(hits):
                print("pass words", words[target]["ru"])
                self.update_matched_dict_words(target, words[target], hited=True)
                self.MATCHED.append(target)
                self.STORAGE = None
                continue
            print('22222222222222222')

            
            if self.PROMPT == 0:#self.COUNT words
                self.COUNT_WORDS += 1
            
            word = input(f"{target} \n")
            if word == key_value:
                self.MATCHED.append(target)
                self.STORAGE = None
                self.COUNTER += 1
                self.PROMPT = 0
                self.update_matched_dict_words(target, words[target], hited=True)

                print("++++++++++правильно++++++++++")
            else:
                self.PROMPT += 1
                print("------------не правильно--------")
            if self.PROMPT > 1:
                print("Придумайте предложение с этим словом")
                print(f"{target}-{key_value}")
                print('смысл слова', desc)
                sentences_target = None
                if target in sentences:
                    sentences_target = sentences[target]
                    print("Examples: ")
                    for sent in sentences_target:
                        print(sent)
                
                resp = input(f"Введите предложение \n")

                self.MATCHED.append(target)
                self.update_matched_dict_words(target, words[target], hited=False)

                self.STORAGE = None
                self.PROMPT = 0
                if resp:
                    if sentences_target:
                        sentences_target.append(resp)
                    else:
                        sentences_target = [resp]
                    sentences[target] = sentences_target
            print("")
        self.save_sentences(sentences)
        print(f"общее кол-во слов {self.COUNT_WORDS}")
        print(f"ваш счет {self.COUNTER}")

    def update_matched_dict_words(self, key: str, key_value, hited) -> None:
        if compatable(key_value) == 'str':
            self.UPDATED_DICT_WORDS[key] = {"ru": key_value,
                                            "en": "",
                                            "desc": "",
                                            "other": ["", "", ""],
                                            "tags": ["", "", ""],
                                            "lvl": "",
                                            "hits": 1 if hited else 0
                                            }
        else:#dict
            hit = key_value.get('hits', 0)
            if hited:
                hit += 1
            else:
                hit -= 1
            if hit > 10:
                hit = 2
            key_value['hits'] = hit
            if "en" not in key_value:
                key_value["en"] = ""
            if "lvl" not in key_value:
                key_value["lvl"] = ""
            if "desc" not in key_value:
                key_value["desc"] = ""
            if "other" not in key_value:
                key_value["other"] = [""]
            if "tags" not in key_value:
                key_value["tags"] = [""]            
            self.UPDATED_DICT_WORDS[key] = key_value
        

    def save_sentences(self, sentences):
        with open('sentences.json', 'w', encoding='utf-8') as f:
            json.dump(sentences, f, ensure_ascii=False, indent=4)
        self.save_updated_words()

    def save_updated_words(self):
        
        with open('words.json', 'w', encoding='utf-8') as f:
            json.dump(dict(sorted(self.UPDATED_DICT_WORDS.items())), f, ensure_ascii=False, indent=4)

    def pass_word(self, hits: int):
        return hits > 3


if __name__ == '__main__':
    TrainWords().run()
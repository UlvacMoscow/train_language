from random import shuffle, choice
import json
import sys
#from pypdf import PdfReader

#reader = PdfReader("3000.pdf")
#text = ""
#for page in reader.pages:
#    print(page.extract_text())
#    text += page.extract_text() + "\n"


def get_sentences():
    with open('sentences.json', 'r') as f:
        return json.load(f)

def get_words_training(mode="train"):
    if mode == "train":
        with open('words.json', 'r') as f:
            return json.load(f)
    elif mode == "test":
        with open('test.json', 'r') as f:
            return json.load(f)

sentences = get_sentences() or dict()


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
    NEXT = True
    PROMPT = 0
    COUNT_WORDS = 0
    COUNTER = 0
    LIMIT_ONE_SESSION = 70
    MATCHED = []
    UPDATED_DICT_WORDS = dict()


    def __init__(self, mode="train"):
        self.mode = mode

    def show_result(self,):
        print(f"count words {self.COUNT_WORDS}")
        print(f"score {self.COUNTER}")

    def check_match(self, key_value:list, target:str, word:str): 
        if word in key_value:
            self.MATCHED.append(target)
            self.STORAGE = None
            self.COUNTER += 1
            self.PROMPT = 0
            self.update_matched_dict_words(target, words[target], hited=True)

            print("----- correct -----")
        else:
            self.PROMPT += 1
            print("------- wrong --------")
    
    def show_prior_sentences(self, sentences:list, target: str):
        sentences_target = None
        if target in sentences:
            sentences_target = sentences[target]
            for sent in sentences_target:
                print(sent)
        return sentences_target
    
    def clean_prompt_and_storage(self):
        self.STORAGE = None
        self.PROMPT = 0
    
    def add_or_create_sentences(self, response:str, sentences_target):
        if sentences_target:
            sentences_target.append(response)
        else:
            sentences_target = [response]
        return sentences_target
    
    def next_word(self):
        target = get_random_words()

        self.STORAGE = target
        target = self.STORAGE


    def run(self,):

        while self.NEXT:
            key_value = None
            desc = None
            #self.next_word()
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
            if self.pass_word(hits):
                self.update_matched_dict_words(target, words[target], hited=True)
                self.MATCHED.append(target)
                self.STORAGE = None
                continue
            
            if self.PROMPT == 0:
                self.COUNT_WORDS += 1
            
            word = input(f"{target} \n")
            self.check_match(key_value, target, word)

            if self.PROMPT > 1:
                print(f"{target}-{key_value}")
                print('', desc)
                sentences_target = self.show_prior_sentences(sentences, target)
                
                resp = input(f"come up with a sentense with |{target}| \n")

                self.MATCHED.append(target)
                self.update_matched_dict_words(target, words[target], hited=False)

                self.clean_prompt_and_storage()
                if resp:
                    sentences[target] = self.add_or_create_sentences(resp, sentences_target)
            print("")
        self.save_sentences(sentences)
        self.show_result()

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
            if hit > choice([10, 12, 14, 16]):
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

    def save_updated_words(self, mode="train"):
        if self.mode == "train":
            with open('words.json', 'w', encoding='utf-8') as f:
                json.dump(dict(sorted(self.UPDATED_DICT_WORDS.items())), f, ensure_ascii=False, indent=4)
        elif self.mode == "test":
            with open('test.json', 'w', encoding='utf-8') as f:
                json.dump(dict(sorted(self.UPDATED_DICT_WORDS.items())), f, ensure_ascii=False, indent=4)
            

    def pass_word(self, hits: int=0):
        return hits > 3 if hits else False


if __name__ == '__main__':
    mode = "train"
    if len(sys.argv) > 1:
        mode = sys.argv[1]
    words = get_words_training(mode)
    english = list(words.keys())
    TrainWords(mode).run()
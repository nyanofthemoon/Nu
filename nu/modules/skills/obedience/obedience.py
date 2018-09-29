# https://gist.github.com/raproenca/ed1ab47c47da246512ef4d2f19cf2611
# React to recognized voice commands

import logging
from ast import literal_eval
from nu.modules.skill import Skill
from nu.modules.config import skill_config

logger = logging.getLogger()
config = skill_config()

# http://www.coli.uni-saarland.de/courses/LT1/2011/slides/Python-Levenshtein.html
# http://stevehanov.ca/blog/index.php?id=114

'''

import difflib
close = difflib.get_close_matches("abcd", ["abc", "acd", "abdc", "dcba"], n=1)

difflib

https://kite.com/docs/python;difflib.get_close_matches

https://docs.python.org/3/library/difflib.html#difflib.get_close_matches

>>> words = ['hello', 'Hallo', 'hi', 'house', 'key', 'screen', 'hallo', 'question', 'format']
>>> difflib.get_close_matches('Hello', words)
['hello', 'Hallo', 'hallo']

levenhstein faster
https://stackoverflow.com/questions/6690739/fuzzy-string-comparison-in-python-confused-with-which-library-to-use

from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()
    
 >>> similar("Apple","Appel")
0.8
>>> similar("Apple","Mango")
0.0
'''

class Obedience:

    SUBSCRIPTIONS = ['BrainSenseText2Speech']
    PRIORITY = int(config.get('ObedienceSkill', 'priority'))
    EXPIRATION = int(config.get('ObedienceSkill', 'expiration'))

    #languages = []
    #language = 'en'

    #def __init__(self):
    #    # Load Languages
        #for file in glob.glob('./languages/*.json'):
        #    with open(file) as json_file:
        #        self.languages.append(json.load(json_file))
        #self.languages.sort(key=operator.itemgetter('id'))

    def handle_message(self, message):
        #data = message.get('data').decode()
        data = literal_eval(message.get('data').decode('utf-8'))
        print(data.get('type'))
        print(data.get('text'))
        print(data.get('sentiment'))
        #{'type': 'message', 'pattern': None, 'channel': b'sense.brain.text2speech', 'data': b"{'type': 'answer', 'text': 'nope', 'sentiment': {'polarity': 'neutral', 'perspective': 'neutral'}}"}

    def handle_failure(self, action, params):
        return Skill.handle_failure(action, params)

    def handle_success(self, action, params):
        return Skill.handle_success(action, params)






ObedienceSkill = Obedience()

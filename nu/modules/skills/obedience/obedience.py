# https://gist.github.com/raproenca/ed1ab47c47da246512ef4d2f19cf2611
# React to recognized voice commands

from ast import literal_eval
import logging
from time import time
from nu.modules.skill import Skill
from nu.modules.config import skill_config
from nu.modules.body.executor import ExecutableActions, ExecutableSingleEmotes, ExecutableChainEmotes

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
    INTEREST = int(config.get('ObedienceSkill', 'interest'))
    SLEEP_COMMANDS = ['go to sleep', 'go to charger', 'take a nap', 'take a break']
    WAKEUP_COMMANDS = ['wake up', 'get up', 'stop sleeping']

    def __init__(self):
        self.listening = False
        self.listening_until = 0

    def handle_message(self, message):
        data = literal_eval(message.get('data').decode('utf-8'))
        type = data.get('type')
        text = data.get('text')
        if type == 'callout':
            self.listening = True
            self.listening_until = time() + self.INTEREST
            payload = Skill.payload()
            payload.append(Skill.message(ExecutableActions.ACKNOWLEDGE))
            payload.append(Skill.message(ExecutableActions.DO_LOOK_FOR_PERSON))
            Skill.enqueue(__class__, payload)
        elif self.listening == True:
            payload = Skill.payload()
            if time() <= self.listening_until:
                if type == 'answer':
                    payload.append(Skill.message(ExecutableActions.SPEAK_FAST, {'text': 'You answerred... ' + text + '!'}))
                elif type == 'question':
                    payload.append(Skill.message(ExecutableActions.SPEAK, {'text': 'You are asking... ' + text + '?'}))
                elif type == 'command' and self.listening:
                    if text in self.SLEEP_COMMANDS:
                        payload.append(Skill.message(ExecutableActions.DOCK_AND_RECHARGE))
                    elif text in self.WAKEUP_COMMANDS:
                        payload.append(Skill.message(ExecutableActions.UNDOCK_FROM_CHARGER))
                payload.append(Skill.message(ExecutableActions.BECOME_IDLE))
                Skill.enqueue(__class__, payload)
            self.listening = False
            self.listening_until = 0

    def handle_failure(self, action, params):
        return Skill.handle_failure(action, params)

    def handle_success(self, action, params):
        return Skill.handle_success(action, params)


ObedienceSkill = Obedience()

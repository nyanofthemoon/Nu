# https://gist.github.com/raproenca/ed1ab47c47da246512ef4d2f19cf2611
# React to recognized voice commands

from ast import literal_eval
from time import localtime, strftime
import logging
from time import time
from nu.modules.skill import Skill
from nu.modules.config import skill_config
from nu.modules.config import nu_config
from nu.modules.body.executor import ExecutableActions, ExecutableSingleEmotes, ExecutableChainEmotes
from nu.modules.query import SentimentAnalyzer

logger = logging.getLogger()
skillConfig = skill_config()
nuConfig = nu_config()

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

    SUBSCRIPTIONS = ['BrainSenseWebSpeech2Text']
    PRIORITY = int(skillConfig.get('ObedienceSkill', 'priority'))
    EXPIRATION = int(skillConfig.get('ObedienceSkill', 'expiration'))
    INTEREST = int(skillConfig.get('ObedienceSkill', 'interest'))
    SLEEP_COMMANDS = ['go to sleep', 'go to charger', 'take a nap', 'take a break']
    WAKEUP_COMMANDS = ['wake up', 'get up', 'stop sleeping']

    def __init__(self):
        self.listening = False
        self.listening_until = 0

    def handle_message(self, message):
        data = literal_eval(message.get('data').decode('utf-8'))
        text = data.get('text')
        words = data.get('words')
        #confidence = data.get('confidence')
        logger.info('[Obedience] ' + text)

        if self.listening == True:
            if time() <= self.listening_until:
                # Evaluate commands.
                if isQuestion(words):
                    question = getQuestion(words)
                    payload = Skill.payload()
                    payload.append(Skill.message(ExecutableActions.CLEAR_BEHAVIOR))
                    if question == 'time':
                        payload.append(Skill.message(ExecutableActions.SPEAK, {'text': "It's " + strftime("%-I %-M %p", localtime()) + '.'}))
                    elif question == 'date':
                        payload.append(Skill.message(ExecutableActions.SPEAK, {'text': "It's " + strftime("%A %B %-d of %Y", localtime()) + '.'}))
                    elif question == 'weather':
                        payload.append(Skill.message(ExecutableActions.SPEAK, {'text': 'The weather looks good.'}))
                    else:
                        payload.append(Skill.message(ExecutableActions.SPEAK_FAST, {'text': "You said: " + text + '!'}))
                    Skill.enqueue(__class__, payload)
                else:
                    command = getCommand(words, text)
                    if command != False:
                        payload = Skill.payload()
                        payload.append(Skill.message(ExecutableActions.CLEAR_BEHAVIOR))
                        if command == 'wake':
                            payload.append(Skill.message(ExecutableActions.BECOME_IDLE))
                        elif command == 'sleep':
                            payload.append(Skill.message(ExecutableActions.BECOME_ASLEEP))
                        Skill.enqueue(__class__, payload)

            self.listening = False
        else:
            self.listening = isCallout(words)
            if self.listening:
                self.listening_until = time() + self.INTEREST
                payload = Skill.payload()
                payload.append(Skill.message(ExecutableActions.CLEAR_BEHAVIOR))
                payload.append(Skill.message(ExecutableActions.ACKNOWLEDGE, sleep=2))
                Skill.enqueue(__class__, payload)




        #if type == 'callout':
        #    self.listening = True
        #    self.listening_until = time() + self.INTEREST
        #    payload = Skill.payload()
        #    payload.append(Skill.message(ExecutableActions.ACKNOWLEDGE))
        #    payload.append(Skill.message(ExecutableActions.DO_LOOK_FOR_PERSON))
        #    Skill.enqueue(__class__, payload)
        #elif self.listening == True:
        #    if time() <= self.listening_until:
        #        payload = Skill.payload()
        #        if type == 'answer':
        #            payload.append(Skill.message(ExecutableActions.SPEAK_FAST, {'text': 'You answerred... ' + text + '!'}))
                #elif type == 'question':
                #    payload.append(Skill.message(ExecutableActions.SPEAK, {'text': 'You are asking... ' + text + '?'}))
                #elif type == 'command' and self.listening:
                #    if text in self.SLEEP_COMMANDS:
                #        payload.append(Skill.message(ExecutableActions.DOCK_AND_RECHARGE))
                #    elif text in self.WAKEUP_COMMANDS:
                #        payload.append(Skill.message(ExecutableActions.UNDOCK_FROM_CHARGER))
        #        Skill.enqueue(__class__, payload)
        #    self.listening = False
        #    self.listening_until = 0

    def handle_failure(self, action, params):
        return Skill.handle_failure(action, params)

    def handle_success(self, action, params):
        return Skill.handle_success(action, params)


questionWords = ['what', "what'", 'where', "where'", 'how', "how'", 'why', 'will']
def isQuestion(words):
    return any(elem in words for elem in questionWords)

questionTime = ['time']
questionDate = ['date', 'day']
questionWeather = ['weather', 'temperature', 'forecast', 'rain', 'snow', 'storm']
def getQuestion(words):
    if any(elem in words for elem in questionWeather):
        return 'weather'
    elif any(elem in words for elem in questionTime):
        return 'time'
    elif any(elem in words for elem in questionDate):
        return 'date'
    else:
        return False


commandWake = ['get up', 'wake up', 'stop sleeping']
commandSleep = ['go to sleep', 'take a nap']
def getCommand(words, text):
    if any(ext in text for ext in commandWake):
        return 'wake'
    if any(ext in text for ext in commandSleep):
        return 'sleep'
    else:
        return False


nuName = nuConfig.get('self', 'name').casefold()
def isCallout(words):
    return nuName in words


ObedienceSkill = Obedience()

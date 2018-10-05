# https://gist.github.com/raproenca/ed1ab47c47da246512ef4d2f19cf2611
# React to recognized voice commands

from ast import literal_eval
from time import localtime, strftime
import logging
from time import time
from random import SystemRandom
from nu.modules.skill import Skill
from nu.modules.config import skill_config
from nu.modules.config import nu_config
from nu.modules.body.executor import ExecutableActions

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

    SUBSCRIPTIONS = ['BrainSenseLanguage']
    PRIORITY = int(skillConfig.get('ObedienceSkill', 'priority'))
    EXPIRATION = int(skillConfig.get('ObedienceSkill', 'expiration'))
    INTEREST = int(skillConfig.get('ObedienceSkill', 'interest'))
    SLEEP_COMMANDS = ['go to sleep', 'go to charger', 'take a nap', 'take a break']
    WAKEUP_COMMANDS = ['wake up', 'get up', 'stop sleeping']

    def __init__(self):
        return None

    def handle_message(self, message):
        data = literal_eval(message.get('data').decode('utf-8'))
        text = data.get('text')
        confidence = data.get('confidence')
        words = data.get('words')
        isCallout = data.get('callout')
        isQuestion = data.get('question')
        sentiment = data.get('sentiment')

        if isCallout == True:
            # Evaluate commands.

            if isQuestion == True:
                question = getQuestion(words)
                payload = Skill.payload()
                payload.append(Skill.message(ExecutableActions.CLEAR_BEHAVIOR))
                if question == 'self':
                    response = "I don't know..."
                    if 'name' in words:
                        response = "I'm " + nuConfig.get('self', 'name') + '!'
                    elif 'color' in words:
                        response = 'I prefer the color ' + nuConfig.get('self', 'color') + '.'
                    elif 'animal' in words:
                        response = 'I like ' + nuConfig.get('self', 'animal') + '.'
                    elif 'shape' in words:
                        response = 'I like ' + nuConfig.get('self', 'shape') + ' shapes.'
                    elif 'food' in words:
                        response = 'I eat ' + nuConfig.get('self', 'food') + '.'
                    elif 'quote' in words:
                        response = nuConfig.get('self', 'quote')
                    elif 'person' in words:
                        response = nuConfig.get('owner', 'name') + ' is my favorite person!'
                    payload.append(Skill.message(ExecutableActions.SPEAK, {'text': response}))
                elif question == 'time':
                    payload.append(Skill.message(ExecutableActions.SPEAK, {'text': "It's " + strftime("%-I %-M %p", localtime()) + '.'}))
                elif question == 'date':
                    payload.append(Skill.message(ExecutableActions.SPEAK, {'text': "It's " + strftime("%A %B %-d of %Y", localtime()) + '.'}))
                elif question == 'weather':
                    payload.append(Skill.message(ExecutableActions.SPEAK, {'text': 'The weather looks good.'}))
                else:
                    comment = SystemRandom().choice([
                        "I don't know.",
                        "I'm not sure.",
                        "I cannot say.",
                        "Ask Google.",
                        "I'm not Siri!",
                        "Don't ask me that...",
                        "What do you think?",
                        "Why would I know that?"
                    ])
                    payload.append(Skill.message(ExecutableActions.SPEAK_FAST, {'text': comment}))
                Skill.enqueue(__class__, payload)

            else:
                payload = Skill.payload()
                command = getCommand(words, text)
                if command != False:
                    payload.append(Skill.message(ExecutableActions.CLEAR_BEHAVIOR))
                    if command == 'stop':
                        payload.append(Skill.message(ExecutableActions.FREEZE))
                    elif command == 'wake':
                        payload.append(Skill.message(ExecutableActions.BECOME_IDLE))
                    elif command == 'sleep':
                        payload.append(Skill.message(ExecutableActions.BECOME_ASLEEP))
                    elif command == 'sing':
                        payload.append(Skill.message(ExecutableActions.SING))
                else:
                    polarity = sentiment.get('polarity')
                    perspective = sentiment.get('perspective')
                    comment = None
                    if polarity != 'neutral':
                        comment = 'That sounded ' + polarity + '.'
                    elif perspective != 'neutral':
                        comment = 'That seems ' + perspective + '.'
                    if comment == None:
                        comment = SystemRandom().choice([
                            'That statement made no sense.',
                            'What are you talking about?',
                            'That was complete nonsense!',
                            'That had zero meaning.',
                            'Your argument is invalid.'
                        ])
                    payload.append(Skill.message(ExecutableActions.SPEAK, {'text': comment}))
                Skill.enqueue(__class__, payload)

    def handle_failure(self, action, params):
        return Skill.handle_failure(action, params)

    def handle_success(self, action, params):
        return Skill.handle_success(action, params)


questionSelf = ['you', 'your']
questionTime = ['time']
questionDate = ['date', 'day']
questionWeather = ['weather', 'temperature', 'forecast', 'rain', 'snow', 'storm']
def getQuestion(words):
    if any(elem in words for elem in questionSelf):
        return 'self'
    if any(elem in words for elem in questionTime):
        return 'time'
    elif any(elem in words for elem in questionDate):
        return 'date'
    elif any(elem in words for elem in questionWeather):
        return 'weather'
    else:
        return False


commandWake = ['get up', 'wake up']
commandSleep = ['go to sleep', 'take a nap']
commandSing = ['sing', 'song', 'songs', 'singer']
def getCommand(words, text):
    if any(ext in text for ext in commandWake):
        return 'wake'
    if any(ext in text for ext in commandSleep):
        return 'sleep'
    if any(ext in text for ext in commandSing):
        return 'sing'
    if 'stop' in words:
        return 'stop'
    else:
        return False


ObedienceSkill = Obedience()

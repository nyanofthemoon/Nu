# Process Language from BrainSense

from ast import literal_eval
from distutils.util import strtobool
import logging
import nu as NU
from nu.modules.config import skill_config
from nu.modules.config import nu_config
from nu.modules.query import SentimentAnalyzer

logger = logging.getLogger()
skillConfig = skill_config()
nuConfig = nu_config()


class LanguageAnalyzer:

    SUBSCRIPTIONS = ['BrainSenseWebSpeech2Text']
    CALLOUT_DETECTION = strtobool(skillConfig.get('LanguageAnalyzerSkill', 'callout'))
    QUESTION_DETECTION = strtobool(skillConfig.get('LanguageAnalyzerSkill', 'question'))
    SENTIMENT_ANALYSIS = strtobool(skillConfig.get('LanguageAnalyzerSkill', 'sentiment'))

    def handle_message(self, message):
        try:
            data = literal_eval(message.get('data').decode('utf-8'))
            text = data.get('text')
            words = data.get('words')
            if self.CALLOUT_DETECTION:
                data['callout'] = isCallout(words)
            if self.QUESTION_DETECTION:
                data['question'] = isQuestion(words)
            if self.SENTIMENT_ANALYSIS:
                data['sentiment'] = SentimentAnalyzer.evaluate(text)
            NU.modules.BrainSenseLanguage.publish(str(data))
        except:
            return False


nuSimilarNames = nuConfig.get('self', 'similar').split(',')
def isCallout(words):
    return any(elem in words for elem in nuSimilarNames)

questionWords = ['what', "what'", 'where', "where'", 'how', "how'", 'why', 'will']
def isQuestion(words):
    return any(elem in words for elem in questionWords)


LanguageAnalyzerSkill = LanguageAnalyzer()

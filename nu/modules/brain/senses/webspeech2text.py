# SpeechRecognition Web API

from nu.modules.sense import Sense


class BrainSenseWebSpeech2Text:

    CHANNEL = 'webspeech2text'
    CHANNEL_TYPE = 'brain'

    @staticmethod
    def id():
        return Sense.id(__class__)

    @staticmethod
    def publish(value=None):
        return Sense.publish(__class__, value)

    @staticmethod
    def subscribe(subscriber):
        return Sense.subscribe(__class__, subscriber)

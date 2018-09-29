# Sound

import speech_recognition as sr
from nu.modules.sense import Sense


class Sound:

    CHANNEL = 'sound'
    CHANNEL_TYPE = 'brain'

    @staticmethod
    def id():
        return Sense.id(__class__)

    @staticmethod
    def set(value):
        return Sense.set(__class__, value)

    @staticmethod
    def get():
        return Sense.get(__class__)

    @staticmethod
    def publish(value=None):
        return Sense.publish(__class__, value)

    @staticmethod
    def subscribe(subscriber):
        return Sense.subscribe(__class__, subscriber)

    @staticmethod
    def listen(segment):
        r.listen_in_background(source=sr.Microphone(), callback=__class__.parse, phrase_time_limit=segment)

    @staticmethod
    def parse(selfR, audio):
        try:
            parsed = audio.sample_rate
            #__class__.set(parsed)
            __class__.publish(parsed)
            return True
        except:
            #__class__.set('')
            return False


r = sr.Recognizer()
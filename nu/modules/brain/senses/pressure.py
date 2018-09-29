# Sense Hat Environment

from nu.modules.sense import Sense


class Pressure:

    CHANNEL = 'pressure'
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
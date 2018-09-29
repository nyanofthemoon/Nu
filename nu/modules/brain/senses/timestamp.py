# System Date and Time

from time import time
from nu.modules.sense import Sense


class Timestamp:

    CHANNEL = 'timestamp'
    CHANNEL_TYPE = 'brain'

    @staticmethod
    def id():
        return Sense.id(__class__)

    @staticmethod
    def publish(value=None):
        if (value == None):
            value = time()
        return Sense.publish(__class__, value)

    @staticmethod
    def subscribe(handler):
        return Sense.subscribe(__class__, handler)

    @staticmethod
    def unsubscribe():
        return Sense.unsubscribe(__class__)

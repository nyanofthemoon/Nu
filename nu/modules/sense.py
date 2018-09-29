# Abstract Sense

import logging
from nu.modules.brain.smemory import SMemoryStorage, SMemoryPubSub

logger = logging.getLogger()


class Sense:

    NAMESPACE = 'sense'

    @staticmethod
    def id(child):
        return __class__.NAMESPACE + '.' + child.CHANNEL_TYPE + '.' + child.CHANNEL

    @staticmethod
    def name(child):
        return str(child.__module__)

    @staticmethod
    def get(child):
        uid = __class__.id(child)
        return SMemoryStorage.get(uid)

    @staticmethod
    def set(child, current):
        previous = __class__.get(child)
        if (current != previous):
            uid = __class__.id(child)
            SMemoryStorage.set(uid, current)

    @staticmethod
    def publish(child, message=None):
        channel = __class__.id(child)
        if message == None:
            message   = __class__.get(child)
        SMemoryStorage.publish(channel, message)
        logger.debug('Published to ' + channel + ' ' + str(message))

    @staticmethod
    def subscribe(child, handler):
        channel = __class__.id(child)
        SMemoryPubSub.subscribe(**{channel: handler})
        logger.debug('Subscribed to ' + channel)

    @staticmethod
    def unsubscribe(child):
        channel = __class__.id(child)
        logger.debug('Unsubscribed from ' + channel)
        SMemoryPubSub.unsubscribe(channel)

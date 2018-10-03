# Cuckoo Clock

from time import time
from datetime import datetime, timedelta
from random import SystemRandom

from nu.modules.body.executor import ExecutableActions
from nu.modules.skill import Skill
from nu.modules.config import skill_config
from nu.modules.config import nu_config

config = skill_config()
nuConfig = nu_config()


class Clock:

    SUBSCRIPTIONS = ['BrainSenseTimestamp']
    PRIORITY = int(config.get('ClockSkill', 'priority'))
    EXPIRATION = int(config.get('ClockSkill', 'expiration'))

    def __init__(self):
        self.announce_every = int(config.get('ClockSkill', 'every'))
        self.current = time()
        self._setNext()

    def _setNext(self):
        self.next = self.current + timedelta(hours=self.announce_every).seconds

    def handle_message(self, message):
        self.current = int(float(message.get('data').decode()))
        if self.current >= self.next:
            text = SystemRandom().choice([
                "It is now %-I %p",
                "It's %-I %p already",
                'Ding ding, the clock says %-I %p',
                'The clock ticks, it is %-I %p'
                'The time is now %-I %p'
            ])

            payload = Skill.payload()
            payload.append(Skill.message(ExecutableActions.SPEAK_SLOW, {'text': datetime.fromtimestamp(self.current).strftime(text)}))
            Skill.enqueue(__class__, payload)
            self._setNext()

    def handle_failure(self, action, params):
        return Skill.handle_failure(action, params)

    def handle_success(self, action, params):
        return Skill.handle_success(action, params)


ClockSkill = Clock()

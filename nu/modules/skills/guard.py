# Guard

from nu.modules.skill import Skill
from nu.modules.config import skill_config
from nu.modules.config import nu_config

config = skill_config()
nuConfig = nu_config()

import logging
logger = logging.getLogger()


class Guard:

    SUBSCRIPTIONS = ['BrainSenseFace']
    PRIORITY = int(config.get('GuardSkill', 'priority'))
    EXPIRATION = int(config.get('GuardSkill', 'expiration'))

    def __init__(self):
        self.owner_is_around = None
        self.last_seen_face = None

    def handle_message(self, message):
        logger.warning(message)
        return True

    def handle_failure(self, action, params):
        return Skill.handle_failure(action, params)

    def handle_success(self, action, params):
        return Skill.handle_success(action, params)


GuardSkill = Guard()

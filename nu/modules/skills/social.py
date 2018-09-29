# Social - People

from nu.modules.skill import Skill
from nu.modules.config import skill_config
from nu.modules.config import nu_config

config = skill_config()
nuConfig = nu_config()

import logging
logger = logging.getLogger()



class Social:

    SUBSCRIPTIONS = ['BrainSenseFace']
    PRIORITY = int(config.get('SocialSkill', 'priority'))
    EXPIRATION = int(config.get('SocialSkill', 'expiration'))
    OWNER_NAME = nuConfig.get('owner', 'name')

    def __init__(self):
        self.people = {}

    def handle_message(self, message):
        logger.warning(message)
        return True

    def handle_failure(self, action, params):
        return Skill.handle_failure(action, params)

    def handle_success(self, action, params):
        return Skill.handle_success(action, params)


SocialSkill = Social()

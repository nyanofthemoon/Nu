# https://gist.github.com/raproenca/ed1ab47c47da246512ef4d2f19cf2611
# React to voice input and attempt conversation

from nu.modules.skill import Skill
from nu.modules.config import skill_config

config = skill_config()


class Conversation:

    SUBSCRIPTIONS = ['BrainSenseText2Speech']
    PRIORITY = int(config.get('ConversationSkill', 'priority'))
    EXPIRATION = int(config.get('ConversationSkill', 'expiration'))

    def handle_message(self, message):
        return True

    def handle_failure(self, action, params):
        return Skill.handle_failure(action, params)

    def handle_success(self, action, params):
        return Skill.handle_success(action, params)


ConversationSkill = Conversation()

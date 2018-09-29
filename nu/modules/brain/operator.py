# Logic Operator - Runs Priority Queue!

import logging
from time import time
from .smemory import SMemoryEntry
from nu.modules.body.executor import Executor
from nu.modules.skills import *

logger = logging.getLogger()


class Operator:

    def __init__(self, executor: Executor):
        self.executor = executor

    def handle_entry(self, entry: SMemoryEntry):
        if entry.expiry >= time():

            if entry.freeplay == False:
                self.executor.disable_freeplay()

            logger.info('Operator running ' + str(entry.name) + ' with updates')

            op_result = None
            op_class = entry.name + 'Skill'

            for operation in entry.payload:
                try:
                    op_action = operation.get('action')
                    op_params = operation.get('params')
                    if op_params != {}:
                        logger.debug('Operator executing ' + op_action + ' using ' + str(op_params))
                        op_result = getattr(self.executor, op_action)(**op_params)
                    else:
                        logger.debug('Operator executing ' + op_action)
                        op_result = getattr(self.executor, op_action)()
                except Exception as op_ex:
                    logger.warning(str(op_ex))

            if op_result != None:
                if op_result == True:
                    logger.debug('Operator ending with handle_success')
                    getattr(globals()[op_class], 'handle_success')(op_action, op_params)
                else:
                    logger.debug('Operator ending with handle_failure')
                    getattr(globals()[op_class], 'handle_failure')(op_action, op_params)

            self.executor.enable_freeplay()

        else:
            logger.info('Operator expired ' + str(entry.name))

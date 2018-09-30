# Logic Operator - Runs Priority Queue!

import logging
from time import time, sleep
from .smemory import SMemoryEntry
from nu.modules.body.executor import Executor
from nu.modules.skills import *

logger = logging.getLogger()


class Operator:

    def __init__(self, executor: Executor):
        self.executor = executor

    def handle_entry(self, entry: SMemoryEntry):
        if entry.expiry >= time():

            logger.info('Operator running ' + str(entry.name) + ' with updates')

            op_result = None
            op_class = entry.name + 'Skill'

            for operation in entry.payload:
                try:
                    op_action = operation.get('action')
                    op_params = operation.get('params')
                    op_sleep = operation.get('sleep')
                    if op_params != {}:
                        logger.debug('Operator executing ' + op_action + ' using ' + str(op_params))
                        op_result = getattr(self.executor, op_action)(**op_params)
                    else:
                        logger.debug('Operator executing ' + op_action)
                        op_result = getattr(self.executor, op_action)()
                    if op_sleep > 0:
                        logger.debug('Operator sleeping for ' + str(op_sleep) + ' seconds...')
                        sleep(op_sleep)
                except Exception as op_ex:
                    logger.warning(str(op_ex))

            if op_result != None:
                if op_result == True:
                    logger.debug('Operator ending with handle_success')
                    getattr(globals()[op_class], 'handle_success')(op_action, op_params)
                else:
                    logger.debug('Operator ending with handle_failure')
                    getattr(globals()[op_class], 'handle_failure')(op_action, op_params)

        else:
            logger.info('Operator expired ' + str(entry.name))

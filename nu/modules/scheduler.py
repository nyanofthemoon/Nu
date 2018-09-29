# Periodic Scheduler

import sched
from time import time, sleep

class Scheduler:

    def __init__(self):
        self.tasks = {}
        self.scheduler = sched.scheduler(time, sleep)

    def add(self, interval, action, actionargs=()):
        action(*actionargs)
        id = self.scheduler.enter(interval, 1, self.add, (interval, action, actionargs))
        self.tasks.update({action: id})

    def start(self):
        self.scheduler.run()

    def stop(self):
        for action, id in self.tasks:
            self.remove(id)

    def remove(self, uid):
        self.scheduler.cancel(uid)

# Short-term memory (PriorityQueue)

import redis
from queue import PriorityQueue
from threading import Thread
from nu.modules.config import smemory_config

class SMemoryStorageManager():

    def __init__(self):
        config = smemory_config()
        hostname = config.get('sense', 'hostname')
        port = config.get('sense', 'port')
        database = config.get('sense', 'database')
        pool = redis.ConnectionPool(host=hostname, port=port, db=database)
        self.storage = redis.Redis(connection_pool=pool)
        self.pubsub = self.storage.pubsub(ignore_subscribe_messages=True)

SMemoryStorageManagerInstance = SMemoryStorageManager()
SMemoryStorage = SMemoryStorageManagerInstance.storage
SMemoryPubSub = SMemoryStorageManagerInstance.pubsub


class SMemoryEntry:

    def __init__(self, name, priority, expiry, payload):
        self.name = name
        self.priority = priority
        self.expiry = expiry
        self.payload = payload

    def __eq__(self, other):
        try:
            return self.priority == other.priority
        except AttributeError:
            return NotImplemented

    def __lt__(self, other):
        try:
            return self.priority < other.priority
        except AttributeError:
            return NotImplemented


class SMemoryQueueManager:

    def __init__(self):
        self.queue = PriorityQueue()
        self.queueThread = None

    def start(self, callback):
        self.queueThread = Thread(target=self.processEntry, args=(self.queue, callback), daemon=True)
        self.queueThread.start()
        self.queue.join()

    def processEntry(self, queue, callback):
        while True:
            next = queue.get()
            callback(next)
            queue.task_done()

    def stop(self):
        self.thread._stop()

    def flush(self):
        self.queue.empty()

    def put(self, name, priority, expiry, payload):
        self.queue.put(SMemoryEntry(name, priority, expiry, payload))

    def get(self):
        return self.queue.get()

SMemoryQueue = SMemoryQueueManager()

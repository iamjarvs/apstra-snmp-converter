"""
Message queue abstraction for Apstra SNMP converter.
Handles queuing and prioritisation.
"""
from core.redis_store import RedisStore
from typing import Dict, Any
import logging

class MessageQueue:
    def __init__(self, redis_store: RedisStore, queue_name: str):
        self.redis_store = redis_store
        self.queue_name = queue_name
        self.logger = logging.getLogger('apstra_snmp_converter')

    def enqueue(self, message: Dict[str, Any]):
        self.redis_store.queue_message(self.queue_name, message)
        queue_length = self.redis_store.client.llen(self.queue_name)
        self.logger.debug(f"Enqueued message to {self.queue_name}. Queue length is now {queue_length}.")

    def dequeue(self, timeout: int = 1) -> Dict[str, Any]:
        msg = self.redis_store.process_message(self.queue_name, timeout)
        queue_length = self.redis_store.client.llen(self.queue_name)
        if msg:
            self.logger.debug(f"Dequeued message from {self.queue_name}. Queue length is now {queue_length}.")
        return msg

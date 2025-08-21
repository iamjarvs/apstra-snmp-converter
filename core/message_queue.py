"""
Message queue abstraction for Apstra SNMP converter.
Handles queuing and prioritisation.
"""
from core.redis_store import RedisStore
from typing import Dict, Any

class MessageQueue:
    def __init__(self, redis_store: RedisStore, queue_name: str):
        self.redis_store = redis_store
        self.queue_name = queue_name

    def enqueue(self, message: Dict[str, Any]):
        self.redis_store.queue_message(self.queue_name, message)

    def dequeue(self, timeout: int = 1) -> Dict[str, Any]:
        return self.redis_store.process_message(self.queue_name, timeout)

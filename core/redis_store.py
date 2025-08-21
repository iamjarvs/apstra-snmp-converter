"""
Redis state and queue management for Apstra SNMP converter.
"""
import redis
import json
from typing import Any, Dict, Optional

class RedisStore:
    def __init__(self, host: str, port: int, db: int, password: str = None, pool_size: int = 10):
        self.pool = redis.ConnectionPool(host=host, port=port, db=db, password=password, max_connections=pool_size)
        self.client = redis.Redis(connection_pool=self.pool)

    def set_task_state(self, key: str, value: Dict[str, Any], ttl: Optional[int] = None):
        self.client.set(key, json.dumps(value))
        if ttl:
            self.client.expire(key, ttl)

    def get_task_state(self, key: str) -> Optional[Dict[str, Any]]:
        val = self.client.get(key)
        if val:
            return json.loads(val)
        return None

    def queue_message(self, queue: str, message: Dict[str, Any]):
        self.client.lpush(queue, json.dumps(message))

    def process_message(self, queue: str, timeout: int = 1) -> Optional[Dict[str, Any]]:
        msg = self.client.brpop(queue, timeout=timeout)
        if msg:
            return json.loads(msg[1])
        return None

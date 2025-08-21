"""
Extensible delivery interface for Apstra SNMP converter.
Add new delivery methods (e.g., SNMP, webhook, Kafka) by implementing DeliveryMethod.
"""
from typing import Dict, Any

class DeliveryMethod:
    def send(self, message: Dict[str, Any]) -> bool:
        """Send a message using this delivery method."""
        raise NotImplementedError()

# Registry for delivery methods
DELIVERY_METHODS = {}

def register_delivery_method(name: str, method: DeliveryMethod):
    DELIVERY_METHODS[name] = method

def get_delivery_method(name: str) -> DeliveryMethod:
    return DELIVERY_METHODS[name]

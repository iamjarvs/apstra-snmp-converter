"""
SNMP trap sender for Apstra SNMP converter.
Implements DeliveryMethod for SNMP.
"""
import subprocess
from core.delivery import DeliveryMethod, register_delivery_method
from typing import Dict, Any
import logging

class SNMPTrapSender(DeliveryMethod):
    def __init__(self, destinations, oids):
        self.destinations = destinations
        self.oids = oids
        self.logger = logging.getLogger('apstra_snmp_converter')

    def send(self, message: Dict[str, Any]) -> bool:
        event_type = message.get('type')
        if event_type == 'alert_probe':
            enterprise_oid = f"{self.oids['base_oid']}.{self.oids['alert_probe']}"
            var_binds = [
                (f"{enterprise_oid}.1", 's', message.get('alertId', '')),
                (f"{enterprise_oid}.2", 's', message.get('blueprintLabel', '')),
                (f"{enterprise_oid}.3", 'i', message.get('severity', 0)),
                (f"{enterprise_oid}.4", 's', message.get('probeLabel', '')),
                (f"{enterprise_oid}.5", 'i', message.get('actualValue', 0)),
                (f"{enterprise_oid}.6", 'i', message.get('expectedMax', 0)),
                (f"{enterprise_oid}.7", 's', message.get('timestamp', '')),
            ]
        elif event_type == 'audit_event':
            enterprise_oid = f"{self.oids['base_oid']}.{self.oids['audit_event']}"
            var_binds = [
                (f"{enterprise_oid}.1", 's', message.get('eventCategory', '')),
                (f"{enterprise_oid}.2", 's', message.get('sourceIP', '')),
                (f"{enterprise_oid}.3", 's', message.get('username', '')),
                (f"{enterprise_oid}.4", 's', message.get('action', '')),
                (f"{enterprise_oid}.5", 's', message.get('timestamp', '')),
            ]
        elif event_type == 'task_event':
            enterprise_oid = f"{self.oids['base_oid']}.{self.oids['task_event']}"
            var_binds = [
                (f"{enterprise_oid}.1", 's', message.get('taskId', '')),
                (f"{enterprise_oid}.2", 's', message.get('blueprintId', '')),
                (f"{enterprise_oid}.3", 's', message.get('taskType', '')),
                (f"{enterprise_oid}.4", 's', message.get('status', '')),
                (f"{enterprise_oid}.5", 's', message.get('username', '')),
                (f"{enterprise_oid}.6", 's', message.get('userIP', '')),
                (f"{enterprise_oid}.7", 's', message.get('beginAt', '')),
                (f"{enterprise_oid}.8", 's', message.get('lastUpdatedAt', '')),
            ]
        else:
            self.logger.error(f"Unknown SNMP trap event type: {event_type}")
            return False

        success = True
        for dest in self.destinations:
            cmd = [
                'snmptrap',
                '-v', dest.get('version', '2c'),
                '-c', dest['community'],
                f"{dest['host']}:{dest.get('port', 162)}",
                '',  # enterprise OID (empty for SNMPv2c)
                enterprise_oid,
            ]
            for oid, vtype, value in var_binds:
                cmd.extend([oid, vtype, str(value)])
            try:
                self.logger.debug(f"Running SNMP trap command: {' '.join(cmd)}")
                result = subprocess.run(cmd, capture_output=True, text=True)
                if result.returncode != 0:
                    self.logger.error(f"SNMP trap send error: {result.stderr}")
                    success = False
                else:
                    self.logger.debug(f"Sent SNMP trap to {dest['host']}:{dest.get('port', 162)} for event {event_type} with varBinds: {var_binds}")
            except Exception as e:
                self.logger.error(f"Exception sending SNMP trap to {dest['host']}:{dest.get('port', 162)}: {e}")
                success = False
        return success

# Register SNMP delivery method
register_delivery_method('snmp', SNMPTrapSender)

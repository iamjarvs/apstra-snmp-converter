import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.snmp_sender import SNMPTrapSender
import yaml

# Load SNMP config from the main config file
with open('config/apstra_snmp_config.yaml') as f:
    config = yaml.safe_load(f)
snmp_cfg = config['snmp']
sender = SNMPTrapSender(snmp_cfg['destinations'], snmp_cfg['oids'])

def test_send_alert_probe():
    message = {
        'type': 'alert_probe',
        'alertId': 'test-alert-001',
        'blueprintLabel': 'test-blueprint',
        'severity': 3,
        'probeLabel': 'leaf_to_spine_interface_statuses',
        'actualValue': 83,
        'expectedMax': 99,
        'timestamp': '2025-08-21T10:00:00.000000Z'
    }
    result = sender.send(message)
    print('Alert probe SNMP trap result:', result)

def test_send_audit_event():
    message = {
        'type': 'audit_event',
        'eventCategory': 'Logout',
        'sourceIP': '172.24.212.62',
        'username': 'admin',
        'action': 'Success',
        'timestamp': '2025-08-21T10:00:00.000000Z'
    }
    result = sender.send(message)
    print('Audit event SNMP trap result:', result)

def test_send_task_event():
    message = {
        'type': 'task_event',
        'taskId': 'test-task-001',
        'blueprintId': 'a7c2cd1d-da6e-4c3c-8e34-acbd131d3e76',
        'taskType': 'blueprint.deploy',
        'status': 'succeeded',
        'username': 'admin',
        'userIP': '10.104.57.20',
        'beginAt': '2025-08-21T10:00:00.000000Z',
        'lastUpdatedAt': '2025-08-21T10:01:00.000000Z'
    }
    result = sender.send(message)
    print('Task event SNMP trap result:', result)

if __name__ == '__main__':
    test_send_alert_probe()
    test_send_audit_event()
    test_send_task_event()

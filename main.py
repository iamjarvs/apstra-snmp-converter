"""
Main entry point for Apstra syslog/API to SNMP converter.
"""
import yaml
import logging
from logging_config import setup_logging
from core.syslog_parser import parse_syslog_message
from core.api_client import ApstraAPIClient
from core.redis_store import RedisStore
from core.message_queue import MessageQueue
from core.delivery import get_delivery_method

CONFIG_PATH = 'config/apstra_snmp_config.yaml'

def load_config(path):
    with open(path) as f:
        return yaml.safe_load(f)

def main():
    config = load_config(CONFIG_PATH)
    setup_logging(config['application']['log_level'], config['application']['log_file'])
    logger = logging.getLogger('apstra_snmp_converter')

    # Redis setup
    redis_cfg = config['redis']
    redis_store = RedisStore(
        host=redis_cfg['host'],
        port=redis_cfg['port'],
        db=redis_cfg['db'],
        password=redis_cfg.get('password'),
        pool_size=redis_cfg.get('connection_pool_size', 10)
    )
    queue = MessageQueue(redis_store, redis_cfg['keys']['message_queue'])

    # API client setup
    apstra_cfg = config['apstra']
    api_client = ApstraAPIClient(
        host=apstra_cfg['host'],
        username=apstra_cfg['username'],
        password=apstra_cfg['password'],
        timeout=apstra_cfg.get('api_timeout', 10)
    )

    # SNMP delivery setup
    snmp_cfg = config['snmp']
    snmp_sender = get_delivery_method('snmp')(snmp_cfg['destinations'], snmp_cfg['oids'])

    # Main loop stub (polling, syslog, queue processing)
    logger.info('Apstra SNMP converter started.')
    # ...existing code for polling, syslog listening, queue processing...

if __name__ == '__main__':
    main()

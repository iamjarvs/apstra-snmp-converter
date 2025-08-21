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
import core.snmp_sender
import argparse
import time


CONFIG_PATH = 'config/apstra_snmp_config.yaml'

def load_config(path):
    with open(path) as f:
        return yaml.safe_load(f)

def main():
    parser = argparse.ArgumentParser(description='Apstra syslog/API to SNMP converter')
    parser.add_argument('-v', '--verbose', action='count', default=0,
                        help='Increase output verbosity (-v, -vv, -vvv)')
    args = parser.parse_args()

    config = load_config(CONFIG_PATH)

    # Map verbosity to logging level
    if args.verbose == 0:
        log_level = config['application'].get('log_level', 'INFO')
    elif args.verbose == 1:
        log_level = 'INFO'
    elif args.verbose == 2:
        log_level = 'DEBUG'
    else:
        log_level = 'DEBUG'

    setup_logging(log_level, config['application']['log_file'])
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

    logger.info('Apstra SNMP converter started.')
    logger.debug('Loaded configuration: %s', config)

    poll_interval = apstra_cfg.get('poll_interval', 30)
    while True:
        for blueprint in apstra_cfg['blueprints']:
            if blueprint.get('enabled'):
                blueprint_id = blueprint['id']
                blueprint_name = blueprint.get('name', blueprint_id)
                logger.info(f"Polling tasks for blueprint {blueprint_name} ({blueprint_id})")
                try:
                    tasks = api_client.get_tasks(blueprint_id)
                    logger.debug(f"API response for blueprint {blueprint_id}: {tasks}")
                    # TODO: Process tasks, queue messages, send SNMP traps
                except Exception as e:
                    logger.error(f"Error polling tasks for blueprint {blueprint_id}: {e}")
        logger.info(f"Sleeping for {poll_interval} seconds before next poll.")
        time.sleep(poll_interval)

if __name__ == '__main__':
    main()

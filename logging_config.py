import logging
import logging.config

def setup_logging(log_level: str, log_file: str):
    logging.basicConfig(
        level=getattr(logging, log_level.upper(), logging.INFO),
        format='%(asctime)s %(levelname)s %(name)s %(message)s',
        handlers=[logging.FileHandler(log_file), logging.StreamHandler()]
    )

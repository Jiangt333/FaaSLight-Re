import logging
import numpy as np
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.info('Loading function')

def lambda_handler(event, context):
    print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/main.py=lambda_handler=12')
    lib_version = {'numpy': np.__version__}
    logger.info(lib_version)
    return lib_version


import logging
import numpy as np
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.info('Loading function')

def lambda_handler(event, context):
    lib_version = {'numpy': np.__version__}
    logger.info(lib_version)
    return lib_version

# if __name__ == "__main__":
#     lambda_handler(None, None)
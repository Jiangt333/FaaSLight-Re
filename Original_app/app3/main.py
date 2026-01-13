import time
init_st = time.time() * 1000
import logging
import numpy as np
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.info('Loading function')
init_ed = time.time() * 1000

def lambda_handler(event, context):
    fun_st = time.time() * 1000
    print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/main.py=lambda_handler=12')
    lib_version = {'numpy': np.__version__}
    logger.info(lib_version)
    fun_ed = time.time() * 1000
    return ',InitStart:{},'.format(init_st) + 'InitEnd:{},'.format(init_ed) + 'functionStart:{},'.format(fun_st) + 'functionEnd:{},'.format(fun_ed)


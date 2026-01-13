import time
# 记录初始化开始时间
init_st = time.time() * 1000

import logging
import numpy as np

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.info('Loading function')

# 记录初始化结束时间
init_ed = time.time() * 1000

def lambda_handler(event, context):
    # 记录函数逻辑开始时间
    fun_st = time.time() * 1000
    
    print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/main.py=lambda_handler=12')
    
    lib_version = {'numpy': np.__version__}
    logger.info(lib_version)
    
    # 记录函数逻辑结束时间
    fun_ed = time.time() * 1000

    # 计算初始化总耗时 (Cold Start 期间的加载时间)
    init_interval = init_ed - init_st
    # 计算函数实际执行耗时
    fun_interval = fun_ed - fun_st

    result = {
        "InitStart": init_st,
        "InitEnd": init_ed,
        "InitInterval_ms": init_interval,
        "FunctionStart": fun_st,
        "FunctionEnd": fun_ed,
        "FunctionInterval_ms": fun_interval,
        "TotalInterval_ms": (fun_ed - init_st) # 从进程启动到执行结束的总时间
    }
    
    logger.info(f"Performance Metrics: {result}")
    
    return (
        'InitStart:{},'.format(init_st) + 
        'InitEnd:{},'.format(init_ed) + 
        'InitInterval:{:.2f}ms,'.format(init_interval) + 
        'functionStart:{},'.format(fun_st) + 
        'functionEnd:{},'.format(fun_ed) + 
        'functionInterval:{:.2f}ms'.format(fun_interval)
    )

# if __name__ == "__main__":
#     lambda_handler(None, None)
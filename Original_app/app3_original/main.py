import time
# 记录整个容器初始化的开始时间
init_st = time.time() * 1000

import logging
import numpy as np

# --- 关键修改：定义冷启动标志 ---
# 只有在容器第一次创建时，这段代码才会执行
IS_COLD_START = True 

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.info('Loading function')

init_ed = time.time() * 1000

def lambda_handler(event, context):
    global IS_COLD_START  # 引用全局变量
    
    # 记录函数逻辑开始时间
    fun_st = time.time() * 1000
    
    # 判断启动类型
    start_type = "Cold Start" if IS_COLD_START else "Warm Start"
    
    print(f'Execution Type: {start_type}')
    print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/main.py=lambda_handler=12')
    
    try:
        lib_version = {'numpy': getattr(np, '__version__', 'Attribute missing')}
    except Exception as e:
        lib_version = {'error': str(e)}
    
    logger.info(lib_version)
    
    fun_ed = time.time() * 1000

    init_interval = init_ed - init_st
    fun_interval = fun_ed - fun_st

    result = {
        "StartType": start_type,
        "InitInterval_ms": init_interval,
        "FunctionInterval_ms": fun_interval,
        "TotalInterval_ms": (fun_ed - init_st) if IS_COLD_START else fun_interval
    }
    
    logger.info(f"Performance Metrics: {result}")
    
    # --- 关键修改：执行一次后将标志置为 False ---
    # 下一次调用同一个 Lambda 实例时，IS_COLD_START 已经是 False 了
    IS_COLD_START = False 

    return (
        'StartType:{},'.format(start_type) +
        'InitInterval:{:.2f}ms,'.format(init_interval) + 
        'functionInterval:{:.2f}ms,'.format(fun_interval) +
        'numpy_version:{}'.format(lib_version.get('numpy', 'Error'))
    )
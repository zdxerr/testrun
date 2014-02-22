import os
import random
import multiprocessing
import time
import logging
from pprint import pprint
from datetime import timedelta

logging.basicConfig(format='%(asctime)s - %(levelname)s/%(processName)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

def __get_logger(name):
    l = logger.getChild(name)
    # logger = logging.getLogger(name)
    l.setLevel(logging.INFO)
    file_handler = logging.FileHandler(
        os.path.join(os.getcwd(), 'testlogs', name + '.log'), mode='a', 
        encoding=None, delay=False)
    l.addHandler(file_handler)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    return l

def work(module_name, functions, running_functions, running_functions_changed, 
         lock):
    try:
        module_logger = __get_logger(module_name)
        module_logger.propagate = False

        name = multiprocessing.current_process().name
        module_logger.info("worker %s: %s", name, module_name)
        for func, wait in functions:
            module_logger.info('ready %s.%s', module_name, func)

            while True:
                with lock:
                    if func not in running_functions:
                        running_functions.append(func)
                        break
                    running_functions_changed.clear()
                if not running_functions_changed.wait(600):
                    module_logger.warn('timeout %s.%s', module_name, func)
                    return False

            module_logger.info('start %s.%s', module_name, func)
            time.sleep(wait)
            module_logger.info('finish %s.%s', module_name, func)

            with lock:
                running_functions.remove(func)
                running_functions_changed.set()

        return True

    except:
        logger.exception("EXC", exc_info=True)


if __name__ == '__main__':
    started = time.time()
    ranges = [(0.01, 0.03), (0.05, 0.08), (0.06, 0.07), (0.08, 0.35)]
    modules = {}
    for i in range(200):
        modules['t_%.6d' % (i, )] = [
            ('t%d' % (level + 1, ), random.uniform(*ranges[level])) 
            for level in range(0, 4)
        ]

    expected_duration = 0
    for functions in modules.values():
        for __, duration in functions:
            expected_duration += duration

    expected_duration = timedelta(seconds=expected_duration)


    mgr = multiprocessing.Manager()
    running_functions = mgr.list()
    running_functions_changed = mgr.Event()
    mutex = mgr.Lock()

    pool = multiprocessing.Pool(8)

    results = []
    logger.warn("expected duration %s", expected_duration)

    # map_async(func, iterable[, chunksize[, callback]])

    for name, functions in modules.items():
        results.append(pool.apply_async(work, (name, functions, running_functions, 
                                        running_functions_changed, mutex)))
        logger.warn("appended %s", name)

    pool.close() # no more tasks
    pool.join()  # wrap up current tasks

    # for r in results:
    #     print(r, r.get(), r.successful())

    logger.warn("expected duration %s", expected_duration)
    duration = timedelta(seconds=time.time() - started)
    logger.warn("duration %s", duration)


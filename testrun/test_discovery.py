
import os
import imp
import sys
import inspect
import multiprocessing
from collections import OrderedDict
from pprint import pprint

from datetime import datetime

logger = multiprocessing.log_to_stderr()
# logger.setLevel(multiprocessing.SUBDEBUG)

__FILE_EXTENSIONS = ('.py', )

def __load_module(path):
    search_path, filename = os.path.split(path)
    module_name, ext = filename.rsplit('.', 1)

    try:
        fp, pathname, description = imp.find_module(module_name, [search_path])
        return imp.load_module(module_name, fp, pathname, description)
    except SyntaxError:
        print('SYNTAX ERROR')
    finally:
        if fp:
            fp.close()


def __get_functions(module):
    return OrderedDict(inspect.getmembers(module, inspect.isfunction))


def __get_possible_test_files(search_path):
    for path, folders, files in os.walk(search_path):
        for filename in files:
            if filename.endswith(__FILE_EXTENSIONS):
                yield os.path.join(path, filename)


lock = multiprocessing.Lock()

def execute_test(testfile):
    try:
        result = []

        module = __load_module(testfile)
        print(module)
        for fn, f in __get_functions(module).items():
            lock.acquire()
            print('start %r %r %r', module, fn, datetime.now())
            f()
            print('finish  %r %r %r', module, fn, datetime.now())
            lock.release()
    except Exception as exc:
        print('EXC', exc)


if __name__ == '__main__':
    pool_size = multiprocessing.cpu_count() * 2
    pool = multiprocessing.Pool(processes=pool_size)


    for testfile in __get_possible_test_files(r'e:\test'):
        pool.apply_async(execute_test, (testfile, ))

    pool.close() # no more tasks
    pool.join()  # wrap up current tasks

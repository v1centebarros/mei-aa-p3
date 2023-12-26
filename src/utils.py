import logging
import time
from collections import namedtuple

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
log = logging.getLogger(__name__)
Result = namedtuple('Result', ['time', 'result', 'algorithm'])


def benchmark(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        return Result(time.time() - start, result, func.__name__)

    return wrapper

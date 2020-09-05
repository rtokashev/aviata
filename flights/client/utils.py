import time
import logging


logging.basicConfig(level=logging.INFO,
                    format='{"level": "%(levelname)s", "name": "%(name)s", "msg": "%(message)s", time":"%(asctime)s"}',
                    datefmt='%Y-%m-%dT%H:%M:%S')


def get_logger(name: str):
    return logging.getLogger(name)


def timeit(f, logger=get_logger(__name__)):
    def timed(*args, **kw):
        ts = time.time()
        result = f(*args, **kw)
        te = time.time()
        logger.info(f'func:{f.__name__} took: {te-ts} sec')
        return result
    return timed

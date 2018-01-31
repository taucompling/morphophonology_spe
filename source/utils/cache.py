from redis import Redis
import pickle
from functools import wraps
from ga_config import CACHE_TYPE


def graceful_fail(func):
    @wraps(func)
    def gracefully_fail(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except:
            return None

    return gracefully_fail


class MemCache:
    def __init__(self):
        self.cache = {}

    def set(self, key, val, prefix=''):
        key = '{}_{}'.format(prefix, key)
        self.cache[key] = val

    def get(self, key, prefix=''):
        key = '{}_{}'.format(prefix, key)
        return self.cache.get(key, None)


class RedisCache:
    def __init__(self):
        self.db = Redis()
        self.db.flushdb()

    @graceful_fail
    def set(self, key, val, prefix=''):
        key = '{}_{}'.format(prefix, key)
        pickled_val = pickle.dumps(val)
        return self.db.set(key, pickled_val)

    @graceful_fail
    def get(self, key, prefix=''):
        key = '{}_{}'.format(prefix, key)
        s = self.db.get(key)
        if s:
            return pickle.loads(s)
        return s


class NoCache:
    def __init__(self):
        pass

    def set(self, *args, **kwrags):
        return None

    def get(self, *args, **kwargs):
        return None


if CACHE_TYPE == 'mem':
    Cache = MemCache
elif CACHE_TYPE == 'redis':
    Cache = RedisCache
elif CACHE_TYPE == 'none':
    Cache = NoCache
else:
    raise ValueError('Cache type {} not found'.format(CACHE_TYPE))

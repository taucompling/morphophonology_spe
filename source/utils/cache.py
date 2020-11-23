import pickle
from sys import stderr
from redis import Redis
from redis.exceptions import ConnectionError
from configuration import Singleton
from ga_config import CACHE_TYPE


class Cache(metaclass=Singleton):
    def set(self, key, val, prefix=''):
        raise NotImplementedError

    def get(self, key, prefix=''):
        raise NotImplementedError

    def flush(self):
        raise NotImplementedError

    @classmethod
    def get_cache(cls):
        if CACHE_TYPE == 'mem':
            return MemCache()
        elif CACHE_TYPE == 'redis':
            redis_cache = RedisCache()
            if redis_cache.is_server_available():
                return redis_cache
            else:
                print('Redis server not available, no cache will be used', file=stderr)
                return NoCache()
        elif CACHE_TYPE == 'none':
            return NoCache()
        else:
            raise ValueError('Cache type "{}" not found'.format(CACHE_TYPE))


class MemCache(Cache):
    def __init__(self):
        self.cache = {}

    def set(self, key, val, prefix=''):
        key = '{}_{}'.format(prefix, key)
        self.cache[key] = val

    def get(self, key, prefix=''):
        key = '{}_{}'.format(prefix, key)
        return self.cache.get(key, None)

    def flush(self):
        self.cache.clear()


class RedisCache(Cache):
    def __init__(self):
        self.db = Redis()

    def set(self, key, val, prefix=''):
        key = '{}_{}'.format(prefix, key)
        pickled_val = pickle.dumps(val)
        return self.db.set(key, pickled_val)

    def get(self, key, prefix=''):
        key = '{}_{}'.format(prefix, key)
        s = self.db.get(key)
        if s:
            return pickle.loads(s)
        return s

    def flush(self):
        self.db.flushall()

    def is_server_available(self):
        try:
            self.set('test_connection', 'test', 'test')
            return True
        except ConnectionError:
            return False


class NoCache(Cache):
    def set(self, *args, **kwrags):
        return None

    def get(self, *args, **kwargs):
        return None

    def flush(self):
        pass

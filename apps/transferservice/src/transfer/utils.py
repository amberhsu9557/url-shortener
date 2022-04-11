import redis
from src import cache
# from src import db

class URLShortener():
    db = redis.Redis(host='redis', port=6379, db=2)

    @classmethod
    @cache.cached(timeout=60 * 60 * 12, key_prefix="search_key")
    def get_from_db(cls, search_key):
        """
        Check the given search_key is in database or not
        """
        try:
            return cls.db.get(search_key)
        except:
            return None

    @classmethod
    def set_to_db(cls, search_key, url):

        """
        Set the given key-val to db, if failed return error message.
        """
        try:
            cls.db.set(search_key, url)
            return True
        except:
            return False

    @classmethod
    def rm_from_db(cls, key):
        """
        remove specify key from database
        """
        try:
            cls.db.delete(key)
            return True
        except:
            return False
import itertools

from django.core.exceptions import ImproperlyConfigured

from constance import settings, utils
from constance.backends import Backend

try:
    from cPickle import loads, dumps
except ImportError:
    from pickle import loads, dumps

try:
    from mongoengine import *
except ImportError:
    raise ImproperlyConfigured(
        "The Mongoengine backend requires mongoengine to be installed.")

class Constance(Document):
    key = StringField()
    value = StringField()

class MongoBackend(Backend):

    def __init__(self):
        super(MongoBackend, self).__init__()
        
    def get(self, key):
        try:
            value = Constance.objects.get(key=key)
        except:
            return None
        if value:
            return loads(value)
        return None

    def mget(self, keys):
        if not keys:
            return
        items = Constance.objects.filter(key__in=keys)
        if items.count() != 0:
            for item in items:
                yield item.key, loads(str(item.value))

    def set(self, key, value):
        try:
            item = Constance.objects.get(key=key)
            item.value = dumps(value)
            item.save()
        except:
            item = Constance(key=key, value=dumps(value))
            item.save()
        

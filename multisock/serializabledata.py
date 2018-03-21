#!/usr/bin/env python
# -*- coding: utf-8 -*-


import json
import inspect
try:
    from types import SimpleNamespace as Namespace
except ImportError:
    # Python 2.x fallback
    from argparse import Namespace

# Found at https://stackoverflow.com/questions/3768895/how-to-make-a-class-json-serializable
# More complex solution supporting class inheritance, data encapsulation and complex structures.
# Provides an alternative to the common pattern:
#   return json.dumps(instance, default=lambda o: o.__dict__, sort_keys=True, indent=2)
class ObjectEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, "to_json"):
            return self.default(obj.to_json())
        elif hasattr(obj, "__dict__"):
            d = dict(
                (key, value)
                for key, value in inspect.getmembers(obj)
                if not key.startswith("__")
                and not inspect.isabstract(value)
                and not inspect.isbuiltin(value)
                and not inspect.isfunction(value)
                and not inspect.isgenerator(value)
                and not inspect.isgeneratorfunction(value)
                and not inspect.ismethod(value)
                and not inspect.ismethoddescriptor(value)
                and not inspect.isroutine(value)
            )
            return self.default(d)
        return obj


class SerializableData():
    def toJSON(self):
        return json.dumps(self, cls=ObjectEncoder, indent=2, sort_keys=True)
    def __repr__(self):
        return self.toJSON()

    @staticmethod
    def fromJSON(_json):
        if _json is None: return None
        retval=SerializableData()
        retval=json.loads(_json, object_hook=lambda d: Namespace(**d))
        return retval

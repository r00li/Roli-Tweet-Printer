#
# Roli Tweet printer
# Written by Andrej Rolih, www.r00li.com
#

class _Singleton(type):
    # works in Python 2 & 3
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(_Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Singleton(_Singleton('SingletonMeta', (object,), {})): pass

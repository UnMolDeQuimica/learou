from .base import *

DEBUG = False

try:
    from .base import *
except ImportError:
    pass

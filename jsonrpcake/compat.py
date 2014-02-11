"""
Python 2/3 compatibility.

"""
#noinspection PyUnresolvedReferences
try:
    #noinspection PyUnresolvedReferences,PyCompatibility
    from urllib.parse import urlsplit
except ImportError:
    #noinspection PyUnresolvedReferences,PyCompatibility
    from urlparse import urlsplit

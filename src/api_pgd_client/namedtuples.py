from collections import namedtuple

HeaderItem = namedtuple("HeaderItem", ("name", "value"))
Endpoint = namedtuple("Endpoint", ("name", "path", "allowed_methods"))

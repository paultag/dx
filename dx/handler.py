
# {'ascii':   {'annotation': {'return': <class 'str'>, 'data': <class 'bytes'>},
#              'function': <function handler.<locals>._ at 0x7f78b13f9730>},
#  'rot13':   {'annotation': {'return': <class 'str'>, 'data': <class 'str'>},
#              'function': <function handler.<locals>._ at 0x7f78b13f9840>},
#  'i2bytes': {'annotation': {'return': <class 'bytes'>, 'data': [<class 'dx.handlers.ascii.ByteableInteger'>, Ellipsis]},
#              'function': <function handler.<locals>._ at 0x7f78b13f99d8>}}
from collections import defaultdict


class Node:
    edges = []
    def __init__(self, type_):
        self.type_ = type_

    def add_edge(self, target, callable_):
        self.edges.append((target, callable_))


def typesig_to_hash(sig):
    if isinstance(sig, list):
        return tuple(sig)
    return sig


class TypeDefaultDict(defaultdict):
    """ sigh """
    def __missing__(self, key):
        if self.default_factory is None:
            raise KeyError((key,))
        self[key] = value = self.default_factory(key)
        return value

TYPE_MAP = TypeDefaultDict(lambda x: Node(x))


def similar_type(t1, t2):
    t1, t2 = [typesig_to_hash(x) for x in [t1, t2]]
    if t1 == t2:
        return True
    if isinstance(t1, tuple) and isinstance(t2, tuple):
        (type1, _) = t1
        (type2, _) = t2
        if (isinstance(type1, TypeConstraint) and
                isinstance(type2, TypeConstraint)):
            return type1.type_ == type2.type_

        for x, y in [(type1, type2), (type2, type1)]:
            if issubclass(x, TypeConstraint):
                if x.type_ == y:
                    return True
    return False


def decode(in_t, out_t, data):
    print(TYPE_MAP)


class TypeConstraint:
    type_ = None
    @classmethod
    def validate(self, el):
        raise NotImplementedError("No implementation")


def validate_spec(spec, data):
    if isinstance(spec, list):
        type_, elip = spec
        data = list(data)
        for el in data:
            if issubclass(type_, TypeConstraint):
                valid = type_.validate(el)
                if not valid:
                    return None
                continue
            if not isinstance(el, type_):
                return None
        return data
    else:
        if isinstance(data, spec):
            return data


def handler(fn):
    ann = fn.__annotations__
    name = fn.__name__
    spec = ann['data']

    def _(*, data=None):
        for x in data:
            valid = validate_spec(spec, x)
            if valid is not None:
                yield from fn(data=valid)
    _.__name__ = name

    itype = ann['data']
    otype = ann['return']

    TYPE_MAP[typesig_to_hash(itype)].add_edge(otype, _)

    return _

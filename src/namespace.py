"""
pysettings.namespace

Houses Namespace object (extends dict)
"""


__all__ = ("Namespace", "as_namespace")

from collections import Mapping, Sequence

class _Dummy:
	pass
CLASS_ATTRS = dir(_Dummy)
del _Dummy


class Namespace(dict):
    """
    Namespace object subclasses dict object to expose
    entries as attributes.

    NOTE: attributes with iterable values are stored
    as nested Namespace objects.
    """

    def __init__(self, obj={}):
        super(Namespace, self).__init__()
        if isinstance(obj, dict):
            for k, v in obj.items():
                self[k] = v

    def __dir__(self):
        return tuple(self)

    def __repr__(self):
        return "%s(%s)" % (type(self).__name__, super(Namespace, self).__repr__())

    def __getattribute__(self, name):
        try:
            return self[name]
        except KeyError:
            msg = "'%s' object has no attribute '%s'"
            raise AttributeError(msg % (type(self).__name__, name))

    def __setitem__(self, key, value):
        """
        hijack dict.__setitem__() to "cast" nested dicts to Namespaces.
        Use object-recursing to ensure all dicts are stored as Namespaces.
        """
        if isinstance(value, dict):
            new = Namespace(value)
            value = new
        super(Namespace, self).__setitem__(key, value)

    def __setattr__(self, name, value):
        self[name] = value

    def __delattr__(self, name):
        del self[name]

    #------------------------
    # "copy constructors"

    @classmethod
    def from_object(cls, obj, names=None):
        if names is None:
            names = dir(obj)
        ns = {name:getattr(obj, name) for name in names}
        return cls(ns)

    @classmethod
    def from_mapping(cls, ns, names=None):
        if names:
            ns = {name:ns[name] for name in names}
        return cls(ns)

    @classmethod
    def from_sequence(cls, seq, names=None):
        if names:
            seq = {name:val for name, val in seq if name in names}
        return cls(seq)

    #------------------------
    # static methods

    @staticmethod
    def hasattr(ns, name):
        try:
            object.__getattribute__(ns, name)
        except AttributeError:
            return False
        return True

    @staticmethod
    def getattr(ns, name):
        return object.__getattribute__(ns, name)

    @staticmethod
    def setattr(ns, name, value):
        return object.__setattr__(ns, name, value)

    @staticmethod
    def delattr(ns, name):
        return object.__delattr__(ns, name)


def as_namespace(obj, names=None):

    # functions
    if isinstance(obj, type(as_namespace)):
        obj = obj()

    # special cases
    if isinstance(obj, type):
        names = (name for name in dir(obj) if name not in CLASS_ATTRS)
        return Namespace.from_object(obj, names)
    if isinstance(obj, Mapping):
        return Namespace.from_mapping(obj, names)
    if isinstance(obj, Sequence):
        return Namespace.from_sequence(obj, names)
    
    # default
    return Namespace.from_object(obj, names)
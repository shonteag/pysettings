"""
pysettings.__init__
Handler namespace registry.

Usage: ::
    
    # in package top-layer entry point
    import pysettings
    pysettings.loadfrom_yaml("package_key", "path/to/settings.yaml")

    # in package submodules or subpackages
    import pysettings
    nm = pysettings.get_namespace("package_key")
    # access (example):
    thing1 = nm.settings.attributes.thing1

"""

import yaml, json
from namespace import Namespace

__all__ = ('new_namespace',
		   'set_namespace',
		   'get_namespace',
		   'delete_namespace',
		   'clear_namespace',
		   'loadfrom_yaml',
		   'loadfrom_json')

"""
this is the top-layer of the tree.
this is where all keyed Namespace access will take place.
"""
REGISTRY = Namespace()

# access methods
def new_namespace(key):
	"""create a new, top level namespace"""
	if key in REGISTRY:
		raise KeyError("key:{0} already exists".format(key))

	REGISTRY[key] = Namespace()


def set_namespace(key, dic):
	"""set a namespace from a dict"""
	new_namespace(key)
	REGISTRY[key] = Namespace(dic)


def get_namespace(key):
	"""return a top level namespace"""
	if key not in REGISTRY:
		raise KeyError("key:{0} does not exist".format(key))

	return REGISTRY[key]


def delete_namespace(key):
	"""remove a namespace entirely"""

	if key not in REGISTRY:
		raise KeyError("key:{0} does not exist".format(key))

	REGISTRY.pop(key, None)


def clear_namespace(key):
	"""re-initialize a namespace"""
	delete_namespace(key)
	new_namespace(key)


# loaders
def _recurse(level, key, iterable, ns):
	"""recurse through a dict and create nested namespaces"""
	if isinstance(iterable, dict):
		new = Namespace()
		setattr(ns, key, new)
		for k, v in iterable.items():
			# add it to the ns
			_recurse(level + 1, k, v, new)
	else:
		# add to the ns
		setattr(ns, key, iterable)

def loadfrom_yaml(key, path):
	"""load a yaml file into a top-level namespace"""
	with open(path, 'r') as f:
		d = yaml.load(f)

		new_namespace(key)
		ns = get_namespace(key)

		for key, value in d.items():
			_recurse(0, key, value, ns)

def loadfrom_json(key, path):
	"""load a json file into a top-level namespace"""
	with open(path, 'r') as f:
		d = json.load(f)

		new_namespace(key)
		ns = get_namespace(key)

		for key, value in d.items():
			_recurse(0, key, value, ns)

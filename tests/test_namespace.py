"""
unittest for namespace.Namespace object
"""

import unittest

# import from inside package.
# this would be replaced by ``import pysettings`` in usecases
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.namespace import Namespace


class TestNamespace(unittest.TestCase):

	def setUp(self):
		self.nm = Namespace()

	def tearDown(self):
		pass

	def test_set_namespace_var(self):
		"""
		simple values (int, bool, string, etc.)
		"""
		self.nm.test = "testvalue"
		self.assertEqual(self.nm.test, "testvalue")

	def test_set_namespace_var_as_object(self):
		"""
		should be able to store objects
		"""
		self.nm.object = [1, 2, 3]
		self.assertIsInstance(self.nm.object, list)
		self.assertEqual(self.nm.object, [1, 2, 3])

	def test_set_namespace_var_as_dict(self):
		"""
		nested dicts should ALWAYS be Namespaces!
		"""
		self.nm.iter = {"key": "value"}
		self.assertIsInstance(self.nm.iter, Namespace)
		self.assertEqual(self.nm.iter.key, "value")

	def test_nested_dicts(self):
		d = {
			"level1": {
				"level2": {
					"level2_key1": "value"
				}
			}
		}

		self.nm.nested = d
		self.assertIsInstance(self.nm.nested, Namespace)
		self.assertEqual(self.nm.nested.level1.level2.level2_key1, "value")


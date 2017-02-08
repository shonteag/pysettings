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
		self.nm.test = "testvalue"
		self.assertEqual(self.nm.test, "testvalue")

	def test_set_namespace_var_as_object(self):
		self.nm.object = [1, 2, 3]
		self.assertIsInstance(self.nm.object, list)
		self.assertEqual(self.nm.object, [1, 2, 3])

	


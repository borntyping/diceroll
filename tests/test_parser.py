""" Test the basic elements of the parser """

import unittest

from diceroll import roll, ParseException
from diceroll.components import RolledDice

from argumented import *
from itertools import product

class TestNumber (unittest.TestCase):
	def setUp (self):
		self.result = roll("1")
		
	def test_parse (self):
		self.assertEquals(self.result, 1)
		
	def test_type (self):
		self.assertIsInstance(self.result, int)

class TestExtras (unittest.TestCase):
	def test_subexpression (self):
		# Test that subexpressions work correctly,
		# as there is no operator precedence
		self.assertEquals(roll("8/2*2"), 8)
		self.assertEquals(roll("8/(2*2)"), 2)
	
	def test_comment (self):
		self.assertIsInstance(roll("d6 // This is a comment"), RolledDice)
	
	def test_return_single (self):
		# An expression with a single result returns only that result
		self.assertIsInstance(roll("d6"), RolledDice)
		
class TestExpressions (unittest.TestCase):
	def setUp (self):
		self.results = roll("d2, d4, d6, d8, d10, d20")
	
	def test_expressions_type (self):
		self.assertIsInstance(self.results, list)
	
	def test_expressions_len (self):
		self.assertEquals(len(self.results), 6)
		
if __name__ == '__main__':
    unittest.main()

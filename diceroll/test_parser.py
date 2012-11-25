""" Test that roll() parses expressions correctly """

import unittest

from diceroll import roll, ParseException
from diceroll.components import RolledDice

from argumented import unpack_arguments, argument, argument_list, argument_tuples
from itertools import product

class TestNumber (unittest.TestCase):
	def test_parse (self):
		self.assertEquals(roll("1"), 1)
		
	def test_type (self):
		self.assertIsInstance(roll("2"), int)

class TestDice (unittest.TestCase):
	def test_parse_d6 (self):
		self.assertIsInstance(roll("d6"), RolledDice)
	
	def test_parse_default_n (self):
		self.assertEquals(roll("d1"), roll("1d1"))
		
	def test_parse_2d6 (self):
		self.assertIsInstance(roll("2d6"), RolledDice)
	
	def test_parse_alternate_case (self):
		self.assertIsInstance(roll("D6"), RolledDice)
	
	def test_type (self):
		self.assertIsInstance(roll("2d6"), RolledDice)
	
	def test_invalid (self):
		self.assertRaises(ParseException, roll, "1dd6")
	
	def test_missing_s (self):
		self.assertRaises(ParseException, roll, "1d")

subatoms = ('6d6', '(6d6)')
atoms = lambda *ops: ((x, {}) for x in product(ops, subatoms))

@unpack_arguments
class TestUnaryOperators (unittest.TestCase):
	@argument_list(*subatoms)
	def test_subatoms (self, subatom):
		self.assertIsInstance(roll(subatom), RolledDice)
	
	@argument_tuples(*atoms("x", "explode"))
	def test_explode (self, op, subatom):
		self.assertIsInstance(roll(subatom + op), RolledDice)
	
	@argument_tuples(*atoms("s", "sort"))
	def test_sort (self, op, subatom):
		result = roll(subatom + op)
		self.assertEquals(result, sorted(result))
	
	@argument_tuples(*atoms("t", "total"))
	def test_total (self, op, subatom):
		self.assertIsInstance(roll(subatom + op), int)
	
@unpack_arguments
class TestBinaryOperators (unittest.TestCase):
	
	@argument_list('v', 'drop')
	def test_drop (self, op):
		self.assertEquals(len(roll("2d1 "+op+" 1")), 1)
				
	@argument_list('^', 'keep')
	def test_keep (self, op):
		self.assertEquals(len(roll("6d1 "+op+" 2")), 2)

if __name__ == '__main__':
    unittest.main()

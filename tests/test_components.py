""" Test the parser components - dice and operators """

import unittest

from diceroll import roll, ParseException
from diceroll.components import RolledDice

from argumented import *
from itertools import product

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

atoms = lambda *ops: ((x, {}) for x in product(ops, ['6d6', '(6d6)']))

@unpack_arguments
class TestUnaryOperators (unittest.TestCase):	
	@argument_tuples(*atoms("x", "explode"))
	def test_explode (self, op, subatom):
		self.assertIsInstance(roll(subatom + op), RolledDice)
	
	@argument_tuples(*atoms("s", "sort"))
	def test_sort (self, op, subatom):
		result = roll(subatom + op)
		self.assertIsInstance(result, RolledDice)
		self.assertEquals(result, sorted(result))
	
	@argument_tuples(*atoms("t", "total"))
	def test_total (self, op, subatom):
		self.assertIsInstance(roll(subatom + op), int)
	
@unpack_arguments
class TestBinaryOperators (unittest.TestCase):
	
	@argument_list('v', 'drop')
	def test_drop (self, op):
		result = roll("2d1 "+op+" 1")
		self.assertIsInstance(result, RolledDice)
		self.assertEquals(len(result), 1)
				
	@argument_list('^', 'keep')
	def test_keep (self, op):
		result = roll("6d1 "+op+" 2")
		self.assertIsInstance(result, RolledDice)
		self.assertEquals(len(result), 2)
	
	@argument_list('r', 'reroll')
	def test_keep (self, op):
		result = roll("6d3 "+op+" 2")
		self.assertIsInstance(result, RolledDice)
		self.assertEquals(len(result), 6)
	
	@argument_list('rr', 'rreroll')
	def test_keep (self, op):
		""" Assert that there are no rolls below `limit` """
		result = roll("6d3 {0} {1}".format(op, 2))
		self.assertIsInstance(result, RolledDice)
		self.assertFalse(filter(lambda x: x <= 2, result))
		self.assertEquals(len(result), 6)

class TestSuccessOperator (unittest.TestCase):
	@classmethod
	def setUpClass (cls):
		cls.basic_result = roll("6d6 success 4")
		
	def test_success (self):
		self.assertGreaterEqual(self.basic_result, 0)
		self.assertLessEqual(self.basic_result, 6)
	
	def test_success_type (self):
		self.assertIsInstance(self.basic_result, int)
		
	def test_success_cancel (self):
		result = roll("6d6 successC 4")
		self.assertGreaterEqual(result, -6)
		self.assertLessEqual(result, 6)
	
	def test_success_bonus (self):
		result = roll("6d6 successB 4")
		self.assertGreaterEqual(result, 0)
		self.assertLessEqual(result, 12)

	def test_success_both (self):
		result = roll("6d6 successCB 4")
		self.assertGreaterEqual(result, -6)
		self.assertLessEqual(result, 12)

if __name__ == '__main__':
    unittest.main()

""" Test that roll() parses expressions correctly """

import unittest

from diceroll import roll, ParseException
from diceroll.components import RolledDice

class TestNumber (unittest.TestCase):
	def test_parse (self):
		self.assertEquals(roll("1"), 1)
		
	def test_type (self):
		self.assertIsInstance(roll("2"), int)

class TestDice (unittest.TestCase):
	def test_parse_d6 (self):
		self.assertTrue(roll("d6"))
	
	def test_parse_default_n (self):
		self.assertEquals(roll("d1"), roll("1d1"))
		
	def test_parse_2d6 (self):
		self.assertTrue(roll("2d6"))
	
	def test_parse_alternate_case (self):
		self.assertTrue(roll("D6"))
	
	def test_type (self):
		self.assertIsInstance(roll("2d6"), RolledDice)
	
	def test_invalid (self):
		self.assertRaises(ParseException, roll, "1dd6")
	
	def test_missing_s (self):
		self.assertRaises(ParseException, roll, "1d")
	
class TestAtom (unittest.TestCase):
	def setUp (self):
		self.subatoms = ("6d6", "(6d6)")
	
	def test_subatoms (self):
		for subatom in self.subatoms:
			self.assertTrue(roll(subatom))
	
	def test_explode (self):
		for subatom in self.subatoms:
			for op in ("x", "explode"):
				self.assertTrue(roll(subatom + op))
	
	def test_sort (self):
		for subatom in self.subatoms:
			for op in ("s", "sort"):
				result = roll(subatom + op)
				self.assertEquals(result, sorted(result))
			
	def test_total (self):
		for subatom in self.subatoms:
			for op in ("t", "total"):
				self.assertTrue(roll(subatom + op))
	
if __name__ == '__main__':
    unittest.main()

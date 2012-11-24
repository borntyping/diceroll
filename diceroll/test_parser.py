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
	
if __name__ == '__main__':
    unittest.main()

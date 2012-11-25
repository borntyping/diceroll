""" Test the basic elements of the parser """

import unittest

from diceroll import roll, ParseException
from diceroll.components import RolledDice

from argumented import *
from itertools import product

class TestNumber (unittest.TestCase):
	def test_parse (self):
		self.assertEquals(roll("1"), 1)
		
	def test_type (self):
		self.assertIsInstance(roll("2"), int)

if __name__ == '__main__':
    unittest.main()

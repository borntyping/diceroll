#!/usr/bin/python

__version__ = 0.2

from random import randint

from pyparsing import *

def catch (func):
	"""
	Becuase sometimes, pyparsing is a bitch.
	Use this when it decides to eat your TypeErrors.
	"""
	def catch (*a, **k):
		try:
			func(*a, **k)
		except:
			print traceback.format_exc()
	return catch

class Dice (list):
	"""	A random list of dicerolls """
	
	def __init__ (self, n, s):
		""" Roll a dice with ``s`` faces ``n`` times """
		for _ in xrange(n):
			self.append(randint(1, s))
	
	# Formatting
	
	def _str_list (self):
		return ', '.join([str(r) for r in self])
	
	def __str__ (self):
		"""	Represent a list of dice rolls in the form ``{a, b, c, ... (total)}`` """
		return "{{{} ({})}}".format(self._str_list(), int(self))
	
	def __repr__ (self):
		"""	Represent a list of dice rolls in the form ``{a, b, c, ... (total)}`` """
		return "{" + self._str_list() + "}"
	
	# Operators
	
	def __int__ (self):
		"""
		Convert the dicerolls to an integer,
		by returning the sum total of the rolls.
		"""
		return sum(self)
	
	def __add__ (self, other): return int(self) + int(other)
	def __sub__ (self, other): return int(self) - int(other)

# Parse numbers into integer values
number = Word(nums)
number.setParseAction(lambda tokens: int(tokens[0]))
number.setName("number")

# Parse dice into a list of rolls
dice = Optional(number, default=1) + CaselessLiteral("d").suppress() + number
dice.setParseAction(lambda tokens: [Dice(tokens[0], tokens[1])])

# Operators
def Operation (operator):
	"""	Decorator. Deals with handling the same operation multiple times, and makes it a little easier to write new operators. """
	def wrapped_operator (tokens):
		# Extract the value to edit from the tokens,
		# and the list of values to call the operator with
		x, operations = tokens[0][0], tokens[0][1:]
		while operations:
			y = operations.pop(0)
			print x, operator(x, y)
			x = operator(x, y)
		return x
	return wrapped_operator

op = lambda s, f: (Literal(s).suppress(), 2, opAssoc.LEFT, f)
operators = operatorPrecedence(dice | number, [op(*x) for x in (
	('+', Operation(lambda x, y: x.__add__(y))),
	('-', Operation(lambda x, y: x - y)),
)])

# Comments
comment = Optional(dblSlashComment).suppress()

# The final expression
expression = operators + comment

def roll (expr):
	""" Roll ``expr`` """
	return expression.parseString(expr)[0]

def cli ():
	""" Command line entry point """
	import sys, argparse
	parser = argparse.ArgumentParser(
		description="Return the results of a dice expression")
	
	parser.add_argument('--version', action='version', version='bones v%s' % __version__)
	parser.add_argument('expression', type=str, help='the expression to roll')
	
	args = parser.parse_args()
	
	print roll(args.expression)

if __name__ == '__main__': cli()

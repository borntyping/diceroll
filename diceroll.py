#!/usr/bin/python

#: This is the version number
__version__ = 0.3

#: Define __all__ so that ``from diceroll import *`` only imports useful items
__all__ = ['Dice', 'Components', 'expression', 'roll', 'cli']

from random import randint
from pyparsing import Word, Optional, CaselessLiteral, Literal
from pyparsing import nums, operatorPrecedence, opAssoc, dblSlashComment

def catch (function):
	"""	As pyparsing often refuses to raise an exception """
	def safe_function (*args, **kwargs):
		try:
			function(*args, **kwargs)
		except Exception, e:
			print "{e.__class__.__name__}: {e}".format(e=e)
			exit()
	return safe_function

class Dice (list):
	"""	A list of dicerolls, generated from given parameters """
	
	def __init__ (self, *args):
		"""
		Given 2 arguments: Roll a dice with ``s`` faces ``n`` times
		Given 1 argument: Construct a Dice object from the given iterable
		"""
		if len(args) == 2:
			num, sides = args
			for _ in xrange(num):
				self.append(randint(1, sides))
		elif len(args) == 1:
			super(Dice, self).__init__(args[0])
	
	#: Represent a list of dice rolls in the form ``a, b, c, ...``
	def __str__ (self):  return ', '.join([str(r) for r in self])
	
	#: Represent a list of dice rolls in the form ``{a, b, c, ...}``
	def __repr__ (self): return "{" + self.__str__() + "}"
	
	#: Convert the dicerolls to an integer, by returning the sum total
	def __int__ (self): return sum(self)
	
	#  Operators
	def __add__ (self, other):	return int(self) + int(other)
	def __sub__ (self, other):	return int(self) - int(other)
	def __mul__ (self, other):	return int(self) * int(other)
	def __div__ (self, other):	return int(self) / int(other)
	
	def drop (self, num):		return [Dice(sorted(self)[num:])]
	def keep (self, num):		return [Dice(sorted(self)[:num:-1])]

class Components (object):
	""" The components that make up a diceroll expression """
	
	# Parse numbers into integer values
	number = Word(nums)
	number.setParseAction(lambda tokens: int(tokens[0]))
	number.setName("number")

	# Parse dice into a list of rolls
	dice = Optional(number, default=1) + CaselessLiteral("d").suppress() + number
	dice.setParseAction(lambda tokens: [Dice(tokens[0], tokens[1])])

	# Create the individual operators
	
	def DiceOnly (operator):
		@catch
		def dice_only_operator (tokens):
			if not isinstance(tokens[0][0], Dice):
				raise NotImplementedError, "Operator {} can only be used on Dice objects".format(tokens[0][1])
			else:
				return operator(tokens)
		return dice_only_operator
	
	def Operation (operator, recursive=True):
		"""	Decorator. Deals with handling the same operation multiple times, and makes it a little easier to write new operators. """
		if recursive:
			def recursive_wrapped_operator (tokens):
				# Extract the value to edit from the tokens,
				# and the list of values to call the operator with
				try:
					x, operations = tokens[0][0], tokens[0][2:]
					while operations:
						y = operations.pop(0)
						x = operator(x, y)
					return x
				except Exception, e:
					import traceback
					print traceback.format_exc(e)
			return recursive_wrapped_operator
		else:
			def wrapped_operator(tokens):
				return operator(tokens[0][0], tokens[0][2])
			return wrapped_operator

	#: The operations to add to the operatorPrecedence syntax
	operators = [
		# Dice only operators
		('v', 'drop',	DiceOnly(Operation(lambda d, n: d.drop(n), recursive=false))),
		('^', 'keep',	DiceOnly(Operation(lambda d, n: d.keep(n), recursive=false))),
		
		# General operators
		('~', 'diff',	Operation(lambda x, y: int(x) - int(y))),
		('+', None,		Operation(lambda x, y: x + y)),
		('-', None,		Operation(lambda x, y: x - y)),
		('*', None,		Operation(lambda x, y: x * y)),
		('/', None,		Operation(lambda x, y: x / y)),
	]
	
	# Generate operators
	operator_list = list()
	for op in operators:
		for n in (0, 1):
			if op[n]:
				operator_list.append((Literal(op[n]), 2, opAssoc.LEFT, op[2]))
	
	operators = operatorPrecedence(dice | number, operator_list)

	# Comments
	comment = Optional(dblSlashComment).suppress()

#: The final diceroll expression
expression = Components.operators + Components.comment

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

#!/usr/bin/python

#: This is the version number
__version__ = 0.3

#: Define __all__ so that ``from diceroll import *`` only imports useful items
__all__ = ['Dice', 'Components', 'expression', 'roll', 'cli']

from random import randint

from pyparsing import Word, Optional, CaselessLiteral, Literal, OnlyOnce
from pyparsing import nums, operatorPrecedence, opAssoc, dblSlashComment
from pyparsing import StringStart, StringEnd

# Enable pyarsings packrat mode, seems to provide a massive speed increase.
# http://pyparsing-public.wikispaces.com/FAQs#Frequently%20Asked%20Questions-What%20the%20heck%20is%20%22packrat%20parsing%22?
from pyparsing import ParserElement
ParserElement.enablePackrat()

def catch (function):
	"""	As pyparsing often refuses to raise an exception """
	def safe_function (*args, **kwargs):
		try:
			return function(*args, **kwargs)
		except Exception:
			#print "{e.__class__.__name__}: {e}".format(e=e)
			from traceback import print_exc; print_exc(); exit()
	safe_function.__name__ = function.__name__
	return safe_function

#: Return a random number between 1 and ``s``
def rand (s): return randint(1, s)

class Dice (list):
	"""
	A list of dicerolls, generated from given parameters
	
	Note:	if returning it to pyparsing, place it in a list,
			otherwise pyparsing will assume it's a list of tokens.
	"""
	
	@classmethod
	def roll (cls, n, sides):
		""" Create a Dice object, with ``n`` rolls """
		return cls(sides, [rand(sides) for _ in xrange(n)])
	
	def __init__ (self, sides, iterable=()):
		"""
		Create a set of dice, with ``sides`` sides.
		"""
		self.sides = sides
		super(Dice, self).__init__(iterable)
	
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
	
	def drop (self, num):		return [Dice(self.sides, sorted(self)[num:])]
	def keep (self, num):		return [Dice(self.sides, sorted(self)[::-1][:num])]
	
	def sort (self):
		super(Dice, self).sort()
		return [self]
	
	@catch
	def explode (self, n=None, recursive=True, limit=10):
		"""	Roll an extra die for each die >= ``n`` """
		n = n or self.sides
		# The dice to return
		dice = Dice(self.sides, self)
		# The list of rolls to check for exploding dice
		new = list(self)
		# Recursively check ``new`` for exploding dice,
		# until ``limit`` reaches 0
		while limit > 0:
			new = [rand(dice.sides) for die in new if die >= n]
			# Return the dice if there are no new dice to try
			# and explode, or recursive checking is disabled.
			if len(new) == 0 or recursive == False:
				return [dice]
			dice.extend(new)
			limit = limit - 1
		raise Exception, "Too many dice exploded"

class Components (object):
	""" The components that make up a diceroll expression """
	
	# Parse numbers into integer values
	number = Word(nums)
	number.setParseAction(lambda tokens: int(tokens[0]))
	number.setName("number")

	# Parse dice into a list of rolls
	dice = Optional(number, default=1) + CaselessLiteral("d").suppress() + number
	dice.setParseAction(lambda tokens: [Dice.roll(tokens[0], tokens[1])])

	# Create the individual operators
	
	def DiceOnly (operator):
		@catch
		def dice_only_operator (string, location, tokens):
			if not isinstance(tokens[0][0], Dice):
				raise NotImplementedError, "Operator {} can only be used on Dice objects ({!r} given)".format(tokens[0][1], tokens[0][0])
			return operator(tokens)
		return dice_only_operator
	
	def Operation (operator, recursive=True):
		"""
		Decorator, to simplify ``X `op` Y`` style operators.
		
		Deals with handling the same operation multiple times (unless `recursive=False`),
		and makes it a little easier to write new operators.
		"""
		if recursive:
			def recursive_wrapped_operator (tokens):
				# Extract the value to edit from the tokens,
				# and the list of values to call the operator with
				x, operations = tokens[0][0], tokens[0][2:]
				while operations:
					y = operations.pop(0)
					x = operator(x, y)
				return x
			return recursive_wrapped_operator
		else:
			def wrapped_operator(tokens):
				x, op, y = tokens[0]
				return operator(x, y)
			return wrapped_operator
	
	#: The operations to add to the operatorPrecedence syntax
	operators = [
		# Dice only operators
		(['*', 'explode'], DiceOnly(lambda t: t[0][0].explode()), 1),
		(['v', 'drop'],    DiceOnly(Operation(lambda d, n: d.drop(n), recursive=False))),
		(['^', 'keep'],    DiceOnly(Operation(lambda d, n: d.keep(n), recursive=False))),
		(['t', 'total'],   DiceOnly(lambda t: int(t[0][0])), 1),
		(['o', 'sort'],    DiceOnly(lambda t: t[0][0].sort()), 1),
		
		# General operators
		(['~', 'diff'],	Operation(lambda x, y: int(x) - int(y))),
		(['+'], Operation(lambda x, y: x + y)),
		(['-'], Operation(lambda x, y: x - y)),
		(['*'], Operation(lambda x, y: x * y)),
		(['/'], Operation(lambda x, y: x / y)),
		
		# Single term operators
	]
	
	# Generate operators
	operator_list = list()
	for op in operators:
		function    = op[1]
		terms       = op[2] if op[2:] else 2
		association = op[3] if op[3:] else opAssoc.LEFT
		for n in op[0]:
			operator = (Literal(n), terms, association, OnlyOnce(function))
			operator_list.append(operator)
	
	operators = operatorPrecedence(dice | number, operator_list)

	# Comments
	comment = Optional(dblSlashComment).suppress()

#: The final diceroll expression
expression = StringStart() + Components.operators + Components.comment + StringEnd()

def roll (expr):
	""" Roll ``expr`` """
	return expression.parseString(expr)[0]

def cli ():
	""" Command line entry point """
	import sys, argparse
	parser = argparse.ArgumentParser(
		description="Return the results of a dice expression")
	
	parser.add_argument('--version', action='version', version='bones v%s' % __version__)
	parser.add_argument('--profile', action='store_true', help='run using the cProfile profiler')
	parser.add_argument('expression', type=str, help='the expression to roll')
	
	args = parser.parse_args()
	
	if args.profile:
		import cProfile
		cProfile.runctx('print roll(args.expression)', globals(), locals())
	else:
		print roll(args.expression)

if __name__ == '__main__': cli()

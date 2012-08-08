"""	Operator classes """

__all__ = ['Operator', 'UnaryOperator', 'BinaryOperator', 'Generic', 'GenericUnaryOperator', 'GenericBinaryOperator', 'generic_unary', 'generic_binary', 'Sort', 'Explode', 'Join', 'Drop', 'Keep', 'Reroll', 'RecursiveReroll', 'Success']

from abc import ABCMeta, abstractmethod

from pyparsing import *

from objects import RolledDice

# -------------------------
# Operator superclasses
# -------------------------

class Operator (object):
	__metaclass__ = ABCMeta
	
	@abstractmethod
	def __call__ (self, args):
		raise NotImplementedError, self.__class__.__name__ + " has not defined a call method"
	
	def require_dice (self, obj, error=None):
		error = error or "Cannot call {operator} on {1}, as it is not a RolledDice object "
		if not isinstance(obj, RolledDice):
			raise NotImplementedError, error.format(operator=self.__class__.__name__, obj=obj)
	
	def __repr__ (self):
		return '<'+self.__class__.__name__+'>'

class UnaryOperator (Operator):
	""" An operator that accepts a single token """
	pass

class BinaryOperator (Operator):
	"""	An operator that accepts two tokens """
	pass

# -------------------------
# Generic operators
# -------------------------
	
class Generic (object):
	"""
	Allows the creation of simple lambda operators, such as::
	
		GenericBinaryOperator('Plus', lambda x,y: x + y)
	"""
	
	def __init__ (self, name, function):
		self.__name__ = name
		self.function = function
	
	def __call__ (self, *args):
		return self.function(*args)
	
	def __repr__ (self):
		return '<'+self.__name__+'>'

class GenericUnaryOperator (Generic, UnaryOperator):
	pass

class GenericBinaryOperator (Generic, BinaryOperator):
	pass

# Shortcut functions that create parse actions
generic_unary  = lambda n, f: (lambda tokens: GenericUnaryOperator(n, f))
generic_binary = lambda n, f: (lambda tokens: GenericBinaryOperator(n, f))

# -------------------------
# Actual operators
# -------------------------

class Sort (UnaryOperator):
	def __call__ (self, x):
		x.sort()
		return x

class Explode (UnaryOperator):
	def __init__ (self, tokens):
		self.n = False
		self.recursive = True
		self.limit = 10
	
	def __call__ (self, dice):
		self.require_dice(dice, "Cannot explode {obj}")
		return self.recursive_explode(dice, self.n or dice.sides)
	
	def recursive_explode (self, dice, n):
		"""	Roll an extra die for each die >= ``n`` """
		new = list(dice)
		for i in xrange(self.limit):
			new = [dice.rand() for d in new if d >= n]
			# Return the dice if there are no new dice to try
			# and explode, or recursive checking is disabled.
			if len(new) == 0 or not self.recursive:
				return dice
			else:
				dice.extend(new)
		raise Exception, "I'll be here forever if I explode any more dice."

class Join (BinaryOperator):
	def __call__ (self, left, right):
		"""
		Joins elements into a tuple,
		adding to an existing tuple where possible
		"""
		if isinstance(left, tuple):
			return left + (right,)
		else:
			return (left, right)
			
class Drop (BinaryOperator):
	def __call__ (self, dice, n):
		self.require_dice(dice, "Cannot drop dice from {obj}")
		return RolledDice(dice, sorted(dice)[n:])

class Keep (BinaryOperator):
	def __call__ (self, dice, n):
		"""	Keeps the ``n`` highest dice from ``d`` """
		self.require_dice(dice, "Cannot keep dice from {obj}")
		return RolledDice(dice, sorted(dice)[::-1][:n])

class Reroll (BinaryOperator):
	def __call__ (self, dice, limit):
		"""	Reroll all dice below ``limit`` """
		self.require_dice(dice, "Cannot reroll dice from {obj}")
		return RolledDice(dice, [(dice.rand() if d <= limit else d) for d in dice])

class RecursiveReroll (Reroll):
	def __call__ (self, dice, limit):
		"""	Recursively reroll dice """
		self.require_dice(dice, "Cannot reroll dice from {obj}")
		while len(filter(lambda d: d <= limit, dice)) > 0:
			dice = Reroll.__call__(self, dice, limit)
		return dice

class Success (BinaryOperator):
	grammars = [
		CaselessLiteral('success').suppress()
		+ Optional(White())
		+ ZeroOrMore(CaselessLiteral('C') | CaselessLiteral('B'))
	]
	
	def __init__ (self, tokens):
		tokens = list(tokens)
		self.canceling = ('C' in tokens)
		self.bonuses = ('B' in tokens)
		
	def __call__ (self, dice, n):
		result = len(filter(lambda d: d >= int(n), dice))
		if self.canceling: result -= len(filter(lambda d: d == 1, dice))
		if self.bonuses:   result += len(filter(lambda d: d >= dice.sides, dice))
		return result

	def __repr__ (self):
		return '<{} ({}{})>'.format(
			self.__class__.__name__,
			'C' if self.canceling else '-',
			'B' if self.bonuses else '-',
		)

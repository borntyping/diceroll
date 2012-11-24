"""	Operator classes """

__all__ = ['RolledDice', 'UnrolledDice', 'Operator', 'Generic'] + ['Total', 'Sort', 'Explode'] + ['Plus', 'Minus', 'Multiply', 'Divide', 'Drop', 'Keep', 'Reroll', 'RecursiveReroll', 'Success']

from abc		import ABCMeta, abstractmethod
from random		import randint

from pyparsing	import *

def grammars (cls, iterable):
	return [cls(g) for g in iterable]

def literals (*g):
	return grammars(Literal, g)
	
def keywords (*g):
	return grammars(CaselessKeyword, g)

# -------------------------
# Dice
# -------------------------

class RolledDice (list):
	"""	A list of dice rolls """
	
	def __init__ (self, a, dice=()):
		"""
		:Parameters:
			- `a`: Either a dice object (which the number of sides will be extracted from), or the number of sides the RolledDice should have.
		"""
		self.sides = a.sides if isinstance(a, RolledDice) else a
			
		for d in dice:
			self.append(d)
	
	def rand (self, sides=False):
		return randint(1, sides or self.sides)
	
	def roll (self, n):
		"""	Roll ``n`` dice and add them to the list """
		for i in xrange(n):
			self.append(self.rand())
		return self
	
	def __str__ (self):
		"""	Strip the [] from the results """
		return super(RolledDice, self).__repr__()[1:-1]
		
	def __repr__ (self):
		return "Dice<{}>{}".format(self.sides, tuple(self))
	
	def __int__ (self):			return sum(self)
	def __add__ (self, other):	return int(self) + int(other)
	def __sub__ (self, other):	return int(self) - int(other)
	def __mul__ (self, other):	return int(self) * int(other)
	def __div__ (self, other):	return int(self) / int(other)
	
	def sort (self): super(RolledDice, self).sort(); return self
		
class UnrolledDice (object):
	"""	A set of *potential* dice rolls, that can be rolled as late as possible """
	def __init__ (self, n, sides):
		self.n = n
		self.sides = sides

	def evaluate (self):
		return RolledDice(self.sides).roll(self.n)
		
	def __repr__ (self):
		return "{n}d{s}".format(n=self.n, s=self.sides)

# -------------------------
# Operator superclasses
# -------------------------

class Operator (object):
	__metaclass__ = ABCMeta
	
	#: The number of terms the operator accepts
	terms = 2
	
	#: The grammars to include in the parser
	grammars = ()
	
	@abstractmethod
	def __call__ (self, *args):
		raise NotImplementedError, self.__class__.__name__ + " has not defined a call method"
	
	@property
	def name (self):
		return self.__class__.__name__
	
	def require_dice (self, obj, error=None):
		error = error or "Cannot call {operator} on {1}, as it is not a RolledDice object "
		if not isinstance(obj, RolledDice):
			raise NotImplementedError, error.format(operator=self.__class__.__name__, obj=obj)
	
	def __repr__ (self):
		return '<'+self.name+'>'

# -------------------------
# Generic operators
# -------------------------

class GenericOperator (Operator):
	def __call__ (self, *args):
		return self.function(*args)

def Generic (name, function, grammars, terms=2):
	return type(name, (GenericOperator,), {
		'function': staticmethod(function),
		'grammars': grammars,
		'terms':	terms,
	})

# -------------------------
# Unary operators
# -------------------------

Total = Generic('total', lambda d: int(d), keywords('t', 'total'), terms=1)
Sort = Generic('sort', lambda d: d.sort(), keywords('s', 'sort'), terms=1)

class Explode (Operator):
	grammars = keywords('x', 'explode')
	terms = 1
	
	def __init__ (self, tokens):
		self.recursive = True
		self.limit = 10
	
	def __call__ (self, dice):
		self.require_dice(dice, "Cannot explode {obj}")
		return self.recursive_explode(dice, dice.sides)
	
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

# -------------------------
# Binary operators
# -------------------------

		
Plus     = Generic('Plus',     lambda x,y: int(x) + int(y), literals('+') + keywords('plus'))
Minus    = Generic('Minus',    lambda x,y: int(x) - int(y), literals('-') + keywords('minus'))
Multiply = Generic('Multiply', lambda x,y: int(x) * int(y), literals('*') + keywords('multiply'))
Divide   = Generic('Divide',   lambda x,y: int(x) / int(y), literals('/') + keywords('divide'))
		
class Drop (Operator):
	grammars = keywords('v', 'drop')
	
	def __call__ (self, dice, n):
		self.require_dice(dice, "Cannot drop dice from {obj}")
		return RolledDice(dice, sorted(dice)[n:])

class Keep (Operator):
	grammars = literals('^') + keywords('keep')
	
	def __call__ (self, dice, n):
		"""	Keeps the ``n`` highest dice from ``d`` """
		self.require_dice(dice, "Cannot keep dice from {obj}")
		return RolledDice(dice, sorted(dice)[::-1][:n])

class Reroll (Operator):
	grammars = keywords('r', 'reroll')
	
	def __call__ (self, dice, limit):
		"""	Reroll all dice below ``limit`` """
		self.require_dice(dice, "Cannot reroll dice from {obj}")
		return RolledDice(dice, [(dice.rand() if d <= limit else d) for d in dice])

class RecursiveReroll (Reroll):
	grammars = keywords('rr', 'rreroll')
	
	def __call__ (self, dice, limit):
		"""	Recursively reroll dice """
		self.require_dice(dice, "Cannot reroll dice from {obj}")
		while len(filter(lambda d: d <= limit, dice)) > 0:
			dice = Reroll.__call__(self, dice, limit)
		return dice

class Success (Operator):
	grammars = [
		CaselessLiteral('success').suppress()
		+ Optional(White())
		+ ZeroOrMore(CaselessLiteral('C') | CaselessLiteral('B'))
	]
	
	def __init__ (self, tokens):
		self.canceling = ('C' in list(tokens))
		self.bonuses = ('B' in list(tokens))
		
	def __call__ (self, dice, n):
		result = len(filter(lambda d: d >= int(n), dice))
		if self.canceling:
			result -= len(filter(lambda d: d == 1, dice))
		if self.bonuses:
			result += len(filter(lambda d: d >= dice.sides, dice))
		return result

	def __repr__ (self):
		return '<{} ({}{})>'.format(
			self.__class__.__name__,
			'C' if self.canceling else '-',
			'B' if self.bonuses else '-',
		)

class Diffrence (Operator):
	grammars = literals('~') + keywords('diff')
	
	def __call__ (self, x, y):
		return int(x) - int(y)

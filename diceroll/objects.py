"""	Objects """

from random import randint

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
			
	def __repr__ (self):
		return "Dice<{}>{}".format(self.__class__.__name__, self.sides, tuple(self))
	
	def __int__ (self):			return sum(self)
	def __add__ (self, other):	return int(self) + int(other)
	def __sub__ (self, other):	return int(self) - int(other)
	def __mul__ (self, other):	return int(self) * int(other)
	def __div__ (self, other):	return int(self) / int(other)
		
class UnrolledDice (object):
	"""	A set of *potential* dice rolls, that can be rolled as late as possible """
	def __init__ (self, n, sides):
		self.n = n
		self.sides = sides

	def evaluate (self, **modifiers):
		return RolledDice(self.sides).roll(self.n)
		
	def __repr__ (self):
		return "{n}d{s}".format(n=self.n, s=self.sides)

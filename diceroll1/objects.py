"""	Objects """

from random import randint

class Atom (object):
	pass

class Number (int, Atom):
	def __repr__ (self):
		return "{}({})".format(self.__class__.__name__, super(Number, self).__repr__())

class RolledDice (list, Atom):
	"""	A list of dice rolls """
	
	def __init__ (self, sides, dice=()):
		self.sides = sides
		for d in dice:
			self.append(d)
	
	def roll (self, n):
		"""	Roll ``n`` dice and add them to the list """
		for i in xrange(n):
			self.append(randint(1, self.sides))
		return self
			
	def __repr__ (self):
		return "{}({}){}".format(self.__class__.__name__, self.sides, tuple(self))
		
class UnrolledDice (object):
	"""	A set of *potential* dice rolls, that can be rolled as late as possible """
	def __init__ (self, n, sides):
		self.n = n
		self.sides = sides

	def roll (self):
		return RolledDice(self.sides).roll(self.n)
		
	def __repr__ (self):
		return "{}({},{})".format(self.__class__.__name__, self.n, self.sides)

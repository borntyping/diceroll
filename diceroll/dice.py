"""	The Dice class """

from random import randint

def rand (s):
	""" Return a random number between 1 and ``s`` """
	return randint(1, s)

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
		
	def rand (self):			return rand(self.sides)
	
	#: Represent a list of dice rolls in the form ``a, b, c, ...``
	def __str__ (self):			return ', '.join([str(r) for r in self])
	
	#: Represent a list of dice rolls in the form ``{a, b, c, ...}``
	def __repr__ (self):		return "{" + self.__str__() + "}"
	
	#: Convert the dicerolls to an integer, by returning the sum total
	def __int__ (self): 		return sum(self)
	
	#  Operators
	def __add__ (self, other):	return int(self) + int(other)
	def __sub__ (self, other):	return int(self) - int(other)
	def __mul__ (self, other):	return int(self) * int(other)
	def __div__ (self, other):	return int(self) / int(other)
	
	def drop (self, num):		return [Dice(self.sides, sorted(self)[num:])]
	def keep (self, num):		return [Dice(self.sides, sorted(self)[::-1][:num])]
	
	def reroll (self, limit):
		"""	Reroll all dice below ``limit`` """
		return [Dice(self.sides, [(self.rand() if d <= limit else d) for d in self])]
	
	def rreroll (self, limit):
		"""	Recursively reroll dice """
		dice = Dice(self.sides, self)
		while len(filter(lambda d: d <= limit, dice)) > 0:
			dice = dice.reroll(limit)[0]
		return [dice]
	
	def sort (self):
		super(Dice, self).sort()
		return [self]
	
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

"""	The evaluate function, and print functions for the functions it performs """

from traceback	import print_exc

from objects	import UnrolledDice
from operators	import Operator, UnaryOperator, BinaryOperator

class Expression (object):
	def __init__ (self, tokens):
		self.depth = 0
		self.tokens = list(tokens)
	
	def __repr__ (self):
		return repr(self.tokens)
		
	def log (self, message, depth=0, **values):
		print ("{depth}"+message).format(
			depth   = '  ' * (self.depth + depth),
			tokens  = self.tokens,
			**values
		)

	def evaluate (self, **modifiers):
		"""
		The parse action for dice expressions (``expr`` in the below grammar)
		
		Rolls the UnrolledDice objects, and then calls the following operators
		"""
		self.depth = modifiers.get('depth', 1)
		
		# If verbose==False, ignore all logging calls
		if not modifiers.get('verbose', True):
			self.log = lambda *a, **k: None
		
		self.log("Evaluating the expression: {tokens!r}", depth=-1)
		try:
			# Roll the dice
			for i in xrange(len(self.tokens)):
				if isinstance(self.tokens[i], Expression):
					self.tokens[i] = self.tokens[i].evaluate(depth=self.depth+1, **modifiers)
				elif isinstance(self.tokens[i], UnrolledDice):
					dice = self.tokens[i]
					self.tokens[i] = self.tokens[i].evaluate(**modifiers)
					self.log("Rolled {n}d{s}: {roll}",
						n=dice.n, s=dice.sides, roll=list(self.tokens[i]))
			
			# Call the operators
			l = 0
			while l < len(self.tokens):
				t = self.tokens[l]
				if isinstance(t, Operator):
					# TODO: Refactor this to use Operator.terms
					if isinstance(t, UnaryOperator):
						result = t(self.tokens[l-1])
						self.tokens = self.tokens[:l-1] + [result] + self.tokens[l+1:]
					elif isinstance(self.tokens[l], BinaryOperator):
						result = t(self.tokens[l-1], self.tokens[l+1])
						self.tokens = self.tokens[:l-1] + [result] + self.tokens[l+2:]
					self.log("Called {operator}", operator=t.__class__.__name__, l=l+1)
				else:
					l += 1
		except Exception, e:
			print_exc()
			exit()
		else:
			if len(self.tokens) == 1:
				return self.tokens[0]
			else:
				return self.tokens

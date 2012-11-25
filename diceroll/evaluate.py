"""	The Expression class """

from diceroll.components import UnrolledDice, Operator

class Expression (object):
	"""	A diceroll expression object, and the evaluator for it """
	
	def __init__ (self, tokens):
		self.depth = 0
		self.tokens = list(tokens)
	
	def __repr__ (self):
		return repr(self.tokens)
		
	def log (self, message, depth=0, **values):
		"""	Print a message at a set depth """
		print ("{depth}"+message).format(
			depth   = '  ' * (self.depth + depth),
			tokens  = self.tokens,
			**values
		)
	
	@staticmethod
	def single (iterable):
		"""
		Returns a single item from a iterable if possible
		
		>>> single([1])
		1
		>>> single([1, 2, 3])
		[1, 2, 3]
		"""
		return iterable[0] if len(iterable) == 1 else iterable

	def evaluate (self, **modifiers):
		"""
		The parse action for dice expressions (``expr`` in the below grammar)
		
		Rolls the UnrolledDice objects, and then calls the following operators
		"""
		self.depth = modifiers.get('depth', 1)
		
		# If verbose==False, ignore all logging calls
		if not modifiers.get('verbose', False):
			self.log = lambda *a, **k: None
		
		self.log("Evaluating the expression: {tokens!r}", depth=-1)
		# Roll the dice, and evaluate sub-expressions
		for i in xrange(len(self.tokens)):
			if isinstance(self.tokens[i], Expression):
				self.tokens[i] = self.tokens[i].evaluate(depth=self.depth+1, **modifiers)
			elif isinstance(self.tokens[i], UnrolledDice):
				dice = self.tokens[i]
				self.tokens[i] = self.tokens[i].evaluate()
				self.log("Rolled {n}d{s}: {roll}",
					n=dice.n, s=dice.sides, roll=list(self.tokens[i]))
		
		# Call the operators
		l = 0
		while l < len(self.tokens):
			op = self.tokens[l]
			if isinstance(op, Operator):
				# The arguments are the previous and next tokens,
				# with no next token if the operator only takes 1 term
				args = [self.tokens[l-1]]
				if not op.terms < 2:
					args += [self.tokens[l+1]]
				result = op(*args)
				# The new token list is the token list with the argument tokens
				# and the operator replaced with the operators result
				self.tokens = self.tokens[:l-1] + [result] + self.tokens[l+op.terms:]
				self.log("Called {operator}: {result}", operator=op.__class__.__name__, result=result)
			else:
				# The location only needs to move on if no operator was called
				l += 1
		return Expression.single(self.tokens)

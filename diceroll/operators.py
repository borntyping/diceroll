"""	Generates the set of operators to use in the grammar """

from pyparsing import opAssoc, Literal

from dice import Dice

def only_dice (func):
	"""	Decorates a function so that it can only accept Dice objects as the first token """
	def only_dice (self, string, location, tokens):
		if not isinstance(tokens[0][0], Dice):
			raise NotImplementedError, "Operator {1} can only be used on Dice objects ({0!r} given)".format(*tokens[0][0:2])
		return func(self, tokens)
	return only_dice

class Operator (object):
	default_terms = 2
	
	def __init__ (self, expressions, function, **kwargs):
		self.expressions = list()
		self.function    = function
		self.terms       = kwargs.get('terms', self.default_terms)
		self.association = kwargs.get('association', opAssoc.LEFT)
		self.repeatable  = kwargs.get('r', False)
		
		# Add each syntax, surrounding strings in Literal()
		for s in expressions:
			if isinstance(s, str):
				s = Literal(s)
			self.expressions.append(s)
	
	def __call__ (tokens):
		return self.function(tokens)

class DiceOperator (Operator):
	"""	A single term operator that acts on dice """
	default_terms = 1
	
	@only_dice
	def __call__ (self, tokens):
		dice, op = tokens[0]
		return self.function(dice)
	
class XYOperator (Operator):
	"""	An operator that acts on two atoms, ``X`` and ``Y`` """
	def __call__ (self, tokens):
		"""
		Calls the function with ``X`` and ``Y``,
		
		The function is called repeatedly if there is a list of ``Y`` values,
		such as in the case ``1+1+1``, where ``X=1`` and ``Y=[1,1]``.
		"""
		x  = tokens[0][0]
		op = tokens[0][1]
		if not self.repeatable:
			return self.function(x, tokens[0][2])
		else:
			# Extract the value to edit from the tokens,
			# and the list of values to call the operator with
			operations = tokens[0][2:]
			while operations:
				x = self.function(x, operations.pop(0))
			return x

class DiceXYOperator (XYOperator):
	"""	Wraps the XPOperator.__call__() method in an only_dice decorator """
	__call__ = only_dice(XYOperator.__call__)
			
#: The operations to add to the operatorPrecedence syntax
operator_list = [
	# Dice only operators
	DiceOperator(['*', 'explode'],	lambda d: d.explode()),
	DiceOperator(['t', 'total'  ],	lambda d: int(d)),
	DiceOperator(['s', 'sort'   ],	lambda d: d.sort()),
	
	DiceXYOperator(['v', 'drop'],	lambda x,y: x.drop(y)),
	DiceXYOperator(['^', 'keep'],	lambda x,y: x.keep(y)),
	
	# General operators
	XYOperator(['~', 'diff'], lambda x,y: int(x) - int(y)),
	XYOperator(['*'], lambda x,y: int(x) * int(y)),
	XYOperator(['/'], lambda x,y: int(x) / int(y)),
	XYOperator(['+'], lambda x,y: int(x) + int(y)),
	XYOperator(['-'], lambda x,y: int(x) - int(y)),
]

# Create a list of operators for use with 
operators = list()
for op in operator_list:
	for expr in op.expressions:
		# (opExpr, numTerms, rightLeftAssoc, parseAction)
		operators.append((expr, op.terms, op.association, op))

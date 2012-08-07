"""	The evaluate function, and print functions for the functions it performs """

from traceback	import print_exc

from objects	import UnrolledDice
from operators	import Operator, UnaryOperator, BinaryOperator

def print_expr (string, location, tokens):
	print "Evaluating the following expression (from '{string}' at character [{location}]):\n  {tokens}\n".format(**locals())

def print_operator (operator, location, tokens):
	print "Called {operator!r} at location [{location}], tokens are now:\n  {tokens}\n".format(**locals())

def print_roll (location, tokens):
	print "Rolled dice at location [{location}], tokens are now:\n  {tokens}\n".format(**locals())

def evaluate (string, location, tokens):
	"""
	The parse action for dice expressions (``expr`` in the below grammar)
	
	Rolls the UnrolledDice objects, and then calls the following operators
	"""
	print_expr(string, location, tokens)
	try:
		tokens = list(tokens)
		
		# Roll the dice
		for i in xrange(len(tokens)):
			if isinstance(tokens[i], UnrolledDice):
				tokens[i] = tokens[i].roll()
				print_roll(i, tokens)
		
		# Call the operators
		l = 0
		while l < len(tokens):
			t = tokens[l]
			if isinstance(t, Operator):
				if isinstance(t, UnaryOperator):
					result = t(tokens[l-1])
					tokens = tokens[:l-1] + [result] + tokens[l+1:]
				elif isinstance(tokens[l], BinaryOperator):
					result = t(tokens[l-1], tokens[l+1])
					tokens = tokens[:l-1] + [result] + tokens[l+2:]
				print_operator(t, l, tokens)
			else:
				l += 1
	except Exception, e:
		print_exc()
		exit()
	else:
		return tokens

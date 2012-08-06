"""	The expression parser """

from traceback import print_exc

from pyparsing import *

ParserElement.enablePackrat()

from objects import Number, RolledDice, UnrolledDice 
from operators import Operator, UnaryOperator, BinaryOperator
from operators import unary_operator_list, binary_operator_list

def print_expr (string, location, tokens):
	print "Evaluating the following expression (from '{string}' at character [{location}]):\n  {tokens}\n".format(**locals())

def print_operator (operator, location, tokens):
	print "Called {operator.__class__.__name__} at location [{location}], tokens are now:\n  {tokens}\n".format(**locals())

def print_roll (location, tokens):
	print "Rolled dice at location [{location}], tokens are now:\n  {tokens}\n".format(**locals())
	
def evaluate (string, location, tokens):
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

# Numbers are evaluated to Number objects
number = Word(nums).setName("number")
number.setParseAction(lambda tokens: Number(tokens[0]))

expr = Forward()
expr.setParseAction(evaluate)

# Dice are evaluated to UnrolledDice objects
dice = Optional(number, default=1) + CaselessLiteral("d") + number
dice.setParseAction(lambda t: UnrolledDice(t[0], t[2]))

# Subexpressions allow atoms to be another expression surrounded by brackets
lparen = Literal('(').suppress()
rparen = Literal(')').suppress()
sub_expr = lparen + expr + rparen

# Unary operators must be placed after an atom
unary_operators = list()
for names, function in unary_operator_list:
	for name in names:
		unary_operators.append(name.setParseAction(function))
unary_operators = Or(unary_operators)

# An atom is the smallest part of an expression
atom = (dice | number | sub_expr) + ZeroOrMore(unary_operators)
atom.setName('dice, number or expression')

# Binary operators must both follow and precede an atom
binary_operators = list()
for names, function in binary_operator_list:
	for name in names:
		# BinaryOperators must allways be followed by an atom
		operator = name + FollowedBy(atom)
		# The parse action should create an Operator instance from the given tokens
		operator.setParseAction(function)
		binary_operators.append(operator)
binary_operators = Or(binary_operators)

expr << atom + ZeroOrMore(binary_operators + atom)
comment = dblSlashComment.suppress().setName("comment")
dicerollexpression = StringStart() + expr + Optional(comment) + StringEnd()

def roll (string):
	result = dicerollexpression.parseString(string)
	return result[0] if len(result) == 1 else result

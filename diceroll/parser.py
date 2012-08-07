"""	The expression parser """

__all__ = ['number', 'dice', 'expr', 'sub_expr', 'unary_operators', 'binary_operators', 'comment', 'dicerollexpression', 'roll']

from pyparsing	import *

ParserElement.enablePackrat()

from evaluate	import evaluate
from objects	import UnrolledDice
from operators	import *

# Numbers are evaluated to Number objects
number = Word(nums).setName("number")
number.setParseAction(lambda tokens: int(tokens[0]))

# Dicerolls are evaluated to UnrolledDice objects
dice = Optional(number, default=1) + CaselessLiteral("d") + number
dice.setParseAction(lambda t: UnrolledDice(n=t[0], sides=t[2]))

# The expression grammar is defined later,
# but is created here so that it can be included in sub-expressions
expr = Forward()
expr.setParseAction(evaluate)

# Subexpressions allow atoms to be another expression surrounded by brackets
lparen = Literal('(').suppress()
rparen = Literal(')').suppress()
sub_expr = lparen + expr + rparen

# Unary operators are made up of a list of parse elements,
# and a function that takes the parsed tokens and returns a UnaryOperator object
# The UnaryOperator object will be called with the previous token at evaluation time
unary_operator_list = [
	([Literal('*'), CaselessLiteral('explode')], Explode),
	
	([CaselessLiteral('t'), CaselessLiteral('total')],
		generic_unary('Total', lambda x: int(x))),
	
	([CaselessLiteral('s'), CaselessLiteral('sort')],
		generic_unary('Sort',  lambda x: x.sort())),
]

# Unary operators must be placed after an atom
unary_operators = list()
for names, function in unary_operator_list:
	unary_operators.extend([name.setParseAction(function) for name in names])
unary_operators = Or(unary_operators)

# An atom is the smallest part of an expression
atom = (dice | sub_expr) + ZeroOrMore(unary_operators) | number
atom.setName('dice, number or expression')

# If numbers had any unary operators, atom could be defined as:
# atom = (dice | number | sub_expr) + ZeroOrMore(unary_operators)

# Binary operators work in much the same was as unary operators,
# but will be given the tokens to their left and right when evaluated
binary_operator_list = [
	([CaselessLiteral('rr'), CaselessLiteral('rreroll')], RecursiveReroll),
	([CaselessLiteral('r'),  CaselessLiteral('reroll')], Reroll),
	([CaselessLiteral('v'),  CaselessLiteral('drop')], Drop),
	([Literal('+')], generic_binary('Plus',      lambda x,y: x + y)),
	([Literal('-')], generic_binary('Minus',     lambda x,y: x - y)),
	([Literal('*')], generic_binary('Multiply',  lambda x,y: x * y)),
	([Literal('/')], generic_binary('Divide',    lambda x,y: x / y)),
	([Literal(',')], Join),
	([Literal('^'), CaselessLiteral('keep')], Keep),
	([Literal('~'), CaselessLiteral('diff')], generic_binary('Diffrence',	lambda x,y: int(x) - int(y))),
	(Success.grammars, Success),
]

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

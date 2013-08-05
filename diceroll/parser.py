"""	The expression parser """

__all__ = ['number', 'dice', 'expr', 'sub_expr', 'unary_operators', 'binary_operators', 'expressions', 'comment', 'dicerollexpression', 'roll']

from pyparsing	import *

ParserElement.enablePackrat()

from evaluate	import Expression
from components	import *

# Numbers are evaluated to Number objects
number = Word(nums).setName("number")
number.setParseAction(lambda tokens: int(tokens[0]))

# RolledDice are evaluated to UnrolledDice objects
dice = Optional(number, default=1) + CaselessLiteral("d") + number
dice.setParseAction(lambda t: UnrolledDice(n=t[0], sides=t[2]))

# The expression grammar is defined later,
# but is created here so that it can be included in sub-expressions
expr = Forward()
expr.setParseAction(Expression)

# Subexpressions allow atoms to be another expression surrounded by brackets
lparen = Literal('(').suppress()
rparen = Literal(')').suppress()
sub_expr = lparen + expr + rparen

# All current unary operators only operate on dice and subexpressions that return dice
unary_operators = list()
for operator in [Explode, Sort, Total]:
	for grammar in operator.grammars:
		unary_operators.append(grammar.setParseAction(operator))
unary_operators = Or(unary_operators)

# An atom is the smallest part of an expression
atom = ( dice | sub_expr ) + ZeroOrMore(unary_operators) | number
atom.setName('dice, number or expression')

# Binary operators must both follow and precede an atom
binary_operators = list()
for operator in [Drop, Keep, Reroll, RecursiveReroll, Success, Plus, Minus, Multiply, Divide]:
	for grammar in operator.grammars:
		# BinaryOperators must allways be followed by an atom
		grammar = grammar + FollowedBy(atom)
		# The parse action should create an Operator instance from the given tokens
		grammar.setParseAction(operator)
		binary_operators.append(grammar)
binary_operators = Or(binary_operators)

expr <<= atom + ZeroOrMore(binary_operators + atom)
expressions = expr + ZeroOrMore(Literal(',').suppress() + expr)
comment = dblSlashComment.suppress().setName("comment")
dicerollexpression = StringStart() + expressions + Optional(comment) + StringEnd()

def roll (expression, **modifiers):
	"""
	Parse and evaluate the given expression
	
	All keywords are passed on to the calls to :py:func:``~Expression.evaluate`` and :py:func:``~components.UnrolledDice.roll``
	
	:Keywords:
		- `single` (bool): Apply :py:func:`single` to the resulting list. Defaults to True.
	"""
	parsed = dicerollexpression.parseString(expression)
	result = [expr.evaluate(**modifiers) for expr in parsed]
	return Expression.single(result) if modifiers.get('single', True) else result

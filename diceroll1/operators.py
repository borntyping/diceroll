"""	Operator classes """

from pyparsing import Literal

class Operator (object):
	__name__ = None
	
	@classmethod
	def new (cls, name, function):
		return lambda tokens: cls(name, function)
	
	def __repr__ (self):
		return "<{0}{1}>".format(self.__class__.__name__, "." + self.__name__ or "")

class UnaryOperator (Operator):
	operators = list()
	
	def __init__ (self, name, function):
		self.__name__ = name
		self.function = function
	
	def __call__ (self, left):
		return self.function(left)

unary_operator_list = [
	([Literal('t')], UnaryOperator.new('Total', lambda x: int(x))),
]
		
class BinaryOperator (Operator):
	operators = list()
	
	def __init__ (self, name, function):
		self.__name__ = name
		self.function = function
	
	def __call__ (self, left, right):
		return self.function(left, right)

binary_operator_list = [
	([Literal('+')], BinaryOperator.new('Plus',     lambda x,y: x + y)),
	([Literal('-')], BinaryOperator.new('Minus',    lambda x,y: x - y)),
	([Literal('*')], BinaryOperator.new('Multiply', lambda x,y: x * y)),
	([Literal('/')], BinaryOperator.new('Divide',   lambda x,y: x / y)),
]

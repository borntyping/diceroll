""" The pyparsing grammar """

from pyparsing import *

# Enable pyarsings packrat mode, seems to provide a massive speed increase.
ParserElement.enablePackrat()

from dice import Dice
from operators import operators

# Parse numbers into integer values
number = Word(nums)
number.setParseAction(lambda tokens: int(tokens[0]))
number.setName("number")

# Parse dice into a list of rolls
dice = Optional(number, default=1) + CaselessLiteral("d").suppress() + number
dice.setParseAction(lambda tokens: [Dice.roll(tokens[0], tokens[1])])

# Comments
comment = Optional(dblSlashComment).suppress()

#: The final diceroll expression
expression = StringStart() + operatorPrecedence(dice | number, operators) + comment + StringEnd()

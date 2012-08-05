diceroll
========

``diceroll`` is a simple command line dice roller.

It can be invoked through the ``roll`` command once installed.

Requirements
------------

Requires the `pyparsing <http://pypi.python.org/pypi/pyparsing/>`_ library.

Syntax
------

``[N]dS``

A set of dice to roll, where ``N`` (optional, defaults to 1) is the number of dice to roll, and ``S`` is the number of sides the dice has.

This returns a list of dice rolls. Numerical operators that are applied to the list (such as ``+``, ``-``, etc) will use the sum total of the dice rolls.

``X + Y``, ``X - Y``, ``X * Y``, ``X / Y``

Performs a basic operation on two atoms (each either a diceroll or an integer) - respectively addition, subtraction, multiplication, division.

``DvN``

Drop the ``N`` lowest rolls from diceroll ``D``.

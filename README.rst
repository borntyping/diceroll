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

``DvN``, ``DdropN``

Drop the ``N`` lowest rolls from diceroll ``D``.

``D^N``, ``DkeepN``

Similar to drop, keeps the ``N`` highest rolls from ``D``.

``X~Y``, ``XdiffY``

Returns the difference between ``X`` and ``Y``.

``Dt``, ``Dtotal``

Returns the sum total of diceroll ``D``.

``D*``, ``Dexplode``

Rolls an extra die for every diceroll that hits the maximum.

Future syntax
-------------

``DsuccessN``

Return the count of dice in ``D`` that land equal to or higher than ``N``.

``[D]successC[N]``

As above, but removes a success every time a die hits the minimum.

``[D]successB[N]``

As ``success``, but adds a success every time a die lands on the maximum.

``DrerollN``

Reroll any dice in ``D`` that are equal to or lower than ``N``.

``[D]o``, ``Dsort``

Sorts the rolls from lowest to highest.

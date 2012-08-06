diceroll
========

``diceroll`` is a simple command line dice roller.

It can be invoked through the ``roll`` command once installed.

Requirements
------------

Requires the `pyparsing <http://pypi.python.org/pypi/pyparsing/>`_ library.

Syntax
------

``[N]d[S]``

A set of dice to roll, where ``N`` (optional, defaults to 1) is the number of dice to roll, and ``S`` is the number of sides the dice has.

This returns a list of dice rolls. Numerical operators that are applied to the list (such as ``+``, ``-``, etc) will use the sum total of the dice rolls.

Dice only operators
*******************

These operators can be used on dice objects, and are listed in order of priority. Some do not return a Dice object, and should not be used before operators that do.

``[D]v[N]``, ``[D]drop[N]``

Drop the ``N`` lowest rolls from diceroll ``D``. 

``[D]^[N]``, ``[D]keep[N]``

Similar to drop, keeps the ``N`` highest rolls from ``D``.

``[D]*``, ``[D]explode``

Rolls an extra die for every diceroll that hits the maximum.

``[D]t``, ``[D]total``

Returns the sum total of diceroll ``D`` (as an integer value).

``[D]o``, ``[D]sort``

Sorts the rolls from lowest to highest.

Other operators
***************

These operators can be used on any two atoms (each either a diceroll or an integer) ``X`` and ``Y``.

``X~[Y]``, ``Xdiff[Y]``

Returns the difference between ``X`` and ``Y``.

``[X] + [Y]``, ``[X] - [Y]``, ``[X] * [Y]``, ``[X] / [Y]``

Performs a basic operation on two atoms  - respectively addition, subtraction, multiplication, division.

Future syntax
-------------

``[D]success[N]``

Return the count of dice in ``D`` that land equal to or higher than ``N``.

``[D]successC[N]``

As above, but removes a success every time a die hits the minimum.

``[D]successB[N]``

As ``success``, but adds a success every time a die lands on the maximum.

``[D]reroll[N]``

Reroll any dice in ``D`` that are equal to or lower than ``N``.


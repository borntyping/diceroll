diceroll
========

``diceroll`` is a simple command line dice roller.

It can be invoked through the ``roll`` command once installed.

Requirements
------------

Requires the `pyparsing <http://pypi.python.org/pypi/pyparsing/>`_ library.

Syntax
------

``<N>d<S>``

A set of dice to roll, where ``N`` (optional, defaults to 1) is the number of dice to roll, and ``S`` is the number of sides the dice has.

This returns a list of dice rolls. Numerical operators that are applied to the list (such as ``+``, ``-``, etc) will use the sum total of the dice rolls.

Dice only operators
*******************

These operators can be used on dice objects, and are listed in order of priority. Some do not return a Dice object, and should not be used before operators that do.

Dice operators which take ``Y`` (such as ``drop`` and ``keep``) may not be followed by a dice only operator, unless you surround the expression in brackets ``()`` before continuing. Failing to do this will result in the dice only operator trying to act on ``Y``, and not the result of the previous expression. For example::

	roll "5d6^3explode"
	NotImplementedError: Operator explode can only be used on Dice objects (3 given)
	
	roll "(5d6^3)explode"
	6, 5, 5, 1

``<X>*``, ``<X>explode``

Rolls an extra die for every diceroll that hits the maximum.

``<X>t``, ``<X>total``

Returns the sum total of diceroll ``X`` (as an integer value).

``<X>o``, ``<X>sort``

Sorts the rolls from lowest to highest.

``<D>success[C][B]<N>``

Return the count of dice in ``D`` that land equal to or higher than ``N``. ``C`` and ``B`` are optional flags: ``C`` removes a success every time a die hits the minimum and ``B`` adds a success every time a die lands on the maximum.

``<X>v<Y>``, ``<X>drop<Y>``

Drop the ``Y`` lowest rolls from diceroll ``X``. 

``<X>^<Y>``, ``<X>keep<Y>``

Similar to drop, keeps the ``Y`` highest rolls from ``X``.


Other operators
***************

These operators can be used on any two atoms (each either a diceroll or an integer) ``X`` and ``Y``.

``X~<Y>``, ``Xdiff<Y>``

Returns the difference between ``X`` and ``Y``.

``<X> * <Y>``, ``<X> / <Y>``, ``<X> + <Y>``, ``<X> - <Y>``

Performs a basic operation on two atoms  - respectively multiplication, division, addition, subtraction.

Future syntax
-------------

``<D>reroll<N>``

Reroll any dice in ``D`` that are equal to or lower than ``N``.


========
diceroll
========

.. image:: https://pypip.in/v/diceroll/badge.png
    :target: https://crate.io/packages/diceroll/
    :alt: Latest PyPI version

.. image:: https://pypip.in/d/diceroll/badge.png
    :target: https://crate.io/packages/diceroll/
    :alt: Number of PyPI downloads

``diceroll`` is a simple command line dice roller.

It can be invoked through the ``roll`` command once installed.

Requirements
************

Requires the `pyparsing <http://pypi.python.org/pypi/pyparsing/>`_ library.

Expression syntax
*****************

The basic components of ``diceroll`` expressions are dice and integers, which can then have operators applied to them. The expression is always read left-to-right, so operators are called in order of position, *not* order of precedence.

Multiple expressions can be given, seperated by commas (``,``).

Dice are expressed in the form ``<N>d<S>``, where ``N`` is the number of dice that will be rolled, and ``S`` is the number of sides those dice have.

Integers are simply expressed as one or more digits (i.e. ``0-9``).

Subexpressions can be placed in parenthesis ``()``, and are evaluated in full before the main expression is evaluated.

Operators
^^^^^^^^^

Unary operators
~~~~~~~~~~~~~~~

These operators act on the previous component, and almost always accept only dice.

Total
-----

``<D>t``, ``<D> total``: Returns the sum total of the diceroll (as an integer value).

Sort
----

``<D>s``, ``<D>sort``: Sorts diceroll ``D``.

Explode
-------

``<D>x``, ``<D>explode``: Rolls an extra die for every diceroll that hits the maximum.

Binary Operators
~~~~~~~~~~~~~~~~

These operators act on two components (the previous and the next).

Arithmetic
----------

``<X>*<Y>``, ``<X>/<Y>``, ``<X>+<Y>``, ``<X>-<Y>``

Performs a basic operation on two components - respectively multiplication, division, addition, subtraction. Dicerolls are converted to integers, using the sum total of the rolls.

Drop and Keep
-------------

``<X>v<Y>``, ``<X>drop<Y>``: Drop the ``Y`` lowest rolls from diceroll ``X``.
``<X>^<Y>``, ``<X>keep<Y>``: Similar to drop, keeps the ``Y`` highest rolls from ``X``.

Reroll and Recursive Reroll
---------------------------

``<D>r<N>``, ``<D>reroll<N>``: Reroll any dice in ``D`` that are equal to or lower than ``N``.
			
``<D>rr<N>``, ``<D>rreroll<N>``: The same as ``reroll``, but does so recursively - any rerolled dice equal to or lower than ``N`` are also rerolled

Diff
----

``<X>~<Y>``, ``<X>diff<Y>``: Returns the difference between ``X`` and ``Y``.
			
Success
-------

``<D> success [C][B] <N>``	Returns the count of dice in ``D`` that land equal to or higher than ``N``. ``C`` and ``B`` are optional flags: ``C`` removes a success every time a die hits the minimum, ``B`` adds a success every time a die lands on the maximum.

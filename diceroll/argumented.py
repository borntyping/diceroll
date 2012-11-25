"""
`argumented` provides a way of 'multiplying' functions - usually test cases -
allowing them to be called with multiple argument sets and still appear as
seperate test cases.

In the following example, `test_with_arguments` would be replaced with two
functions (`test_with_arguments_0` and `test_with_arguments_1`), each of which
would called the test with one of the given arguments.

`test_greeting` would also be replaced with two functions, each calling one of
the argument sets given to the decorators. `test_greeting_0` would print "hello
world", and `test_greeting_1` would print "goodbye world"

The original test cases are removed from the class.

	@unpack_arguments
	class TestArgumentedCases (unittest.TestCase):
	
		@arguments(1, 2)
		def test_with_arguments (self, n):
			self.assertIsInstance(n, int)
			
		@argument("hello", thing="world")
		@argument("goodbye", thing="world")
		def test_greeting (self, greeting, thing):
			print "{} {}".format(greeting, thing)
			
Originally inspired by [github.com/santtu/ddt](http://github.com/santtu/ddt),
though it ended up working somewhat diffrently.
"""

from functools import wraps

def unpack_arguments (cls):
	"""
	Unpacks any function in the class that has a list of argumented functions
	
	The argumented functions are set as attributes on the class,
	and the original function is removed from the class
	"""
	for name, attr in cls.__dict__.items():
		if callable(attr) and hasattr(attr, '__argumented__'):
			for i, func in enumerate(attr.__argumented__):
				setattr(cls, name + "_" + str(i), func)
			delattr(cls, name)
	return cls

def pack_arguments (func, *args, **kwargs):
	"""
	Packs a wrapper around `func` into `func.__argumented__`
	
	The wrapper calls `func` with the given arguments, and will be moved into
	the main namespace when `@unpack_arguments` is called on the class
	containing the function.
	"""
	
	# Ensure the list of argumented functions exists
	if not hasattr(func, '__argumented__'):
		func.__argumented__ = []
	
	# Create a wrapper for the function, using the given arguments
	@wraps(func)
	def argumented_function (self):
		return func(self, *args, **kwargs)
		
	# Add the function to the argumented list
	func.__argumented__.append(argumented_function)
	
	return func

def argument (*args, **kwargs):
	"""	Calls `pack_arguments` with the given arguments """
	return lambda f: pack_arguments(f, *args, **kwargs) and f
	
def arguments (*args):
	"""	Calls `pack_arguments` with each given argument """
	return lambda f: [pack_arguments(f, a) for a in args] and f

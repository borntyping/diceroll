"""
`argumented` provides a way of 'multiplying' functions - usually test cases -
allowing them to be called with multiple argument sets and still appear as
seperate test cases.

In the following example, each of the test cases would be replaced with two test
cases, each of which would call the test case with the given arguments.

`@argument(*args, **kwargs)`

Will call the test case with the given argument set

`@argument_list(*args)`

Will call the test case with each item in `*args`

`@argument_tuples(*args)`

Each item in `*args` must be a tuple containing an interable and a mapping,
which will then be used as an argument set for the test case (i.e. `([], {})`)

The decorators can be used multiple times, or used together - each of them 
takes the arguments they are given and passes it to `pack_arguments(func, *args,
**kwargs)`, which adds a wrapped function to `func.__argumented__`.

	@unpack_arguments
	class TestArgumentedCases (unittest.TestCase):
			
		@argument("hello", thing="world")
		@argument("goodbye", thing="world")
		def test_greeting (self, greeting, thing):
			self.assertIn(greeting, ["hello", "goodbye"])
			self.assertEquals(thing, "world")
		
		@argument_list(1, 2)
		def test_with_arguments (self, n):
			self.assertIsInstance(n, int)
		
		@argument_tuples( ([1, 2], {'a': 'A'}), ([1, 2], {'a': 'B'}) )
		def test_with_arguments (self, *args, *kwargs):
			self.assertEquals(args, (1, 2))
			self.assertIn(kwargs['a'], ['A', 'B'])
			
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
	
def argument_list (*args):
	"""	Calls `pack_arguments` with each given argument """
	return lambda f: [pack_arguments(f, a) for a in args] and f

def argument_tuples (*args):
	"""	Calls `pack_arguments` with each given argument list """
	return lambda f: [pack_arguments(f, *a, **b) for (a, b) in args] and f

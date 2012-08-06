#!/usr/bin/python

__version__ = 0.4
__all__     = ['expression', 'roll']

from grammar import expression

def roll (expr):
	""" Roll ``expr`` """
	return expression.parseString(expr)[0]

def cli ():
	""" Command line entry point """
	import sys, argparse
	parser = argparse.ArgumentParser(description="Return the results of a dice expression")
	
	parser.add_argument('--version', action='version',
		version='bones v%s' % __version__)
	
	parser.add_argument('--profile', action='store_true',
		help='run using the cProfile profiler')
	
	parser.add_argument('expression', type=str,
		help='the expression to roll')
	
	args = parser.parse_args()
	
	if args.profile:
		import cProfile
		cProfile.runctx('print roll(args.expression)', globals(), locals())
	else:
		print roll(args.expression)

if __name__ == '__main__': cli()

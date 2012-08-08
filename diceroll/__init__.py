"""	Command line entry point and metadata """

__version__ = 1.2

from parser		import roll
from pyparsing	import ParseException

def command ():
	""" Command line entry point """
	import sys, argparse
	parser = argparse.ArgumentParser(description="Return the results of a dice expression")
	
	parser.add_argument('--version', action='version',
		version='bones v%s' % __version__)
	
	parser.add_argument('-v', '--verbose', action='store_true',
		help='log the evaluation')
	
	parser.add_argument('expression', type=str,
		help='the expression to roll')
		
	args = parser.parse_args()
	
	try:
		result = roll(**vars(args))
		if args.verbose:
			print "Result:",
		print result
	except ParseException as e:
		import sys
		print >> sys.stderr, "Parse failed:", e

if __name__ == '__main__':
	command()

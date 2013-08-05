#!/usr/bin/python

from setuptools import setup, find_packages

setup(
	name             = 'diceroll',
	version          = '2.3',

	author           = 'Sam Clements',
	author_email     = 'sam@borntyping.co.uk',
	url              = 'https://github.com/borntyping/diceroll',
	
	description      = 'A command line dice roller',
	long_description = open('README.rst').read(),
	
	packages         = find_packages(),
	install_requires = ['pyparsing>=1.5.6'],
	tests_require    = ['argumented'],
	
	entry_points     = {
        'console_scripts': [
            'roll  = diceroll:command',
        ]
    },

	classifiers     = [
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Terminals',
        'Topic :: Utilities',
    ],
)

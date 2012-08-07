#!/usr/bin/python

from setuptools import setup, find_packages
from diceroll import __version__

setup(
    name             = 'diceroll',
    version          = __version__,

    author           = 'Sam Clements',
    author_email     = 'sam@borntyping.co.uk',
    url              = 'https://github.com/borntyping/diceroll',
    
    description      = 'A command line dice roller',
    long_description = open('README.rst').read(),
    
    packages         = find_packages(),
    install_requires = ['pyparsing>=1.5.6'],
    
    entry_points = {'console_scripts': [
		'roll  = diceroll:command',
	]},
)

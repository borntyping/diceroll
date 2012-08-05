#!/usr/bin/python

from setuptools import setup, find_packages
from bones import __version__

setup(
    name             = 'bones',
    version          = __version__,

    author           = 'Sam Clements',
    author_email     = 'sam@borntyping.co.uk',
    url              = 'https://github.com/borntyping/bones',
    
    description      = 'A command line dice roller',
    long_description = open('README.rst').read(),
    
    packages         = find_packages(),
    
    entry_points = {'console_scripts': [
		'roll  = bones:bones [pyparsing]',
	]},
)

#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from distutils.core import setup

try:
    # 3.x
    from distutils.command.build_py import build_py_2to3 as build_py
except ImportError:
    # 2.x
    from distutils.command.build_py import build_py

cmdclass = {'build_py': build_py}
command_options = {}

setup(
    name='CSV2XML',
    version='0.0.1',
    author='Vauxoo team',
    author_email='info@vauxoo.com',
    packages=['csv2xml'],
    scripts=['bin/csv2xml'],
    #~ url='http://pypi.python.org/pypi/.../',
    #~ license='LICENSE.txt',
    description='Updating openerp module xml data tool via csv files.',
    #~ keywords= define keywords,
    long_description=open('README.rst').read(),
    #~ install_requires=[],
    cmdclass=cmdclass,
    command_options=command_options,
)

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
    author='Vauxoo Team',
    author_email='info@vauxoo.com',
    packages=['csv2xml'],
    package_data={'csv2xml': [
        'data/__config__.py',
        'data/csv/account_account/*',
        'data/csv/account_account_type/*',
        'data/csv/account_fiscalyear/*',
        'data/csv/account_journal/*',
        'data/csv/account_tax/*',
        'data/csv/islr_wh_concept/*',
        'data/csv/product_category/*',
        'data/csv/product_product/*',
        'data/csv/product_uom/*',
        'data/csv/product_uom_categ/*',
        'data/csv/res_bank/*',
        'data/csv/res_company/*',
        'data/csv/res_currency/*',
        'data/csv/sale_shop/*',
        'data/csv/stock_location/*',
        'data/csv/stock_warehouse/*',
        ]},
    scripts=['bin/csv2xml'],
    #~ url='http://pypi.python.org/pypi/.../',
    #~ license='LICENSE.txt',
    description='Updating openerp module xml data tool via csv files.',
    keywords= ['openerp', 'csv', 'xml'],
    long_description=open('README.rst').read(),
    #~ install_requires=[],
    cmdclass=cmdclass,
    command_options=command_options,
)

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
        'data/csv_template/__config__.py',
        'data/csv_template/account_account/*',
        'data/csv_template/account_account_type/*',
        'data/csv_template/account_fiscalyear/*',
        'data/csv_template/account_journal/*',
        'data/csv_template/account_tax/*',
        'data/csv_template/islr_wh_concept/*',
        'data/csv_template/product_category/*',
        'data/csv_template/product_product/*',
        'data/csv_template/product_uom/*',
        'data/csv_template/product_uom_categ/*',
        'data/csv_template/product_pricelist/*',
        'data/csv_template/res_bank/*',
        'data/csv_template/res_company/*',
        'data/csv_template/res_currency/*',
        'data/csv_template/sale_shop/*',
        'data/csv_template/stock_location/*',
        'data/csv_template/stock_warehouse/*',
        'data/csv_template/res_users/*',
        'data/csv_template/res_partner/*',
        'data/csv_template/res_country_state/*',
        'data/csv_template/payment_term/*',
        'data/csv_template/hr/*',
        'data/csv_template/stock_warehouse_orderpoint/*',
        'data/csv_template/ir_sequence/*',
        'data/csv_template/ir_mail_server/*',
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

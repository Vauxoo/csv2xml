#!/usr/bin/python
# -*- encoding: utf-8 -*-
###############################################################################
#    Module Writen to OpenERP, Open Source Management Solution
#    Copyright (C) OpenERP Venezuela (<http://www.vauxoo.com>).
#    All Rights Reserved
############# Credits #########################################################
#    Coded by: Katherine Zaoral <kathy@vauxoo.com>
#    Planified by: Katherine Zaoral <kathy@vauxoo.com>
#    Audited by: Katherine Zaoral <kathy@vauxoo.com>
###############################################################################
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
###############################################################################

{
    'name': 'mycompany_data',
    'version': '1.0',
    'author': 'Vauxoo',
    'website': 'http://www.vauxoo.com/',
    'category': '',
    'description': '''
''',
    'depends': [
        "base",
        "account",
        "sale",
        "stock",
        "ovl",
        "account_anglo_saxon",
        ],
    'data': [
        'data/account_account.xml',
        'data/account_account_type.xml',
        'data/account_fiscalyear.xml',
        'data/account_journal.xml',
        'data/account_tax.xml',
        'data/islr_wh_concept.xml',
        'data/res_bank.xml',
        'data/res_company.xml',
        'data/res_currency.xml',
        'data/sale_shop.xml',
        'data/stock_location.xml',
        'data/stock_warehouse.xml',
    ],
    'demo': [],
    'test': [],
    'active': False,
    'installable': True,
}

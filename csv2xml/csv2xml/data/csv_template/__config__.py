[
    {'ir_sequence': {
        'depends': 'base',
        'csv': ['ir_sequence_type.csv','ir_sequence.csv']
        }},
    {'account_account_type': {
        'depends': 'account',
        'csv': ['account_account_type.csv']
        }},
    {'account_account': {
        'depends': 'account',
        'csv': ['account_account.csv']
        }},
    {'account_fiscalyear': {
        'depends': 'account',
        'csv': ['account_fiscalyear.csv', 'account_period.csv']
        }},
    {'account_journal': {
        'depends': 'account',
        'csv': ['account_journal.csv']
        }},
    {'account_tax': {
        'depends': 'account',
        'csv': ['account_tax.csv']
        }},
    {'res_company': {
        'depends': 'base',
        'csv': ['res_company.csv']
        }},
    {'islr_wh_concept': {
        'depends': 'l10n_ve_withholding_islr',
        'csv': ['islr_wh_concept.csv']
        }},
    {'payment_term': {
        'depends': 'account',
        'csv': ['payment_term.csv', 'account_payment_term_line.csv']
        }},

    {'product_uom_categ': {
        'depends': 'product',
        'csv': ['product_uom_categ.csv']
        }},
    {'product_uom': {
        'depends': 'product',
        'csv': ['product_uom.csv']
        }},
    {'product_category': {
        'depends': 'product',
        'csv': ['product_category.csv']
        }},
    {'product_product': {
        'depends': 'product',
        'csv': ['product_template.csv', 'product_product.csv']
        }},
    {'product_pricelist': {
        'depends': 'product',
        'csv': ['product_pricelist.csv',
        'product_pricelist_version.csv','product_pricelist_item.csv']
        }},

    {'res_country_state': {
        'depends': 'base',
        'csv': ['res_country_state.csv']
        }},
    {'res_bank': {
        'depends': 'base',
        'csv': ['res_bank.csv']
        }},
    {'res_currency': {
        'depends': 'base',
        'csv': ['res_currency.csv','res_currency_rate.csv']
        }},

    {'res_partner': {
        'depends': 'base',
        'csv': ['res_partner.csv','res_partner_bank.csv']
        }},
    {'res_groups': {
        'depends': 'base',
        'csv': ['res_groups.csv']
        }},
    {'res_users': {
        'depends': 'base',
        'csv': ['res_users.csv']
        }},

    {'hr': {
        'depends': 'hr',
        'csv': ['hr_employee_category.csv', 'hr_job.csv', 'hr_department.csv', 'hr_employee.csv', 'hr_department_2.csv', 'hr_job_2.csv']
        }},

    {'stock_location': {
        'depends': 'stock',
        'csv': ['stock_location.csv']
        }},
    {'stock_warehouse': {
        'depends': 'stock',
        'csv': ['stock_warehouse.csv']
        }},
    {'sale_shop': {
        'depends': 'sale',
        'csv': ['sale_shop.csv']
        }},
    {'stock_warehouse_orderpoint': {
        'depends': 'stock',
        'csv': ['stock_warehouse_orderpoint.csv']
        }},
    {'ir_mail_server' : {
        'depends': 'base',
        'csv': ['ir_mail_server.csv']
        }},
    {'fetchmail_server': {
        'depends': 'fetchmail',
        'csv': ['fetchmail_server.csv']
}},
]

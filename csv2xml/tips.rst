TIPS
----

- account_account_type:

  - xml_id of the form att_typename.
  - 'report_type' columne if not defined must be 'none' value.

- account_account:

  - xml id of the form aa_coa_000, aa_coa_001, etc.
  - before fill the 'user_type' field create the 'account_account_type.csv'
    records.
  - always need to define the 'aa_coa_000' like a view account fore be the top
    of the account chartter.

- res.country.state:

    - the 'country_id' column is of type search, only need to add the country
      code. Example: For Venezuela type 'VE'.

- res_partner:

    - overwrite the 'base.main_partner' record updating the needed columns.
    - the 'country_id' column is of type search, only need to add the country
      code. Example: For Venezuela type 'VE'.
    - first need to describe the 'res_country_state.csv' record.
    - I recommend notification_email_send attribute put it at 'all'

- stock.location:

    - overwrite the "stock.stock_location_company" record updating the 'name'
      column. with your company name. 
    - xml_id rcords using the format 'sl_mycompany_001' y 'sl_mycompany_002'.
    - 'company_id' column must be linked to the 'base.main_company' record.
    - 'location_id' column must be linked to the 'stock.stock_location_company'

- stock.warehouse:

    - For fill the "lot_input_id", "lot_output_id", "lot_stock_id" columns need
      to first the stock_location.csv records. 
    - overweirte the "stock.warehouse0" record and only change the 'name'
      column to add your company information.
    - xml_id of the new records is recommended to be of the form
      'sw_warehouse_001' and 'sw_warehouse_002'
    - 'company_id' column must be linked to the 'base.main_company' record.
    - We recommend to use the "" inside the name column if yor are goint to use
      complex sentences for stock warehouse names (special characters or use of
      colons or another separators).

- account.period:

    - This csv file have generic data preloaded. Must not be change if it will
      used for a venezuelan non-multiple company.
    - xml_id format is like 'ap_mycompany_01', 'ap_mycompany_02', etc.
    - all the period must be related to the 'af_mycompany' at the
      fiscalyear_id.
    - 'company_id' column must be linked to the 'base.main_company' record.

- account.fiscalyear:

    - This csv file have generic data preloaded. Must not be change if it will
      used for a venezuelan non-multiple company.
    - If you need to create a new fislcalyear record take into account that you
      need to create also the corresponding periods.
    - 'company_id' column must be linked to the 'base.main_company' record.

- sale.shop:

    - overwrithe the 'sale.sale_shop_1' record.
    - 'warehouse_id' column must be realted to a 'stock.warehouse' record
      created in the stock.warehouse.csv file.
    - 'company_id' column must be linked to the 'base.main_company' record.

- account.tax:

    - This csv file have generic data preloaded. Must not be change if it will
      used for a venezuelan company.
    - xml_id format like 'at_mycomany' ... 
    - The only files that need to be fill are the 'account_paid_id' and
      'account_collected_id'. This are account.account records first created in
      account_account.csv. They belogs to VAT Credit and VAT Debit accounts. It
      is a search file so the sccount code numbre is the one to be writed in
      this field.

- account.journal:

    - This csv file have generic data preloaded. Must not be change if it will
      used for a non-multiple venezuelan company.
    - 'company_id' column must be linked to the 'base.main_company' record.

- islr.wh.concept:

    - This csv file have generic data preloaded for venezuelan company, pull
      from the openerp venezuela localization data.
    - The only columns that need to be set are the
      'property_retencion_islr_payable' and
      'property_retencion_islr_receivable' columns. This columns type is
      account.account type. Refefers to the accounts that will be use to save
      the withholding. First need to declare this accounts at the
      account.account.csv file and the fill this columns with the code of the
      corresponding account.

- res.bank:

    - xml_id of the format 'rb_mycompany_bankname'
    - csv file preload with some bankks that can be used an thouse who not can
      be deleted.

- res.company:

    - overwrithe the 'base.main_company' record updating the next columns:
        - 'name': Your company name.
        - 'rml_header': Your company name printed in the rml report headers.
        - 'wh_src_collected_account_id': The code of the account defined for
          the src withholding for...
        - 'wh_src_paid_account_id': The code of the account defined for
          the src withholding for...

.. TODO: complete account account files.

- res.currency:

    - This csv file have generic data preloaded for venezuelan company with the
      VEF like principal currency.

- res.currency.rate:

    - This csv file have generic data preloaded for venezuelan company with the
      VEF like principal currency and the USD like a second currency.

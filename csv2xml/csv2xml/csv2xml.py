#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import libxml2
import csv
import lxml.etree as etree
import pdb
import unidecode

def _get_image( name):
    fil = open(name, 'rb')
    data = fil.read()
    fil.close()
    binary = data.encode('base64')
    return binary 

def initializate_xml_out():
    out_doc = libxml2.parseDoc("<openerp/>") 
    out_root = out_doc.getRootElement()
    out_data = libxml2.newNode('data')
    out_data.setProp('noupdate','1')
    out_root.addChild(out_data)
    return out_doc, out_data

def set_property(type_field, value, out_field, folder = None):
    band = True    
    if  type_field == 'ref':
        out_field.setProp(type_field, value)
    elif type_field == 'eval':
        out_field.setProp(type_field, "time.strftime('%s')" % value)
    elif type_field ==  'evalc':
        out_field.setProp('eval', value)
    elif type_field == 'search':
        out_field.setProp(type_field, "[('code', '=', '%s')]" % value)
    elif type_field == 'bin':
        und = re.compile('\n')
        binario = und.sub('', _get_image(folder +'/'+value ) )
        out_field.setContent( binario )
    else:
        band = False
    return band

def genrate_xml_tree(csv_files, out_data, folder):
    for csv_name in csv_files: 
        print ' generating the xml of %s file' % (csv_name,)
        lines = csv.DictReader(open(folder + '/' + csv_name))
        line = lines.next()
        line.pop('model')
        line.pop('id')
        fields_type = line
        field_names = fields_type.keys()

        for line in lines:
            out_record = libxml2.newNode('record')
            out_record.setProp('id', line.pop('id'))
            out_record.setProp('model', line.pop('model'))
            out_data.addChild(out_record)
            for field_name in field_names:
                if line[field_name]:
                    out_field = libxml2.newNode('field')
                    out_field.setProp('name', field_name)

                    type_field = fields_type[field_name]
                    if not set_property( type_field, line[field_name], out_field, folder):
                        out_field.setContent(line[field_name])
                    out_record.addChild(out_field)

def get_bank_data():
    """
    Read the account account cvs and extract a list of tuples
    [(xml_acc_id, acc_name)].
    """
    csv_name = 'account_account/account_account.csv'
    lines = csv.DictReader(open(csv_name))
    return [(line['id'], line['name'])
              for line in lines
              if line['type'] == 'liquidity']

def journal_parser(out_data):
    """
    This method generate the account journals xml records taking in base the
    account account records in the account account csv of type liquidity.
    @param acc_data_list: list of account data information.
    """
    # TODO:
    # - change the jorunal code to upper case everytime (this is helps for
    # thouse personal accounts (no numbers).
    # - try to use more account numbers in the journal code.
    # - manage the uniqueness of the journal code before write the xml.
    my_model = 'account.journal'
    bank_data = get_bank_data()
    pattern = re.compile(r'(cta|cuenta|cc|cte|ca|no)(\.|-)*(\s)*', re.DOTALL)
    pattern2 = re.compile(r'(\s|\.)', re.DOTALL)
    value = {
       'company_id': 'base.main_company',
       'type': 'bank',
       }
    field_type = {
        'name': 'str',
        'code': 'str',
        'type': 'str',
        'default_credit_account_id': 'ref',
        'default_debit_account_id': 'ref',
        'company_id': 'ref',
    }

    for line in bank_data:
        value['name'] = unicode(line[-1], 'utf-8')
        value['name'] = unidecode.unidecode(value['name'])
        value['default_credit_account_id'] = line[0]
        value['default_debit_account_id'] = line[0]
        xml_id = pattern.sub('', value['name'].lower())
        xml_id = pattern2.sub('_', xml_id)
        out_record = libxml2.newNode('record')
        out_record.setProp('id', 'aj_mycompany_%s' % (xml_id,))
        out_record.setProp('model', my_model)

        value['code'] = 'BJ' + xml_id.split('_')[-1][-3:]

        for aj_field in value.keys():
            out_field = libxml2.newNode('field')
            out_field.setProp('name', aj_field)
            if field_type[aj_field] == 'str':
                out_field.setContent(value[aj_field])
            elif field_type[aj_field] == 'ref':
                out_field.setProp('ref', value[aj_field])
            else:
                assert False, ('Error. This field type is not defined yet.'
                    'define Field %s' % (aj_field,))
            out_record.addChild(out_field)

        out_data.addChild(out_record)
    return True 

def aditional_parser(model_name, out_data):
    """
    Check if there is a parser that need to be add for some models
    """
    model_name == 'account_journal' and journal_parser(out_data)
    return True

def write_xml_doc(out_doc, xml_name):
    f = open(xml_name, 'w')
    out_doc.saveTo(f)
    out_doc.freeDoc()
    f.close()

    print '*** generating the xml of %s file' % (xml_name,)
    x = etree.parse(xml_name)
    k = etree.tostring(x, pretty_print = True, xml_declaration=True, encoding='UTF-8')
    f = open(xml_name, 'w')
    f.write(k)
    f.close()


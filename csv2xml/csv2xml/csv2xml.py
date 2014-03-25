#!/usr/bin/python
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import argparse
import argcomplete
import re
import os
import libxml2
import csv
import lxml.etree as etree
import pdb
import unidecode
from urlparse import urljoin

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
        print ' ---- generating the xml of %s file' % (csv_name,)
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

def get_bank_data(folder):
    """
    Read the account account csv and extract a list of tuples
    [(xml_acc_id, acc_name)].
    """
    csv_name = 'account_account.csv'
    folder = folder.replace('account_journal', 'account_account')
    lines = csv.DictReader(open('/'.join([folder, csv_name])))
    return [(line['id'], line['name'])
              for line in lines
              if line['type'] == 'liquidity']

def journal_parser(out_data, folder, args):
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
    bank_data = get_bank_data(folder)
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
        out_record.setProp('id', 'aj_%s_%s' % (args['company_name'], xml_id,))
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

def aditional_parser(model_name, out_data, folder, args):
    """
    Check if there is a parser that need to be add for some models
    """
    model_name == 'account_journal' and journal_parser(out_data, folder, args)
    return True

def write_xml_doc(out_doc, xml_name):
    f = open(xml_name, 'w')
    out_doc.saveTo(f)
    out_doc.freeDoc()
    f.close()

    x = etree.parse(xml_name)
    k = etree.tostring(x, pretty_print = True, xml_declaration=True, encoding='UTF-8')
    f = open(xml_name, 'w')
    f.write(k)
    f.close()
    print ' **** write over %s' % (xml_name,)

def create_csv_template(args):
    """
    Create a new csv directory with the templates of the csv files.
    @return: True
    """
    print '... Creating the csv template'
    this_dir, this_filename = os.path.split(__file__)
    os.system('cp %s/data/csv %s -r' % (this_dir, args['csv_dir_full_path']))
    
    file_list = []
    for (dirpath, dirnames, filenames) in os.walk(args['csv_dir_full_path']):
        for filename in filenames:
            if filename.lower().endswith('.csv'):
                file_list.append( '/'.join([dirpath, filename]))
    for file_elem  in file_list:
        os.system('sed -i \'s/mycompany/%s/g\' %s' % (args['company_name'],
            file_elem))
    return True

def update_xml(args):
 
    print '... Updating the data xml files.'
    f = open( '/'.join([args['csv_dir_full_path'], '__config__.py']), 'r')
    d = eval(f.read())
    f.close()
    print ' ---- The script is running, please wait...'
    for i in d.iteritems():
        folder = '/'.join([args['csv_dir_full_path'], i[0]])
        out_doc, out_data = initializate_xml_out()
        csv_files = i[1]
        genrate_xml_tree(csv_files, out_data, folder)
        aditional_parser(i[0], out_data, folder, args)
        write_xml_doc(out_doc, '%s/data/%s.xml' % (args['module_full_path'], i[0]) )
    print ' --- The script successfully finish.' 

def argument_parser():
    """
    This function create the help command line and manage and filter the
    parameters of this program (default values, choices values)
    @return the dictionary of type {argument: value} generated by the user
    input.
    """
    parser = argparse.ArgumentParser(
        prog='csv2xml',
        description='Update data xml from a module via csv files.',
        epilog="""
Openerp Developer Comunity Tool
Development by Vauxoo Team (lp:~vauxoo)
Coded by Katherine Zaoral <kathy@vauxoo.com>.
Source code at lp:~vauxoo-private/vauxoo-private/data_init-dev-kty.""",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    # create subparsers
    subparsers = parser.add_subparsers(
        dest='action',
        help='subcommands help')
    update_parser = subparsers.add_parser(
        'update', help='Update a module data xml files.')
    create_parser = subparsers.add_parser(
        'create', help='Create csv files templates.')

    update_parser.add_argument(
        '-m', '--module-name',
        metavar='MODULE_NAME',
        required=True,
        type=str,
        help='name of the module to be update.')
    update_parser.add_argument(
        '-csv','--csv-dir',
        metavar='CSV_DIR', 
        required=True,
        type=str,
        help='the folder where your csv and config files are.')
    update_parser.add_argument(
        '-co', '--company-name',
        metavar='COMPANY_NAME',
        required=True,
        type=str,
        help='name of the company, this will be to name some default journals.')

    create_parser.add_argument(
        '-csv','--csv-dir',
        metavar='CSV_DIR', 
        required=True,
        type=str,
        help='where to put the csv templates folder.')
    create_parser.add_argument(
        '-co', '--company-name',
        metavar='COMPANY_NAME',
        required=True,
        type=str,
        help=('The name of your company. This name will be use to customize'
            ' xml ids data with your company name.'))

    argcomplete.autocomplete(parser)
    return parser.parse_args().__dict__

def fix_args(args):
    if args['action'] == 'update':
        args['module_name'] = args['module_name'].replace('/', '')
    return args

def extra_args(args):
    """
    Add extra args for manipalition of full path of the directories. 
    """
    full_path = os.getcwd() + '/'
    if args['action'] == 'update':
        args['module_full_path'] = urljoin(full_path, args['module_name'])
    args['csv_dir_full_path'] = urljoin(full_path, args['csv_dir'])
    return args

def confirm_run(args):
    """
    Manual confirmation before runing the script. Very usefull.
    """
    print'\n... Configuration of Parameters Set'
    for (parameter, value) in args.iteritems():
        print '%s = %s' % (parameter, value)

    confirm_flag = False
    while confirm_flag not in ['y', 'n']:
        confirm_flag = raw_input(
            'Confirm the run with the above parameters? [y/n]: ')
        if confirm_flag == 'y':
            print 'The script parameters were confirmed by the user'
        elif confirm_flag == 'n':
            print 'The user cancel the operation'
            exit()
        else:
            print 'The entry is not valid, please enter y or n.'
    return True

def run(args):
    extra_args(args)
    if args ['action'] == 'create':
        create_csv_template(args)
    elif args['action'] == 'update':
        update_xml(args)
    return True

def main():
    args = argument_parser()
    fix_args(args)
    confirm_run(args)
    run(args)
    return True

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
import unidecode
import json


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
    elif type_field == 'date':
        out_field.setProp('eval', "time.strftime('%s')" % value)
    elif type_field ==  'evalc':
        out_field.setProp('eval', value)
    elif type_field == 'search':
        out_field.setProp(type_field, "[('code', '=', '%s')]" % value)
    elif type_field == 'searchname':
        out_field.setProp('search', "[('name', '=', '%s')]" % value)
    elif 'search_' in type_field:
        field_name = type_field.split('_', 1)[1]
        out_field.setProp('search', str([(field_name, '=', value)]))
    elif type_field == 'bin':
        und = re.compile('\n')
        binario = und.sub('', _get_image(folder +'/'+value ) )
        out_field.setContent( binario )
    elif type_field == 'm2m':
        ref_list = ''
        for i in value.split(';'):
            if ref_list is '':
                ref_list = "[ref('{id_xml}')".format(id_xml=i)
            else:
                ref_list = "{lista},ref('{id_xml}')".format(lista=ref_list,id_xml=i)
        ref_list = "[(6, 0, {lista}])]".format(lista=ref_list)
        out_field.setProp('eval', ref_list)
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
    Read the account account csv and extract a list of dictionariers with the
    keys ['aa_xml_id', 'aa_name'].
    """
    csv_name = 'account_account.csv'
    folder = folder.replace('account_journal', 'account_account')
    lines = csv.DictReader(open('/'.join([folder, csv_name])))
    return [{'aa_xml_id': line['id'], 'aa_name': line['name'],
             'acc_currency': line['currency_id']}
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
    field_type = {
        'name': 'str',
        'code': 'str',
        'type': 'str',
        'default_credit_account_id': 'ref',
        'default_debit_account_id': 'ref',
        'company_id': 'ref',
        'currency': 'ref',
    }

    for (index, line) in enumerate(bank_data, 1):
        value = dict(
            company_id='base.main_company',
            type='bank')
        value['name'] = unicode(line['aa_name'], 'utf-8')
        value['name'] = unidecode.unidecode(value['name'])
        value['default_credit_account_id'] = line['aa_xml_id']
        value['default_debit_account_id'] = line['aa_xml_id']
        xml_id = pattern.sub('', value['name'].lower())
        xml_id = pattern2.sub('_', xml_id)
        out_record = libxml2.newNode('record')
        out_record.setProp('id', 'aj_{}_{}'.format(
            args['company_name'], line['aa_xml_id']))
        out_record.setProp('model', my_model)
        value['code'] = 'BJ{0:03d}'.format(index)
        if line['acc_currency']:
            value['currency'] = line['acc_currency']

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
    print ' .. Creating the csv template'
    os.system('cp {path}/data/csv_template {new_folder} -r'.format(
        path=get_main_script_dir(), new_folder=args['csv_dir']))

    file_list = []
    for (dirpath, dirnames, filenames) in os.walk(args['csv_dir']):
        for filename in filenames:
            if filename.lower().endswith('.csv'):
                file_list.append( '/'.join([dirpath, filename]))
    for file_elem  in file_list:
        os.system('sed -i \'s/mycompany/%s/g\' %s' % (args['company_name'],
            file_elem))
    return True

def update_xml(args):
    """
    Given the module path it add the xml data correspond to the given csv
    files folder. Also update the module descriptor file, the depends and data
    keys.
    """
    data = get_data_from_config_file(args)
    print '... Updating the data xml files.'

    print ' ---- The script is running, please wait...'
    for item in data.get('xml_files', []):
        folder = os.path.join(args['csv_dir'], item.get('name'))
        out_doc, out_data = initializate_xml_out()
        csv_files = item.get('csv')
        genrate_xml_tree(csv_files, out_data, folder)
        aditional_parser(item.get('name'), out_data, folder, args)
        write_xml_doc(out_doc, '{}/{}.xml'.format(
            args['new_path'],
            item.get('name')))

    print '... Update the module descriptor with the new data'
    update_file = '__openerp__.py'
    hard_update_file(args, update_file, 'data')
    hard_update_file(args, update_file, 'depends')

    print ' --- The script successfully finish.'
    return True

def hard_update_file(args, update_file, openerp_key):
    """
    Read a file, get the string version of it, and then replace once
    portion of the string with another one and overwrite the file with this
    new change.
    @param args: this run arguments.
    @param update_file: the name of the file to change.
    @param openerp_key: the key name that will be update in the module
                        descriptor (in __openerp__.py).
    @return True
    """
    path = args['module_name']
    file_path = os.path.join(path, update_file)
    with open(file_path, 'r') as f:
        file_str = f.read()

    pattern = "(?P<base>[\"']{}[\"']\s*:\s*\[)(?P<cnt>(\n*[^\]]*)*)(?P<end>\]\s*,)".format(openerp_key)
    rp = re.compile(pattern)
    cr_data = rp.search(file_str).group('cnt')
    result = rp.sub(
        '\g<base>{data}\g<end>'.format(
            data=get_key_value(args, openerp_key, cr_data)), file_str)

    with open(file_path, 'w') as f:
        f.write(result)
    return True

def get_list_from_str(str_values):
    """
    Transforms the string with the values of the an openerp key (descriptor of
    a Odoo module) and return a list of strings of the elements.
    @param str_values: string with the content of the openerp key (string).
    @return a list of strings with the content data (list).
    """
    return eval('[{}]'.format(str_values))

def get_str_from_list(list_data):
    """
    Transforms a list into a string.
    @param list_data: list of string to convert.
    @return string with a form like a list
    """
    str_data = str()
    for item in list_data:
        str_data += '\n        \'%s\',' % (item)
    str_data = str_data[:-1]
    return str_data

def get_main_script_dir():
    """
    Get the path of the script that is runing.
    @return the full path of the current script (string).
    """
    return __name__ == '__main__' and os.getcwd() \
        or os.path.split(__file__)[0]

def get_key_value(args, openerp_key, cr_data):
    """
    Read the current data for a key in the user module descriptor, read the
    neccesaries keys to be add and then add the ones who are missing.
    @param openerp_key: the key name that will be update in the module
                        descriptor (in __openerp__.py).
    @param cr_data: string of the values inside the openerp key given.
    @return an string that will be replace the value of openerp_key given.
    """
    cr_data = get_list_from_str(cr_data)
    if openerp_key in ['data']:
        required_data = get_xml_files_from_config(args, openerp_key)
    elif openerp_key in ['depends']:
        required_data = list(set(get_depens_from_config(args) +
        get_depends_form_xml_files(args)))

    for item in required_data:
        if item in cr_data:
            cr_data.remove(item)

    new_data = required_data + cr_data
    return get_str_from_list(new_data)

def get_data_from_config_file(args):
    """
    @ return a dictionary with the data given for the user in the config
    file.
    """
    data_file = os.path.join(args['csv_dir'], '__config__.py')
    with open(data_file, 'r') as f:
        data = eval(f.read())
    return data

def get_depens_from_config(args):
    """
    @return a list of strings with de modules that will be dependecies of the
    updated module. This data is extract for the config file given by the
    user.
    """
    data = get_data_from_config_file(args)
    depends_list = list()
    for item in data.get('xml_files'):
        depends_list.extend(item.get('depends'))
    return list(set(depends_list))

def get_depends_form_xml_files(args):
    """
    @return a list of strings with the new required values of the depends
    openerp key.
    """
    data = get_data_from_config_file(args)
    full_ids = list()
    for item in data.get('xml_files'):
        folder = os.path.join(args['csv_dir'], item.get('name'))
        csv_files = item.get('csv')
        for csv_name in csv_files:
            lines = csv.DictReader(open(folder + '/' + csv_name))
            line = lines.next()
            line.pop('model')
            line.pop('id')
            fields_type = line
            field_names = fields_type.keys()

            for line in lines:
                full_ids.append(line.pop('id'))
    depends_list = list(set([
        item.split('.')[0]
        for item in full_ids
        if len(item.split('.')) == 2]))
    return depends_list

def get_xml_files_from_config(args, openerp_key):
    """
    @return a list of strings with the new required values of the openerp key
    """
    data = get_data_from_config_file(args)
    prefix = openerp_key == 'data' and 'data/' or ''
    data = data.get('xml_files', [])
    return [
        '{prefix}{filename}.xml'.format(
            prefix=prefix, filename=xml_data.get('name'))
        for xml_data in data]

def get_str_data(openerp_key):
    """
    @return a list of strings with the new required values of the openerp key
    in the Odoo descriptor file.
    """
    data_file = '{path}/data/openerp_key.json'.format(
        path=get_main_script_dir())
    with open(data_file, 'r') as f:
        data = json.load(f)
    return data[openerp_key]

def argument_parser(args_list=None):
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
Odoo Developer Comunity Tool Development by Vauxoo Team (https://www.github.com/Vauxoo)
Coded by:
    - Katherine Zaoral <kathy@vauxoo.com>,
    - Yanina Aular <yanina@vauxoo.com>,
    - Saul Gonzanlez <saul@vauxoo.com>.
Source code at git@github.com:Vauxoo/csv2xml.git
""",
        formatter_class=argparse.RawDescriptionHelpFormatter)

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
        type=fix_module_name,
        help='name of the module to be update.')
    update_parser.add_argument(
        '-csv','--csv-dir',
        metavar='CSV_DIR',
        required=True,
        type=dir_full_path,
        help='the folder where your csv and config files are.')
    update_parser.add_argument(
        '-n', '--new-path',
        metavar='PATH',
        required=True,
        type=dir_full_path,
        help='the folder where xml file will be created.')
    update_parser.add_argument(
        '-co', '--company-name',
        metavar='COMPANY_NAME',
        required=True,
        type=str,
        help='name of the company, this will be to name some default journals.')

    create_parser.add_argument(
        '-csv','--csv-dir',
        metavar='CSV_DIR',
        type=dir_full_path,
        default=os.getcwd(),
        help=('Where to put the csv templates folder. If not specificated'
              ' then use the current path as base.'))
    create_parser.add_argument(
        '-co', '--company-name',
        metavar='COMPANY_NAME',
        required=True,
        type=str,
        help=('The name of your company. This name will be use to customize'
            ' xml ids data with your company name.'))

    argcomplete.autocomplete(parser)
    return parser.parse_args(args=args_list).__dict__

def fix_module_name(path):
    """
    Return the module full path, but before it checks that is a openerp module
    with a defined data folder like the standard.
        - Get the full path of the module and check if exsits.
        - Check that the module have a data folder.
    @return the full path of the module.
    """
    print ' ---- entre aqui'
    path = dir_full_path(path)
    openerp_file = os.path.join(path, '__openerp__.py')
    manifest_file = os.path.join(path, '__manifest__.py')
    if os.path.exists(openerp_file) and os.path.isfile(openerp_file):
        pass
    if os.path.exists(manifest_file) and os.path.isfile(manifest_file):
        pass
    else:
        msg = ('The given module is not a openerp module. Missing'
                ' __openerp__.py or __manifest__.py file.')
        raise argparse.ArgumentTypeError(msg)
    return path

def dir_full_path(path, msg=None):
    """
    Calculate the abosulte path for a given path. It get the absolute path
    taking into account the current path were the tool is running.
    @param path: a directory path
    @return: the absolute path of a directory.
    """
    my_path = os.path.abspath(path)
    if not os.path.isdir(my_path):
        msg = msg or 'The directory given did not exist %s' % my_path
        raise argparse.ArgumentTypeError(msg)
    return my_path

def dir_exists(path):
    """
    Check is a Directory exist-
    @return True if exist, False is not exist.
    """
    return ((os.path.exists(path) and not os.path.isfile(path))
           and True or False)


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
    if args ['action'] == 'create':
        create_csv_template(args)
    elif args['action'] == 'update':
        update_xml(args)
    return True

def main():
    args = argument_parser()
    confirm_run(args)
    run(args)
    return True

if __name__ == "__main__":
    import doctest
    doctest.testmod()

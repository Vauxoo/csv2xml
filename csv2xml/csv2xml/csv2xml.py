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

    >>> args = {'csv_dir': '/home/kathy/bzr_projects/temp/new_templates',
    ...         'company_name': 'kmt'} 
    >>> import os
    >>> import shutil
    >>> if os.path.exists(args['csv_dir']):
    ...     shutil.rmtree(args['csv_dir'])
    >>> create_csv_template(args)
     .. Creating the csv template
    True

    >>> if os.path.exists(args['csv_dir']):
    ...     shutil.rmtree(args['csv_dir'])

    """
    print ' .. Creating the csv template'
    this_dir = __name__ == '__main__' and os.getcwd() \
        or os.path.split(__file__)[0]
    os.system('cp %s/data/csv_template %s -r' % (this_dir, args['csv_dir']))
    
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
 
    print '... Updating the data xml files.'
    f = open( '/'.join([args['csv_dir'], '__config__.py']), 'r')
    d = eval(f.read())
    f.close()
    print ' ---- The script is running, please wait...'
    for i in d.iteritems():
        folder = '/'.join([args['csv_dir'], i[0]])
        out_doc, out_data = initializate_xml_out()
        csv_files = i[1]
        genrate_xml_tree(csv_files, out_data, folder)
        aditional_parser(i[0], out_data, folder, args)
        write_xml_doc(out_doc, '%s/data/%s.xml' % (args['module_name'], i[0]) )

    print '... Update the module descriptor with the new data'
    update_file = '__openerp__.py'
    hard_update_file(args, update_file, 'data')
    hard_update_file(args, update_file, 'depends')

    print ' --- The script successfully finish.' 

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
    a openerp module) and return a list of strings of the elements.
    @param str_values: string with the content of the openerp key (string).
    @return a list of strings with the content data (list).
    """
    for item in ['"', '\'', ',']:
        str_values = str_values.replace(item, '')

    # delete comments inside the keys 
    rp = re.compile('(?P<data>.*)(?P<comment>#.*\n)')
    str_values = rp.sub('', str_values)
    return str_values.split()

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
    required_data = get_str_data(openerp_key)

    for item in required_data:
        if item in cr_data:
            cr_data.remove(item)

    new_data = required_data + cr_data
    return get_str_from_list(new_data)

def get_str_data(openerp_key):
    """
    @return a list of strings with the new required values of the openerp key
    in the openerp descriptor file. 
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
Openerp Developer Comunity Tool Development by Vauxoo Team (lp:~vauxoo)
Coded by:
    - Katherine Zaoral <kathy@vauxoo.com>,
    - Yanina Aular <yanina@vauxoo.com>,
    - Saul Gonzanlez <saul@vauxoo.com>.
Source code at lp:vauxoo-private/csv2xml
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
    if os.path.exists(openerp_file) and os.path.isfile(openerp_file):
        pass
    else:
        msg = ('The given module is not a openerp module. Missing'
                ' __openerp__.py file.')
        raise argparse.ArgumentTypeError(msg)
    dir_full_path(
        os.path.join(path, 'data'),
        ('The openerp module needs to have a data folder were to put the new'
         ' xml data.'))
    return path

def dir_full_path(path, msg=None):
    """
    Calculate the abosulte path for a given path. It get the absolute path
    taking into account the current path were the tool is running.
    @param path: a directory path
    @return: the absolute path of a directory.
    
    Absolute exist path
    >>> import os
    >>> absolute = '/home/kathy/bzr_projects/temp'
    >>> #current = os.getcwd()
    >>> #absolute = os.path.abspath('path-test/absolute')
    >>> #os.makedirs(absolute)
    >>> error = not os.path.exists(absolute) and 'The directory not exists' or False
    >>> not error and dir_full_path(absolute) or error
    '/home/kathy/bzr_projects/temp'

    #Absolute non-exist path
    >>> absolute = '/home/kathy/bzr_projects/temp/k'
    >>> dir_full_path(absolute)
    Traceback (most recent call last):
    ArgumentTypeError: The directory given did not exist /home/kathy/bzr_projects/temp/k

    #Relative foward path 
    >>> relative_foward_path = 'data/csv_template'
    >>> dir_full_path(relative_foward_path)
    '/home/kathy/bzr_projects/vauxoo_private/csv2xml-rev1-kty/csv2xml/csv2xml/data/csv_template'

    #Non-exist Relative foward path 
    >>> relative_foward_path = 'kdata/csv'
    >>> dir_full_path(relative_foward_path)
    Traceback (most recent call last):
    ArgumentTypeError: The directory given did not exist /home/kathy/bzr_projects/vauxoo_private/csv2xml-rev1-kty/csv2xml/csv2xml/kdata/csv

    #Relative foward path
    >>> relative_backward_path = '../../../../temp'
    >>> dir_full_path(relative_backward_path)
    '/home/kathy/bzr_projects/temp'

    #Non-exist Relative foward path
    >>> relative_backward_path = '../../../../tempk'
    >>> dir_full_path(relative_backward_path)
    Traceback (most recent call last):
    ArgumentTypeError: The directory given did not exist /home/kathy/bzr_projects/tempk

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

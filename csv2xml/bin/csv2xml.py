#!/usr/bin/python
import csv2xml
import argparse
import argcomplete


def main():
    f = open('../src/__config__.py','r')
    d = eval(f.read())
    f.close()
    print ' --- The script is running, please wait...'
    for i in d.iteritems():
        out_doc, out_data = initializate_xml_out()
        csv_files = i[1]
        genrate_xml_tree(csv_files, out_data, i[0])
        aditional_parser(i[0], out_data)
        write_xml_doc(out_doc, '../mycompany_data/data/%s.xml' % i[0] )
    print ' --- The script successfully finish.' 

if __name__ == '__main__':
    main()

README
======

Install
-------

Open your command line promt and go to the downloaded package folder to run
this command::

    # sudo python setup.py install

Now check that the package was correctly installed by running this command that
will display the script options::

    $ csv2xml --help
    usage: csv2xml [-h] {update,create} ...

    Update data xml from a module via csv files.

    positional arguments:
      {update,create}  subcommands help
        update         Update a module data xml files.
        create         Create csv files templates.

    optional arguments:
      -h, --help       show this help message and exit

    Openerp Developer Comunity Tool Development by Vauxoo Team (lp:~vauxoo)
    Coded by:
        - Katherine Zaoral <kathy@vauxoo.com>,
        - Yanina Aular <yanina@vauxoo.com>,
        - Saul Gonzanlez <saul@vauxoo.com>.
    Source code at lp:vauxoo-private/csv2xml


Configure
---------

No configuration is needed.

Actions
-------

To run the installed script just type the command `csv2xml` and it will show
you what are avaible actions and the required parameters. For more detail
information you can write in your console::

    $ csv2xml --help
    $ csv2xml <action> --help

To create a new csv template folder you need to run the next command::

    $ csv2xml create -co <company-acronym>

To update a openerp module xml data just need to indicate the module path and
the csv path were youre csv data is::

    $ csv2xml update -m <module-folder-path> -csv <csv-folder-path> \
    -co <company-acronym>

Uninstall
---------

In the install folder there is a uninstall file. This is an executable file.
Just run in your console::

    $ sudo ./uninstall

If the file have not excecution permissions then just change the file
permissions (chmod) and execute the above command.

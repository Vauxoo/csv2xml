===============================
csv2xml
===============================

.. image:: https://img.shields.io/travis/vauxoo/csv2xml.svg
        :target: https://travis-ci.org/vauxoo/csv2xml

This module python is a tool to Odoo developers that permit to generate data
xml files from csv files. This is a practical way to work with a client. The
client give the company data in csv files and then the developer run this tool
to generate the corresponding xml files. This tool is a time saver and also
reduce in a big way the human errors in the data transition.

Download
--------

This python module is hosted on github repository branch. Can be
downloaded by running this command::
    
    git clone git@github.com:Vauxoo/csv2xml.git

Dependencies
------------

This module python use some imports of python modules, some of then really
commom and another need to be found, downloaded and then installed via apt-get
install or pip, if not, then you need to search in the web for the official
page of the module, download the module and install it with the installation
instruction given for the module autor. The list of python modules until the
last versions is this: ``os``, ``argparse``, ``re``, ``libxml2``,
``argcomplete``, ``csv``, ``lxml``, ``shutil``, ``doctest`` and ``unidecode``.

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

    Odoo Developer Comunity Tool Development by Vauxoo Team (https://www.github.com/Vauxoo)
    Coded by:
        - Katherine Zaoral <kathy@vauxoo.com>,
        - Yanina Aular <yanina@vauxoo.com>,
        - Saul Gonzanlez <saul@vauxoo.com>.
    Source code at git@github.com:Vauxoo/csv2xml.git

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

To update a Odoo module xml data just need to indicate the module path and
the csv path were youre csv data is::

    $ csv2xml update -m <module-folder-path> -csv <csv-folder-path> \
    -co <company-acronym>

Documentation
-------------

The detail documentation about this tool can be found inside the vauxoo
documentation branch in the section CSV Tools.

Uninstall
---------

In the install folder there is a uninstall file. This is an executable file.
Just run in your console::

    $ sudo ./uninstall

If the file have not excecution permissions then just change the file
permissions (chmod) and execute the above command.

Credits
---------

This package was created by Vauxoo_

.. _Vauxoo: https://www.vauxoo.com/

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

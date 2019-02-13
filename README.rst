PyCodegen  |Build Status| |PyPi Version| |License|
==================================================

Pycodegen is a tool to help you generate code in your project using
powerful `Jinja2 <http://jinja.pocoo.org/>`__ templates.

To get started:

.. code:: bash

    # Install
    python3 -m pip install pycodegen
  
    # Run cli  
    pycodegen

    # Run cli using module
    python3 -m pycodegen.cli

========  ================================================
Frontend  Description
========  ================================================
cpp       Parses C/C++ using libclang
json      Passes a JSON file directly to the driver
========  ================================================


How it works
------------

#. The requested frontend reads the input file and generates an intermediate representation.
#. The representation is passed to the driver
#. Driver does any processing required of the representation.
#. Driver selects the output filename and template to be used and render the output file.


Example usage
-------------

.. code:: bash

    # Generate the simple JSON example
    pycodegen json examples/simple/input_file.json --driver examples/simple/driver.py --debug

    # Get intermediate representation of a C++ file (to aid in driver development)
    pycodegen cpp <name-of-file.cpp> --dump-json


.. |Build Status| image:: https://img.shields.io/circleci/project/github/blejdfist/pycodegen/master.svg?style=flat
   :target: https://circleci.com/gh/blejdfist/pycodegen

.. |PyPi Version| image:: https://img.shields.io/pypi/v/pycodegen.svg?style=flat
   :target: https://pypi.org/project/pycodegen/
   
.. |License| image:: https://img.shields.io/github/license/blejdfist/pycodegen.svg?style=flat
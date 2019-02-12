PyCodegen  |Build Status|
=========================

Pycodegen is a tool to help you generate code in your project using
powerful `Jinja2 <http://jinja.pocoo.org/>`__ templates.

To get started:

.. code:: bash

    python3 setup.py install
  
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

  1. The requested frontend reads the input file and generates an intermediate
     representation.
  2. The representation is passed to the driver
  3. Driver does any processing required of the representation.
  4. Driver selects the output filename and template to be used and
     render the output file.


Example usage
-------------

.. code:: bash

    # Generate the simple JSON example
    pycodegen json examples/simple/input_file.json --driver examples/simple/driver.py --debug

    # Get intermediate representation of a C++ file (to aid in driver development)
    pycodegen cpp <name-of-file.cpp> --dump-json


.. |Build Status| image:: https://circleci.com/gh/blejdfist/pycodegen.svg?style=svg
   :target: https://circleci.com/gh/blejdfist/pycodegen


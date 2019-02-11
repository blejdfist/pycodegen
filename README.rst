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
json      Passes a json file directoy to the driver
========  ================================================


How it works
------------

Pycodegen works by passing a file through a frontend for parsing. This can example be a C++ file passed through the cpp frontend to produce a simplified representation of the file.

The result from the frontend is then passed to a driver that optionally process the representation for before it is rendered through a template that the driver decides.


Example usage
-------------

.. code:: bash

    # Generate the simple JSON example
    pycodegen json examples/simple/input_file.json --driver examples/simple/driver.py --debug
    
    # Get intermediate representation of a C++ file (to aid in driver development)
    pycodegen cpp <name-of-file.cpp> --dump-json


.. |Build Status| image:: https://circleci.com/gh/blejdfist/pycodegen.svg?style=svg
   :target: https://circleci.com/gh/blejdfist/pycodegen


import logging
import argparse

from pycodegen.core import run_driver
from pycodegen.frontend import register_frontends

log = logging.getLogger(__name__)


def do_run_generator(frontend, input_file, options):
    """
    Run the selected frontend and pass the result to the driver

    :param frontend: Frontend module to execute
    :param input_file: Input file to pass to frontend
    :param options: Options parsed from commandline
    """
    result = frontend.run(input_file, vars(options))

    try:
        run_driver(input_data=result,
                   driver_filename=options.driver_script,
                   input_filename=input_file,
                   output_dir=options.output_dir)
    except RuntimeError as e:
        log.error("Error while running driver: %s", str(e))


def main():
    parser = argparse.ArgumentParser()
    parser.set_defaults(frontend=None, debug=False)
    subparsers = parser.add_subparsers()

    register_frontends(subparsers)

    options = parser.parse_args()

    if options.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig()

    if options.frontend:
        do_run_generator(options.frontend, options.input_file, options)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()

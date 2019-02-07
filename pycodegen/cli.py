import logging
import argparse
import json

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

    log.debug("Executing frontend")
    result = frontend.run(input_file, vars(options))

    if options.dump_json:
        print(json.dumps(result, indent=2))

    if options.driver:
        try:
            run_driver(input_data=result,
                       driver_filename=options.driver,
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
        if not (options.driver or options.dump_json):
            parser.error("No action given. You must specify '--driver' or '--dump-json'")

        do_run_generator(options.frontend, options.input_file, options)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()

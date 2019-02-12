import logging
import argparse
import json
import os
import sys

from pycodegen import get_frontend_by_name, load_driver
from pycodegen.frontend import register_frontends
from pycodegen.driver_base import DriverEnvironment

log = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser()
    parser.set_defaults(frontend_name=None, debug=False)
    subparsers = parser.add_subparsers()

    register_frontends(subparsers)

    options = parser.parse_args()

    if options.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig()

    if options.frontend_name:
        if not (options.driver or options.dump_json):
            parser.error("No action given. You must specify '--driver' or '--dump-json'")

        # Load frontend
        frontend_module = get_frontend_by_name(options.frontend_name)
        if frontend_module is None:
            log.error("Unable to load the frontend '%s'", options.frontend_name)
            sys.exit(1)

        # Run frontend if needed
        if not (options.list_deps or options.list_output):
            frontend_result = frontend_module.run(options.input_file, vars(options))
        else:
            frontend_result = None

        if options.dump_json:
            print(json.dumps(frontend_result, indent=2))

        if options.driver:
            # Instantiate driver
            env = DriverEnvironment(
                working_dir=os.getcwd(),
                driver_dir=os.path.dirname(options.driver),
                output_dir=options.output_dir,
                input_filename=options.input_file)

            # Load driver
            driver_module = load_driver(options.driver)
            driver_instance = driver_module.create(env)

            # Determine action
            if options.list_deps:
                # Print list of dependencies
                print(" ".join([os.path.join(env.driver_dir, dep) for dep in driver_instance.get_dependencies()]))
            elif options.list_output:
                # Print list of generated files
                if options.output_dir:
                    output_files = [os.path.join(env.output_dir, os.path.basename(output_file))
                                    for output_file in driver_instance.get_generated_files()]
                else:
                    output_files = driver_instance.get_generated_files()

                print(";".join(output_files))
            else:
                driver_instance.render(frontend_result)

    else:
        parser.print_help()


if __name__ == '__main__':
    main()

from . import frontend_cpp
from . import frontend_json

ALL_FRONTENDS = {
    "cpp": frontend_cpp,
    "json": frontend_json
}


def register_frontends(subparsers):
    """
    Register all frontends in the commandline parser

    :param subparsers: ArgumentParser subparsers instance
    """
    for name, module in ALL_FRONTENDS.items():
        frontend_parser = subparsers.add_parser(name, help=module.__doc__)

        frontend_parser.add_argument("--debug",
                                     action="store_true",
                                     help="Enable debug logging")

        frontend_parser.add_argument("--dump-json",
                                     action="store_true",
                                     help="Dump intermediate data as JSON instead of passing it to the driver")

        frontend_parser.add_argument("--driver", metavar="DRIVER_SCRIPT", help="Driver Python script")

        frontend_parser.add_argument("--list-deps",
                                     action="store_true",
                                     help="Print a list of dependencies [Requires --driver]")

        frontend_parser.add_argument("--list-output",
                                     action="store_true",
                                     help="Print a list of generated files [Requires --driver]")

        frontend_parser.add_argument("--output-dir",
                                     metavar="DIR",
                                     help="Output directory")

        frontend_parser.add_argument("input_file", metavar="INPUT_FILE", help="Input file to frontend")
        frontend_parser.set_defaults(frontend_name=name)

        module.register_arguments(frontend_parser)

from . import cpp

ALL_FRONTENDS = {
    "cpp": cpp
}


def get_frontend_by_name(name):
    return ALL_FRONTENDS.get(name)


def register_frontends(subparsers):
    """
    Register all frontends in the commandline parser

    :param subparsers: ArgumentParser subparsers instance
    """
    for name, module in ALL_FRONTENDS.items():
        frontend_parser = subparsers.add_parser(name)

        frontend_parser.add_argument("--debug",
                                     default=False,
                                     action="store_true",
                                     help="Enable debug logging")

        frontend_parser.add_argument("--dump-json",
                                     default=False,
                                     action='store_true',
                                     help="Dump intermediate data as JSON instead of passing it to the driver")

        frontend_parser.add_argument("--driver", metavar="DRIVER_SCRIPT", help="Driver Python script")

        frontend_parser.add_argument("--output-dir",
                                     metavar="DIR",
                                     help="Output directory")

        frontend_parser.add_argument("input_file", metavar="INPUT_FILE", help="Input file to frontend")
        frontend_parser.set_defaults(frontend=module)

        module.register_arguments(frontend_parser)

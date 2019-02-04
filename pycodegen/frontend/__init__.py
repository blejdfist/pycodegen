from . import cpp

ALL_FRONTENDS = {
    "cpp": cpp
}


def register_frontends(subparsers):
    """
    Register all frontends in the commandline parser

    :param subparsers: ArgumentParser subparsers instance
    """
    for name, module in ALL_FRONTENDS.items():
        frontend_parser = subparsers.add_parser(name)

        frontend_parser.add_argument("--debug", action="store_true", default=False, help="Enable debug logging")
        frontend_parser.add_argument("--output-dir", metavar="DIR", help="Output directory")

        frontend_parser.add_argument("input_file", metavar="INPUT_FILE", help="Input file to frontend")
        frontend_parser.add_argument("driver_script", metavar="DRIVER_SCRIPT", help="Driver python script")

        frontend_parser.set_defaults(frontend=module)

        module.register_arguments(frontend_parser)
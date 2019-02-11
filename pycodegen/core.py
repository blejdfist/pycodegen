import os
import sys
import logging
from .frontend import ALL_FRONTENDS

log = logging.getLogger(__name__)


def load_driver(driver_filename):
    if not os.path.exists(driver_filename):
        log.error("Driver does not exist")
        return

    if sys.version_info >= (3, 1):
        import importlib.util
        spec = importlib.util.spec_from_file_location(driver_filename, driver_filename)
        driver_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(driver_module)
        return driver_module
    else:
        import imp
        return imp.load_source("module", driver_filename)


def get_frontend_by_name(name):
    return ALL_FRONTENDS.get(name)


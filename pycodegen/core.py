import os
import logging
import importlib.util
from .frontend import ALL_FRONTENDS

_LOGGER = logging.getLogger(__name__)


def load_driver(driver_filename):
    if not os.path.exists(driver_filename):
        _LOGGER.error("Driver does not exist")
        return

    spec = importlib.util.spec_from_file_location(driver_filename, driver_filename)
    driver_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(driver_module)
    return driver_module


def get_frontend_by_name(name):
    return ALL_FRONTENDS.get(name)

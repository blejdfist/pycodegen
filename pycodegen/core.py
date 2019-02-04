import os
import logging
import importlib.util

from .driver_base import DriverEnvironment

log = logging.getLogger(__name__)


def load_driver(driver_filename):
    spec = importlib.util.spec_from_file_location(".", driver_filename)
    driver_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(driver_module)

    return driver_module


def run_driver(input_data, driver_filename, input_filename=None, output_dir=None):
    """
    Load and run a driver

    :param input_data: Parse result from the frontend
    :param driver_filename: Driver script to execute
    :param input_filename: The original filename that was being processed
    :param output_dir: Output directory where to store the generated files
    """
    # Load driver script
    driver_module = load_driver(driver_filename)

    if not hasattr(driver_module, "create"):
        raise RuntimeError("Driver does not have a 'create' method")

    driver_directory = os.path.dirname(driver_filename)

    # Instantiate driver
    env = DriverEnvironment(
        working_dir=os.getcwd(),
        driver_dir=driver_directory,
        output_dir=output_dir)

    log.debug("Instantiating driver %s", driver_filename)
    driver = driver_module.create(env)

    log.debug("Running driver")
    driver.render(input_filename, input_data)
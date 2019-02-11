import os
import datetime
import logging

from pycodegen import DriverBase

log = logging.getLogger(__name__)


class SimpleDriver(DriverBase):

    def render(self, input_filename, input_data):
        data = {
            "greeting_data": input_data,
            "time_generated": datetime.datetime.now().isoformat()
        }

        # Output file is relative to the working directory
        # We can use the name of the input file to write the output to the same directory
        output_file = os.path.join(os.path.dirname(input_filename), "output.txt")

        log.info("Rendering")
        self.render_to_file("template.jinja", data, output_file)


def create(environment):
    """Create and return an instance of the driver"""
    return SimpleDriver(environment)

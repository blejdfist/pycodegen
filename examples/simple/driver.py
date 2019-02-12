import os
import datetime
import logging

from pycodegen import DriverBase

TEMPLATE_FILE = "template.jinja"

log = logging.getLogger(__name__)


class SimpleDriver(DriverBase):

    def render(self, input_data):
        data = {
            "greeting_data": input_data,
            "time_generated": datetime.datetime.now().isoformat()
        }

        log.info("Rendering")
        output_file = self._make_output_path("output.txt")
        self.render_to_file(TEMPLATE_FILE, data, output_file)

    def get_dependencies(self):
        return [TEMPLATE_FILE]

    def get_generated_files(self):
        return [self._make_output_path("output.txt")]

    def _make_output_path(self, filename):
        # Output file is relative to the working directory
        # We can use the name of the input file to write the output to the same directory
        # Please not that the path can be overriden with the --output-dir argument
        return os.path.join(os.path.dirname(self.environment.input_filename), filename)


def create(environment):
    """Create and return an instance of the driver"""
    return SimpleDriver(environment)

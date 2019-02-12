import os
import logging

from pycodegen import DriverBase

log = logging.getLogger(__name__)

TEMPLATE_FILE = "enum_reflection.jinja.h"


def make_output_name(input_filename):
    return os.path.splitext(input_filename)[0] + ".gen.h"


class EnumReflectionGenerator(DriverBase):

    def render(self, data: dict):
        # Filter out all the enums in the data
        result = {
            'enums': [item for item in data if item.get('type') == 'enum']
        }

        output_filename = make_output_name(self.environment.input_filename)
        log.debug("Rendering to %s", output_filename)
        self.render_to_file(TEMPLATE_FILE, result, output_filename)

    def get_dependencies(self):
        return [TEMPLATE_FILE]

    def get_generated_files(self):
        return [make_output_name(self.environment.input_filename)]


def create(environment):
    return EnumReflectionGenerator(environment)

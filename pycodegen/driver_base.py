from jinja2 import Environment, FileSystemLoader
from collections import namedtuple
import os
import logging

DriverEnvironment = namedtuple("DriverEnvironment", ["working_dir", "driver_dir", "output_dir"])


class DriverBase:
    """Base class for driver scripts"""

    log = logging.getLogger(__name__)

    def __init__(self, environment):
        self._env = Environment(
            loader=FileSystemLoader([environment.working_dir, environment.driver_dir])
        )

        self._output_path = environment.output_dir

    def render_to_file(self, template_file, variables, output_file):
        """
        Render data to an output file using a Jinja2 template

        :param template_file: Path to Jinja2 template. The working directory as well as the directory
                              where the driver script is will be used to find the template file.
        :param variables: Variables to pass to the template
        :param output_file: Name to save the generated file to
        """
        template = self._env.get_template(template_file)
        result = template.render(**variables)

        if self._output_path:
            if not os.path.exists(self._output_path):
                os.makedirs(self._output_path)
            output_file = os.path.join(self._output_path, os.path.basename(output_file))

        self.log.debug("Rendering template %s -> %s", template_file, output_file)

        with open(output_file, "w") as fp:
            fp.write(result)

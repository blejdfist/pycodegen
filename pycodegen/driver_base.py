from jinja2 import Environment, FileSystemLoader
from collections import namedtuple
import os
import logging
from abc import ABC, abstractmethod

DriverEnvironment = namedtuple("DriverEnvironment", ["working_dir", "driver_dir", "output_dir", "input_filename"])


class DriverBase(ABC):
    """Base class for driver scripts"""

    log = logging.getLogger(__name__)

    def __init__(self, environment: DriverEnvironment):
        self._jinja_env = Environment(
            loader=FileSystemLoader([environment.driver_dir])
        )

        self._env = environment
        self._generated_files = []

    @property
    def environment(self):
        return self._env

    def render_to_file(self, template_file: str, variables: dict, output_file: str):
        """
        Render data to an output file using a Jinja2 template

        :param template_file: Path to Jinja2 template relative to the driver directory
        :param variables: Variables to pass to the template
        :param output_file: Name to save the generated file to
        """
        template = self._jinja_env.get_template(template_file)
        result = template.render(**variables)

        if self._env.output_dir:
            if not os.path.exists(self._env.output_dir):
                os.makedirs(self._env.output_dir)
            output_file = os.path.join(self._env.output_dir, os.path.basename(output_file))

        self.log.debug("Rendering template %s -> %s", template_file, output_file)

        with open(output_file, "w") as fp:
            fp.write(result)

    @abstractmethod
    def render(self, data: dict):
        pass

    @abstractmethod
    def get_dependencies(self):
        """
        :return: List of dependencies to be used by a build system to know when files need to be re-generated.
                 This should normally include the templates used.
        """
        pass

    @abstractmethod
    def get_generated_files(self):
        """
        :return: List of generated files to be used by a build system to know what files would be generated.
        """
        pass

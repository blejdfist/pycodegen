import json
import os
import tempfile

import pytest

from pycodegen import get_frontend_by_name
from pycodegen.driver_base import DriverBase, DriverEnvironment

class DriverFixture:
    def __init__(self, tmpdir, input_data, frontend):
        self._tmpdir = tmpdir
        self._frontend = frontend
        input_path = os.path.join(tmpdir, "input_file")
        with open(input_path, "w") as f:
            if frontend == "json":
                json.dump(input_data, f)
            else:
                f.write(input_data)
        self._input_path = input_path

    def render(self, template):
        with open(os.path.join(self._tmpdir, "template.jinja"), "w") as f:
            f.write(template)

        frontend = get_frontend_by_name(self._frontend)
        data = frontend.run(self._input_path)

        env = DriverEnvironment(
            working_dir=self._tmpdir,
            driver_dir=self._tmpdir,
            output_dir=None,
            input_filename=self._input_path,
        )
        driver = _SimpleDriver(env)
        driver.render(data)
        return driver.output


class _SimpleDriver(DriverBase):
    def __init__(self, environment):
        super().__init__(environment)
        self.output = None

    def render(self, data):
        template = self._jinja_env.get_template("template.jinja")
        self.output = template.render(items=data)

    def get_dependencies(self):
        return ["template.jinja"]

    def get_generated_files(self):
        return []


@pytest.fixture
def driver():
    with tempfile.TemporaryDirectory() as tmpdir:
        def _create(input_data, frontend):
            return DriverFixture(tmpdir, input_data, frontend)
        yield _create

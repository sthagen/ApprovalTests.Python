import subprocess

from approvaltests import ensure_file_exists
from approvaltests.command import Command
from approvaltests.core.reporter import Reporter
from approvaltests.utils import to_json
from typing import List, Optional, Tuple, Union


def create_config(config):
    name = config[0]
    path = config[1]
    if len(config) > 2:
        extra_args = config[2]
    else:
        extra_args = []
    return GenericDiffReporterConfig(name, path, extra_args)


class GenericDiffReporterConfig:
    def __init__(self, name: str, path: str, extra_args: Optional[List[str]]=None):
        self.name = name
        self.path = path
        self.extra_args = extra_args

    def serialize(self):
        result = [self.name, self.path]
        if self.extra_args:
            result.append(self.extra_args)
        return result


class GenericDiffReporter(Reporter):
    """
    A reporter that launches
    an external diff tool given by config.
    """

    @staticmethod
    def create(diff_tool_path: str) -> "GenericDiffReporter":
        return GenericDiffReporter(create_config(["custom", diff_tool_path]))

    def __init__(self, config: GenericDiffReporterConfig) -> None:
        self.name = config.name
        self.path = config.path
        self.extra_args = config.extra_args

    def __str__(self) -> str:
        config = {"name": self.name, "path": self.path}
        if self.extra_args:
            config.update({"arguments": self.extra_args})
        return to_json(config)

    @staticmethod
    def run_command(command_array):
        subprocess.Popen(command_array)

    def get_command(self, received: str, approved: str) -> List[str]:
        return [self.path] + self.extra_args + [received, approved]

    def report(self, received_path: str, approved_path: str) -> bool:
        if not self.is_working():
            return False
        ensure_file_exists(approved_path)
        command_array = self.get_command(received_path, approved_path)
        self.run_command(command_array)
        return True

    def is_working(self) -> Optional[str]:
        return Command(self.path).locate()

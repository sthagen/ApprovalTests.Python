import json
from typing import Any, Iterator, Union, List

from approvaltests.reporters import Reporter
from approvaltests.reporters.generic_diff_reporter import GenericDiffReporter, GenericDiffReporterConfig, create_config
from approvaltests.utils import get_adjacent_file


class GenericDiffReporterFactory(object):
    reporters: List[GenericDiffReporterConfig] = []

    def __init__(self) -> None:
        self.load(get_adjacent_file("reporters.json"))

    def add_default_reporter_config(self, config):
        self.reporters.insert(0, create_config(config))

    def list(self) -> List[str]:
        return [r.name for r in self.reporters]

    def get(self, reporter_name: str) -> Union[GenericDiffReporter, None]:
        config = next((r for r in self.reporters if r.name == reporter_name), None)
        if not config:
            return None
        return self._create_reporter(config)

    @staticmethod
    def _create_reporter(config: GenericDiffReporterConfig) -> GenericDiffReporter:
        return GenericDiffReporter(config)

    def save(self, file_name: str) -> str:
        with open(file_name, "w") as f:
            json.dump(
                [reporter.serialize() for reporter in self.reporters], f, sort_keys=True, indent=2, separators=(",", ": ")
            )
        return file_name

    def load(self, file_name: str) -> List[GenericDiffReporterConfig]:
        with open(file_name, "r") as f:
            configs = json.load(f)
        self.reporters = [create_config(config) for config in configs]
        return self.reporters

    def get_first_working(self) -> GenericDiffReporter:
        working = (i for i in self.get_all_reporters() if i.is_working())
        return next(working, None)

    def get_all_reporters(self) -> Iterator[GenericDiffReporter]:
        instances = (self._create_reporter(r) for r in self.reporters)
        return instances

    def remove(self, reporter_name: str) -> None:
        self.reporters = [r for r in self.reporters if r.name != reporter_name]

from subprocess import call
from typing import List

from approvaltests.core.reporter import Reporter


class ReceivedFileLauncherReporter(Reporter):
    """
    A reporter that attempts to
    open the received file using the
    system default file viewer.

    Depending on the file viewer being launched,
    the test suite execution may halt until the
    user has closed the new process.

    Note: only works on Windows for now.
    """

    @staticmethod
    def get_command(approved_path: str, received_path: str) -> List[str]:
        return ["cmd", "/C", "start", received_path, "/B"]

    def report(self, approved_path, received_path):
        command_array = self.get_command(approved_path, received_path)
        call(command_array)

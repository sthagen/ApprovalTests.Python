from unittest import TestCase

from approvaltests import approvals


class TestSubdirectories(TestCase):
    def test_subdirectory(self) -> None:
        approvals.verify("xxx")

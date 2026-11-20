"""Tests module."""

from pathlib import Path

from pyrig_containers.rig.configs.containers.compose import ComposeConfigFile


class TestComposeConfigFile:
    """Test class."""

    def test__configs(self) -> None:
        """Test method."""
        assert ComposeConfigFile.I._configs() == {  # noqa: SLF001
            "services": {
                "app": {
                    "build": {},
                },
            },
        }

    def test_parent_path(self) -> None:
        """Test method."""
        assert ComposeConfigFile.I.parent_path() == Path()

    def test_stem(self) -> None:
        """Test method."""
        assert ComposeConfigFile.I.stem() == "compose"

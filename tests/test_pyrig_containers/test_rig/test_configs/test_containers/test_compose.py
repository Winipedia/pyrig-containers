"""Tests module."""

from pathlib import Path

from pyrig_containers.rig.configs.containers.compose import ComposeConfigFile


class TestComposeConfigFile:
    """Test class."""

    def test__configs(self) -> None:
        """Test method."""
        assert ComposeConfigFile.I._configs() == {  # noqa: SLF001
            "name": "pyrig-containers",
            "services": {
                "app": {
                    "build": {},
                    "cap_drop": ["ALL"],
                    "security_opt": ["no-new-privileges:true"],
                },
            },
        }

    def test_name(self) -> None:
        """Test method."""
        assert ComposeConfigFile.I.name() == "pyrig-containers"

    def test_parent_path(self) -> None:
        """Test method."""
        assert ComposeConfigFile.I.parent_path() == Path()

    def test_service(self) -> None:
        """Test method."""
        assert ComposeConfigFile.I.service(
            "app",
            before={"build": {}},
            after={"image": "example"},
        ) == {
            "app": {
                "build": {},
                "cap_drop": ["ALL"],
                "security_opt": ["no-new-privileges:true"],
                "image": "example",
            },
        }
        assert ComposeConfigFile.I.service("smth") == {
            "smth": {
                "cap_drop": ["ALL"],
                "security_opt": ["no-new-privileges:true"],
            },
        }

    def test_service_app(self) -> None:
        """Test method."""
        assert ComposeConfigFile.I.service_app() == {
            "app": {
                "build": {},
                "cap_drop": ["ALL"],
                "security_opt": ["no-new-privileges:true"],
            },
        }

    def test_service_app_after(self) -> None:
        """Test method."""
        assert ComposeConfigFile.I.service_app_after() == {}

    def test_service_app_before(self) -> None:
        """Test method."""
        assert ComposeConfigFile.I.service_app_before() == {"build": {}}

    def test_stem(self) -> None:
        """Test method."""
        assert ComposeConfigFile.I.stem() == "compose"

"""Tests module."""

from collections.abc import Callable
from pathlib import Path
from typing import Any, override

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
        compose = ComposeConfigFile.I
        assert ComposeConfigFile.I.service(
            compose.service_app,
            build={},
            image="example",
        ) == {
            "service_name": "app",
            "image": "example",
            "build": {},
            "cap_drop": ["ALL"],
            "security_opt": ["no-new-privileges:true"],
        }
        assert compose.service(compose.service_app) == {
            "service_name": "app",
            "cap_drop": ["ALL"],
            "security_opt": ["no-new-privileges:true"],
        }

        settings = ComposeConfigFile.I.service(
            compose.service_app,
            security_opt=[],
            cap_drop=[],
            cap_add=["NET_BIND_SERVICE"],
            read_only=False,
            labels=[],
            restart="no",
            healthcheck={},
            networks={},
            depends_on=[],
            secrets=[],
            volumes=[],
            ports=[],
            env_file=[],
            environment={},
            user="",
            entrypoint=[],
            command="",
            image="example",
            build={},
        )
        expected = {
            "service_name": "app",
            "image": "example",
            "build": {},
            "entrypoint": [],
            "command": "",
            "env_file": [],
            "environment": {},
            "secrets": [],
            "ports": [],
            "networks": {},
            "volumes": [],
            "depends_on": [],
            "restart": "no",
            "healthcheck": {},
            "labels": [],
            "user": "",
            "read_only": False,
            "cap_drop": [],
            "cap_add": ["NET_BIND_SERVICE"],
            "security_opt": [],
        }
        assert settings == expected
        assert list(settings) == list(expected)
        assert compose.service(compose.service_app, cap_add=[])["cap_add"] == []

    def test_service_app(self) -> None:
        """Test method."""
        assert ComposeConfigFile.I.service_app() == {
            "service_name": "app",
            "build": {},
            "cap_drop": ["ALL"],
            "security_opt": ["no-new-privileges:true"],
        }

    def test_service_app_settings(self) -> None:
        """Test method."""
        assert ComposeConfigFile.I.service_app_settings() == {"build": {}}

    def test_service_by_name(self) -> None:
        """Test method."""
        assert ComposeConfigFile.I.service_by_name(ComposeConfigFile.I.service_app) == {
            "app": {
                "build": {},
                "cap_drop": ["ALL"],
                "security_opt": ["no-new-privileges:true"],
            },
        }

    def test_service_name(self) -> None:
        """Test method."""
        assert (
            ComposeConfigFile.I.service_name(ComposeConfigFile.I.service_app) == "app"
        )
        assert ComposeConfigFile.I.service_name(self.test_service_name) == (
            "test-service-name"
        )

    def test_services(self) -> None:
        """Test method."""
        assert ComposeConfigFile.I.services() == (ComposeConfigFile.I.service_app,)

    def test_services_configs(self) -> None:
        """Test method."""

        class MultipleServices(ComposeConfigFile):
            def service_database_server(self) -> dict[str, Any]:
                return self.service(self.service_database_server, image="postgres")

            @override
            def services(self) -> tuple[Callable[[], dict[str, Any]], ...]:
                return (*super().services(), self.service_database_server)

        compose = MultipleServices()
        expected = {
            "app": {
                "build": {},
                "cap_drop": ["ALL"],
                "security_opt": ["no-new-privileges:true"],
            },
            "database-server": {
                "image": "postgres",
                "cap_drop": ["ALL"],
                "security_opt": ["no-new-privileges:true"],
            },
        }
        assert compose.services_configs() == expected
        assert list(compose.services_configs()) == ["app", "database-server"]
        assert compose._configs()["services"] == expected  # noqa: SLF001

    def test_stem(self) -> None:
        """Test method."""
        assert ComposeConfigFile.I.stem() == "compose"

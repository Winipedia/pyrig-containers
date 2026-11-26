"""Tests module."""

from collections.abc import Callable
from pathlib import Path
from typing import Any, override

from pyrig_containers.rig.configs.containers.compose import (
    ComposeBuildConfigFile,
    ComposeConfigFile,
    ComposePullConfigFile,
)


class TestComposeAppOverrideConfigFile:
    """Test class."""

    def test__configs(self) -> None:
        """Test method."""
        assert ComposeBuildConfigFile.I._configs() == {  # noqa: SLF001
            "services": {"app": {"build": {}}},
        }

    def test_service_app_settings(self) -> None:
        """Test method."""
        assert ComposeBuildConfigFile.I.service_app_settings() == {"build": {}}


class TestComposeBuildConfigFile:
    """Test class."""

    def test_mode(self) -> None:
        """Test method."""
        assert ComposeBuildConfigFile.I.mode() == "build"

    def test_service_app_settings(self) -> None:
        """Test method."""
        assert ComposeBuildConfigFile.I.service_app_settings() == {"build": {}}


class TestComposeConfigFile:
    """Test class."""

    def test__configs(self) -> None:
        """Test method."""
        assert ComposeConfigFile.I._configs() == {  # noqa: SLF001
            "name": "pyrig-containers",
            "services": {
                "app": {
                    "cap_drop": ["ALL"],
                    "security_opt": ["no-new-privileges:true"],
                },
            },
        }

    def test_name(self) -> None:
        """Test method."""
        assert ComposeConfigFile.I.name() == "pyrig-containers"

    def test_override_file(self) -> None:
        """Test method."""
        assert ComposeConfigFile.I.override_file("build") == Path("compose.build.yml")
        assert ComposeConfigFile.I.override_file("pull") == Path("compose.pull.yml")

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
        assert compose.service(
            compose.service_app,
            image="example",
            pull_policy="always",
            build={},
        ) == {
            "service_name": "app",
            "image": "example",
            "pull_policy": "always",
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
            pull_policy="missing",
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
            "pull_policy": "missing",
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
            "cap_drop": ["ALL"],
            "security_opt": ["no-new-privileges:true"],
        }

    def test_service_app_name(self) -> None:
        """Test method."""
        assert ComposeConfigFile.I.service_app_name() == "app"

    def test_service_app_settings(self) -> None:
        """Test method."""
        assert ComposeConfigFile.I.service_app_settings() == {}

    def test_service_by_name(self) -> None:
        """Test method."""
        assert ComposeConfigFile.I.service_by_name(ComposeConfigFile.I.service_app) == {
            "app": {
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


class TestComposeOverrideConfigFile:
    """Test class."""

    def test_extension(self) -> None:
        """Test method."""
        assert ComposeBuildConfigFile.I.extension() == "yml"
        assert ComposeBuildConfigFile.I.path() == Path("compose.build.yml")

    def test_mode(self) -> None:
        """Test method."""
        assert ComposeBuildConfigFile.I.mode() == "build"

    def test_parent_path(self) -> None:
        """Test method."""
        assert ComposeBuildConfigFile.I.parent_path() == Path()

    def test_stem(self) -> None:
        """Test method."""
        assert ComposeBuildConfigFile.I.stem() == "compose.build"


class TestComposePullConfigFile:
    """Test class."""

    def test_mode(self) -> None:
        """Test method."""
        assert ComposePullConfigFile.I.mode() == "pull"

    def test_service_app_settings(self) -> None:
        """Test method."""
        assert ComposePullConfigFile.I.service_app_settings() == {
            "image": "ghcr.io/winipedia/pyrig-containers:latest",
            "pull_policy": "always",
        }

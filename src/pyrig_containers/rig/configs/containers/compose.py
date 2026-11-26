"""Compose configuration management."""

from abc import abstractmethod
from collections.abc import Callable
from pathlib import Path
from types import MethodType
from typing import Any, override

from pyrig.rig.configs.base.yaml import YMLDictConfigFile
from pyrig.rig.tools.packages.manager import PackageManager

from pyrig_containers.rig.tools.containers.registry import ContainerRegistry


class ComposeOverrideConfigFile(YMLDictConfigFile):
    """Configure a Compose override file for a specific mode."""

    @abstractmethod
    def mode(self) -> str:
        """Return the Compose override mode."""

    @override
    def parent_path(self) -> Path:
        """Return the directory containing the base Compose file."""
        return ComposeConfigFile.I.parent_path()

    @override
    def stem(self) -> str:
        """Return the override filename stem."""
        return ComposeConfigFile.I.override_file(self.mode()).stem


class ComposeAppOverrideConfigFile(ComposeOverrideConfigFile):
    """Configure the app service for a specific Compose mode."""

    @abstractmethod
    def service_app_settings(self) -> dict[str, Any]:
        """Return the app service settings for this mode."""

    @override
    def _configs(self) -> dict[str, Any]:
        """Return the app service override."""
        return {
            "services": {
                ComposeConfigFile.I.service_app_name(): self.service_app_settings(),
            },
        }


class ComposeBuildConfigFile(ComposeAppOverrideConfigFile):
    """Configure the app image to be built locally."""

    @override
    def mode(self) -> str:
        """Return the build mode."""
        return "build"

    @override
    def service_app_settings(self) -> dict[str, Any]:
        """Return the app build settings."""
        return {"build": {}}


class ComposeConfigFile(YMLDictConfigFile):
    """The project's generated Compose configuration with runtime hardening."""

    SERVICE_NAME_KEY = "service_name"

    @override
    def parent_path(self) -> Path:
        """Return the project root directory."""
        return Path()

    @override
    def stem(self) -> str:
        """Return `"compose"`."""
        return "compose"

    @override
    def _configs(self) -> dict[str, Any]:
        """Return the project name and all configured services."""
        return {
            "name": self.name(),
            "services": self.services_configs(),
        }

    def override_file(self, mode: str) -> Path:
        """Return the path to the Compose override for the selected mode."""
        path = self.path()
        return path.with_suffix(f".{mode}{path.suffix}")

    def service_app_name(self) -> str:
        """Return the app service name."""
        return self.service_name(self.service_app)

    def name(self) -> str:
        """Return the Compose project name derived from the package manager."""
        return PackageManager.I.project_name().lower()

    def services_configs(self) -> dict[str, dict[str, Any]]:
        """Assemble service configurations keyed by their derived names."""
        return {
            name: settings
            for service in self.services()
            for name, settings in self.service_by_name(service).items()
        }

    def service_by_name(
        self,
        service: Callable[[], dict[str, Any]],
    ) -> dict[str, dict[str, Any]]:
        """Call a service builder and move its internal name to the mapping key."""
        settings = service()
        return {settings.pop(self.SERVICE_NAME_KEY): settings}

    def services(self) -> tuple[Callable[[], dict[str, Any]], ...]:
        """Return the service builders for this Compose configuration."""
        return (self.service_app,)

    def service_app(self) -> dict[str, Any]:
        """Return the app service."""
        return self.service(self.service_app, **self.service_app_settings())

    def service(  # noqa: C901, PLR0912, PLR0913
        self,
        method: MethodType,
        *,
        image: str | None = None,
        pull_policy: str | None = None,
        build: str | dict[str, Any] | None = None,
        entrypoint: str | list[str] | None = None,
        command: str | list[str] | None = None,
        env_file: str | list[Any] | None = None,
        environment: dict[str, Any] | list[str] | None = None,
        secrets: list[Any] | None = None,
        ports: list[Any] | None = None,
        networks: list[str] | dict[str, Any] | None = None,
        volumes: list[Any] | None = None,
        depends_on: list[str] | dict[str, Any] | None = None,
        restart: str | None = None,
        healthcheck: dict[str, Any] | None = None,
        labels: dict[str, Any] | list[str] | None = None,
        user: str | None = None,
        read_only: bool | None = None,
        cap_drop: list[str] | None = None,
        cap_add: list[str] | None = None,
        security_opt: list[str] | None = None,
    ) -> dict[str, Any]:
        """Return a named service with ordered settings and hardening defaults.

        Args:
            method: The service method.
            image: Image name.
            pull_policy: Image pull policy.
            build: Build context or build configuration.
            entrypoint: Entrypoint overriding the image default.
            command: Command overriding the image default.
            env_file: Environment file or list of environment files.
            environment: Container environment variables.
            secrets: Secrets granted to the service.
            ports: Published ports.
            networks: Networks attached to the service.
            volumes: Mounted volumes.
            depends_on: Service dependencies.
            restart: Container restart policy.
            healthcheck: Container health check.
            labels: Container labels.
            user: User running the container.
            read_only: Whether the container filesystem is read-only.
            cap_drop: Linux capabilities to drop; defaults to `["ALL"]`.
            cap_add: Linux capabilities to add; omitted when `None`.
            security_opt: Security options; defaults to `["no-new-privileges:true"]`.

        Returns:
            Service settings containing the derived name under `SERVICE_NAME_KEY`.
        """
        settings: dict[str, Any] = {self.SERVICE_NAME_KEY: self.service_name(method)}
        if image is not None:
            settings["image"] = image
        if pull_policy is not None:
            settings["pull_policy"] = pull_policy
        if build is not None:
            settings["build"] = build
        if entrypoint is not None:
            settings["entrypoint"] = entrypoint
        if command is not None:
            settings["command"] = command
        if env_file is not None:
            settings["env_file"] = env_file
        if environment is not None:
            settings["environment"] = environment
        if secrets is not None:
            settings["secrets"] = secrets
        if ports is not None:
            settings["ports"] = ports
        if networks is not None:
            settings["networks"] = networks
        if volumes is not None:
            settings["volumes"] = volumes
        if depends_on is not None:
            settings["depends_on"] = depends_on
        if restart is not None:
            settings["restart"] = restart
        if healthcheck is not None:
            settings["healthcheck"] = healthcheck
        if labels is not None:
            settings["labels"] = labels
        if user is not None:
            settings["user"] = user
        if read_only is not None:
            settings["read_only"] = read_only
        settings["cap_drop"] = ["ALL"] if cap_drop is None else cap_drop
        if cap_add is not None:
            settings["cap_add"] = cap_add
        settings["security_opt"] = (
            ["no-new-privileges:true"] if security_opt is None else security_opt
        )
        return settings

    def service_app_settings(self) -> dict[str, Any]:
        """Return the default settings for the app service."""
        return {}

    def service_name(self, method: MethodType) -> str:
        """Derive a kebab-case service name from a `service_*` method."""
        return method.__name__.removeprefix(f"{self.service.__name__}_").replace(
            "_",
            "-",
        )


class ComposePullConfigFile(ComposeAppOverrideConfigFile):
    """Configure the app image to be pulled from the registry."""

    @override
    def mode(self) -> str:
        """Return the pull mode."""
        return "pull"

    @override
    def service_app_settings(self) -> dict[str, Any]:
        """Return the app registry settings."""
        return {
            "image": ContainerRegistry.I.image_tag_latest(),
            "pull_policy": "always",
        }

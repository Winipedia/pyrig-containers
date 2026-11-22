"""Compose configuration management."""

from pathlib import Path
from typing import Any, override

from pyrig.rig.configs.base.yaml import YMLDictConfigFile
from pyrig.rig.tools.packages.manager import PackageManager


class ComposeConfigFile(YMLDictConfigFile):
    """The project's generated Compose configuration with runtime hardening."""

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
        """Return the project name and the app service's build configuration."""
        return {
            "name": self.name(),
            "services": {
                **self.app_service(),
            },
        }

    def app_service(self) -> dict[str, Any]:
        """Return the app service."""
        return self.service(
            "app",
            before=self.app_service_before(),
            after=self.app_service_after(),
        )

    def name(self) -> str:
        """Return the Compose project name derived from the package manager."""
        return PackageManager.I.project_name().lower()

    def app_service_after(self) -> dict[str, Any]:
        """Return the app service's settings placed after the defaults."""
        return {}

    def app_service_before(self) -> dict[str, Any]:
        """Return the app service's settings placed before the defaults."""
        return {"build": {}}

    def service(
        self,
        name: str,
        *,
        before: dict[str, Any] | None = None,
        after: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Return a named service with runtime hardening defaults.

        Args:
            name: Name of the service.
            before: Settings placed before the defaults; defaults take precedence.
            after: Settings placed after the defaults; these take precedence.

        Returns:
            A mapping from the service name to its settings.
        """
        return {
            name: {
                **(before or {}),
                "cap_drop": ["ALL"],
                "security_opt": ["no-new-privileges:true"],
                **(after or {}),
            },
        }

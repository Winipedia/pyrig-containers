"""Compose configuration management."""

from pathlib import Path
from typing import Any, override

from pyrig.rig.configs.base.yaml import YMLDictConfigFile


class ComposeConfigFile(YMLDictConfigFile):
    """The project's `compose.yml`, using podman-compose's Containerfile discovery."""

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
        """Return the service configuration that builds the project's image."""
        return {
            "services": {
                "app": {
                    "build": {},
                },
            },
        }

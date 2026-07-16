"""Test module."""

from pyrig_containers.rig.tools.packages.manager import PackageManager


class TestPackageManager:
    """Test class."""

    def test_container_image(self) -> None:
        """Test method."""
        assert PackageManager.I.container_image() == (
            "ghcr.io/astral-sh/uv:latest",
            "/uv",
            "/usr/local/bin/uv",
        )

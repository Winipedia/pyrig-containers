"""Test module."""

from pyrig_containers.rig.tools.packages.manager import PackageManager


class TestPackageManager:
    """Test class."""

    def test_container_binary_copy_spec(self) -> None:
        """Test method."""
        assert PackageManager.I.container_binary_copy_spec() == (
            "ghcr.io/astral-sh/uv:latest",
            "/uv",
            "/usr/local/bin/uv",
        )

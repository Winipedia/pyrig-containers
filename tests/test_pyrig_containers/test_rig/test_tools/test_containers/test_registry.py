"""module."""

from pyrig_containers.rig.tools.containers import registry
from pyrig_containers.rig.tools.containers.registry import ContainerRegistry


class TestContainerRegistry:
    """Test class."""

    def test_name(self) -> None:
        """Test method."""
        assert ContainerRegistry.I.name() == "ghcr"

    def test_group(self) -> None:
        """Test method."""
        assert ContainerRegistry.I.group() == "project-info"

    def test_image_url(self) -> None:
        """Test method."""
        assert ContainerRegistry.I.image_url() == (
            "https://img.shields.io/badge/GHCR-Container_Image-181717"
            "?logo=github&logoColor=white"
        )

    def test_link_url(self) -> None:
        """Test method."""
        assert (
            ContainerRegistry.I.link_url()
            == "https://github.com/Winipedia/pyrig-containers"
            "/pkgs/container/pyrig-containers"
        )

    def test_dev_dependencies(self) -> None:
        """Test method."""
        assert ContainerRegistry.I.dev_dependencies() == ()

    def test_host(self) -> None:
        """Test method."""
        assert ContainerRegistry.I.host() == "ghcr.io"

    def test_image_name(self) -> None:
        """Test method."""
        assert ContainerRegistry.I.image_name() == "ghcr.io/winipedia/pyrig-containers"

    def test_image_tag(self) -> None:
        """Test method."""
        assert (
            ContainerRegistry.I.image_tag("v1.2.3")
            == "ghcr.io/winipedia/pyrig-containers:v1.2.3"
        )


def test_module_docstring() -> None:
    """Test module docstring."""
    assert (
        registry.__doc__
        == """Container registry wrapper.

Wraps the container registry information for publishing container images.
"""
    )

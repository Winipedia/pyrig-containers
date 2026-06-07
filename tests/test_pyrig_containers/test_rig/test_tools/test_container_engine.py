"""module."""

from pyrig_containers.rig.tools import container_engine
from pyrig_containers.rig.tools.container_engine import ContainerEngine


class TestContainerEngine:
    """Test class."""

    def test_image_url(self) -> None:
        """Test method."""
        assert (
            ContainerEngine.I.image_url()
            == "https://img.shields.io/badge/Container-Podman-A23CD6?logo=podman&logoColor=grey&colorA=0D1F3F&colorB=A23CD6"
        )

    def test_link_url(self) -> None:
        """Test method."""
        assert ContainerEngine.I.link_url() == "https://podman.io"

    def test_group(self) -> None:
        """Test method."""
        result = ContainerEngine.I.group()
        assert isinstance(result, str)
        assert result == "tooling"

    def test_dev_dependencies(self) -> None:
        """Test method."""
        result = ContainerEngine.I.dev_dependencies()
        assert result == ()

    def test_name(self) -> None:
        """Test method."""
        result = ContainerEngine.I.name()
        assert result == "podman"


def test_module_docstring() -> None:
    """Test module docstring."""
    assert (
        container_engine.__doc__
        == """Container engine wrapper.

Wraps container engine commands and information.
"""
    )

"""module."""

from pyrig_containers.rig.tools.containers import engine
from pyrig_containers.rig.tools.containers.engine import ContainerEngine


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

    def test_login_args(self) -> None:
        """Test method."""
        result = ContainerEngine.I.login_args(
            "ghcr.io",
            username="user",
            password="token",  # noqa: S106  # nosec: B106
        )
        assert str(result) == ("podman login ghcr.io --username user --password token")

    def test_build_args(self) -> None:
        """Test method."""
        result = ContainerEngine.I.build_args(
            "image:v1.0.0", "image:latest", containerfile="Containerfile"
        )
        assert str(result) == (
            "podman build --file Containerfile --tag image:v1.0.0 --tag image:latest ."
        )

    def test_build_args_custom_context(self) -> None:
        """Test method."""
        result = ContainerEngine.I.build_args(
            "image:latest", containerfile="Containerfile", context="src"
        )
        assert str(result) == (
            "podman build --file Containerfile --tag image:latest src"
        )

    def test_push_args(self) -> None:
        """Test method."""
        result = ContainerEngine.I.push_args("ghcr.io/owner/repo:latest")
        assert str(result) == "podman push ghcr.io/owner/repo:latest"


def test_module_docstring() -> None:
    """Test module docstring."""
    assert (
        engine.__doc__
        == """Container engine wrapper.

Wraps container engine commands and information.
"""
    )

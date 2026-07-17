"""module."""

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
        random_string = "something"
        result = ContainerEngine.I.login_args(
            registry="ghcr.io",
            username="user",
            password=random_string,  # nosec: B106
        )
        assert (
            str(result)
            == f"podman login ghcr.io --username=user --password={random_string}"
        )

    def test_login_args_extra_args(self) -> None:
        """Test method."""
        random_string = "something"
        result = ContainerEngine.I.login_args(
            "--tls-verify=false",
            registry="ghcr.io",
            username="user",
            password=random_string,  # nosec: B106
        )
        assert str(result) == (
            f"podman login ghcr.io --username=user --password={random_string} --tls-verify=false"  # noqa: E501
        )

    def test_build_args(self) -> None:
        """Test method."""
        result = ContainerEngine.I.build_args(tags=("image:v1.0.0", "image:latest"))
        assert str(result) == ("podman build --tag=image:v1.0.0 --tag=image:latest .")

    def test_build_args_custom_context(self) -> None:
        """Test method."""
        result = ContainerEngine.I.build_args(tags=("image:latest",), context="src")
        assert str(result) == "podman build --tag=image:latest src"

    def test_build_args_extra_args(self) -> None:
        """Test method."""
        result = ContainerEngine.I.build_args("--no-cache", tags=("image:latest",))
        assert str(result) == "podman build --tag=image:latest --no-cache ."

    def test_push_args(self) -> None:
        """Test method."""
        result = ContainerEngine.I.push_args(tag="ghcr.io/owner/repo:latest")
        assert str(result) == "podman push ghcr.io/owner/repo:latest"

    def test_push_args_extra_args(self) -> None:
        """Test method."""
        result = ContainerEngine.I.push_args(
            "--tls-verify=false",
            tag="ghcr.io/owner/repo:latest",
        )
        assert str(result) == (
            "podman push ghcr.io/owner/repo:latest --tls-verify=false"
        )

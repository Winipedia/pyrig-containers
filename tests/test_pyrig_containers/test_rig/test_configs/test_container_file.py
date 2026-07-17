"""module."""

from pathlib import Path

from pyrig_containers.rig.configs.container_file import ContainerfileConfigFile


class TestContainerfileConfigFile:
    """Test class."""

    def test_stem(self) -> None:
        """Test method."""
        assert ContainerfileConfigFile.I.stem() == "Containerfile"

    def test_parent_path(self) -> None:
        """Test method."""
        assert ContainerfileConfigFile.I.parent_path() == Path()

    def test_extension(self) -> None:
        """Test method."""
        assert ContainerfileConfigFile.I.extension() == ""

    def test_extension_separator(self) -> None:
        """Test method."""
        assert ContainerfileConfigFile.I.extension_separator() == ""

    def test_content(self) -> None:
        """Test method."""
        content = ContainerfileConfigFile.I.content()
        assert content.startswith("FROM python:")
        assert "WORKDIR" in content
        assert "COPY --from=" in content
        assert "COPY" in content
        assert "RUN useradd --create-home --uid=1000 appuser" in content
        assert "RUN chown --recursive appuser:appuser ." in content
        assert "USER appuser" in content

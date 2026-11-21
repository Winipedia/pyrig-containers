"""module."""

from pathlib import Path

from pyrig_containers.rig.configs.containers.file import (
    ContainerfileConfigFile,
)


class TestContainerfileConfigFile:
    """Test class."""

    def test_add_user_args(self) -> None:
        """Test method."""
        assert str(ContainerfileConfigFile.I.add_user_args()) == (
            "useradd --create-home --uid=1000 appuser"
        )

    def test_base_image(self) -> None:
        """Test method."""
        assert ContainerfileConfigFile.I.base_image() == "python:3.15-slim"

    def test_chown_workdir_args(self) -> None:
        """Test method."""
        assert str(ContainerfileConfigFile.I.chown_workdir_args()) == (
            "chown appuser:appuser ."
        )

    def test_content(self) -> None:
        """Test method."""
        assert (
            ContainerfileConfigFile.I.content()
            == r"""FROM python:3.15-slim
WORKDIR /pyrig-containers

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
COPY LICENSE README.md pyproject.toml uv.lock ./
COPY src/pyrig_containers src/pyrig_containers

RUN uv sync --no-group=dev

RUN useradd --create-home --uid=1000 appuser \
    && chown appuser:appuser .
USER 1000

ENTRYPOINT ["uv", "run", "--no-sync", "pyrig-containers"]
"""
        )

    def test_copy_binaries(self) -> None:
        """Test method."""
        assert ContainerfileConfigFile.I.copy_binaries() == (
            "COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv"
        )

    def test_copy_required_dirs(self) -> None:
        """Test method."""
        assert ContainerfileConfigFile.I.copy_required_dirs() == (
            "COPY src/pyrig_containers src/pyrig_containers"
        )

    def test_copy_required_files(self) -> None:
        """Test method."""
        assert ContainerfileConfigFile.I.copy_required_files() == (
            "COPY LICENSE README.md pyproject.toml uv.lock ./"
        )

    def test_entrypoint(self) -> None:
        """Test method."""
        assert ContainerfileConfigFile.I.entrypoint() == (
            'ENTRYPOINT ["uv", "run", "--no-sync", "pyrig-containers"]'
        )

    def test_entrypoint_args(self) -> None:
        """Test method."""
        assert str(ContainerfileConfigFile.I.entrypoint_args()) == (
            "uv run --no-sync pyrig-containers"
        )

    def test_extension(self) -> None:
        """Test method."""
        assert ContainerfileConfigFile.I.extension() == ""

    def test_extension_separator(self) -> None:
        """Test method."""
        assert ContainerfileConfigFile.I.extension_separator() == ""

    def test_from_image(self) -> None:
        """Test method."""
        assert ContainerfileConfigFile.I.from_image() == "FROM python:3.15-slim"

    def test_install_dependencies_args(self) -> None:
        """Test method."""
        assert str(ContainerfileConfigFile.I.install_dependencies_args()) == (
            "uv sync --no-group=dev"
        )

    def test_parent_path(self) -> None:
        """Test method."""
        assert ContainerfileConfigFile.I.parent_path() == Path()

    def test_project_command(self) -> None:
        """Test method."""
        assert str(ContainerfileConfigFile.I.project_command()) == "pyrig-containers"

    def test_required_binaries(self) -> None:
        """Test method."""
        assert ContainerfileConfigFile.I.required_binaries() == (
            ("ghcr.io/astral-sh/uv:latest", "/uv", "/usr/local/bin/uv"),
        )

    def test_required_dirs(self) -> None:
        """Test method."""
        assert ContainerfileConfigFile.I.required_dirs() == (
            Path("src/pyrig_containers"),
        )

    def test_required_files(self) -> None:
        """Test method."""
        assert ContainerfileConfigFile.I.required_files() == (
            Path("README.md"),
            Path("LICENSE"),
            Path("pyproject.toml"),
            Path("uv.lock"),
        )

    def test_run_add_and_chown_user(self) -> None:
        """Test method."""
        assert (
            ContainerfileConfigFile.I.run_add_and_chown_user()
            == r"""RUN useradd --create-home --uid=1000 appuser \
    && chown appuser:appuser ."""
        )

    def test_run_install_dependencies(self) -> None:
        """Test method."""
        assert ContainerfileConfigFile.I.run_install_dependencies() == (
            "RUN uv sync --no-group=dev"
        )

    def test_stem(self) -> None:
        """Test method."""
        assert ContainerfileConfigFile.I.stem() == "Containerfile"

    def test_user(self) -> None:
        """Test method."""
        assert ContainerfileConfigFile.I.user() == "USER 1000"

    def test_user_id(self) -> None:
        """Test method."""
        expected_user_id = 1000
        assert ContainerfileConfigFile.I.user_id() == expected_user_id

    def test_username(self) -> None:
        """Test method."""
        assert ContainerfileConfigFile.I.username() == "appuser"

    def test_workdir(self) -> None:
        """Test method."""
        assert ContainerfileConfigFile.I.workdir() == "WORKDIR /pyrig-containers"

    def test_working_dir(self) -> None:
        """Test method."""
        assert ContainerfileConfigFile.I.working_dir() == Path("pyrig-containers")

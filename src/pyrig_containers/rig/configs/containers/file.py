"""Containerfile configuration management."""

import json
from collections import defaultdict
from pathlib import Path
from typing import override

from pyrig.core.subprocesses import Args
from pyrig.rig.configs.base.string_ import StringConfigFile
from pyrig.rig.configs.community.license import LicenseConfigFile
from pyrig.rig.configs.pyproject import PyprojectConfigFile
from pyrig.rig.configs.readme import ReadmeConfigFile

from pyrig_containers.rig.tools.packages.manager import PackageManager


class ContainerfileConfigFile(StringConfigFile):
    """The project's `Containerfile`, built from a Python slim base image.

    Copies in required binaries, installs runtime dependencies with uv, and
    runs the project as a non-root user (`appuser`, UID 1000).
    """

    @override
    def content(self) -> str:
        """Build the required `Containerfile` text.

        Returns:
            Containerfile instructions that copy in required binaries,
            install the project's runtime dependencies, and run the project
            as the non-root `appuser` user.
        """
        return f"""{self.from_image()}
{self.workdir()}

{self.copy_required_binaries()}
{self.copy_required_files()}
{self.copy_required_dirs()}

{self.env()}

{self.run_install_dependencies()}

{self.run_add_and_chown_user()}
{self.user()}

{self.entrypoint()}
"""

    @override
    def extension(self) -> str:
        """Return an empty string; `Containerfile` has no file extension."""
        return ""

    @override
    def extension_separator(self) -> str:
        """Return an empty string, overriding the default `.` separator.

        Prevents a trailing dot from being appended when the extension is
        empty, so the filename remains `Containerfile` instead of
        `Containerfile.`.
        """
        return ""

    @override
    def parent_path(self) -> Path:
        """Return the project root directory."""
        return Path()

    @override
    def stem(self) -> str:
        """Return `"Containerfile"`."""
        return "Containerfile"

    def copy_required_binaries(self) -> str:
        """Return COPY instructions for the required binaries."""
        return "\n".join(
            f"COPY --from={image_url} {image_source_path} {image_destination_path}"
            for image_url, image_source_path, image_destination_path in sorted(
                self.required_binaries(),
            )
        )

    def copy_required_dirs(self) -> str:
        """Return COPY instructions for the required directories."""
        return "\n".join(
            f"COPY {d.as_posix()} {d.as_posix()}" for d in sorted(self.required_dirs())
        )

    def copy_required_files(self) -> str:
        """Return COPY instructions grouping required files by parent directory.

        Paths are expected to be relative to the build context and contain no
        spaces. Destination directories retain their relative paths.
        """
        by_dir: defaultdict[str, list[str]] = defaultdict(list)
        for path in self.required_files():
            parent = f"{path.parent.as_posix()}/"
            by_dir[parent].append(path.as_posix())
        return "\n".join(
            f"COPY {' '.join(sorted(srcs))} {dst}"
            for dst, srcs in sorted(by_dir.items())
        )

    def entrypoint(self) -> str:
        """Return the JSON-form ENTRYPOINT instruction."""
        return f"ENTRYPOINT {json.dumps(list(self.entrypoint_args()))}"

    def env(self) -> str:
        """Return ENV instructions for the configured environment groups."""
        return "\n".join(
            f"ENV {' '.join(f'{key}={value}' for key, value in env.items())}"
            for env in self.environments()
        )

    def from_image(self) -> str:
        """Return the FROM instruction for the base image."""
        return f"FROM {self.base_image()}"

    def run_add_and_chown_user(self) -> str:
        """Return a multiline RUN instruction creating the user and workdir owner."""
        return rf"""RUN {self.add_user_args()} \
    && {self.chown_workdir_args()}"""

    def run_install_dependencies(self) -> str:
        """Return the RUN instruction installing non-development dependencies."""
        return f"RUN {self.install_dependencies_args()}"

    def user(self) -> str:
        """Return the USER instruction selecting the application user ID."""
        return f"USER {self.user_id()}"

    def workdir(self) -> str:
        """Return the WORKDIR instruction for the project directory."""
        return f"WORKDIR /{self.working_dir().as_posix()}"

    def add_user_args(self) -> Args:
        """Return arguments to create the application user and its home directory."""
        return Args(
            "useradd",
            "--create-home",
            f"--uid={self.user_id()}",
            self.username(),
        )

    def base_image(self) -> str:
        """Return the Python slim image for the latest supported Python version."""
        return f"python:{PyprojectConfigFile.I.latest_possible_python_version()}-slim"

    def chown_workdir_args(self) -> Args:
        """Return arguments to give the application user workdir ownership."""
        username = self.username()
        return Args("chown", f"{username}:{username}", Path().as_posix())

    def entrypoint_args(self) -> Args:
        """Return arguments to run the project without syncing dependencies."""
        return PackageManager.I.run_no_install_args(*self.project_command())

    def environments(self) -> tuple[dict[str, str], ...]:
        """Return the environment groups to include in the container."""
        return (self.python_environment(),)

    def install_dependencies_args(self) -> Args:
        """Return arguments to install dependencies without the dev group."""
        return PackageManager.I.install_dependencies_no_dev_args()

    def required_binaries(self) -> tuple[tuple[str, str, str], ...]:
        """Return image and paths for binaries copied into the container."""
        return (PackageManager.I.container_binary_copy_spec(),)

    def required_dirs(self) -> tuple[Path, ...]:
        """Return source directories to copy from the build context."""
        return (PackageManager.I.package_root(),)

    def required_files(self) -> tuple[Path, ...]:
        """Return metadata and lock files to copy from the build context."""
        return (
            ReadmeConfigFile.I.path(),
            LicenseConfigFile.I.path(),
            PyprojectConfigFile.I.path(),
            PackageManager.I.lock_file(),
        )

    def working_dir(self) -> Path:
        """Return the project name used as the container's working directory."""
        return Path(PackageManager.I.project_name())

    def project_command(self) -> Args:
        """Return the project command invoked by the container entrypoint."""
        return Args(PackageManager.I.project_name())

    def python_environment(self) -> dict[str, str]:
        """Return the Python environment settings used in the container."""
        return {
            "PYTHONUNBUFFERED": "1",
            "PYTHONDONTWRITEBYTECODE": "1",
        }

    def user_id(self) -> int:
        """Return the application user's numeric ID, 1000."""
        return 1000

    def username(self) -> str:
        """Return the application user's name, `appuser`."""
        return "appuser"

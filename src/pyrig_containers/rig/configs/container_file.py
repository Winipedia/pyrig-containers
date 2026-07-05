"""Containerfile configuration management."""

import json
from pathlib import Path

from pyrig.rig.configs.base.string_ import StringConfigFile
from pyrig.rig.configs.license import LicenseConfigFile
from pyrig.rig.configs.pyproject import PyprojectConfigFile
from pyrig.rig.configs.readme import ReadmeConfigFile

from pyrig_containers.rig.tools.package_manager import PackageManager


class ContainerfileConfigFile(StringConfigFile):
    """The project's `Containerfile`, built from a Python slim base image.

    Copies in the uv binary, installs runtime dependencies with uv, and runs
    the project as a non-root user (`appuser`, UID 1000).
    """

    def stem(self) -> str:
        """Return `"Containerfile"`."""
        return "Containerfile"

    def parent_path(self) -> Path:
        """Return the project root directory."""
        return Path()

    def extension(self) -> str:
        """Return an empty string; `Containerfile` has no file extension."""
        return ""

    def extension_separator(self) -> str:
        """Return an empty string, overriding the default `.` separator.

        Prevents a trailing dot from being appended when the extension is
        empty, so the filename remains `Containerfile` instead of
        `Containerfile.`.
        """
        return ""

    def lines(self) -> list[str]:
        """Return the Containerfile build instructions."""
        return self.layers()

    def layers(self) -> list[str]:
        """Build the ordered sequence of Containerfile instructions.

        Project metadata and the lock file are copied in their own layer,
        ahead of the application source tree, so that a source-only change
        does not invalidate the earlier layers.

        Returns:
            Containerfile instruction lines, ending with a trailing empty
            string.
        """
        latest_python_version = PyprojectConfigFile.I.latest_possible_python_version()
        package_root = PackageManager.I.package_root().as_posix()
        project_name = PackageManager.I.project_name()
        workdir = Path(project_name).as_posix()
        app_username = "appuser"
        entrypoint = json.dumps(list(PackageManager.I.run_args(project_name)))
        readme_path, license_path, pyproject_path, lock_file_path = (
            ReadmeConfigFile.I.path().as_posix(),
            LicenseConfigFile.I.path().as_posix(),
            PyprojectConfigFile.I.path().as_posix(),
            PackageManager.I.lock_file().as_posix(),
        )
        copy_files = f"{readme_path} {license_path} {pyproject_path} {lock_file_path}"
        install_dependencies_no_dev = (
            PackageManager.I.install_dependencies_no_dev_args()
        )
        image_url, image_source_path, image_destination_path = (
            PackageManager.I.container_image()
        )

        return [
            f"FROM python:{latest_python_version}-slim",
            f"WORKDIR /{workdir}",
            f"COPY --from={image_url} {image_source_path} {image_destination_path}",
            f"COPY {copy_files} ./",
            f"RUN useradd -m -u 1000 {app_username}",
            f"RUN chown -R {app_username}:{app_username} .",
            f"USER {app_username}",
            f"COPY --chown={app_username}:{app_username} {package_root} {package_root}",
            f"RUN {install_dependencies_no_dev}",
            f"RUN rm {copy_files}",
            f"ENTRYPOINT {entrypoint}",
            "",
        ]

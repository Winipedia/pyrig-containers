"""Container registry identity and badge metadata for publishing images."""

from pyrig.rig.tools.base.tool import Group, Tool
from pyrig.rig.tools.version_control.controller import VersionController
from pyrig.rig.tools.version_control.remote.controller import RemoteVersionController

from pyrig_containers.rig.tools.packages.manager import PackageManager


class ContainerRegistry(Tool):
    """GitHub Container Registry (GHCR) wrapper.

    Provides the registry host, the project's fully qualified image
    reference within it, and badge metadata for GHCR.
    """

    def dev_dependencies(self) -> tuple[str, ...]:
        """Return an empty tuple; the registry requires no Python package."""
        return ()

    def group(self) -> str:
        """Return `Group.PROJECT_INFO`."""
        return Group.PROJECT_INFO

    def image_url(self) -> str:
        """Return the Shields.io badge URL for GHCR."""
        return "https://img.shields.io/badge/GHCR-Container_Image-black?logo=github&logoColor=white"

    def link_url(self) -> str:
        """Return the URL of the project's GHCR container package page."""
        repo_url = RemoteVersionController.I.repo_url()
        package = PackageManager.I.project_name()
        return f"{repo_url}/pkgs/container/{package}"

    def name(self) -> str:
        """Return `"ghcr"`."""
        return "ghcr"

    def image_tag(self, tag: str) -> str:
        """Build the project's image reference for the given tag.

        Args:
            tag: Tag to append to the image name (e.g. `latest` or `1.2.3`).

        Returns:
            Image reference in the form `ghcr.io/<owner>/<project>:<tag>`.
        """
        return f"{self.image_name()}:{tag}"

    def image_name(self) -> str:
        """Build the project's fully qualified image name without a tag.

        Combines the registry host with the lowercased repository owner and
        project name, as GHCR requires image names to be lowercase.

        Returns:
            Image name in the form `ghcr.io/<owner>/<project>`.
        """
        owner = VersionController.I.repo_owner().lower()
        project = PackageManager.I.project_name().lower()
        return f"{self.host()}/{owner}/{project}"

    def host(self) -> str:
        """Return `"ghcr.io"`."""
        return "ghcr.io"

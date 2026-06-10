"""Container registry wrapper.

Wraps the container registry information for publishing container images.
"""

from pyrig.rig.tools.base.tool import Group, Tool
from pyrig.rig.tools.package_manager import PackageManager
from pyrig.rig.tools.version_control.remote import RemoteVersionController
from pyrig.rig.tools.version_control.version_controller import VersionController


class ContainerRegistry(Tool):
    """GitHub Container Registry (GHCR) wrapper.

    Models the registry that container images are published to, kept separate
    from the container engine that builds and pushes them (a registry is not a
    property of the engine, nor of the remote version controller). Provides the
    registry host, the project's image reference within it, and badge metadata
    for GHCR.
    """

    def name(self) -> str:
        """Get tool name.

        Returns:
            'ghcr'
        """
        return "ghcr"

    def group(self) -> str:
        """Returns the group the tool belongs to."""
        return Group.PROJECT_INFO

    def image_url(self) -> str:
        """Return the badge image URL for this tool.

        Returns:
            The URL of the badge image as a string.
        """
        return "https://img.shields.io/badge/GHCR-Container_Image-181717?logo=github&logoColor=white"

    def link_url(self) -> str:
        """Return the URL that the badge should link to for this tool.

        Returns:
            The URL of the repository's GHCR container package page as a string.
        """
        repo_url = RemoteVersionController.I.repo_url()
        package = PackageManager.I.project_name()
        return f"{repo_url}/pkgs/container/{package}"

    def dev_dependencies(self) -> tuple[str, ...]:
        """Get development dependencies for this tool.

        Returns an empty tuple because the registry itself requires no extra
        development dependency; pushing images is handled by the container
        engine (e.g. podman).

        Returns:
            Empty tuple.
        """
        return ()

    def host(self) -> str:
        """Get the container registry host to publish to.

        Returns:
            ``"ghcr.io"`` (the GitHub Container Registry).
        """
        return "ghcr.io"

    def image_name(self) -> str:
        """Build the project's fully qualified image reference without a tag.

        Combines the registry host with the lowercased repository owner and
        project name, as required by GHCR (image references must be lowercase).

        Returns:
            Image reference in the form ``ghcr.io/<owner>/<project>``.
        """
        owner = VersionController.I.repo_owner().lower()
        project = PackageManager.I.project_name().lower()
        return f"{self.host()}/{owner}/{project}"

    def image_tag(self, tag: str) -> str:
        """Build the project's image reference for the given tag.

        Appends the tag to :meth:`image_name`.

        Args:
            tag: Tag to append to the image name (e.g. ``latest`` or
                ``v1.2.3``).

        Returns:
            Image reference in the form ``ghcr.io/<owner>/<project>:<tag>``.
        """
        return f"{self.image_name()}:{tag}"

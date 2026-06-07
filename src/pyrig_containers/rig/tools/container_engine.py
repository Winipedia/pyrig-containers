"""Container engine wrapper.

Wraps container engine commands and information.
"""

from pyrig.rig.tools.base.tool import Group, Tool


class ContainerEngine(Tool):
    """Container engine wrapper.

    Constructs podman command arguments for building and saving container images.
    Typical usage: call ``build_args`` to build the image, then ``save_args``
    to export it as a tar archive.
    """

    def name(self) -> str:
        """Get tool name.

        Returns:
            'podman'
        """
        return "podman"

    def group(self) -> str:
        """Returns the group the tool belongs to."""
        return Group.TOOLING

    def image_url(self) -> str:
        """Return the badge image URL for this tool.

        Returns:
            The URL of the badge image as a string.
        """
        return "https://img.shields.io/badge/Container-Podman-A23CD6?logo=podman&logoColor=grey&colorA=0D1F3F&colorB=A23CD6"

    def link_url(self) -> str:
        """Return the URL that the badge should link to for this tool.

        Returns:
            The URL of the project page as a string.
        """
        return "https://podman.io"

    def dev_dependencies(self) -> tuple[str, ...]:
        """Get tool dependencies.

        Podman is a system package (not a Python dependency), so this
        returns an empty tuple.

        Returns:
            Empty tuple — podman must be installed at the OS level.
        """
        return ()

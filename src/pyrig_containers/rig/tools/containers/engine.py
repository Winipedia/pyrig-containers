"""Container engine wrapper.

Wraps container engine commands and information.
"""

from pyrig.core.subprocesses import Args
from pyrig.rig.tools.base.tool import Group, Tool


class ContainerEngine(Tool):
    """Container engine wrapper.

    Constructs podman command arguments for authenticating with a registry and
    building and pushing container images. Typical usage: call ``login_args`` to
    authenticate, ``build_args`` to build and tag the image, then ``push_args``
    to publish each tag to the registry.
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

    def login_args(self, registry: str, *, username: str, password: str) -> Args:
        """Build args to authenticate the container engine with a registry.

        Constructs ``podman login <registry> --username <username>
        --password <password>``.

        Args:
            registry: Registry host to authenticate against (e.g. ``ghcr.io``).
            username: Account name to log in as.
            password: Token or password for the account.

        Returns:
            Args for the ``podman login`` command.
        """
        return self.args(
            "login", registry, "--username", username, "--password", password
        )

    def build_args(self, *tags: str, containerfile: str, context: str = ".") -> Args:
        """Build args to build and tag an image from a Containerfile.

        Constructs ``podman build --file <containerfile> --tag <tag>...
        <context>``, repeating ``--tag`` for each provided tag.

        Args:
            *tags: Image references to tag the built image with.
            containerfile: Path to the Containerfile/Dockerfile to build.
            context: Build context directory. Defaults to the current directory.

        Returns:
            Args for the ``podman build`` command.
        """
        tag_args = (arg for tag in tags for arg in ("--tag", tag))
        return self.args("build", "--file", containerfile, *tag_args, context)

    def push_args(self, tag: str) -> Args:
        """Build args to push a tagged image to its registry.

        Constructs ``podman push <tag>``.

        Args:
            tag: Fully qualified image reference to push (e.g.
                ``ghcr.io/owner/repo:latest``).

        Returns:
            Args for the ``podman push`` command.
        """
        return self.args("push", tag)

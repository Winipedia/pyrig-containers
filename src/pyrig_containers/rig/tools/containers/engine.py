"""Podman command construction for authenticating, building, and publishing images."""

from collections.abc import Iterable

from pyrig.core.subprocesses import Args
from pyrig.rig.tools.base.tool import Group, Tool


class ContainerEngine(Tool):
    """`podman` command wrapper.

    Constructs `podman` command arguments for authenticating with a registry
    and building and pushing container images. Typical usage: call
    `login_args` to authenticate, `build_args` to build and tag the image,
    then `push_args` to publish each tag to the registry.
    """

    def dev_dependencies(self) -> tuple[str, ...]:
        """Return an empty tuple; `podman` is a system package, not a Python one."""
        return ()

    def group(self) -> str:
        """Return `Group.TOOLING`."""
        return Group.TOOLING

    def image_url(self) -> str:
        """Return the Shields.io badge URL for `podman`."""
        return f"https://img.shields.io/badge/container-{self.shield_name()}-A23CD6?logo=podman&logoColor=grey&colorA=0D1F3F&colorB=A23CD6"

    def link_url(self) -> str:
        """Return the URL of the `podman` project page."""
        return "https://podman.io"

    def name(self) -> str:
        """Return `"podman"`."""
        return "podman"

    def build_args(
        self,
        *args: str,
        tags: Iterable[str] = (),
        context: str = ".",
    ) -> Args:
        """Build args to build and tag an image from the build context.

        Constructs `podman build --tag <tag>... <context>`, repeating
        `--tag` for each provided tag and inserting `*args` before the
        context. No `--file` is passed, so podman discovers the
        `Containerfile` in the build context automatically.

        Args:
            *args: Additional arguments appended before the context (e.g.
                `--file` to point at a specific Containerfile, or
                `--no-cache`).
            tags: Image references to tag the built image with. Defaults to none.
            context: Build context directory. Defaults to the current directory.

        Returns:
            Args for the `podman build` command.
        """
        tag_args = (arg for tag in tags for arg in ("--tag", tag))
        return self.args("build", *tag_args, *args, context)

    def login_args(
        self,
        *args: str,
        registry: str,
        username: str,
        password: str,
    ) -> Args:
        """Build args to authenticate the container engine with a registry.

        Constructs `podman login <registry> --username <username>
        --password <password>`, appending `*args` at the end.

        Args:
            *args: Additional arguments appended to the command.
            registry: Registry host to authenticate against (e.g. `ghcr.io`).
            username: Account name to log in as.
            password: Token or password for the account.

        Returns:
            Args for the `podman login` command.
        """
        return self.args(
            "login",
            registry,
            "--username",
            username,
            "--password",
            password,
            *args,
        )

    def push_args(self, *args: str, tag: str) -> Args:
        """Build args to push a tagged image to its registry.

        Constructs `podman push <tag>`, appending `*args` at the end.

        Args:
            *args: Additional arguments appended to the command.
            tag: Fully qualified image reference to push (e.g.
                `ghcr.io/owner/repo:latest`).

        Returns:
            Args for the `podman push` command.
        """
        return self.args("push", tag, *args)

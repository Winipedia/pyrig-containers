"""Podman commands for building, archiving, loading, and publishing images."""

from collections.abc import Iterable
from typing import override

from pyrig.core.subprocesses import Args
from pyrig.rig.tools.base.tool import Group, Tool


class ContainerEngine(Tool):
    """`podman` command wrapper.

    Constructs `podman` command arguments for authenticating with a registry
    and building, archiving, loading, and pushing container images. Call
    `login_args` to authenticate, `build_args` to build and tag the image,
    then `push_args` to publish each tag to the registry. Use `save_args` and
    `load_args` to transfer images between runners without rebuilding.
    """

    @override
    def dev_dependencies(self) -> tuple[str, ...]:
        """Return an empty tuple; `podman` is a system package, not a Python one."""
        return ()

    @override
    def group(self) -> str:
        """Return `Group.TOOLING`."""
        return Group.TOOLING

    @override
    def image_url(self) -> str:
        """Return the Shields.io badge URL for `podman`."""
        return f"https://img.shields.io/badge/Container-{self.shield_name().capitalize()}-A23CD6?logo=podman&logoColor=grey&colorA=0D1F3F&colorB=A23CD6"

    @override
    def link_url(self) -> str:
        """Return the URL of the `podman` project repository."""
        return "https://github.com/podman-container-tools/podman"

    @override
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

        Constructs `podman build --tag=<tag>... <context>`, repeating
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
        tag_args = (f"--tag={tag}" for tag in tags)
        return self.args("build", *tag_args, *args, context)

    def load_args(self, *args: str, input_: str) -> Args:
        """Build args to load an image archive.

        Args:
            *args: Additional arguments appended to the command.
            input_: Archive path, image-layout directory, or archive URL.

        Returns:
            Args for the `podman load` command.
        """
        return self.args("load", f"--input={input_}", *args)

    def login_args(
        self,
        *args: str,
        registry: str,
        username: str,
        password: str,
    ) -> Args:
        """Build args to authenticate the container engine with a registry.

        Constructs `podman login <registry> --username=<username>
        --password=<password>`, appending `*args` at the end.

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
            f"--username={username}",
            f"--password={password}",
            *args,
        )

    def push_args(self, *args: str, tag: str) -> Args:
        """Build args to push a tagged image to its registry.

        Constructs `podman push <tag>`, appending `*args` at the end.
        A destination reference may be supplied as the first extra argument.

        Args:
            *args: Additional arguments appended to the command.
            tag: Image reference to push. If no destination is supplied,
                this must include the target registry (e.g.
                `ghcr.io/owner/repo:latest`).

        Returns:
            Args for the `podman push` command.
        """
        return self.args("push", tag, *args)

    def save_args(self, *args: str, image: str, output: str) -> Args:
        """Build args to save an image in a Docker archive.

        Args:
            *args: Additional arguments appended before the image reference.
            image: Local image reference to save.
            output: Archive file path.

        Returns:
            Args for the `podman save` command.
        """
        return self.args(
            "save",
            f"--output={output}",
            *args,
            image,
        )

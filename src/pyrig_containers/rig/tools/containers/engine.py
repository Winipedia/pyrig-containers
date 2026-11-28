"""Podman and Compose commands for managing container images and services."""

from collections.abc import Iterable
from pathlib import Path
from typing import override

from pyrig.core.subprocesses import Args
from pyrig.rig.tools.base.tool import Group, Tool


class ContainerEngine(Tool):
    """`podman` command wrapper.

    Constructs `podman` command arguments for authenticating with a registry
    and building, archiving, loading, and pushing container images. It also
    constructs arguments for running Compose commands with selected files.
    Call `login_args` to authenticate, `build_args` to build and tag the image,
    then `push_args` to publish each tag to the registry. Use `save_args` and
    `load_args` to transfer images between runners without rebuilding.
    """

    @override
    def dev_dependencies(self) -> tuple[str, ...]:
        """Return `podman-compose` as a dev dependency; Podman is a system package."""
        return (self.compose_provider(),)

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

    def compose_up_production_args(
        self,
        *args: str,
        files: Iterable[Path],
        compose_args: Args | None = None,
    ) -> Args:
        """Return Compose up arguments for the production environment.

        This adds the following flags to the Compose up command:
            - `--remove-orphans`: Remove containers for services not defined in the
                Compose files.
            - `--force-recreate`: Recreate containers even if their configuration
                and image haven't changed.
            - `--wait`: Wait for containers to be healthy/ready.
            - `--detach`: Run containers in the background.

        Args:
            *args: Additional arguments for the Compose up command.
            files: Compose files to use for the production environment.
            compose_args: Additional arguments for the Compose provider.

        Returns:
            Arguments for `podman-compose up` with the production environment flags.
        """
        if compose_args is None:
            compose_args = Args()
        return self.compose_up_files_args(
            *args,
            files=files,
            compose_args=compose_args,
            remove_orphans=True,
            force_recreate=True,
            wait=True,
            detach=True,
        )

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
        """Build arguments to authenticate with a container registry.

        Args:
            *args: Additional arguments appended to the command.
            registry: Registry host to authenticate against (e.g. `ghcr.io`).
            username: Account name to log in as.
            password: Token or password for the account.

        Returns:
            Arguments for `podman login`.
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

    def compose_up_files_args(
        self,
        *args: str,
        files: Iterable[Path],
        compose_args: Args | None = None,
        **kwargs: bool,
    ) -> Args:
        """Return Compose up arguments using the selected files.

        Args:
            *args: Arguments for the `up` command.
            files: Compose files to include.
            compose_args: Additional arguments for the Compose provider.
            **kwargs: Additional keyword arguments passed to the method.

        Returns:
            Arguments for `podman-compose up`.
        """
        if compose_args is None:
            compose_args = Args()
        return self.compose_up_args(
            *args,
            compose_args=Args(
                *(f"--file={file.as_posix()}" for file in files),
                *compose_args,
            ),
            **kwargs,
        )

    def compose_up_args(  # noqa: PLR0913
        self,
        *args: str,
        remove_orphans: bool = False,
        force_recreate: bool = False,
        build: bool = False,
        wait: bool = False,
        detach: bool = False,
        compose_args: Args | None = None,
    ) -> Args:
        """Return arguments for the Compose up command.

        Args:
            *args: Arguments for the `up` command.
            remove_orphans: If `True`, add the `--remove-orphans` flag.
            force_recreate: If `True`, add the `--force-recreate` flag.
            build: If `True`, add the `--build` flag.
            wait: If `True`, add the `--wait` flag.
            detach: If `True`, add the `--detach` flag.
            compose_args: Additional arguments for the Compose provider.

        Returns:
            Arguments for `podman-compose up`.
        """
        if compose_args is None:
            compose_args = Args()

        up_args = ()
        if remove_orphans:
            up_args = (*up_args, "--remove-orphans")
        if force_recreate:
            up_args = (*up_args, "--force-recreate")
        if build:
            up_args = (*up_args, "--build")
        if wait:
            up_args = (*up_args, "--wait")
        if detach:
            up_args = (*up_args, "--detach")

        return self.compose_args(
            *compose_args,
            "up",
            *up_args,
            *args,
        )

    def compose_args(self, *args: str) -> Args:
        """Return arguments for the Compose provider.

        Args:
            *args: Arguments for the Compose provider.

        Returns:
            Arguments for `podman-compose`.
        """
        return Args(self.compose_provider(), *args)

    def compose_provider(self) -> str:
        """Return the Compose provider for Podman."""
        return f"{self.name()}-compose"

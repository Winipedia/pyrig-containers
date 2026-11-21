"""Container-specific conventions for the project's package manager."""

from pyrig.rig.tools.packages.manager import PackageManager as BasePackageManager


class PackageManager(BasePackageManager):
    """`uv` package manager, extended with a container binary-copy convention.

    Adds `container_binary_copy_spec`, which supplies the image and paths
    needed to copy the `uv` binary into a container image.
    """

    def container_binary_copy_spec(self) -> tuple[str, str, str]:
        """Return the image and paths for copying uv into a container image.

        Returns:
            Tuple of `(image, source_path, destination_path)`.
        """
        return "ghcr.io/astral-sh/uv:latest", "/uv", "/usr/local/bin/uv"

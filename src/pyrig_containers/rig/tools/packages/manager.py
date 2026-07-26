"""Container-specific conventions for the project's package manager."""

from pyrig.rig.tools.packages.manager import PackageManager as BasePackageManager


class PackageManager(BasePackageManager):
    """`uv` package manager, extended with a container-image convention.

    Adds `container_image`, which supplies the image and paths needed to
    embed the `uv` binary in a container image.
    """

    def container_image(self) -> tuple[str, str, str]:
        """Return the image and paths for copying uv into a container image.

        Returns:
            Tuple of `(image, path_in_source_image, path_in_target_image)`.
        """
        return "ghcr.io/astral-sh/uv:latest", "/uv", "/usr/local/bin/uv"
